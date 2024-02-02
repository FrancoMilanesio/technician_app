""" Register models """
from django.contrib import admin
from .models import Tecnico, Pedido, Scheme, Company

admin.site.register(Tecnico)
admin.site.register(Pedido)
admin.site.register(Scheme)
admin.site.register(Company)