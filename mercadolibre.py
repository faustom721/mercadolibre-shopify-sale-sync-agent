import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

from utils import saveLastJobDate, readLastJobDate

load_dotenv()


def fetchOrders():
    access_token = os.getenv("MERCADOLIBRE_ACCESS_TOKEN")
    user_id = os.getenv("MERCADOLIBRE_SELLER_ID")

    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S-03:00")
    last_job_date = readLastJobDate()
    if not last_job_date:
        last_job_date = (datetime.now() - timedelta(days=7)).strftime(
            "%Y-%m-%dT%H:%M:%S-03:00"
        )

    # Fetch orders from one week ago to today
    orders_url = f"https://api.mercadolibre.com/orders/search?seller={user_id}&order.date_created.from={last_job_date}&order.date_created.to={now}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(orders_url, headers=headers)

    saveLastJobDate(now)

    # Check for successful response
    if response.status_code == 200:
        orders = response.json().get("results", [])
        for order in orders:
            for item in order["order_items"]:
                product = item["item"]
                quantity = item["quantity"]
                print(product["id"])
                print(product["title"])
                print(quantity)
    else:
        print(f"Error: {response.status_code} - {response.json()}")


fetchOrders()
