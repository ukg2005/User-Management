from django.core.management.base import BaseCommand
from blog.models import Category

class Command(BaseCommand):
    help = 'Create initial categories for the blog system'

    def handle(self, *args, **kwargs):
        default_categories = [
            ('Mental Health', 'mental-health'),
            ('Heart Disease', 'heart-disease'),
            ('Covid19', 'covid19'),
            ('Immunization', 'immunization')
        ]

        for name, slug in default_categories:
            Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name}
            )
            self.stdout.write(self.style.SUCCESS(f'Category "{name}" created or already exists'))
