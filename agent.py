import os
import json
import ollama
from dotenv import load_dotenv
from harness import validate_and_authorize
from tools import search_products, check_stock, delete_product

load_dotenv()

LLM_MODEL = os.getenv("LLM_MODEL", "qwen3:4b")

TOOL_MAP = {
    "search_products": search_products,
    "check_stock": check_stock,
    "delete_product": delete_product
}

OLLAMA_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search products by name keyword.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "Search keyword"}},
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_stock",
            "description": "Check inventory stock for a product ID.",
            "parameters": {
                "type": "object",
                "properties": {"product_id": {"type": "integer", "description": "Positive product ID"}},
                "required": ["product_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_product",
            "description": "Delete a product from inventory (Admin action).",
            "parameters": {
                "type": "object",
                "properties": {"product_id": {"type": "integer", "description": "Positive product ID"}},
                "required": ["product_id"]
            }
        }
    }
]

def run_agent(user_request: str, user_role: str = "Customer", max_iterations: int = 5):
    """Executes the safe agent loop with authorization and iteration limits."""
    messages = [{"role": "user", "content": user_request}]
    iterations = 0

    print(f"\n=== New Request [{user_role}]: '{user_request}' ===")

    while iterations < max_iterations: # Section 2.D: Iteration Limit Control
        iterations += 1
        print(f"\n--- [Iteration {iterations}/{max_iterations}] ---")

        response = ollama.chat(
            model=LLM_MODEL,
            messages=messages,
            tools=OLLAMA_TOOLS
        )
        
        response_message = response["message"]
        tool_calls = response_message.get("tool_calls")

        if not tool_calls:
            print("Agent produced final answer.")
            return response_message.get("content", "Completed.")

        messages.append(response_message)

        for tool_call in tool_calls:
            function_info = tool_call["function"]
            tool_name = function_info["name"]
            tool_args = function_info.get("arguments", {})

            print(f"Agent requested tool: '{tool_name}' with args: {tool_args}")

           
            is_valid, validation_msg = validate_and_authorize(user_role, tool_name, tool_args)

            if not is_valid:
                observation = f"ERROR: {validation_msg}"
                print(f"Harness Blocked Execution: {observation}")
            else:
             
                try:
                    tool_func = TOOL_MAP[tool_name]
                    observation = str(tool_func(**tool_args))
                    print(f"Tool Execution Result: {observation}")
                except Exception as e:
                    observation = f"EXECUTION ERROR: {str(e)}"

           
            messages.append({
                "role": "tool",
                "content": observation
            })

    return "AGENT STOPPED: Exceeded maximum tool call iteration limit."