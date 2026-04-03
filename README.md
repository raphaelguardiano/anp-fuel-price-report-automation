# ANP Fuel Price Report Automation

Automação de análise de preços de combustíveis utilizando dados públicos da ANP.

## Problema

A análise de preços de combustíveis por região normalmente envolve processos manuais, repetitivos e sujeitos a erro, especialmente ao lidar com múltiplos arquivos e consolidação de dados.

## Solução

Este projeto automatiza todo o pipeline de dados:

* leitura de múltiplos arquivos CSV da ANP
* consolidação da base
* limpeza e padronização dos dados
* tratamento de datas e valores
* cálculo de indicadores (KPIs)
* geração automática de relatório em Excel

## Pipeline

data/raw → data/processed → output

* raw: dados brutos da ANP
* processed: base tratada e pronta para análise
* output: relatório final em Excel

## Principais análises

* preço médio por estado
* preço médio por mês
* variação de preço por estado
* análise por estado e período
* impacto de outliers nos resultados

## Entrega

O script gera automaticamente um arquivo Excel com múltiplas abas:

* Base_Dados
* KPI_Estado
* KPI_Mensal
* KPI_Variacao

Com:

* colunas ajustadas
* cabeçalho formatado
* leitura otimizada

## Tecnologias

* Python
* pandas
* xlsxwriter

## Como executar

pip install -r requirements.txt
python scripts/transform_anp_data.py

## Resultado

* redução de trabalho manual
* maior consistência nos dados
* geração rápida de relatórios analíticos

## Autor

Raphael Guardiano
Projeto desenvolvido como parte do portfólio em análise e automação de dados.
