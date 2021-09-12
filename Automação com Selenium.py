#!/usr/bin/env python
# coding: utf-8

# # Automação Web e Busca de Informações com Python
# 
# #### Desafio: 
# 
# Trabalhamos em uma importadora e o preço dos nossos produtos é vinculado a cotação de:
# - Dólar
# - Euro
# - Ouro
# 
# Precisamos pegar na internet, de forma automática, a cotação desses 3 itens e saber quanto devemos cobrar pelos nossos produtos, considerando uma margem de contribuição que temos na nossa base de dados.
# 
# Base de Dados: https://drive.google.com/drive/folders/1KmAdo593nD8J9QBaZxPOG1yxHZua4Rtv?usp=sharing
# 
# Para isso, vamos criar uma automação web:
# 
# - Usaremos o selenium
# - Importante: baixar o webdriver

# In[24]:


# Passo 1: Entrar na internet
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

navegador = webdriver.Chrome()

# Passo 2: Pegar as cotações do Dolar
# entrar no google
navegador.get("https://www.google.com/")

# pesquisar "cotação dolar"
navegador.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("Cotação dólar")
navegador.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

# pegar o número que aparece no resultado do Google
cotacao_dolar = navegador.find_element_by_xpath('//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")
print(cotacao_dolar)

# Passo 3: Pegar a cotação do Euro
# entrar no google
navegador.get("https://www.google.com/")

# pesquisar "cotação dolar"
navegador.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("Cotação euro")
navegador.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

# pegar o número que aparece no resultado do Google
cotacao_euro = navegador.find_element_by_xpath('//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")
print(cotacao_euro)

# Passo 4: Pegar a cotação do Ouro
# entrar no site do melhor cambio 
navegador.get("https://www.melhorcambio.com/ouro-hoje")

# pegar a cotação do ouro
cotacao_ouro = navegador.find_element_by_xpath('//*[@id="comercial"]').get_attribute("value")
cotacao_ouro = cotacao_ouro.replace(",", ".")
print(cotacao_ouro)

navegador.quit()


# ### Agora vamos atualiza a nossa base de preços com as novas cotações

# - Importando a base de dados

# In[26]:


# Passo 5: Importar e atualizar a base de dados
import pandas as pd

tabela = pd.read_excel("Produtos.xlsx") #caso tenha mais de uma aba do excel usar o parametro Sheets="Nome_da_aba"
display(tabela)


# - Atualizando os preços e o cálculo do Preço Final

# In[31]:


# Atualizara cotação
# Onde a coluna "Moeda" = "Dólar"
# tabela.loc[linha, coluna]
tabela.loc[tabela["Moeda"] == "Dólar", "Cotação"] = float(cotacao_dolar)

tabela.loc[tabela["Moeda"] == "Euro", "Cotação"] = float(cotacao_euro)

tabela.loc[tabela["Moeda"] == "Ouro", "Cotação"] = float(cotacao_ouro)

# Atualizar o preço de compra > preço original * cotação
tabela["Preço Base Reais"] = tabela["Preço Base Original"] * tabela["Cotação"]

# Atualizar o preço de venda > preço de compra * margem
tabela["Preço Final"] = tabela["Preço Base Reais"] * tabela["Margem"]

# Formatar as casas decimais de algumas colunas
tabela["Preço Final"] = tabela["Preço Final"].map("{:.2f}".format)
tabela["Preço Base Reais"] = tabela["Preço Base Reais"].map("{:.2f}".format)
tabela["Cotação"] = tabela["Cotação"].map("{:.2f}".format)

display(tabela)


# ### Agora vamos exportar a nova base de preços atualizada

# In[32]:


# Passo 6: Exportar a base de dados atualizados
tabela.to_excel("Produtos Novo.xlsx", index=False)


# In[ ]:




