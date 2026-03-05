#!/usr/bin/env python
# coding: utf-8

# In[1]:


# importando bibliotecas
import pandas as pd
import requests 
from datetime import datetime


# In[2]:


# listando todas as moedas

url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/Moedas?$format=json"
response = requests.get(url).json()

# validando campos
print(response)


# In[3]:


# consultando lista de moedas
for moeda in response["value"]:
    print(moeda["simbolo"], "-", moeda["nomeFormatado"])


# In[4]:


# importando biblioteca e classe para datas e horas
from datetime import datetime, timedelta

# definindo período de consulta
data_final = datetime.today()
data_inicial = data_final - timedelta(days=30)

data_final_str = data_final.strftime("%m-%d-%Y")
data_inicial_str = data_inicial.strftime("%m-%d-%Y")


# In[5]:


# pegando lista de moedas da API
url_moedas = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/Moedas?$format=json"
response = requests.get(url_moedas).json()


# In[6]:


# armazenando os dados
dados = []


# In[7]:


# consultando cotações históricas  de todas as moedas disponíveis no API
for moeda in response["value"]:
    simbolo = moeda["simbolo"]
    nome = moeda["nomeFormatado"]

    url_cotacao = (f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
                   f"CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?"
                   f"@moeda='{simbolo}'&@dataInicial='{data_inicial_str}'&@dataFinalCotacao='{data_final_str}'&$format=json")

    cotacao = requests.get(url_cotacao).json()

    for item in cotacao["value"]:
        dados.append({
            "Moeda": simbolo,
            "Nome": nome,
            "Data": item["dataHoraCotacao"],
            "Compra": item["cotacaoCompra"],
            "Venda": item["cotacaoVenda"]
        })


# In[8]:


# extraindo e armazenando as cotações de cada moeda nos últimos 30 dias
for item in cotacao["value"]:
    dados.append({
        "Moeda": simbolo,
        "Nome": nome,
        "Data": item["dataHoraCotacao"],
        "Compra": item["cotacaoCompra"],
        "Venda": item["cotacaoVenda"]
    })


# In[9]:


# convertendo em dataframe e salvando em Excel
df = pd.DataFrame(dados)
df.to_excel("data/cotacoes_30_dias.xlsx", index=False)

print("Relatório com todas as moedas dos últimos 30 dias salvo com sucesso!")


# In[10]:


# resumindo automaticamente as cotações geradas em Excel
num_moedas = df["Moeda"].nunique()   # quantidade de moedas diferentes
num_registros = len(df)              # total de linhas (cotações)
periodo_inicio = df["Data"].min()    # primeira data
periodo_fim = df["Data"].max()       # última data

print(f"Foram coletadas {num_registros} cotações de {num_moedas} moedas.")
print(f"Período: de {periodo_inicio} até {periodo_fim}")
print("Moedas disponíveis:", df["Moeda"].unique())


# In[11]:


import os
print(os.getcwd())


# In[ ]:




