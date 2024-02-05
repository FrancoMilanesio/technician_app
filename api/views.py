from api.selector import get_clients, get_orders, get_schemas, get_technicians, get_technicians_list, get_technicians_report, update_order
from rest_framework import viewsets, permissions, serializers, status
from rapihogar.models import Company, Pedido, Tecnico, User, Scheme
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response

class CompanySerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Company
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Pedido
        fields = '__all__'
        depth = 1


class TechniciansSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Tecnico
        fields = '__all__'

class ClientsSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = User
        fields = '__all__'


class SchemasSerializer(serializers.ModelSerializer):
      
     class Meta:
          model = Scheme
          fields = '__all__'

class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.filter()

### 5. Endpoint listado de técnicos ###
class ListOfTechniciansAPIView(APIView):

    def get(self, request):
        try:
            results = get_technicians_list()
            return JsonResponse(results, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

### 6. Endpoint informe ###
class TechniciansReportAPIView(APIView):
    
        def get(self, request):
            try:
                results = get_technicians_report()
                return JsonResponse(results, safe=False)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
            

### 7. Endpoint UPDATE (Opcional) ###
class OrdersAPIView(APIView):
    serializer_class = OrdersSerializer
    def get(self, request):
        try:
            results = get_orders()
            return Response(OrdersSerializer(results, many=True).data, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

class OrderUpdateAPIView(APIView):
    class InputSerializer(serializers.Serializer):
        order_id = serializers.IntegerField()
        client_id = serializers.IntegerField()
        technician = serializers.IntegerField()
        hours_worked = serializers.IntegerField()
        type_request = serializers.IntegerField()
        scheme_id = serializers.IntegerField(allow_null=True)
        
    def put(self, request):
        try:
            serializer = self.InputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            results = update_order(**serializer.validated_data)
            return Response(OrdersSerializer(results).data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListTechniciansAPIView(APIView):
    def get(self, request):
        try:
            results = get_technicians()
            return Response(TechniciansSerializer(results, many=True).data, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

class ListClientsAPIView(APIView):
    def get(self, request):
        try:
            results = get_clients()
            return Response(ClientsSerializer(results, many=True).data, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

class SchemasListAPIView(APIView):
    def get (self, request):
        try:
            results = get_schemas()
            return Response(SchemasSerializer(results, many=True).data, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)