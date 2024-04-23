import streamlit as st

st.title('Widgets - parte B')

st.write('São as componentes interativas que o Streamlit oferece.')

st.divider()

st.header('Datas')

import datetime
data = st.date_input(label = 'Escolha uma data', 
	#value = datetime.date(2023,7,1), 
	value = [datetime.date(2023,7,1), datetime.date(2023,7,7)], 
	min_value = datetime.date(2023,6,15), 
	max_value = datetime.date(2023,7,15), 
	key=None, 
	help='Ajuda', 
	on_change=None, 
	args=None, 
	kwargs=None,
	disabled=False, 
	label_visibility="visible")

st.write(data)
#st.write(data.strftime('%d/%m/%Y'))
st.write(data[0].strftime('%d/%m/%Y'))
st.write(data[1].strftime('%d/%m/%Y'))

st.divider()

st.header('Horas')

import datetime
hora = st.time_input(label = 'Escolha uma hora', 
	value= datetime.time(13,30), # hora, minuto
	key=None, 
	help='Ajuda', 
	on_change=None, 
	args=None, 
	kwargs=None, 
	disabled=False, 
	label_visibility="visible", 
	step=600)

st.write(hora) 

st.divider()

st.header('Camera')

cam = st.camera_input(label = 'Tire uma foto', 
	key=None, 
	help=None, 
	on_change=None, 
	args=None, 
	kwargs=None, 
	disabled=False, 
	label_visibility="visible") 

st.write(cam) 

st.divider()

st.header('Cor')

cor = st.color_picker(label = 'Escolha uma cor', 
	value='#0fc4c9', 
	key=None, 
	help='Ajuda', 
	on_change=None, 
	args=None, 
	kwargs=None, 
	disabled=False, 
	label_visibility="visible")

st.write(cor) 

st.divider()

st.header('Upload de Arquivos')
 
arquivo = st.file_uploader(label = 'Carregue seu arquivo', 
	type='csv', 
	accept_multiple_files=False, 
	key=None, 
	help='Ajuda', 
	on_change=None, 
	args=None, 
	kwargs=None, 
	disabled=False, 
	label_visibility="visible")

st.write(arquivo) 

#st.image(arquivo)

import pandas as pd
dados = pd.read_csv(arquivo)
st.write(dados.head())


st.divider()

st.header('Download de Arquivos')

texto = 'Ricardo Rocha'

st.download_button(label = 'Clique para baixar', 
	data = texto, 
	file_name='superdados.txt', 
	mime=None, 
	key=None, 
	help='Ajuda', 
	on_click=None, 
	args=None, 
	kwargs=None,
	disabled=False, 
	use_container_width=True)


st.divider()

st.header('Editor de DataSets')
 

d = {'Nomes': ['Ricardo', 'João', 'Carlos'],
     'Idades': [36, 50, 25]}

dados = pd.DataFrame(d)

novo = st.experimental_data_editor(data = dados, 
	width=400, 
	height=300, 
	use_container_width=False, 
	#hide_index=None,     
	#column_order=None, #só funcionam na versao 1.23 (st.data_editor) (versao anterior é st.experimental_data_editor)
	#column_config=None, 
	num_rows= 'dynamic', #"fixed", 
	disabled=False, 
	key=None, 
	on_change=None, 
	args=None, 
	kwargs=None)

st.write(novo)




