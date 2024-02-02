from django.core.management.base import BaseCommand
from rapihogar.models import (
    Tecnico
)
import random


technicians = [
    {
        'first_name': 'Juan',
        'last_name': 'Perez',
        'category': 'Electricista'
    },
    {
        'first_name': 'Pedro',
        'last_name': 'Gomez',
        'category': 'Plomero'
    },
    {
        'first_name': 'Luis',
        'last_name': 'Lopez',
        'category': 'Carpintero'
    },
    {
        'first_name': 'Carlos',
        'last_name': 'Gonzalez',
        'category': 'Electricista'
    },
    {
        'first_name': 'Jose',
        'last_name': 'Rodriguez',
        'category': 'Plomero'
    }
]



class Command(BaseCommand):
    help = 'Cargar 5 técnicos'

    def handle(self, *args, **options):
        """
        The function creates technician objects in the database using the provided data and prints a
        success message.
        """
        
        for technical in technicians:
            Tecnico.objects.create(
                first_name=technical['first_name'],
                last_name=technical['last_name'],
                category=technical['category']
            )

        self.stdout.write(self.style.SUCCESS(f'Se cargaron 5 técnicos exitosamente.'))