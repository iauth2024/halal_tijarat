from django.db import models

class ScreenerHistory(models.Model):
    screener_name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    stocks = models.JSONField()  # Store stock list as JSON
from django.db import models

class Stock(models.Model):
    nsecode = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    bsecode = models.CharField(max_length=20, null=True, blank=True)
    per_chg = models.FloatField()
    close = models.FloatField()
    volume = models.BigIntegerField()
    screener = models.CharField(max_length=255, null=True, blank=True)  # Add this field

    def __str__(self):
        return self.name
from django.db import models
from datetime import datetime

class Performance(models.Model):
    symbol = models.CharField(max_length=20)
    screener_name = models.CharField(max_length=100)
    triggered_at = models.DateTimeField(default=datetime.now)
    timeframe = models.CharField(max_length=255)

    initial_price = models.FloatField()

    # New fields for tracking alerts
    alert_sent = models.BooleanField(default=False)  # Indicates if an alert has been sent
    alert_sent_at = models.DateTimeField(null=True, blank=True)  # Time the alert was sent
