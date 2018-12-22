from django_celery_beat.models import *
from django_celery_beat.admin import *
from django.shortcuts import render,redirect
from django.http import HttpResponse
from micro.models import Equipamento,Gpequipamentos
from .form import *
from datetime import datetime
from celery.decorators import task
from celery import Celery
import serial
import time
from django.contrib.auth.decorators import login_required
########################################################
########################################################

def logout(request):
    
    return render (request,'micro/logout.html')
#def login(request):
    
 #   return render (request,'micro/login.html')


@login_required
def home(request):
    hora = datetime.now()
    form = EquipamentoForm()
    return render (request,'micro/index.html',{'hora':hora,'form':form})

########################################################
########################################################

@login_required
def onoff(request):  

	busca = request.GET.get('pesquisa',None)

	if busca:
		botao = Equipamento.objects.all()
		botao = botao.filter(descricao__istartswith=busca)

	else:	
			
		botao = Equipamento.objects.all()
		  

	form = EquipamentoForm()
	hora = datetime.now() 
	return render (request,'micro/onoff.html',{'botao':botao ,'hora': hora,'form':form})

@login_required
def criar_equipamentos(request):
	form = EquipamentoForm()
	botao = Equipamento.objects.all()
	return render (request,'micro/equipamentos.html',{'form':form})

@login_required
def equipamento_cadastrados(request):

	busca = request.GET.get('pesquisa',None)

	if busca:
		botao = Equipamento.objects.all()
		botao = botao.filter(descricao__istartswith=busca)

	else:	

		botao = Equipamento.objects.all()	
	return render (request,'micro/equipamento_cadastrados.html',{'botao':botao})


@login_required
def botao_novo(request):
    form = EquipamentoForm(request.POST or None)
    if form.is_valid():
        form.save()
    return redirect('micro_criar_equipamentos')    

@login_required
def equipamentos(request,id):	

	botao = Equipamento.objects.get(id=id)
	 
	if botao.status == "ON" :
		#ser = serial.Serial('COM2')
		a = r'#RL1001D'
		#str(ser.write(a.encode('utf-8')))
		#str(ser.write(a))
		#ser.read()
		botao.codigo = '#RL1001D'
		#time.sleep(5)
		#ser.close()
		botao.status = "OFF"
		botao.cor = "btn btn-secondary"	
		botao.save()
		return redirect('micro_onoff')

	else:
		#ser = serial.Serial('COM2')
		#a = '#RL1001L'
		#str(ser.write(a.encode('utf-8')))
		#str(ser.write(a))
		#read = ser.read(10)
		#time.sleep(0.0072)
		botao.codigo = '#RL1001L'
		#ser.close()
		botao.status = "ON" 
		#data['botao'] = form.status
		botao.cor = "btn btn-success"
		botao.save()
		#cores.save()
		return redirect('micro_onoff')

@login_required
def update_equipamento(request,id):
	equip = Equipamento.objects.get(id=id)
	form = EquipamentoForm(request.POST or None,instance=equip)

	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect('micro_equipamento_cadastrados')

	else:
		return render (request,'micro/update_equipamentos.html',{'equip':equip,'form':form})

@login_required
def delete_equipamento(request,id):
	form = Equipamento.objects.get(id=id)	
	if request.method == 'POST':
		if form.status == 'OFF':
		
			form.delete()
			return redirect('micro_equipamento_cadastrados')

		else:
			return render (request,'micro/not_delete.html',{'form':form})	
	else:
		return render (request,'micro/delete_equipamento.html',{'form':form})

########################################################
########################################################


@task
def desligar(request,id):	

	botao = Equipamento.objects.get(id=id)
	 
	if botao.status == "ON" :
		#ser = serial.Serial('COM2')
		a = r'#RL1001D'
		#str(ser.write(a.encode('utf-8')))
		#str(ser.write(a))
		#ser.read()
		botao.codigo = '#RL1001D'
		#time.sleep(5)
		#ser.close()
		botao.status = "OFF"
		botao.cor = "btn btn-danger"	
		botao.save()
		return render (request,'micro/onoff.html')


@task
def ligar(request,id):	

	botao = Equipamento.objects.get(id=id)
	 
	if botao.status == "OFF" :
		#ser = serial.Serial('COM2')
		a = r'#RL1001L'
		#str(ser.write(a.encode('utf-8')))
		#str(ser.write(a))
		#ser.read()
		botao.codigo = '#RL1001L'
		#ser.close()
		botao.status = "ON" 
		#data['botao'] = form.status
		botao.cor = "btn btn-primary"
		botao.save()
		#cores.save()
		return render (request,'micro/onoff.html')			

