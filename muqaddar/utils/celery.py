# muqaddar/utils/celery.py
from celery import Celery
from celery.schedules import crontab

# Set up the Celery app
app = Celery('muqaddar')

# Configure the Celery app with Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery beat schedule
app.conf.beat_schedule = {
    'check-stocks-every-5-minutes': {
        'task': 'muqaddar.tasks.check_stock_updates',
        'schedule': crontab(minute='*/5', hour='9-15', day_of_week='mon-fri'),  # Runs every 5 minutes between 9:15 AM and 3:30 PM
    },
}

@app.task
def check_stock_updates():
    # Your logic to check if stocks are updated
    stock_changed = check_for_stock_updates()  # Implement your stock update logic here
    if stock_changed:
        send_notifications()
