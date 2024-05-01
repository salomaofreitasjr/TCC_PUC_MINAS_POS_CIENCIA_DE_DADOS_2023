import streamlit as st
import datetime
import pandas as pd
import pickle


st.set_page_config(
    page_title = 'Predições de Público nos Jogos do Campeonato Brasileiro',
    page_icon = '⚽',
    layout = 'wide' # configurando o formato de tela
)

##### PREPARAÇÃO ###########
# Para publicação, precisamos colocar os paths assim, senão não funciona 
logo_puc_minas = r'Aplicacao_Producao/figuras/puc_minas.jpg'
arquivo_dataset = r'Aplicacao_Producao/datasets/brasileirao_serie_a_preparada_final_op2.csv' 

#Para rodar na máquina local, colocamos assim, senão não funciona
#logo_puc_minas = r'figuras/puc_minas.jpg'
#arquivo_dataset = r'datasets/brasileirao_serie_a_preparada_final_op2.csv' 

# 1º Melhor Modelo, mas arquivo do modelo ficou muito grande (+300MB) para comitar no GitHub
# (o que é necessário para publicar a aplicação no servidor do streamlita ou do GitHub )
#arquivo_modelo = r'modelos\modelo_treinado_final.sav'

# 2º Melhor Modelo - vamos usar para publicar a aplicação para demonstração, já que o tamanho do arquivo ficou pequeno (-2MB)
arquivo_modelo = r'Aplicacao_Producao/modelos/modelo_treinado_GradientBoostingRegressor().sav' # Colocamos a barra ao contrário para func no Windows e Linux (deploy)

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
times_2024 = ['Athletico-PR', 'Atlético-GO', 'Atlético-MG', 'Botafogo', 'Corinthians', 'Criciúma EC', 'Cuiabá-MT', 'Cruzeiro', 'EC Bahia', 'EC Vitória',
              'Flamengo', 'Fluminense', 'Fortaleza', 'Grêmio', 'Internacional', 'Juventude', 'Palmeiras', 'RB Bragantino', 'São Paulo', 'Vasco da Gama']

grau_investimento_times_2024 = ['alto', 'muito_baixo', 'alto', 'medio', 'alto', 'muito_baixo', 'muito_baixo', 'baixo', 'baixo', 'muito_baixo',
                                'muito_alto', 'medio', 'baixo', 'medio', 'medio', 'muito_baixo', 'muito_alto', 'medio', 'medio', 'medio']



#Dados com escolha de categoria (Aqui com os campos normais - sem ser dummie. É a forma como o usuário informará os dados)
#Esse dicionário vai ser a base para a criação dos campos dummizados,mais abaixo
x_listas = {'trimestre': trimestres_dummies,
            'dia_semana': dias_semana_dummies,
            'time_mandante': todos_times_dummies, 'time_visitante': todos_times_dummies}



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

# Formatação de exibição de data
def formata_data(data):
    return data.strftime("%d/%m/%Y")

# Formatação de exibição de número
def formata_numero(num):
    return '{:,.0f}'.format(num).replace(',','.')


###### INÍCIO DO APLICATIVO (INTERFACE) ##########

#st.title(':blue[Aplicativo de Previsão Público em Jogos do Campeonato Brasileiro de Futebol]')

col1, col2 = st.columns([0.5,9.5])
col1.image(logo_puc_minas, width=80)
col2.header('Aplicativo de Previsão Público em Jogos do Campeonato Brasileiro de Futebol ⚽')

aba_previsao_individual, aba_previsao_arquivo, aba_sobre = st.tabs(['Previsão de Público - Jogo Individual',
                                                                    'Previsão de Público - Jogos em lote', 
                                                                    'Sobre'])

