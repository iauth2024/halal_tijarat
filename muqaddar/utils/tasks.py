from celery import shared_task
from muqaddar.utils import send_notifications  # Import notifications from utils

@shared_task
def check_for_stock_updates():
    # This function checks whether the stock has been updated or added
    # Implement your stock update checking logic here
    stock_added_or_removed = check_stock_changes()  # Replace this with your actual logic
    return stock_added_or_removed

# muqaddar/utils.py
def send_notifications():
    # Logic for sending notifications (could be through email, popups, etc.)
    print("Stock updates detected! Sending notification...")
