import json
from api.selector import get_orders, get_technicians_list
from api.views import OrderUpdateAPIView, OrdersSerializer
from rapihogar.models import User, Tecnico, Pedido, Scheme
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rapihogar.models import Company
from rest_framework.test import APIClient
from rest_framework import status


class CompanyListCreateAPIViewTestCase(APITestCase):
    url = reverse("company-list")

    def setUp(self):
        self.username = "user_test"
        self.email = "test@rapihigar.com"
        self.password = "Rapi123"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_company(self):
        response = self.client.post(self.url,
                                    {
                                        "name": "company delete!",
                                        "phone": "123456789",
                                        "email": "test@rapihigar.com",
                                        "website": "http://www.rapitest.com"
                                    }
                                    )
        self.assertEqual(201, response.status_code)

    def test_list_company(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(json.loads(response.content)) == Company.objects.count())


class ListOfTechniciansAPIViewTestCase(APITestCase):
    def setUp(self):
        self.username = "user_test"
        self.email = "test@rapihigar.com"
        self.password = "Rapi123"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        # Crear un técnico y asignarle algunos pedidos para probar la función
        tecnico = Tecnico.objects.create(
            first_name='John',
            last_name='Doe',
            category='Plomero'
        )
        Pedido.objects.create(
            client=self.user,
            hours_worked=20,
            technician=tecnico
        )

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_list_of_technicians(self):
        url = reverse('technical-list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        technicians_list = response.json()

        # Asegurar de que la lista de técnicos no esté vacía
        self.assertTrue(len(technicians_list) > 0)

        # Asegurar de que la lista contiene las claves esperadas
        expected_keys = {'full_name', 'category', 'total_hours_worked', 'hours_worked_total_amount', 'orders_cuantity'}
        for technician in technicians_list:
            self.assertTrue(expected_keys.issubset(technician.keys()))

    def test_get_technicians_list_function(self):

        # Llamar a la función para obtener la lista de técnicos
        technicians_list = get_technicians_list()

        # Asegurar de que la lista no esté vacía y contenga las claves esperadas
        self.assertTrue(len(technicians_list) > 0)
        expected_keys = {'full_name', 'category', 'total_hours_worked', 'hours_worked_total_amount', 'orders_cuantity'}
        for technician in technicians_list:
            self.assertTrue(expected_keys.issubset(technician.keys()))

        # Asegurar de que el monto total a cobrar sea mayor o igual a 1
        for technician in technicians_list:
            self.assertTrue(technician['hours_worked_total_amount'] >= 1)
        
        # Asegurar de que las horas trabajadas sean mayores o iguales a 1
        for technician in technicians_list:
            self.assertTrue(technician['total_hours_worked'] >= 1)
        
        # Asegurar de que la cantidad de pedidos sea mayor o igual a 1
        for technician in technicians_list:
            self.assertTrue(technician['orders_cuantity'] >= 1)

        # Asegurar de que el nombre completo no esté vacío
        for technician in technicians_list:
            self.assertTrue(technician['full_name'])


class TechniciansReportAPIViewTestCase(APITestCase):
    def setUp(self):
        self.username = "user_test"
        self.email = "test@rapihigar.com"
        self.password = "Rapi123"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        tecnico = Tecnico.objects.create(
            first_name='John',
            last_name='Doe',
            category='Plomero'
        )
        Pedido.objects.create(
            client=self.user,
            hours_worked=20,
            technician=tecnico
        )

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_technicians_report(self):
        url = reverse('technicians_report')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        report_data = response.json()

        # Asegurar que el informe contiene las claves esperadas
        expected_keys = {'average_amount', 'less_than_average', 'highest_amount', 'lowest_amount'}
        self.assertTrue(expected_keys.issubset(report_data.keys()))

        # Asegurar que los datos en 'less_than_average', 'highest_amount', y 'lowest_amount' contengan las claves adecuadas
        list_keys = {'full_name', 'total_hours_worked', 'hours_worked_total_amount', 'orders_cuantity'}
        for key in ['less_than_average', 'highest_amount', 'lowest_amount']:
            if isinstance(report_data[key], list) and report_data[key]:  # Asegurar que sea una lista no vacía antes de acceder al índice 0
                self.assertTrue(list_keys.issubset(report_data[key][0].keys()))

        # Asegurar que el monto promedio sea mayor o igual a 1
        self.assertTrue(report_data['average_amount'] >= 1)


class OrdersAPIViewTest(APITestCase):
    def setUp(self):
        self.username = "user_test"
        self.email = "test@rapihigar.com"
        self.password = "Rapi123"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        technician = Tecnico.objects.create(
            first_name='John',
            last_name='Doe',
            category='Plomero'
        )
        Pedido.objects.create(
            client=self.user,
            hours_worked=20,
            technician=technician
        )

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_orders(self):
        # Realiza una solicitud GET a la API
        response = self.client.get('/api/orders/')

        # Verifica que la respuesta tenga un código de estado 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Obtiene los datos de la respuesta
        orders_data = response.data

        # Obtiene todos los pedidos de la base de datos
        all_orders = get_orders()

        # Serializa los objetos Pedido
        serializer = OrdersSerializer(all_orders, many=True)

        # Verifica que los datos de la respuesta sean iguales a los datos serializados
        self.assertEqual(orders_data, serializer.data)


class OrderUpdateAPIViewTest(APITestCase):
    maxDiff = None

    def setUp(self):
        self.username = "user_test"
        self.email = "test@rapihigar.com"
        self.password = "Rapi123"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        self.technician = Tecnico.objects.create(
            first_name='John',
            last_name='Doe',
            category='Plomero'
        )
        self.scheme = Scheme.objects.create(name='Scheme 1')

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
    def test_update_order_success(self):
        # Crear un pedido para probar la función
        order = Pedido.objects.create(
            client=self.user,
            hours_worked=20,
            technician=self.technician,
            type_request=1
        )

        # Preparar los datos para la solicitud PUT
        data = {
            'order_id': order.id,
            'client_id': self.user.id,
            'technician': self.technician.id,
            'hours_worked': 10,
            'type_request': 0,
            'scheme_id': self.scheme.id
        }

        # Realizar una solicitud PUT a la API
        response = self.client.put('/api/order/update/', data, format='json')

        # Verificar que la respuesta tenga un código de estado 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar que el pedido fue actualizado correctamente
        updated_order = Pedido.objects.get(id=order.id)
        self.assertEqual(updated_order.technician, self.technician)
        self.assertEqual(updated_order.hours_worked, 10)
        self.assertEqual(updated_order.type_request, 0)
        self.assertEqual(updated_order.scheme, self.scheme)

        # Verificar que la respuesta contiene los datos esperados
        expected_data = OrdersSerializer(updated_order).data
        self.assertEqual(response.data, expected_data)

    def test_update_order_invalid_data(self):
        # Preparar datos inválidos para la solicitud PUT
        invalid_data = {
            'order_id': 'invalid',
            'client_id': 'invalid',
            'technician': 'invalid',
            'hours_worked': 'invalid',
            'type_request': 'invalid',
            'scheme_id': 'invalid'
        }

        # Realizar una solicitud PUT a la API con datos inválidos
        response = self.client.put('/api/order/update/', invalid_data)

        # Verificar que la respuesta tenga un código de estado 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verificar que la respuesta contiene los errores esperados
        expected_error = {
            'error': "{'order_id': [ErrorDetail(string='A valid integer is required.', code='invalid')], 'client_id': [ErrorDetail(string='A valid integer is required.', code='invalid')], 'technician': [ErrorDetail(string='A valid integer is required.', code='invalid')], 'hours_worked': [ErrorDetail(string='A valid integer is required.', code='invalid')], 'type_request': [ErrorDetail(string='A valid integer is required.', code='invalid')], 'scheme_id': [ErrorDetail(string='A valid integer is required.', code='invalid')]}"
        }
        self.assertEqual(response.data, expected_error)
        
    def tearDown(self):
        # Eliminar todos los objetos de la base de datos
        User.objects.all().delete()
        Tecnico.objects.all().delete()
        Scheme.objects.all().delete()
        Pedido.objects.all().delete()