with aba_previsao_individual:
    #### PREPARAÇÃO DOS DADOS #####################
    # VAMOS USAR DICIONÁRIOS PARA AJUDAR A ORGANIZAR E COLETAR OS DADOS
    # AQUI SÃO AS COLUNAS DA BASE FINAL COM OS CAMPOS E VALORES NORMAIS (ANTES DA PADRONIZAÇÃO, DUMMIZAÇÃO E ENCODING)
    #Dados numéricos
    x_numericos = {'rodada': 1, 'points_mand_last_5': 0, 'points_visit_last_5': 0, 'colocacao_mandante_antes': 1, 
                   'colocacao_visitante_antes': 1}

    #Dados encoded (categóricos com ordenação)
    x_encoded = {'grau_investimento_mandante': 0, 'grau_investimento_visitante': 0}
    
    #como o dicionário x_listas está organizado de uma forma a propiciar a organização de como os dados serão coletados,
    #vamos precisar de um dicionário auxiliar, que estará organizado da forma como a nossa base de dados foi organizada para o nosso
    #modelo de predição (ou seja, com colunas dummies)
    #então, criamos a seguir esse dicionário auxiliar e já ajustamos os seus valores para zero (inicialização)
    dicionario = {}
    for item in x_listas:
        for valor in x_listas[item]:
            dicionario[f'{item}_{valor}'] = 0  #composição do nome da chave(coluna dummie) e atribuição do valor inicial 0
    #print(dicionario) # apenas para visualizarmos o dicionário com campos dummies



    ######## INTERFACE ########################
    st.markdown('### Forneça os dados do jogo para predição do público esperado')    
    
    with st.container(border=True):  # linha 1
        st.markdown('###### Dados do Jogo')    

        # Recebe a entrada de dados de cada campo
        # E já atualiza o valor no dicionário
        col1_1, col1_2 = st.columns([2, 8], gap='small') # cria duas colunas informando a proporção da largura
        with col1_1:
            with st.container(border=True, height=115):
                #Data (trimestre e dia_semana)
                data = st.date_input(label = '**Data do Jogo:**', value = datetime.date(2024,1,13), min_value = datetime.date(2024,1,1), 
                                    max_value = datetime.date(2024,12,31), format="DD/MM/YYYY"	)
                # Atualizar no dicionário os campos trimestre e dia_semana
                trim = get_trimestre(data)
                dia_sem = get_weekday(data)
                if trim not in ['1º Trimestre', '2º Trimestre']: # 1 não tem no modelo treinado, e 2 foi retirado na dummização
                    dicionario[f'trimestre_{trim}'] = 1 # coluna dummie
                if dia_sem not in ['Domingo']: # Domingo retirado na dummização 
                    dicionario[f'dia_semana_{dia_sem}'] = 1 # coluna dummie
            
        with col1_2:
            with st.container(border=True, height=115):
                # rodada
                rodada = st.slider(label = '**Rodada do Campeonato:**',
                        min_value = 1,
                        max_value = 38,
                        step = 1)    
                x_numericos['rodada'] = rodada # atualiza o valor no dicionário
        
    with st.container(border=True): # linha 2
        st.markdown('###### Dados do Mandante')
        col2_1, col2_2, col2_3 = st.columns([2, 4.3, 3.7], gap='small') # cria duas colunas informando a proporção da largura
        with col2_1:
            with st.container(border=True, height=115):
                # time_mandante (e grau_investimento_mandante)
                mandante = st.selectbox('**Time Mandante:**', times_2024)
                grau_mand = grau_investimento_times_2024[times_2024.index(mandante)]
                if mandante not in ['América-MG']: #'América-MG' saiu na dummização
                    dicionario[f'time_mandante_{mandante}'] = 1 # coluna dummie
                x_encoded['grau_investimento_mandante'] = grau_mand # coluna encoded

        with col2_2:
            with st.container(border=True, height=115):
                # colocacao_mandante_antes
                coloc_mand = st.slider(label = '**Colocação do mandante na tabela:**',
                        min_value = 1,
                        max_value = 20,
                        step = 1)    
                x_numericos['colocacao_mandante_antes'] = coloc_mand # atualiza o valor no dicionário

        with col2_3:
            with st.container(border=True, height=115):
                # points_mand_last_5
                pontos_mand = st.slider(label = '**Pontos conquistados pelo mandante nas últimas 5 rodadas:**',
                        min_value = 0,
                        max_value = 15,
                        step = 1)    
                x_numericos['points_mand_last_5'] = pontos_mand # atualiza o valor no dicionário

    with st.container(border=True): # linha 3
        st.markdown('###### Dados do Visitante')
        col3_1, col3_2, col3_3 = st.columns([2, 4.3, 3.7], gap='small') # cria duas colunas informando a proporção da largura
        with col3_1:
            with st.container(border=True, height=115):
                # time_visitante (e grau_investimento_visitante)
                #times_2024.remove(mandante)
                visitante = st.selectbox('**Time Visitante:**', times_2024)
                grau_visit = grau_investimento_times_2024[times_2024.index(visitante)]
                if visitante not in ['América-MG']: #'América-MG' saiu na dummização
                    dicionario[f'time_visitante_{visitante}'] = 1 # coluna dummie
                x_encoded['grau_investimento_visitante'] = grau_visit # coluna encoded
        with col3_2:
            with st.container(border=True, height=115):
                # colocacao_visitante_antes
                coloc_visit = st.slider(label = '**Colocação do visitante na tabela:**',
                        min_value = 1,
                        max_value = 20,
                        step = 1)    
                x_numericos['colocacao_visitante_antes'] = coloc_visit # atualiza o valor no dicionário

        with col3_3:
            with st.container(border=True, height=115):
                # points_visit_last_5
                pontos_visit = st.slider(label = '**Pontos conquistados pelo visitante nas últimas 5 rodadas:**',
                        min_value = 0,
                        max_value = 15,
                        step = 1)    
                x_numericos['points_visit_last_5'] = pontos_visit # atualiza o valor no dicionário


    botao = st.button('**Prever público para o jogo**')

    if botao: #se botão foi clicado
        #juntamos tudo em dicionario para passar ao nosso modelo
        dicionario.update(x_numericos) #este método update "junta" dois dicionários (acrescenta o x_numericos a dicionario)
        dicionario.update(x_encoded) #acrescenta x_encoded à dicionario
    
        #criando um DF a partir do dicionario, para poder passar ao nosso modelo (como é apenas uma linha, passamos o indice 0 - poderíamos passar um range com a quantidade de linhas)
        valores_x = pd.DataFrame(dicionario, index=[0]) 
        
        #leitura do arquivo que salvamos após os ajustes finais da base, só para pegar as colunas
        dados = pd.read_csv(arquivo_dataset, sep =';', encoding='utf-8') 
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
        #valores_x

        # carrega o modelo 
        modelo = pickle.load(open(arquivo_modelo, 'rb'))  #carregando o modelo salvo (desta forma vai carregar de novo toda vez que clicar no botão. Poderia carregar sío uma vez fora do laço, no início do código)
        
        # Faz a predição e exibe, formatando a saída com . separador de milhar e sem casas decimais
        publico = modelo.predict(valores_x)
        st.markdown( '### Público estimado: ' + formata_numero(publico[0]) )

