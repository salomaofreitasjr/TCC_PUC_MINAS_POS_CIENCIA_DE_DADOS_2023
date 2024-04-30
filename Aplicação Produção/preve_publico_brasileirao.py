import streamlit as st
import datetime
import pandas as pd
import pickle # para salvamento e carregamento de modelos
import joblib # para salvamento e carregamento de modelos
import sklearn
#from sklearn.ensemble import _gb_losses


st.set_page_config(
    page_title = 'Predições de Público nos Jogos do Campeonato Brasileiro',
    page_icon = '⚽',
    layout = 'wide' # configurando o formato de tela
)

##### PREPARAÇÃO ###########

# Todos os times da base, exceto 'América-MG', pois este foi dexiado de fora na dummização
todos_times_dummies = ['América-RN', 'Athletico-PR', 'Atlético-GO', 'Atlético-MG', 'Avaí FC', 'Barueri', 'Botafogo', 'CSA', 'Ceará SC', 'Chapecoense',
               'Corinthians', 'Coritiba FC', 'Criciúma EC', 'Cruzeiro', 'Cuiabá-MT', 'EC Bahia', 'EC Vitória', 'Figueirense FC', 'Flamengo',
               'Fluminense', 'Fortaleza', 'Goiás', 'Grêmio', 'Guarani', 'Internacional', 'Ipatinga FC', 'Joinville-SC', 'Juventude', 'Náutico',
               'Palmeiras', 'Paraná', 'Ponte Preta', 'Portuguesa', 'RB Bragantino', 'Santa Cruz', 'Santo André', 'Santos', 'Sport Recife', 
               'São Paulo', 'Vasco da Gama']

#Graus de investimento possíveis
graus_investimento = ['muito_baixo', 'baixo', 'medio', 'alto', 'muito_alto']

# Dias da semana possíveis
dias_semana_possiveis = ['Domingo', 'Segunda-Feira', 'Terça-Feira', 'Quarta-Feira','Quinta-Feira', 'Sexta-Feira', 'Sábado']
dias_semana_dummies = ['Segunda-Feira', 'Terça-Feira', 'Quarta-Feira','Quinta-Feira', 'Sexta-Feira', 'Sábado'] #Domingo ficou fora na dummização

#  Trimestres possíveis
trimestres_possiveis = ['2º Trimestre', '3º Trimestre', '4º Trimestre']
#  Trimestres dummies
trimestres_dummies = ['3º Trimestre', '4º Trimestre'] #2º Trimestre ficou fora na dummização

# Times no campeonato de 2024 e seus respectivos graus de investimento
times_2024 = ['Athletico-PR', 'Atlético-GO', 'Atlético-MG', 'Botafogo', 'Corinthians', 'Criciúma EC', 'Cuiabá', 'Cruzeiro', 'EC Bahia', 'EC Vitória',
              'Flamengo', 'Fluminense', 'Fortaleza', 'Grêmio', 'Internacional', 'Juventude', 'Palmeiras', 'RB Bragantino', 'São Paulo', 'Vasco da Gama']

grau_investimento_times_2024 = ['alto', 'muito_baixo', 'alto', 'medio', 'alto', 'muito_baixo', 'muito_baixo', 'baixo', 'baixo', 'muito_baixo',
                                'muito_alto', 'medio', 'baixo', 'medio', 'medio', 'muito_baixo', 'muito_alto', 'medio', 'medio', 'medio']

# VAMOS USAR DICIONÁRIOS PARA AJUDAR A ORGANIZAR E COLETAR OS DADOS
# AQUI SÃO AS COLUNAS DA BASE FINAL COM OS CAMPOS E VALORES NORMAIS (ANTES DA PADRONIZAÇÃO, DUMMIZAÇÃO E ENCODING)
#Dados numéricos
x_numericos = {'rodada': 1, 'points_mand_last_5': 0, 'points_visit_last_5': 0, 'colocacao_mandante_antes': 1, 
               'colocacao_visitante_antes': 1}

#Dados encoded (categóricos com ordenação)
x_encoded = {'grau_investimento_mandante': 0, 
             'grau_investimento_visitante': 0}


#Dados com escolha de categoria (Aqui com os campos normais - sem ser dummie. É a forma como o usuário informará os dados)
#Esse dicionário vai ser a base para a criação dos campos dummizados,mais abaixo
x_listas = {'trimestre': trimestres_dummies,
            'dia_semana': dias_semana_dummies,
            'time_mandante': todos_times_dummies, 'time_visitante': todos_times_dummies}

