from datetime import datetime
from mercadolibre_services import fetch_orders
from utils import read_first_line_file, remove_first_line_file, write_line_file


def sync_mercadolibre_to_shopify_orders():
    fetch_orders()
    today = datetime.now().strftime("%d-%m-%Y")

    # Read from file one by one and create order in Shopify
    while True:
        ml_sale = read_first_line_file("ml_sales_buffer.txt")
        if ml_sale:
            # Create order in Shopify
            print(f"Creating order in Shopify for {ml_sale}")
            remove_first_line_file("ml_sales_buffer.txt")

            # Log the synced order in file
            write_line_file(f"logs/{today}.txt", ml_sale)
        else:
            break


sync_mercadolibre_to_shopify_orders()
