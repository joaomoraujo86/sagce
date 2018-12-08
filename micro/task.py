from django_celery_beat.models import *
from django.shortcuts import render,redirect
from django.http import HttpResponse
from micro.models import Botao, Botao1, Botao2
from .form import BotaoForm , IntervalForm , CrontabForm
import serial
import time
from datetime import datetime
#from .task import add,teste
from celery.decorators import task
from celery import Celery



 
# We can have either registered task 



	
	

	

    