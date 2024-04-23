import streamlit as st

st.title('Widgets')

st.write('São as componentes interativas que o Streamlit oferece.')

st.divider()

st.header('Botão')

def funcao(x):
	st.write('{}, você clicou no botão!'.format(x))

botao = st.button(
	label = 'Clique em mim!',
	key = None,
	help = 'Cuidado ao clicar!',
	type = 'primary',
	disabled = False,
	use_container_width = True,
	on_click = funcao,
	#args = ('Ricardo',),
	kwargs = {'x': 'Fernando'} ) #'primary' ou 'secondary'

st.write(botao)

if botao:
	st.write('Você apertou o botão. Parabéns!')


st.divider()

st.header('Checkbox')

checkbox = st.checkbox(label = 'Assinale a caixa ao lado', 
 	value=True, 
 	key=None, 
 	help='Instrução!', 
 	on_change=None, 
	args=None, 
	kwargs=None,
 	disabled=False, 
 	label_visibility="visible") #hidden #collapsed

st.write(checkbox) 

if checkbox:
	st.write('Você checkou a caixinha!')
else:
	st.write('Assinale a caixinha!')

st.divider()

st.header('Radio')

def aux(x):
	return f'Opção {x}'

radio = st.radio(label = 'Botões de radio', 
	options = ['A', 'B', 'C'] , 
	index = 1, 
	format_func = aux, 
	key = None, 
	help = 'Escolha uma alternativa', 
	on_change = None,  
	args=None, 
	kwargs=None,
	disabled = False, 
	horizontal = True, 
	label_visibility = "visible") #hidden #collapsed

st.write(radio) 

st.divider()

st.header('Selectbox')

selecao = st.selectbox(label = 'Caixa de Seleção', 
	options = ['A', 'B', 'C'] ,
	index = 2, 
	format_func = aux, 
	key = None, 
	help = 'Ajuda!', 
	on_change = None, 
	args=None, 
	kwargs=None,
	disabled = False, 
	label_visibility = "visible")

st.write(selecao) 


st.divider()

st.header('Multiselect')

multipla = st.multiselect(label = 'Caixa de Seleção Multipla', 
	options = ['A', 'B', 'C', 'D'], 
	default = ['A', 'B'], 
	format_func=aux, 
	key=None, 
	help=None, 
	on_change=None, 
	args=None, 
	kwargs=None,
	disabled=False, 
	label_visibility="visible", 
	max_selections=3)

st.write(multipla) 


st.divider()

st.header('Slider')

n = st.slider(label = 'Slider', 
	min_value=25., 
	max_value=200., 
	value= [40., 60.], # é possivel colocar horários e datas (biblioteca datetime)
	step=2.1734, 
	format='%.1f', 
	key=None, 
	help='Entrada numérica!', 
	on_change=None, 
	args=None, 
	kwargs=None,
	disabled=False, 
	label_visibility="visible")

st.write(n) 

st.divider()

st.header('Selection Slider')

s = st.select_slider(label = 'Slider de Seleção', 
	options=['A', 'B', 'C', 'D', 'E'], 
	value='C', 
	format_func=aux, 
	key=None, 
	help='Ajuda', 
	on_change=None, 
	args=None, 
	kwargs=None,
	disabled=False, 
	label_visibility="visible")

st.write(s) 

st.divider()

st.header('Text Input')

texto = st.text_input(label = 'Input de Texto', 
	value="", 
	max_chars=50, 
	key=None, 
	type="default", #"default" ou "password"
	help='Texto', 
	autocomplete=None, 
	on_change=None, 
	args=None, 
	kwargs=None,
	placeholder='Digite seu e-mail', 
	disabled=False, 
	label_visibility="collapsed")
 
st.write(texto) 

st.divider()

st.header('Number Input')

numero = st.number_input(label = 'Entre com um número', 
	min_value = 1., 
	max_value = 15., 
	value = 5., 
	step = 3.141592, 
	format = "%.2f", # '%d' para inteiros, '%e' para notacao cientifica, '%f' para numeros reais
	key = None, 
	help = 'Número', 
	on_change = None, 
	args = None, 
	kwargs = None, 
	disabled = False, 
	label_visibility = "visible")

st.write(numero) 

st.divider()

st.header('Text Area')

texto = st.text_area(label = 'Entre com um texto grande', 
	value="", 
	height=250, 
	max_chars=1500, 
	key=None, 
	help='Texto', 
	on_change=None, 
	args=None, 
	kwargs=None, 
	placeholder='Coloca um texto grandão aqui', 
	disabled=False, 
	label_visibility="visible") # "visible" ou "hidden" ou "collapsed"

st.write(texto) 


