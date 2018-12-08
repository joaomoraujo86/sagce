from datetime import datetime



class Horario():		
	data_e_hora_atuais = datetime.now()
	#data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y')
	horario = data_e_hora_atuais.strftime('%d/%m/%Y\n %H:%M')

	
