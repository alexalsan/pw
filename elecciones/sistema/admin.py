from django.contrib import admin
from .models import Partido,Mesa,Resultado,Circunscripcion

# Register your models here.
admin.site.register(Mesa)
admin.site.register(Partido)
admin.site.register(Circunscripcion)
admin.site.register(Resultado)