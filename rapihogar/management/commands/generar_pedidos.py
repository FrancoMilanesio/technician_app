from django.core.management.base import BaseCommand
from rapihogar.models import (
    User,
    Tecnico,
    Pedido,
    Scheme
)
import random

### 4. Comando para generar pedidos ###
class Command(BaseCommand):
    help = 'Generar N pedidos'

    def add_arguments(self, parser):
        parser.add_argument('order_quantity', type=int)

    def handle(self, *args, **options):
        """
        The above function generates a specified number of random orders and assigns them to random
        technicians and clients.
        """
        order_quantity = options['order_quantity']
        
        if order_quantity in range(1, 101):
            technicians = Tecnico.objects.all()
            clients = User.objects.filter(is_active=True)
            selected_scheme = Scheme.objects.all()

            for _ in range(order_quantity):
                technical = random.choice(technicians)
                client = random.choice(clients)
                hours_worked = random.randint(1, 10)
                scheme = random.choice(selected_scheme)

                Pedido.objects.create(
                    client=client,
                    hours_worked=hours_worked,
                    technician=technical,
                    type_request=random.choice([0, 1]),
                    scheme=scheme,
                )

            self.stdout.write(self.style.SUCCESS(f'Se generaron {order_quantity} pedidos exitosamente.'))
        else:
            self.stdout.write(self.style.ERROR(f'La cantidad de pedidos debe estar entre 1 y 100.'))