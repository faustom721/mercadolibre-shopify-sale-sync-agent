import os
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

from utils import write_line_file, read_first_line_file

load_dotenv()


def create_shopify_order(order_data):
    """
    Creates an order in Shopify with the given order data.
    """

    url = f"https://{os.getenv("SHOPIFY_API_KEY")}:{os.getenv('SHOPIFY_API_PASSWORD')}@{os.getenv('SHOPIFY_STORE_URL')}/admin/api/2023-10/orders.json"
    order_data_json = json.dumps(order_data)

    # Headers for the request
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=order_data_json)

    # Check if the request was successful
    if response.status_code == 201:
        print("Order created successfully in Shopify")
        return True
    else:
        print("Error creating order in Shopify")
        return False


def get_product_info(product_id):
    """
    Fetches the product information from Shopify using the product ID.
    """

    url = f"https://{os.getenv('SHOPIFY_API_KEY')}:{os.getenv('SHOPIFY_API_PASSWORD')}@{os.getenv('SHOPIFY_STORE_URL')}/admin/api/2023-10/products/{product_id}.json"

    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        product_info = response.json().get("product", {})
        return product_info
    else:
        print("Error fetching product information from Shopify")
        return None
