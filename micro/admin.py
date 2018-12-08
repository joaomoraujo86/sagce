from django.contrib import admin
from .models import Equipamento,Gpequipamentos

class EquipamentoAdmin(admin.ModelAdmin):
	fields = ['__all__']

	

# Register your models here.
admin.site.register(Equipamento)
