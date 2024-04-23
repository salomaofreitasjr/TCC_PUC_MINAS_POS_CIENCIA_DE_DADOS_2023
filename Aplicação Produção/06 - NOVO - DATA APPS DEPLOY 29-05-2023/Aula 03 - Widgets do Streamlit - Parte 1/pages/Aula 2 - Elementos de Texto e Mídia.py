import streamlit as st

st.title('Elementos de Texto e de Mídia')

st.header('Estrutura de Página com Condicionais')

# paginas = ['Home', 'Primeira Página', 'Segunda Página']
# pagina = st.radio('Escolha a sua página', paginas)


# if pagina == 'Home':
#  	st.subheader('Home')


# if pagina == 'Primeira Página':
#  	st.subheader('Primeira Página')


# if pagina == 'Segunda Página':
#  	st.subheader('Segunda Página')


st.divider()

st.header('🔹 Linguagem Markdown')

st.markdown('# Título 1')

st.title('Título 1')

st.write('# Título 1')


"""
---

# Título 1  

## Título 2   

### Título 3 

#### Título 4

##### Título 5

###### Título 6

---

Texto normal

**Texto em negrito**

*Texto em itálico*

***Texto em negrito e itálico***

~~Texto riscado~~

---

Novos parágrafos são feitos deixando uma linha vazia entre linhas de texto.

Frase simples número 1. 
Frase simples número 2.

É uma boa prática em 
markdown sempre 
deixar uma linha 
vazia entre elementos 
utilizados.

---

## 🔹 Listas

1. Item terceiro
3. Item segundo
1. Item primeiro
	1. Sublista
	2. Sublista.
	1. Sublista..

---

+ Item terceiro
+ Item segundo
+ Item primeiro
	- Sublista
	- Sublista.
	- Sublista..

---

- [ ] Tarefa 1
- [x] ~~Tarefa 2~~


---

## 🔹 Links 

Confira a documentação do [Markdown](https://www.markdownguide.org/ "Documentação OFICIAL").

https://www.markdownguide.org/

---

## 🔹 Emojis

🎭 :smiley: 🙈

---

## 🔹 Tabelas

Coluna 1 | Coluna 2 | Coluna Especial
--- | ---: | :------:
A | Alberto | **Praia** 
B | *Bruna* | ~~Montanha~~

---

## 🔹 Latex

Latex é uma linguagem textual para escrita científica

$$\int_x^y = g(x) - A^2$$


"""

st.latex('\int_x^y = g(x) - A^2')


st.title('Elementos de Mídia')

st.image('arquivos/banner-flai.png')
#st.audio() # para arquivos de áudio. Exemplo *.mp3
st.video('https://s3-us-west-2.amazonaws.com/assets.streamlit.io/videos/hero-video.mp4') # para arquivos de vídeo. Exemplo *.mp4
























































