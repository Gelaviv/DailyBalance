from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from schedules.models import DailySchedule

class Command(BaseCommand):
    help = 'Generate daily schedules for all users'
    
    def handle(self, *args, **options):
        today = date.today()
        
        # Get or create daily schedules for all users
        for schedule in DailySchedule.objects.all():
            # This will automatically generate tasks through the save method
            schedule.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated daily schedules for {today}')
        )