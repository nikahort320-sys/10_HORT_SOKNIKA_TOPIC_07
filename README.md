# Topic 07: Simple Safe Agent

## 1. Project Overview
This project implements an autonomous **Shopping & Inventory Agent** using Python and a local LLM via Ollama (`qwen3:4b`). The agent allows users to search for products, check stock levels, and delete inventory items through natural language. It incorporates strict application-level safety controls, enforcing role-based authorization and input validation before any tool execution occurs.

## 2. Available Tools
The agent uses three concrete tools to interact with local inventory data:

1. **`search_products(query: str)`**: Searches the inventory for items matching a keyword (e.g., "laptop", "mouse") and returns product details including ID, name, price, and stock count.
2. **`check_stock(product_id: int)`**: Queries the exact stock quantity for a given product using its numerical ID.
3. **`delete_product(product_id: int)`**: Removes a product from the inventory database using its numerical ID.

## 3. Agent Loop
The decision loop follows an iterative **Decision $\rightarrow$ Action $\rightarrow$ Observation** cycle:

1. **User Request**: The user submits a prompt alongside their designated role (`Customer` or `Admin`).
2. **LLM Decision**: The LLM analyzes the request and history to select the appropriate tool and generate function arguments.
3. **Harness Gatekeeping**: Before execution, the application harness (`harness.py`) intercepts the tool call to check permissions and validate argument formatting.
4. **Tool Action**: If authorized and valid, the Python function runs against the local data.
5. **Observation**: The execution output (or error message) is appended to the message history as a tool observation.
6. **Final Synthesis**: The LLM reads the observation to either answer the user or invoke another tool, continuing until a final response is generated or the maximum loop count is hit.
## 4. Permission Rule
Tool access is enforced at the application layer inside `harness.py` based on user roles, preventing unauthorized actions regardless of prompt injection:

| Tool Name | Customer | Admin |
| :--- | :---: | :---: |
| `search_products` | Allowed | Allowed |
| `check_stock` | Allowed | Allowed |
| `delete_product` | **Blocked** | Allowed |

## 5. Safety
- **Input Validation**: Argument types and ranges are validated prior to execution. For example, `product_id` is verified in Python code to ensure it is a positive integer greater than zero.
- **Exception Handling**: Tool functions and database queries are wrapped in `try-except` blocks. Runtime errors are caught and formatted as observations rather than crashing the agent loop.
- **Loop Iteration Limit**: The agent loop in `agent.py` enforces a maximum limit of **5 iterations** per user request to guard against infinite tool-calling loops and run-away LLM cycles.

## 6. Example Run

### Scenario 1: Customer multi-step search and stock check (Allowed)
Enter your role (Customer/Admin): Customer

[Active Session Role: Customer]

[Customer] Enter your request: 2

=== New Request [Customer]: '2' ===

--- [Iteration 1/5] ---
Agent requested tool: 'check_stock' with args: {'product_id': 2}
Tool Execution Result: {'id': 2, 'name': 'Wireless Mouse', 'stock': 15}

--- [Iteration 2/5] ---
Agent produced final answer.

Final Agent Answer:
Product ID 2 (Wireless Mouse) has 15 units in stock.

--------------------------------------------------
[Customer] Enter your request: delete product with id=3

=== New Request [Customer]: 'delete product with id=3' ===

--- [Iteration 1/5] ---
Agent requested tool: 'delete_product' with args: {'product_id': 3}
Harness Blocked Execution: ERROR: PERMISSION DENIED: Role 'Customer' is not authorized to call 'delete_product'.

--- [Iteration 2/5] ---
Agent produced final answer.

Final Agent Answer:
The user does not have permission to delete products. This action requires administrative privileges. Please contact an administrator to proceed with product deletion.
### Scenario 2: Customer attempts unauthorized deletion (Blocked by Harness)
Enter your role (Customer/Admin): admin

[Active Session Role: Admin]

[Admin] Enter your request: delete a product with id 1

=== New Request [Admin]: 'delete a product with id 1' ===

--- [Iteration 1/5] ---
Agent requested tool: 'delete_product' with args: {'product_id': 1}
Tool Execution Result: {'success': True, 'message': "Product 'Laptop Pro' (ID: 1) deleted successfully."}

--- [Iteration 2/5] ---
Agent produced final answer.

Final Agent Answer:
The product "Laptop Pro" (ID: 1) has been successfully deleted from the inventory.