#!/usr/bin/env python
# coding: utf-8

# In[9]:


#import os
#import sys

#print(os.path.dirname(sys.executable))


# In[ ]:


#! pip install --upgrade streamlit

#! pip install --upgrade jinja2

#! pip install --upgrade pandas --user


# In[7]:


import pandas as pd

#Faz isso aqui para obter as colunas da base que usamos no treino do nosso modelo, na ordem correta
#(necessário dessa forma qundo formos passar os dados do usuário para o nosso modelo fazer a predição do preço)
#dados = pd.read_csv("dados.csv", sep =';', encoding='utf-8') #leitura do arquivo que salvamos após os ajustes finais da base
#VAMOS COLOCAR ESSA CARGA LÁ NO LAÇO FOR ANTES DE FAZER A PREDIÇÃO, POIS SENÃO FICA MUITO PESADA A CARGA NO INÍCIO
#E PIOR, PERCEBI QUE A CADA MUDANÇA DE CAMPO ELE PARECE FAZER DE NOVO, FICANDO IMPRATICÁVEL O PREENCHIMENTO
#ENTÃO VAMOS COLOCAR NO LAÇO DO BOTÃO, QUE ELE SÓ VAI FAZER QUANDO FOR ACIONADO O BOTÃO

#print(dados.columns)
#display(dados)

#colunas = list(dados.columns)[:-1] # para retirar a coluna price(que é o y. Mantemos só as colunas de parâmetros X)
#print(colunas)


# In[10]:


import streamlit as st
import joblib

# Leitura do modelo treinado, já salvo em arquivo joblib
# Caso eu não tivesse salvo o modelo, poderia acrescentar aqui o código de treinamento do modelo novamente (mais demorado do que ler)
# Nesse caso precisaria da base de dados para o treino
#modelo = joblib.load('modelo.joblib')
#VAMOS COLOCAR ESSA CARGA LÁ NO LAÇO FOR ANTES DE FAZER A PREDIÇÃO, POIS SENÃO FICA MUITO PESADA A CARGA NO INÍCIO
#E PIOR, PERCEBI QUE A CADA MUDANÇA DE CAMPO ELE PARECE FAZER DE NOVO, FICANDO IMPRATICÁVEL O PREENCHIMENTO
#ENTÃO VAMOS COLOCAR NO LAÇO DO BOTÃO, QUE ELE SÓ VAI FAZER QUANDO FOR ACIONADO O BOTÃO




# VAMOS USAR DICIONÁRIOS PARA AJUDAR A ORGANIZAR E COLETAR OS DADOS

#Dados numéricos
x_numericos = {'latitude': 0, 'longitude': 0, 'accommodates': 0, 'bathrooms': 0, 'bedrooms': 0, 'beds': 0, 'extra_people': 0,
               'minimum_nights': 0, 'ano': 0, 'mes': 0, 'n_amenities': 0, 'host_listings_count': 0}

#Dados true/false
x_tf = {'host_is_superhost': 0, 'instant_bookable': 0}

#Dados com escolha de categoria (Aqui com os campos normais - sem ser dummie. É a forma como o usuário informará os dados)
x_listas = {'property_type': ['Apartment', 'Bed and breakfast', 'Condominium', 'Guest suite', 'Guesthouse', 'Hostel', 'House', 'Loft', 'Outros', 'Serviced apartment'],
            'room_type': ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'],
            'cancellation_policy': ['flexible', 'moderate', 'strict', 'strict_14_with_grace_period']
            }

#como o dicionário x_listas está organizado de uma forma a propiciar a organização de como os dados serão coletados,
#vamos precisar de um dicionário auxiliar, que estará organizado da forma como a nossa base de dados foi organizada para o nosso
#modelo de predição (ou seja, com colunas dummies)
#então, criamos  asegui resse dicionário auxiliar e já ajustamos os seus valores para zero (inicialização)
dicionario = {}
for item in x_listas:
    for valor in x_listas[item]:
        dicionario[f'{item}_{valor}'] = 0  #composição do nome da chave(coluna dummie) e atribuição do valor inicial 0