with aba_previsao_arquivo:
    st.markdown('### Upload de arquivo com dados de jogos para predição do público esperado') 
    with st.container(border=True): # linha 3
        arquivo = st.file_uploader(label = '**Carregue seu arquivo**', type=['csv','xlsx'], accept_multiple_files=False, 
                                   key=None, help='Ajuda', on_change=None, args=None, kwargs=None, 
                                   disabled=False, label_visibility="visible")

    if not (arquivo is None): 
        #st.write(arquivo.type) 
    
        # Lê em um DF
        if arquivo.type == 'text/csv':
            dados = pd.read_csv(arquivo, sep =';', encoding='latin')             
        else: # excel
            dados = pd.read_excel(arquivo)

        dados['data'] = pd.to_datetime(dados['data'], dayfirst=True) # para garantir o reconhecimento do tipo dada corretamente
        #st.write(dados.head(10))

        ###### PREPARAÇÃO DOS DADOS ########################################
        dicionario = {}
        for item in x_listas:
            for valor in x_listas[item]:
                dicionario[f'{item}_{valor}'] = [0] * len(dados)  # os itens são criados todos zerados
        
        #Dados numéricos - CRIADOS COM OS DADOS DO ARQUIVO LIDO
        x_numericos = {'rodada': list(dados['rodada']), 
                       'points_mand_last_5': list(dados['points_mand_last_5']), 
                       'points_visit_last_5': list(dados['points_visit_last_5']), 
                       'colocacao_mandante_antes': list(dados['colocacao_mandante_antes']), 
                       'colocacao_visitante_antes': list(dados['colocacao_visitante_antes'])}

        #Dados encoded (categóricos com ordenação) - VALORES TEMPORÁRIOS
        x_encoded = {'grau_investimento_mandante': list(dados['time_mandante']),  # aqui os valores são temporários, depois colocaremos o valore correto
                     'grau_investimento_visitante': list(dados['time_visitante'])}
        

        # Ajuste de dados transformados
        for i in range(len(dados)):
            # Atualizar no dicionário os campos trimestre e dia_semana
            trim = get_trimestre(dados.loc[i, 'data'])
            dia_sem = get_weekday(dados.loc[i, 'data'])
            if trim not in ['1º Trimestre', '2º Trimestre']: # 1 não tem no modelo treinado, e 2 foi retirado na dummização
                dicionario[f'trimestre_{trim}'][i] = 1 # coluna dummie
            if dia_sem not in ['Domingo']: # Domingo retirado na dummização 
                dicionario[f'dia_semana_{dia_sem}'][i] = 1 # coluna dummie
        
            # time_mandante (e grau_investimento_mandante)
            mandante = dados.loc[i, 'time_mandante']
            grau_mand = grau_investimento_times_2024[times_2024.index(mandante)]
            if mandante not in ['América-MG']: #'América-MG' saiu na dummização
                dicionario[f'time_mandante_{mandante}'][i] = 1 # coluna dummie
                x_encoded['grau_investimento_mandante'][i] = grau_mand # coluna encoded
            
            # time_visitante (e grau_investimento_visitante)
            visitante = dados.loc[i, 'time_visitante']
            grau_visit = grau_investimento_times_2024[times_2024.index(visitante)]
            if visitante not in ['América-MG']: #'América-MG' saiu na dummização
                dicionario[f'time_visitante_{visitante}'][i] = 1 # coluna dummie
                x_encoded['grau_investimento_visitante'][i] = grau_visit # coluna encoded

        
        #juntamos tudo em dicionario para passar ao nosso modelo
        dicionario.update(x_numericos) #este método update "junta" dois dicionários (acrescenta o x_numericos a dicionario)
        dicionario.update(x_encoded) #acrescenta x_encoded à dicionario

        #criando um DF a partir do dicionario, para poder passar ao nosso modelo (como é apenas uma linha, passamos o indice 0 - poderíamos passar um range com a quantidade de linhas)
        valores_x = pd.DataFrame(dicionario) #, index=[0]) 
       
        #leitura do arquivo que salvamos após os ajustes finais da base, só para pegar as colunas
        dados_prep = pd.read_csv(arquivo_dataset, sep =';', encoding='utf-8') 
        colunas = list(dados_prep.drop('publico', axis = 1).columns) # para retirar a coluna publico(que é o y. Mantemos só as colunas de parâmetros X)
        valores_x = valores_x[colunas] #fazendo isso, reordenamos as colunas do DF na mesma ordem do base que o modelo foi treinado (List colunas obtida na linha anterior anterior no código)
        
        # Aplicando as normalizações e codificações no DF
        valores_x['rodada'] = valores_x['rodada'].apply(norm_escala, args = (1, 38) )
        valores_x['points_mand_last_5'] = valores_x['points_mand_last_5'].apply(norm_escala, args = (0, 15) )
        valores_x['points_visit_last_5'] = valores_x['points_visit_last_5'].apply(norm_escala, args = (0, 15) )
        valores_x['colocacao_mandante_antes'] = valores_x['colocacao_mandante_antes'].apply(norm_escala, args = (1, 20) )
        valores_x['colocacao_visitante_antes'] = valores_x['colocacao_visitante_antes'].apply(norm_escala, args = (1, 20) )
        valores_x['grau_investimento_mandante'] = valores_x['grau_investimento_mandante'].map({'muito_baixo': 1, 'baixo': 2, 'medio': 3, 'alto': 4, 'muito_alto': 5}).apply(norm_escala, args = (1, 5))
        valores_x['grau_investimento_visitante'] = valores_x['grau_investimento_visitante'].map({'muito_baixo': 1, 'baixo': 2, 'medio': 3, 'alto': 4, 'muito_alto': 5}).apply(norm_escala, args = (1, 5))
        ###############################################

        

        # carrega o modelo 
        modelo = pickle.load(open(arquivo_modelo, 'rb'))  
                
        # Faz a predição e inclui como uma coluna do DF referente ao arquivo de entrada, formatando a saída com . separador de milhar e sem casas decimais
        #publico = modelo.predict(valores_x)
        dados['PÚBLICO ESTIMADO'] = modelo.predict(valores_x)
               

        #st.divider()
        #st.write(valores_x.head(10)) # DF com os valores preparados para aplicação no modelo de ML

        st.write('')
        st.markdown( '### Veja abaixo a quantidade de público prevista para cada jogo no arquivo indicado'  )
        
        #### Ajuste de algumas colunas para visualização
        #st.markdown( '### Público estimado: {:,.0f} pessoas'.format(int(publico[0])).replace(',','.')  )
        dados['data'] = dados['data'].apply(formata_data)
        dados['points_mand_last_5'] = dados['points_mand_last_5'].apply(int)
        dados['points_visit_last_5'] = dados['points_visit_last_5'].apply(int)
        dados['colocacao_mandante_antes'] = dados['colocacao_mandante_antes'].apply(int)
        dados['colocacao_visitante_antes'] = dados['colocacao_visitante_antes'].apply(int)
        
        dados['publico'] = dados['publico'].apply(formata_numero)
        dados['PÚBLICO ESTIMADO'] = dados['PÚBLICO ESTIMADO'].apply(formata_numero)

        dados = dados.rename(columns={'rodada': 'Rodada', 'data': 'Data', 'time_mandante': 'Time Mandante', 'time_visitante': 'Time Visitante',
                              'points_mand_last_5': 'Pontos do Mandante nas Últimas 5 Rodadas',
                              'points_visit_last_5': 'Pontos do Visitante nas Últimas 5 Rodadas',
                              'colocacao_mandante_antes': 'Classificação do Mandante na Tabela',
                              'colocacao_visitante_antes': 'Classificação do Visitante na Tabela',
                              'publico': 'Público Real' })


        #dados.index = [''] * len(dados)
        dados.index = dados.index + 1  # para os índices mostrarem o numero da linha
        
        # funçao para colorir as linhas do DF
        # row.name é o indice da linha
        def color_row_coding(row):
            return ['background-color:lightgray'] * len(row) if row.name % 2 == 0 else ['background-color:white'] * len(row)
                
        with st.container(border=True): # linha 3
            st.dataframe(dados.style.apply(color_row_coding, axis=1))#, hide_index=True)

with aba_sobre:
        col1, col2 = st.columns([0.13, 0.87]) # cria duas colunas informando a proporção da largura
        col1.image(logo_puc_minas, width=200)
        col2.markdown('#### PÓS GRADUAÇÃO EM CIÊNCIA DE DADOS E BIG DATA')
        col2.markdown('#### TRABALHO DE CONCLUSÃO DE CURSO')    
        col2.markdown('#### MAIO/2024')
        
        st.write('')
        st.write('')
        
        st.subheader('Esse aplicativo é parte do trabalho: ' +
                     '"Um Modelo de Aprendizado de Máquina Supervisionado para Previsão ' + 
                     'de Quantidade de Público nos Jogos do Campeonato Brasileiro de Futebol"')    
        
        st.subheader('Etapa 03: Implantação do Modelo em Produção')

        st.write('')
        st.write('')        
        
        st.markdown('#### Salomão Fernandes de Freitas Júnior ' +
                     '(salomaofreitasjr@gmail.com)')

        
        st.markdown('#### Repositório do Projeto: https://github.com/salomaofreitasjr/TCC_PUC_MINAS_POS_CIENCIA_DE_DADOS_2023')


        