########################################################
########################################################

@login_required
def automacao(request):
	form = IntervalForm()
	return render (request,'micro/automacao.html',{'form':form})
########################################################
########################################################

@login_required
def cronometro(request):
	cronometro = IntervalForm()
	return render (request,'micro/cronometro.html',{'cronometro':cronometro})

@login_required
def cronometro_cadastrados(request):
	form = IntervalSchedule.objects.all()
	return render (request,'micro/cronometro_cadastrados.html',{'form':form})
@login_required
def update_cronometro(request,id):
	equip = IntervalSchedule.objects.get(id=id)
	form = IntervalForm(request.POST or None,instance=equip)

	if request.method == 'POST':
		if form.is_valid():
			a = form.save(commit=False)
			if a.every < 0:
				a.every = 0
				a.save()
			else:
				a.save()
			return redirect('micro_cronometro_cadastrados')

	else:
		return render (request,'micro/update_cronometro.html',{'equip':equip,'form':form})
@login_required
def delete_cronometro(request,id):
	form = IntervalSchedule.objects.get(id=id)	
	if request.method == 'POST':
		
		form.delete()
		return redirect('micro_cronometro_cadastrados')

	else:
		return render (request,'micro/delete_cronometro.html',{'form':form})



@login_required
def cronometro_novo(request):
    #li = <button type="submit">teste</button>
    form = IntervalForm(request.POST or None)
    if form.is_valid():
        form.save()
    return redirect('micro_cronometro')   

########################################################
########################################################
@login_required
def agenda(request):
	form = CrontabSchedule.objects.all()
	agenda = CrontabForm()
	return render (request,'micro/agenda.html',{'agenda':agenda,'form':form})

@login_required
def agenda_cadastrados(request):
	form = CrontabSchedule.objects.all()
	return render (request,'micro/agenda_cadastrados.html',{'form':form})
@login_required
def update_agenda(request,id):
	equip = CrontabSchedule.objects.get(id=id)
	form = CrontabForm(request.POST or None,instance=equip)
	
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect('micro_agenda_cadastrados')

	else:
		return render (request,'micro/update_agenda.html',{'equip':equip,'form':form})

@login_required
def delete_agenda(request,id):
	form = CrontabSchedule.objects.get(id=id)	
	if request.method == 'POST':
		
		form.delete()
		return redirect('micro_agenda_cadastrados')

	else:
		return render (request,'micro/delete_agenda.html',{'form':form})

@login_required
def agenda_novo(request):
    form = CrontabForm(request.POST or None)
    if form.is_valid():
        form.save()
    return redirect('micro_agenda') 
########################################################
########################################################
@login_required
def agenda_task(request):
	teste = GpequipamentosForm()		
	agenda_task = PeriodicTaskForm()
	return render (request,'micro/agenda_task.html',{
					'agenda_task':agenda_task,'teste':teste })
@login_required
def agenda_task_cadastradas(request):

	busca = request.GET.get('pesquisa',None)

	if busca:
		form = PeriodicTask.objects.all()
		form = form.filter(name__istartswith=busca)

	else:	

		teste = Gpequipamentos.objects.all()
		form = PeriodicTask.objects.all()	

	
	return render (request,'micro/agenda_task_cadastradas.html',{'form':form,})
@login_required
def update_agenda_task(request,id):
	equip = PeriodicTask.objects.get(id=id)
	form = PeriodicTaskForm(request.POST or None,instance=equip)
	
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect('micro_agenda_task_cadastradas')

	else:
		return render (request,'micro/update_agenda_task.html',{'equip':equip,'form':form})


@login_required
def delete_agenda_task(request,id):
	form = PeriodicTask.objects.get(id=id)	
	if request.method == 'POST':
		
		form.delete()
		return redirect('micro_agenda_task_cadastradas')

	else:
		return render (request,'micro/delete_agenda_task.html',{'form':form})



@login_required	
def agenda_task_novo(request):    
    teste = GpequipamentosForm(request.POST or None)     
    if teste.is_valid():	    	
    	l = teste.save(commit=False)
    	m = l.Equipamentos_id
    	o = l.Equipamentos.descricao
    	l.save()
    equipamento = o	 
    args= str([1,m])
    form = PeriodicTaskForm(request.POST or None)
    if form.is_valid():
        p = form.save(commit=False)
        p.equipamento = equipamento
        p.args = args
        p.save()
        
    return redirect('micro_agenda_task_cadastradas')
########################################################
########################################################
