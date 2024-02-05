from typing import Iterable
from django.db import transaction
from django.db.models import (
    Sum, 
    Count, 
    Case, 
    When, 
    F, 
    Value, 
    IntegerField, 
    Max, 
    Min, 
    Avg,
    FloatField
)
from rapihogar.models import (
    Company, 
    Tecnico,
    Pedido,
    Scheme,
    User
)


def get_technicians_list() -> list[dict]:
    """
    The function `get_technicians_list` calculates the total amount to be paid to technicians based on
    the number of hours worked and applies discounts according to a given table.
    :return: The function `get_technicians_list()` returns a list of dictionaries. Each dictionary
    represents a technician and contains the following information:
    - 'full_name' (full name of the technician),
    - 'total_hours_worked' (total number of hours worked by the technician),
    - 'hours_worked_total_amount' (total amount to be paid to the technician), and
    - 'orders_cuantity' (total number of orders assigned to the technician).
    """
    
    """
    Cálculo de Pago según la siguiente tabla:

    | Cantidad De Horas | Valor Hora  | Porcentaje de descuento  |
    | --------   | -------- | -------- |
    |  0-14 | 200 | 15% |
    | 15-28 | 250 | 16% |
    | 29-47 | 300 | 17% |
    |  >48 | 350 | 18% |
    """
    """
    Por ejemplo: Trabajador “Larusso Daniel”, Horas trabajadas = 20
        total = (20 * 250) – (20 * 250 * 0.16)
        total = (5.000) – (800)
        total = 4.200
    """

    # Obtener los datos agregados
    technicians_hours_worked = Tecnico.objects.annotate(
        total_hours_worked=Sum('pedido__hours_worked'),
        orders_cuantity=Count('pedido'),
        technicians_category=F('category'),
        technicians_pk=F('pk')
    )

    # Calcular el pago según la tabla dada
    technicians_data = technicians_hours_worked.annotate(
        pay=Case(
            When(total_hours_worked__lte=14, then=F('total_hours_worked') * 200),
            When(total_hours_worked__range=(15, 28), then=F('total_hours_worked') * 250),
            When(total_hours_worked__range=(29, 47), then=F('total_hours_worked') * 300),
            When(total_hours_worked__gt=48, then=F('total_hours_worked') * 350),
            default=Value(0),
            output_field=IntegerField(),
        )
    )

    # Aplicar descuento
    technicians_data = technicians_data.annotate(
        discount=F('pay') * 0.01 * Case(
            When(total_hours_worked__lte=14, then=Value(15)),
            When(total_hours_worked__range=(15, 28), then=Value(16)),
            When(total_hours_worked__range=(29, 47), then=Value(17)),
            When(total_hours_worked__gt=48, then=Value(18)),
            default=Value(0),
            output_field=IntegerField(),
        )
    )

    # Calcular el total a cobrar
    technicians_data = technicians_data.annotate(
        hours_worked_total_amount=F('pay') - F('discount')
    )

    # Obtener datos finales
    results = [
        {
            'id': technical.technicians_pk,
            'full_name': technical.full_name,
            'category': technical.technicians_category,
            'total_hours_worked': technical.total_hours_worked if technical.total_hours_worked else 0,
            'hours_worked_total_amount': technical.hours_worked_total_amount,
            'orders_cuantity': technical.orders_cuantity
        }
        for technical in technicians_data
    ]

    return results


def get_technicians_report() -> dict:
    """
    The `get_technicians_report` function calculates the average amount charged by technicians,
    identifies technicians who charged less than the average, and determines the technician with the
    lowest and highest charges.
    :return: The function `get_technicians_report` returns a dictionary containing the following
    information:
    - 'average_amount' (average amount charged by all technicians),
    - 'less_than_average' (list of technicians who charged less than the average),
    - 'highest_amount' (technician who charged the highest amount), and
    - 'lowest_amount' (technician who charged the lowest amount).
    """
    technicians_list_data = get_technicians_list()

    # Monto promedio cobrado por todos los técnicos
    average_amount = sum([technical['hours_worked_total_amount'] for technical in technicians_list_data]) / len(technicians_list_data)

    # Datos de todos los técnicos que cobraron menos que el promedio
    less_than_average = [technical for technical in technicians_list_data if technical['hours_worked_total_amount'] < average_amount]

    sorted_tech_list = sorted(technicians_list_data, key=lambda tech: tech["id"], reverse=True)

    # El último trabajador ingresado que cobró el monto más bajo
    lowest_amount = min(sorted_tech_list, key=lambda tech: tech["hours_worked_total_amount"]) #sorted(technicians_list_data, key=lambda x: (x['id'], x['hours_worked_total_amount']))[0]

    # El último trabajador ingresado que cobró el monto más alto
    highest_amount = max(technicians_list_data, key=lambda tech: tech["hours_worked_total_amount"]) #sorted(technicians_list_data, key=lambda x: (x['id'], x['hours_worked_total_amount']), reverse=True)[0]
    
    return {
        'average_amount': round(average_amount, 2),
        'less_than_average': less_than_average,
        'highest_amount': highest_amount,
        'lowest_amount': lowest_amount
    }
    

def get_orders() -> Iterable[Pedido]:
    """
    The `get_orders` function returns all orders in the database.
    :return: The function `get_orders` returns a QuerySet containing all orders in the database.
    """
    return Pedido.objects.all().order_by('-id')


def update_order(order_id: int, client_id: int, technician: str, hours_worked: int, type_request: int, scheme_id: int) -> None:
    """
    The function updates an order with the given order ID, client ID, technician ID, hours worked, and
    type of request.
    
    :param order_id: The order_id parameter is an integer that represents the unique identifier of the
    order that needs to be updated
    :type order_id: int
    :param client_id: The client_id parameter is an integer that represents the ID of the client
    associated with the order
    :type client_id: int
    :param technician_id: The `technician_id` parameter is an integer that represents the ID of the
    technician assigned to the order
    :type technician_id: int
    :param hours_worked: The parameter "hours_worked" represents the number of hours worked on the order
    :type hours_worked: int
    :param type_request: The parameter `type_request` is an integer that represents the type of request
    for the order. The specific values and their meanings would depend on the context of your
    application. You would need to define and document the possible values for `type_request` in your
    application
    :type type_request: int
    :return: the updated `pedido` object.
    """
    
    with transaction.atomic():
        new_type_request = Pedido.SOLICITUD if type_request == 0 else Pedido.PEDIDO
        pedido = Pedido.objects.get(id=order_id)
        pedido.client_id = client_id
        pedido.technician_id = technician
        pedido.hours_worked = hours_worked
        pedido.type_request = new_type_request
        pedido.scheme_id = scheme_id
        pedido.save()

    return pedido


def get_technicians() -> Iterable[Tecnico]:
    """
    The `get_technicians` function returns all technicians in the database.
    :return: The function `get_technicians` returns a QuerySet containing all technicians in the database.
    """
    return Tecnico.objects.all()


def get_clients() -> Iterable[User]:
    """
    The `get_clients` function returns all clients in the database.
    :return: The function `get_clients` returns a QuerySet containing all clients in the database.
    """
    return User.objects.all()


def get_schemas() -> Iterable[Scheme]:
    """
    The `get_schemas` function returns all schemas in the database.
    :return: The function `get_schemas` returns a QuerySet containing all schemas in the database.
    """
    return Scheme.objects.all()