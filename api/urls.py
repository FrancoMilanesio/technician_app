from rapihogar.models import Company
from rest_framework import routers
from django.urls import path, include
from .views import (
    CompanyViewSet, 
    ListOfTechniciansAPIView,
    TechniciansReportAPIView,
    OrdersAPIView,
    OrderUpdateAPIView,
    ListTechniciansAPIView,
    ListClientsAPIView,
    SchemasListAPIView
)

router = routers.DefaultRouter()
router.register(r'company', CompanyViewSet, basename='company')


urlpatterns = [
    path('', include(router.urls)),
    path('technical/', ListOfTechniciansAPIView.as_view(), name='technical-list'),
    path('technical/report/', TechniciansReportAPIView.as_view(), name='technicians_report'),
    path('orders/', OrdersAPIView.as_view(), name='orders-list'),
    path('order/update/', OrderUpdateAPIView.as_view(), name='order-update'),
    path('technicians/list/', ListTechniciansAPIView.as_view(), name='technicians-list'),
    path('clients/list/', ListClientsAPIView.as_view(), name='clients-list'),
    path('schemas/', SchemasListAPIView.as_view(), name='schemas-list')
]
