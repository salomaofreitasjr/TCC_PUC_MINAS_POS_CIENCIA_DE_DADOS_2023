import streamlit as st 

st.title('Meu Primeiro Aplicativo Streamlit!')

st.markdown('# Título')
st.sidebar.markdown('## Título')
st.markdown('### Título')
st.sidebar.markdown('**Título**')

st.markdown('Emojis do markdown: :smiley: :poop: :sparkles:')

st.write('Entrada padrao de texto')

st.text('Texto com aquela fonte quadrada')

st.code('import pandas as pd')

st.sidebar.latex('\int_a^bf(x)dx = F(b) - F(a)')

st.sidebar.title('Barra Lateral')

n = st.slider('Entre com um número', 10, 70, 20, 2)

st.title(f'O quadrado de {n} é {n**2}')


nome = st.text_input('Digite o seu nome!')

botao = st.button('Clique aqui para finalizar a aula!')

if botao:
	st.info(f'**{nome.upper()}**, parabéns! Você concluiu a sua primeira aula de Streamlit!')
	st.balloons()







