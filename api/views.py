from api.selector import get_technicians_list, get_technicians_report
from rest_framework import viewsets, permissions, serializers
from rapihogar.models import Company
from rest_framework.views import APIView
from django.http import JsonResponse

class CompanySerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Company
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