from django.contrib import admin
from .models import Patient, Operation
from .models import AnesthesiaInfo

admin.site.register(Patient)
admin.site.register(Operation)
admin.site.register(AnesthesiaInfo)
