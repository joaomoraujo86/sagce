from django.db import models
from datetime import datetime


# Create your models here.

class Equipamento(models.Model):
	descricao = models.CharField(max_length = 16)
	status = models.CharField(max_length = 10,default='OFF')
	codigo = models.CharField(max_length = 8 , default='0') 
	cor =  models.CharField(max_length = 30 , default='btn btn-danger')
	def __str__(self):
		return self.descricao

class Horario(models.Model):
	data_e_hora_atuais = datetime.now()
	#data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y')
	horario = data_e_hora_atuais.strftime('%d/%m/%Y\n %H:%M')

class Gpequipamentos(models.Model):
	
	Equipamentos = models.ForeignKey(Equipamento,on_delete=models.CASCADE)
	
    
    
	def __str__(self):
		return self.Equipamento.id

		



			