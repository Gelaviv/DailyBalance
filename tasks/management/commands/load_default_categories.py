from django.core.management.base import BaseCommand
from tasks.models import Category

class Command(BaseCommand):
    help = 'Load default categories'
    
    def handle(self, *args, **options):
        categories = [
            {'name': 'spiritual', 'color': '#FF6B6B'},
            {'name': 'family', 'color': '#4ECDC4'},
            {'name': 'study', 'color': '#45B7D1'},
            {'name': 'work', 'color': '#F9A602'},
            {'name': 'personal', 'color': '#9B59B6'},
            {'name': 'health', 'color': '#2ECC71'},
            {'name': 'other', 'color': '#95A5A6'},
        ]
        
        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'color': cat_data['color']}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created category: {category.get_name_display()}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.get_name_display()}')
                )