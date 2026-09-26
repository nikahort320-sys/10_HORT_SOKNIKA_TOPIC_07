PERMISSIONS = {
    "Customer": ["search_products", "check_stock"],
    "Admin": ["search_products", "check_stock", "delete_product"]
}

def validate_and_authorize(user_role: str, tool_name: str, tool_args: dict):
    """Validates authorization permissions and argument constraints in application code."""
    allowed_tools = PERMISSIONS.get(user_role, [])
    if tool_name not in allowed_tools:
        return False, f"PERMISSION DENIED: Role '{user_role}' is not authorized to call '{tool_name}'."

    if "product_id" in tool_args:
        product_id = tool_args.get("product_id")
        if not isinstance(product_id, int) or product_id <= 0:
            return False, "VALIDATION ERROR: 'product_id' must be a positive integer greater than 0."

    return True, "Authorized"