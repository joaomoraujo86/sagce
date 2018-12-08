
from django.urls import path,include,re_path
from .views import *

urlpatterns = [

#########################################################################################################

	path(r'', home ,name='micro_home'),
	path('onoff', onoff ,name='micro_onoff'),
	path(r'onoff/<int:id>/',equipamentos,name='micro_equipamentos'),
	path('criar_equipamentos', criar_equipamentos ,name='micro_criar_equipamentos'),
	path('equipamento_cadastrados', equipamento_cadastrados ,name='micro_equipamento_cadastrados'),
	path('botao_novo', botao_novo ,name='micro_botao'),
	path(r'update_equipamento/<int:id>/', update_equipamento ,name='micro_update_equipamento'),
	path(r'delete_equipamento/<int:id>/', delete_equipamento ,name='micro_delete_equipamento'),

#########################################################################################################

	path('logout', logout ,name='micro_logout'),
	#path('login', login ,name='micro_login'),
	

#########################################################################################################
	
	path('automacao', automacao ,name='micro_automacao'),


#########################################################################################################
	
	path('agenda_task', agenda_task ,name='micro_agenda_task'),
	path(r'agenda_task/<int:id>/', agenda_task ,name='micro_agenda_task'),
	path('agenda_task_novo', agenda_task_novo ,name='micro_agenda_task_novo'),
	path('agenda_task_cadastradas', agenda_task_cadastradas ,name='micro_agenda_task_cadastradas'),
	path(r'update_agenda_task/<int:id>/', update_agenda_task ,name='micro_update_agenda_task'),
	path(r'delete_agenda_task/<int:id>/', delete_agenda_task ,name='micro_delete_agenda_task'),

#########################################################################################################

	path('agenda', agenda ,name='micro_agenda'),
	path('agenda_novo', agenda_novo ,name='micro_agenda_novo'),
	path('agenda_cadastrados', agenda_cadastrados ,name='micro_agenda_cadastrados'),
	path(r'update_agenda/<int:id>/', update_agenda ,name='micro_update_agenda'),
	path(r'delete_agenda/<int:id>/', delete_agenda ,name='micro_delete_agenda'),
	
#########################################################################################################


	path('cronometro', cronometro ,name='micro_cronometro'),
	path('cronometro_novo', cronometro_novo ,name='micro_cronometro_novo'),
	path(r'update_cronometro/<int:id>/', update_cronometro ,name='micro_update_cronometro'),
	path('cronometro_cadastrados', cronometro_cadastrados ,name='micro_cronometro_cadastrados'),
	path(r'delete_cronometro/<int:id>/', delete_cronometro ,name='micro_delete_cronometro'),

#########################################################################################################
	
    
]
#/(?P<id>\d+)/$