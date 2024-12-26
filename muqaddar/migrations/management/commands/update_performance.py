from django.core.management.base import BaseCommand
from muqaddar.models import Performance
from datetime import datetime
from muqaddar.utils import fetch_live_price  # Update this import to match the function location

class Command(BaseCommand):
    help = "Update all performance records"

    def handle(self, *args, **kwargs):
        performances = Performance.objects.all()
        for perf in performances:
            current_price = fetch_live_price(perf.symbol)
            if current_price:
                perf.update_performance(current_price)
        self.stdout.write(self.style.SUCCESS("Performance updated successfully."))
