from crewai.tools import tool
from database.sql_manager import db
from database.vector_manager import vector_db

@tool
def get_order_status(order_id: str) -> str:
    """Get the current status of an order by order ID"""
    try:
        result = db.get_order_status(order_id)
        if not result.empty:
            order = result.iloc[0]
            return f"Order {order_id}: Status is '{order['status']}', Total: ${order['total_amount']}, Tracking: {order['tracking_number'] or 'Not assigned yet'}"
        else:
            return f"Order {order_id} not found. Please check the order ID."
    except Exception as e:
        return f"Error retrieving order status: {str(e)}"

@tool
def get_customer_orders(customer_id: str) -> str:
    """Get all orders for a specific customer"""
    try:
        result = db.get_customer_orders(customer_id)
        if not result.empty:
            orders_info = []
            for _, order in result.iterrows():
                orders_info.append(f"Order {order['order_id']}: {order['status']} - ${order['total_amount']}")
            return f"Your orders:\n" + "\n".join(orders_info)
        else:
            return "No orders found for this customer."
    except Exception as e:
        return f"Error retrieving orders: {str(e)}"

@tool
def search_ecommerce_knowledge(query: str) -> str:
    """Search e-commerce knowledge base for relevant information"""
    try:
        results = vector_db.search_knowledge("ecommerce", query, n_results=2)
        if results and results['documents']:
            knowledge = "\n".join(results['documents'][0])
            return f"Here's what I found: {knowledge}"
        else:
            return "No relevant information found in knowledge base."
    except Exception as e:
        return f"Error searching knowledge base: {str(e)}"

@tool
def check_product_availability(product_id: str) -> str:
    """Check if a product is available and get its details"""
    try:
        query = "SELECT * FROM products WHERE product_id = ?"
        result = db.execute_query(query, (product_id,))
        if not result.empty:
            product = result.iloc[0]
            availability = "In Stock" if product['stock_quantity'] > 0 else "Out of Stock"
            return f"Product: {product['name']}, Price: ${product['price']}, Status: {availability} ({product['stock_quantity']} units)"
        else:
            return f"Product {product_id} not found."
    except Exception as e:
        return f"Error checking product availability: {str(e)}"