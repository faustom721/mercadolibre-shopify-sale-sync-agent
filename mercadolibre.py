import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

from utils import save_last_job_date, read_last_job_date

load_dotenv()


def extract_shopify_identifier(product_id):
    """
    Extracts the Shopify identifier from a MercadoLibre product ID. We store this in the MercadoLibre products' description in the last line with the prefix "CSS-SHOP-ID:".
    (Yes I know, ML has a custom field for this, but this is just simpler for now)
    """
    # Fetch the product's description
    access_token = os.getenv("MERCADOLIBRE_ACCESS_TOKEN")
    description_url = f"https://api.mercadolibre.com/items/{product_id}/description"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(description_url, headers=headers)
    description = response.json().get("plain_text", "")


def fetch_orders():
    access_token = os.getenv("MERCADOLIBRE_ACCESS_TOKEN")
    user_id = os.getenv("MERCADOLIBRE_SELLER_ID")

    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S-03:00")
    last_job_date = read_last_job_date()
    if not last_job_date:
        last_job_date = (datetime.now() - timedelta(days=7)).strftime(
            "%Y-%m-%dT%H:%M:%S-03:00"
        )

    # Fetch orders from one week ago to today
    orders_url = f"https://api.mercadolibre.com/orders/search?seller={user_id}&order.date_created.from={last_job_date}&order.date_created.to={now}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(orders_url, headers=headers)

    save_last_job_date(now)

    # Check for successful response
    if response.status_code == 200:
        orders = response.json().get("results", [])
        for order in orders:
            for item in order["order_items"]:
                product = item["item"]
                quantity = item["quantity"]
                shopify_identifier = extract_shopify_identifier(product["id"])
    else:
        print(f"Error: {response.status_code} - {response.json()}")
