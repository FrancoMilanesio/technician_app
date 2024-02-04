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
    Pedido
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
        technicians_category=F('category')
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
            'full_name': technical.full_name,
            'category': technical.technicians_category,
            'total_hours_worked': technical.total_hours_worked,
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

    # El último trabajador ingresado que cobró el monto más bajo
    lowest_amount = sorted(technicians_list_data, key=lambda x: x['hours_worked_total_amount'])[0]

    # El último trabajador ingresado que cobró el monto más alto
    highest_amount = sorted(technicians_list_data, key=lambda x: x['hours_worked_total_amount'], reverse=True)[0]
    
    return {
        'average_amount': average_amount,
        'less_than_average': less_than_average,
        'highest_amount': highest_amount,
        'lowest_amount': lowest_amount
    }
    

