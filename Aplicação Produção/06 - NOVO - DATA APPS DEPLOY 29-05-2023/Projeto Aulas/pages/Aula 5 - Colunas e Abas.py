import streamlit as st

st.title('Colunas e Abas')

st.write('Como adicionar colunas - Maneira direta')

col1, col2, col3 = st.columns(3)

col1.header('Coluna 1')
col2.header('Coluna 2')

col1.button('Botão da Coluna 1')
col2.button('Botão da Coluna 2')

col3.header('Coluna 3')
col3.button('Botão da Coluna 3')


st.divider()

st.write('Como adicionar colunas - Maneira via "with"')

col1, col2, col3 = st.columns(3)

with col1:  #with é do básico Python. Não é do streamlit
	st.header('Coluna 1')
	#st.button('Botão da Coluna 1', key = 'b') # quando não colocamos o argumento key, ele usa o label como identificador, como já tem um, dá problema
	st.button('Botão - Coluna 1')  # Aqui simplesmente colocamos um label diferente do de cima
	

with col2:
	st.header('Coluna 2')
	st.button('Botão - Coluna 2')

with col3:
	st.header('Coluna 3')
	st.button('Botão - Coluna 3')



st.divider()

st.write('Como mexer no tamanho de cada coluna')

#col1, col2, col3 = st.columns([1,1,1])  #[1,1,1] significa a proporção de uma coluna em relação às outras. Aqui é tudo igual
col1, col2, col3 = st.columns([2,3,2])

with col1:
	st.subheader('Coluna 1')
	st.button('Botão -> Coluna 1', use_container_width = True) #use_container_width = True, o botão usa o tamanho total da coluna

with col2:
	st.subheader('Coluna 2')
	st.button('Botão -> Coluna 2', use_container_width = True)

with col3:
	st.subheader('Coluna 3')
	st.button('Botão -> Coluna 3', use_container_width = True)



st.divider()

st.write('Como colocar espaço entre as colunas')

#col1, col_vazia1, col2, col_vazia2, col3 = st.columns([4,1,4,1,8])
col1, _, col2, _, col3 = st.columns([4,1,4,1,8])

with col1:
	st.subheader('Coluna 1')
	st.button('Botão --> Coluna 1', use_container_width = True)

with col2:
	st.subheader('Coluna 2')
	st.button('Botão --> Coluna 2', use_container_width = True)

with col3:
	st.subheader('Coluna 3')
	st.button('Botão --> Coluna 3', use_container_width = True)

#Colunas dentro de coluna
	c1, c2 = st.columns(2)

	with c1:
		st.write('Sub-Coluna 1')
		st.button('Botão Sub1', use_container_width = True)

	with c2:
		st.write('Sub-Coluna 2')
		st.button('Botão Sub2', use_container_width = True)


st.divider()

st.write('Como adicionar abas')

abas = ['Primeira Aba', 'Segunda Aba', 'Terceira Aba']
aba1, aba2, aba3 = st.tabs(abas)

with aba1:
	st.subheader('Aba 1')
	st.button('Botão -> Aba 1', use_container_width = True)

with aba2:
	st.subheader('Aba 2')
	st.button('Botão -> Aba 2', use_container_width = True)

with aba3:
	st.subheader('Aba 3')
	st.button('Botão -> Aba 3', use_container_width = True)


	c1, c2 = st.columns(2)

	with c1:
		st.write('Sub-Coluna 1')
		st.button('Botão Aba 1', use_container_width = True)

	with c2:
		st.write('Sub-Coluna 2')
		st.button('Botão Aba 2', use_container_width = True)



st.divider()

st.write('Como adicionar abas na "gambiarra"')

radio = st.radio(label = 'Botões de radio', 
	options = ['Aba 1', 'Aba 2', 'Aba 3'] , 
	horizontal = True,
	label_visibility = "collapsed")

if radio == 'Aba 1':
	st.header('Conteudo da ABA 1')

if radio == 'Aba 2':
	st.header('Conteudo da ABA 2')

if radio == 'Aba 3':
	st.header('Conteudo da ABA 3')