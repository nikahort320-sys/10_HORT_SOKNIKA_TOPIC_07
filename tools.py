
MOCK_PRODUCTS = [
    {"id": 1, "name": "Laptop Pro", "price": 1200.0, "stock": 5},
    {"id": 2, "name": "Wireless Mouse", "price": 25.0, "stock": 15},
    {"id": 3, "name": "Gaming Monitor", "price": 300.0, "stock": 0}
]

def search_products(query: str):
    """Searches products by keyword."""
    results = [p for p in MOCK_PRODUCTS if query.lower() in p["name"].lower()]
    if results:
        return results
    return f"No products found matching '{query}'."

def check_stock(product_id: int):
    """Checks inventory stock for a specific product ID."""
    for p in MOCK_PRODUCTS:
        if p["id"] == product_id:
            return {"id": p["id"], "name": p["name"], "stock": p["stock"]}
    return {"error": f"Product ID {product_id} not found."}

def delete_product(product_id: int):
    """Deletes a product from inventory (Admin action)."""
    global MOCK_PRODUCTS
    for i, p in enumerate(MOCK_PRODUCTS):
        if p["id"] == product_id:
            deleted_item = MOCK_PRODUCTS.pop(i)
            return {"success": True, "message": f"Product '{deleted_item['name']}' (ID: {product_id}) deleted successfully."}
    return {"error": f"Product ID {product_id} not found."}