#print(dicionario) # apenas para visualizarmos o dicionário com campos dummies



# Cria no streamlit(st) os inputs numericos
for item in x_numericos:
    if item == 'latitude' or item == 'longitude':
        valor = st.number_input(f'{item}', step=0.00001, value=0.0, format="%.5f") #format um pouquinho diferente do format do python (% em vez de :)
    elif item == 'extra_people':
        valor = st.number_input(f'{item}', step=0.01, value=0.0) # padrão float já é 2 casas decimais, por isso não uso o format
    else:
        valor = st.number_input(f'{item}', step=1, value=0)
    x_numericos[item] = valor # atualiza o valor no dicionário


# Cria no streamlit(st) os inputs TRUE/FALSE
for item in x_tf:
    valor = st.selectbox(f'{item}', ('Sim', 'Não'))
    if valor == "Sim":
        x_tf[item] = 1
    else:
        x_tf[item] = 0

        
        
# Cria no streamlit(st) os inputs com escolha de categoria que vem de x_listas
# depois, de acordo com a seleção do usuário, atribui o valor (1) no campo dummie (correspondente à escolha do usuário) em dicionario
# veja o artifício usado para construir os nomes dos campos em dicionario (campos dummies)
for item in x_listas:
    valor = st.selectbox(f'{item}', x_listas[item])
    dicionario[f'{item}_{valor}'] = 1
    
botao = st.button('Prever Valor do Imóvel')

if botao: #se botão foi clicado
    #juntamos tudo em dicionario para passar ao nosso modelo
    dicionario.update(x_numericos) #este método update "junta" dois dicionários (acrescenta o x_numericos a dicionario)
    dicionario.update(x_tf) #acrescenta x_tf à dicionario
    
    valores_x = pd.DataFrame(dicionario, index=[0]) #criando um DF a partir do dicionario, para poder passar ao nosso modelo (como é apenas uma linha, passamos o indice 0 - poderíamos passar um range com a quantidade de linhas)
    
    dados = pd.read_csv("dados.csv", sep =';', encoding='utf-8') #leitura do arquivo que salvamos após os ajustes finais da base
    colunas = list(dados.columns)[:-1] # para retirar a coluna price(que é o y. Mantemos só as colunas de parâmetros X)
    valores_x = valores_x[colunas] #fazendo isso, reordenamos as colunas do DF na mesma ordem do base que o modelo foi treinado (List colunas obtida na linha anterior anterior no código)
    
    modelo = joblib.load('modelo.joblib')  #carregando o modelo salvo (desta forma vai carregar de novo toda vez que clicar no botão. Poderia carregar sío uma vez fora do laço, no início do código)
    preco = modelo.predict(valores_x)
    st.write(preco[0])
    

# PARA EXECUTAR NOSSO PROJETO, NÃO CONSEGUIREMOS DIRETO DO JUPYTER. ENTÃO VAMOS GERAR UM ARQUIVO .py
# FILE -> DOWNLOAD AS -> PYTHON (.py)
# EM SEGUIDA VAMOS EXECUTÁ-LO DO PROMPT DE COMANDO (VER AULA 57. Criando botões para as características)
# (streamlit run "003 DeployProjetoAirbnb.py")
# Lembrar de navegar no prompt para a pasta onde estão os arquivos usados: dados.csv, modelo.joblib, e o próprio "003 DeployProjetoAirbnb.py"
# (C:\Users\Salomão Jr\Curso Python Impressionador\Módulo 36 - Projeto 3 - Ciência de Dados - Aplicação de Mercado de Trabalho) ou copiar para uma pasta mais acessível
#
# AQUI NO MEU COMPUTADOR FUNCIONA DO PROMPT NORMAL (E NÃO DO PROMPT DO ANACONDA)
#
# SE FOSSE DO PYCHARM OU DO VSCODE, PODERÍAMOS EXECUTAR MAIS FACILMENTE DE DENTRO DA PRÓPRIA IDE


# In[ ]:





# In[ ]:




