import streamlit as st 

# Para acesar o emoji picker, Atalho "Windows" + "."
st.title('😁 Meu primeiro Aplicativo Web com Streamlit')

st.header('➡ Brincando com o Streamlit.py')

# Widgets para entrada de dados
n = st.slider('Entre com um número:')

# 'Back-end' em python, com as contas pertinentes
quadrado = n**2
frase = 'O número selecionado ao quadrado é {}'.format(quadrado)

# Colocar na tela os resultados
st.write(frase)