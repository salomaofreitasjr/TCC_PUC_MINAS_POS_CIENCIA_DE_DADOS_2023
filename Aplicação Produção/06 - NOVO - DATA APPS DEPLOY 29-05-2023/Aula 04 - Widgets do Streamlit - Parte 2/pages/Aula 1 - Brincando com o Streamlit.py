import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title('➡ Brincando com o Streamlit')

#Widgets para entrada de dados
n = st.slider(label = 'Entre com um número:',
			  min_value = 100,
			  max_value = 10000,
			  step = 200)
titulo = st.text_input('Entre com o título do gráfico')
cor = st.color_picker('Escolha a cor do gráfico')

tipo = st.radio('Escolha o tipo de gráfico', ['Linha', 'Histograma'])

#'Back-end' em python, com as contas pertinentes
u = np.random.uniform(size = n)

if tipo == 'Linha':
	plt.plot(u, color = cor)
if tipo == 'Histograma':
	plt.hist(u, color = cor, edgecolor = 'white')
plt.title(titulo)

#Colocar na tela os resultados
st.pyplot(plt)

