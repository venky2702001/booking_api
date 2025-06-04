from django.core.management.base import BaseCommand
from booking.models import FitnessClass
from datetime import datetime
from zoneinfo import ZoneInfo

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        FitnessClass.objects.all().delete()
        ist = ZoneInfo('Asia/Kolkata')
        FitnessClass.objects.create(name='Yoga', datetime=datetime(2025, 6, 5, 7, 0, tzinfo=ist), instructor='Aditi', available_slots=5)
        FitnessClass.objects.create(name='Zumba', datetime=datetime(2025, 6, 5, 18, 0, tzinfo=ist), instructor='Rahul', available_slots=3)
        FitnessClass.objects.create(name='HIIT', datetime=datetime(2025, 6, 6, 6, 30, tzinfo=ist), instructor='Neha', available_slots=4)
        self.stdout.write('Seeded successfully')