#como o dicionário x_listas está organizado de uma forma a propiciar a organização de como os dados serão coletados,
#vamos precisar de um dicionário auxiliar, que estará organizado da forma como a nossa base de dados foi organizada para o nosso
#modelo de predição (ou seja, com colunas dummies)
#então, criamos a seguir esse dicionário auxiliar e já ajustamos os seus valores para zero (inicialização)
dicionario = {}
for item in x_listas:
    for valor in x_listas[item]:
        dicionario[f'{item}_{valor}'] = 0  #composição do nome da chave(coluna dummie) e atribuição do valor inicial 0
#print(dicionario) # apenas para visualizarmos o dicionário com campos dummies

####### ALGUMAS FUNÇÕES AUXILIARES ##############
# Retorna o dia da semana por extenso
def get_weekday(data):
  # The day of the week with Monday=0, Sunday=6.
  week_days =['Segunda-Feira', 'Terça-Feira', 'Quarta-Feira', 'Quinta-Feira', 'Sexta-Feira', 'Sábado', 'Domingo']
  return week_days[data.weekday()]

# Retorna o Trimestre por extenso
def get_trimestre(data):
  trim_number = ( (data.month - 1) // 3 ) + 1  # calcula o numero do trimestre
  return '{}º Trimestre'.format(trim_number)

# Função de Normalizaçao por escala
# Transforma o valor para um intervalo entre 0 e 1 
def norm_escala(valor, min, max):
  return (valor - min) / (max - min)

###### INÍCIO DO APLICATIVO (INTERFACE) ##########

st.markdown('## Aplicativo de Previsão Público em Jogos do Campeonato Brasileiro de Futebol')

aba_previsao, aba_sobre = st.tabs(['Previsão de Público', 'Sobre'])

with aba_previsao:
    #st.image('puc_minas.jpg', width=30)
    st.markdown('### Forneça os dados do jogo para predição do público esperado')    
    
    # Recebe a entrada de dados de cada campo
    # E já atualiza o valor no dicionário
    #Data (trimestre e dia_semana)
    data = st.date_input(label = 'Data do Jogo:', 
	value = datetime.date(2024,1,1), 
	min_value = datetime.date(2024,1,1), 
	max_value = datetime.date(2024,12,31), 
	)
    # Atualizar no dicionário os campos trimestre e dia_semana
    trim = get_trimestre(data)
    dia_sem = get_weekday(data)
    if trim not in ['1º Trimestre', '2º Trimestre']: # 1 não tem no modelo treinado, e 2 foi retirado na dummização
        dicionario[f'trimestre_{trim}'] = 1 # coluna dummie
    if dia_sem not in ['Domingo']: # Domingo retirado na dummização 
        dicionario[f'dia_semana_{dia_sem}'] = 1 # coluna dummie
    
    # rodada
    rodada = st.slider(label = 'Rodada:',
			  min_value = 1,
			  max_value = 38,
			  step = 1)    
    x_numericos['rodada'] = rodada # atualiza o valor no dicionário

    # time_mandante (e grau_investimento_mandante)
    mandante = st.selectbox('Time Mandante:', times_2024)
    grau_mand = grau_investimento_times_2024[times_2024.index(mandante)]
    if mandante not in ['América-MG']: #'América-MG' saiu na dummização
        dicionario[f'time_mandante_{mandante}'] = 1 # coluna dummie
    x_encoded['grau_investimento_mandante'] = grau_mand # coluna encoded
    
    # time_visitante (e grau_investimento_visitante)
    #times_2024.remove(mandante)
    visitante = st.selectbox('Time Visitante:', times_2024)
    grau_visit = grau_investimento_times_2024[times_2024.index(visitante)]
    if visitante not in ['América-MG']: #'América-MG' saiu na dummização
        dicionario[f'time_visitante_{visitante}'] = 1 # coluna dummie
    x_encoded['grau_investimento_visitante'] = grau_visit # coluna encoded

    # colocacao_mandante_antes
    coloc_mand = st.slider(label = 'Colocação do mandante na tabela:',
			  min_value = 1,
			  max_value = 20,
			  step = 1)    
    x_numericos['colocacao_mandante_antes'] = coloc_mand # atualiza o valor no dicionário
         
    # colocacao_visitante_antes
    coloc_visit = st.slider(label = 'Colocação do visitante na tabela:',
			  min_value = 1,
			  max_value = 20,
			  step = 1)    
    x_numericos['colocacao_visitante_antes'] = coloc_visit # atualiza o valor no dicionário

    # points_mand_last_5
    pontos_mand = st.slider(label = 'Pontos conquistados pelo mandante nas últimas 5 rodadas:',
			  min_value = 0,
			  max_value = 15,
			  step = 1)    
    x_numericos['points_mand_last_5'] = pontos_mand # atualiza o valor no dicionário

    # points_visit_last_5
    pontos_visit = st.slider(label = 'Pontos conquistados pelo visitante nas últimas 5 rodadas:',
			  min_value = 0,
			  max_value = 15,
			  step = 1)    
    x_numericos['points_visit_last_5'] = pontos_visit # atualiza o valor no dicionário

    botao = st.button('Prever Valor do Imóvel')

    if botao: #se botão foi clicado
        #juntamos tudo em dicionario para passar ao nosso modelo
        dicionario.update(x_numericos) #este método update "junta" dois dicionários (acrescenta o x_numericos a dicionario)
        dicionario.update(x_encoded) #acrescenta x_encoded à dicionario
    
        #criando um DF a partir do dicionario, para poder passar ao nosso modelo (como é apenas uma linha, passamos o indice 0 - poderíamos passar um range com a quantidade de linhas)
        valores_x = pd.DataFrame(dicionario, index=[0]) 
        
        #leitura do arquivo que salvamos após os ajustes finais da base, só para pegar as colunas
        dados = pd.read_csv(r'datasets\brasileirao_serie_a_preparada_final_op2.csv', sep =';', encoding='utf-8') 
        colunas = list(dados.drop('publico', axis = 1).columns) # para retirar a coluna publico(que é o y. Mantemos só as colunas de parâmetros X)
        valores_x = valores_x[colunas] #fazendo isso, reordenamos as colunas do DF na mesma ordem do base que o modelo foi treinado (List colunas obtida na linha anterior anterior no código)
        
        # Aplicando as normalizações e codificações no DF
        valores_x['rodada'] = valores_x['rodada'].apply(norm_escala, args = (1, 38) )
        valores_x['points_mand_last_5'] = valores_x['points_mand_last_5'].apply(norm_escala, args = (0, 15) )
        valores_x['points_visit_last_5'] = valores_x['points_visit_last_5'].apply(norm_escala, args = (0, 15) )
        valores_x['colocacao_mandante_antes'] = valores_x['colocacao_mandante_antes'].apply(norm_escala, args = (1, 20) )
        valores_x['colocacao_visitante_antes'] = valores_x['colocacao_visitante_antes'].apply(norm_escala, args = (1, 20) )
        valores_x['grau_investimento_mandante'] = valores_x['grau_investimento_mandante'].map({'muito_baixo': 1, 'baixo': 2, 'medio': 3, 'alto': 4, 'muito_alto': 5}).apply(norm_escala, args = (1, 5))
        valores_x['grau_investimento_visitante'] = valores_x['grau_investimento_visitante'].map({'muito_baixo': 1, 'baixo': 2, 'medio': 3, 'alto': 4, 'muito_alto': 5}).apply(norm_escala, args = (1, 5))
        
        #Exibe para observarmos
        valores_x

        # carrega o modelo 
        modelo = pickle.load(open('modelo_treinado_final.sav', 'rb'))  #carregando o modelo salvo (desta forma vai carregar de novo toda vez que clicar no botão. Poderia carregar sío uma vez fora do laço, no início do código)
        
        # resgatando com joblib o modelo salvo com pickle
        #modelo = joblib.load('modelo_treinado_final.sav')

        # resgatando com joblib o modelo salvo com joblib
        #modelo = joblib.load('melhor_modelo.joblib')

        # Faz a predição e exibe
        publico = modelo.predict(valores_x)
        st.write(publico[0])
    

    with aba_sobre:
        col1, col2 = st.columns([0.07, 0.7]) # cria duas colunas informando a proporção da largura
        col1.image('puc_minas.jpg', width=130)
        col2.subheader('Pós Graduação em Ciência de Dados e Big Data')
        col2.subheader('Trabalho de Conclusão de Curso')    
        st.subheader('UM MODELO DE APRENDIZADO DE MÁQUINA SUPERVISIONADO PARA PREVISÃO DE QUANTIDADE DE PÚBLICO NOS JOGOS DO CAMPEONATO BRASILEIRO DE FUTEBOL')
        st.subheader('Etapa 04: Implantação do Modelo em Produção')
    