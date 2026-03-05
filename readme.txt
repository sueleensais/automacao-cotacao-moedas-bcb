# **Automação de Cotações de Moedas – Banco Central do Brasil**

Este projeto em Python consome a API oficial do Banco Central (PTAX) para coletar cotações de moedas estrangeiras. Os dados são tratados com Pandas e exportados para Excel, permitindo análises rápidas e organizadas. A execução é automatizada diariamente via Agendador de Tarefas do Windows, garantindo relatórios atualizados sem intervenção manual.

## Funcionalidades

- Consulta automática à API de moedas disponíveis.
- Coleta das cotações dos últimos 30 dias.
- Exportação dos dados para Excel (cotacoes_30_dias.xlsx).
- Automação da execução com o Agendador de Tarefas.

## Tecnologias utilizadas
- Python 3.x
- Pandas
- Requests
- Datetime
- Agendador de Tarefas (Windows)

## Script
```python
# importando bibliotecas
import pandas as pd
import requests 
from datetime import datetime

# listando todas as moedas
url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/Moedas?$format=json"
response = requests.get(url).json()

# validando campos
print(response)

# consultando lista de moedas
for moeda in response["value"]:
    print(moeda["simbolo"], "-", moeda["nomeFormatado"])

# importando biblioteca e classe para datas e horas
from datetime import datetime, timedelta

# definindo período de consulta
data_final = datetime.today()
data_inicial = data_final - timedelta(days=30)

data_final_str = data_final.strftime("%m-%d-%Y")
data_inicial_str = data_inicial.strftime("%m-%d-%Y")

# pegando lista de moedas da API
url_moedas = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/Moedas?$format=json"
response = requests.get(url_moedas).json()
# armazenando os dados
dados = []

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

# extraindo e armazenando as cotações de cada moeda nos últimos 30 dias
for item in cotacao["value"]:
    dados.append({
        "Moeda": simbolo,
        "Nome": nome,
        "Data": item["dataHoraCotacao"],
        "Compra": item["cotacaoCompra"],
        "Venda": item["cotacaoVenda"]
    })

# convertendo em dataframe e salvando em Excel
df = pd.DataFrame(dados)
df.to_excel("data/cotacoes_30_dias.xlsx", index=False)

print("Relatório com todas as moedas dos últimos 30 dias salvo com sucesso!")

# resumindo automaticamente as cotações geradas em Excel
num_moedas = df["Moeda"].nunique()   # quantidade de moedas diferentes
num_registros = len(df)              # total de linhas (cotações)
periodo_inicio = df["Data"].min()    # primeira data
periodo_fim = df["Data"].max()       # última data

print(f"Foram coletadas {num_registros} cotações de {num_moedas} moedas.")
print(f"Período: de {periodo_inicio} até {periodo_fim}")
print("Moedas disponíveis:", df["Moeda"].unique())
```
## Como executar
1. Clone este repositório
2. Instale as dependências: 
```python
pip install pandas requests
```
3. Execute o script manualmente:
```python
python cotacao-moedas.py
4. O relatório será gerado na pasta data/.
```
## Automação
- Configure o Agendador de Tarefas do Windows para rodar o script diariamente.
- Exemplo de configuração:
- Programa/script: caminho completo do Python (ex.: C:\Users\sueleen\anaconda3\python.exe)
- Argumentos: "C:\Users\sueleen\OneDrive\Documents\Projetos\cotacao-moedas\cotacao-moedas.py"
- Iniciar em: C:\Users\sueleen\OneDrive\Documents\Projetos\cotacao-moedas

## Resultados
- Relatório em Excel com todas as moedas disponíveis e suas cotações de compra e venda nos últimos 30 dias.
- Exemplo de saída:

```python
Moeda | Nome        | Data                | Compra   | Venda
USD   | Dólar EUA   | 2026-03-05 13:00:00 | 5.12     | 5.13
EUR   | Euro        | 2026-03-05 13:00:00 | 5.55     | 5.57
...