import streamlit as st

st.set_page_config(
    page_title = 'Predições de Público nos Jogos do Campeonato Brasileiro',
    page_icon = '⚽',
    layout = 'wide' # configurando o formato de tela
)

st.markdown('### Previsão de Tendência de Público em Jogos do Campeonato Brasileiro de Futebol')

aba1, aba2 = st.tabs(['Previsão de Público', 'Sobre'])

with aba1:
    st.image('puc_minas.jpg', width=30)
    st.title('Meu Primeiro Aplicativo Streamlit!')
    st.markdown('# Título')    

with aba2:
    col1, col2 = st.columns([0.07, 0.7]) # cria duas colunas informando a proporção da largura
    col1.image('puc_minas.jpg', width=130)
    col2.subheader('Pós Graduação em Ciência de Dados e Big Data')
    col2.subheader('Trabalho de Conclusão de Curso')    
    st.subheader('UM MODELO DE APRENDIZADO DE MÁQUINA SUPERVISIONADO PARA PREVISÃO DE QUANTIDADE DE PÚBLICO NOS JOGOS DO CAMPEONATO BRASILEIRO DE FUTEBOL')
    st.subheader('Etapa 04: Implantação do Modelo em Produção')
    