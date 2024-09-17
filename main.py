from datetime import datetime
from mercadolibre_services import fetch_orders
from shopify_services import create_shopify_order, get_product_info
from utils import read_first_line_file, remove_first_line_file, write_line_file


def sync_mercadolibre_to_shopify_orders():
    """
    See which orders are in MercadoLibre and not in Shopify, and create them in Shopify.
    """
    fetch_orders()
    today = datetime.now().strftime("%d-%m-%Y")

    # Read from file one by one and create order in Shopify
    while True:
        ml_sale = read_first_line_file("ml_sales_buffer.txt")
        if not ml_sale:
            break
        # TODO: we have to go through all lines in the buffer, getting all the lines that are from the same order so we can create the order in Shopify with all the items
        # Read first line, delete, read the next one, if it's from the same order, delete and repeat until we have all the items from the order
        current_order_id = ml_sale.split(",")[0]
        current_order_items = [ml_sale]
        remove_first_line_file("ml_sales_buffer.txt")
        while True:
            next_sale = read_first_line_file("ml_sales_buffer.txt")
            if not next_sale:
                break
            next_order_id = next_sale.split(",")[0]
            if next_order_id == current_order_id:
                current_order_items.append(next_sale)
                remove_first_line_file("ml_sales_buffer.txt")
            else:
                break
        # Now we have all the items from the order, we can create the order in Shopify
        order_data = {
            "order": {
                "line_items": [],
                "financial_status": "paid",
                "note": f"MercadoLibre - Order ID: {current_order_id}"

            }
        }
        # TODO: Somewhere here we have to contemplate the case when the item in Mercadolibre is more expensive than in Shopify, and add that as a delivery fee
        # TODO: If the item is cheaper, we have to add a discount to the order
        for item in current_order_items:
            _, shopify_identifier, quantity, _ = item.split(",")
            product_info = get_product_info(shopify_identifier)
            order_data["order"]["line_items"].append({
                "variant_id": product_info["variants"][0]["id"],
                "quantity": quantity
            })
        if create_shopify_order(order_data):
            write_line_file(
                f"logs/{today}/mercadolibre_synced_orders.txt", current_order_id)
        else:
            write_line_file(
                f"logs/{today}/mercadolibre_not_synced_orders.txt", current_order_id)


def sync_shopify_to_mercadolibre_inventory():
    """
    See that products in MercadoLibre have the same stock as in Shopify.
    """
    pass


sync_mercadolibre_to_shopify_orders()
sync_shopify_to_mercadolibre_inventory()
