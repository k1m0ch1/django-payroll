from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args, **options):
    	self.stdout.write(self.style.SUCCESS('Successfully'))