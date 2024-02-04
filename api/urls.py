from rapihogar.models import Company
from rest_framework import routers
from django.urls import path, include
from .views import (
    CompanyViewSet, 
    ListOfTechniciansAPIView,
    TechniciansReportAPIView
)

router = routers.DefaultRouter()
router.register(r'company', CompanyViewSet, basename='company')


urlpatterns = [
    path('', include(router.urls)),
    #path('login/', include('rest_framework.urls', namespace='rest_framework')),
    path('technical/', ListOfTechniciansAPIView.as_view(), name='technical-list'),
    path('technical/report/', TechniciansReportAPIView.as_view(), name='technicians_report'),
]
