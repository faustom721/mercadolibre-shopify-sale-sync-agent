import os
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv

load_dotenv()


def fetchOrders():
    access_token = os.getenv("MERCADOLIBRE_ACCESS_TOKEN")
    user_id = os.getenv("MERCADOLIBRE_SELLER_ID")

    today = datetime.now().strftime("%Y-%m-%d")
    one_week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    # Fetch orders from one week ago to today
    orders_url = f"https://api.mercadolibre.com/orders/search?seller={user_id}&order.date_created.from={one_week_ago}T00:00:00.000-00:00&order.date_created.to={today}T23:59:59.999-00:00"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(orders_url, headers=headers)

    # Check for successful response
    if response.status_code == 200:
        orders = response.json().get("results", [])
        for order in orders:
            for item in order["order_items"]:
                product = item["item"]
                quantity = item["quantity"]
                print(product["id"])
                print(quantity)
    else:
        print(f"Error: {response.status_code} - {response.json()}")


fetchOrders()
