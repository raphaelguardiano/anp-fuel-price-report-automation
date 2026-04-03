# ANP Fuel Price Report Automation

Projeto de portfólio focado na automação de análise de preços de combustíveis com dados públicos da ANP.

## Visão geral

Este projeto foi desenvolvido com o objetivo de automatizar o processo de leitura, tratamento, análise e geração de relatório em Excel a partir de dados públicos de preços de combustíveis.

A proposta foi transformar uma base bruta em uma entrega analítica estruturada, reduzindo trabalho manual e aumentando a confiabilidade das informações.

## Problema de negócio

O acompanhamento de preços de combustíveis por estado e período pode ser um processo manual, repetitivo e sujeito a erros, principalmente quando envolve múltiplos arquivos, tratamento de dados e consolidação de indicadores.

Esse projeto busca resolver esse problema por meio de uma automação simples e prática, com foco em análise de preços da gasolina.

## Objetivo do projeto

Automatizar o fluxo de:

- leitura de múltiplos arquivos CSV da ANP
- consolidação da base
- limpeza e padronização dos dados
- tratamento de preços e datas
- cálculo de indicadores
- geração de relatório final em Excel

## Fonte de dados

Os dados utilizados neste projeto são públicos e foram obtidos a partir da base da ANP (Agência Nacional do Petróleo, Gás Natural e Biocombustíveis), com foco em preços de combustíveis.

Recorte inicial do projeto:

- produto: gasolina
- período: janeiro e fevereiro de 2026
- formato original: arquivos CSV

## Processo da automação

O pipeline desenvolvido segue as etapas abaixo:

1. leitura dos arquivos CSV
2. consolidação em uma única base
3. filtro do produto `GASOLINA`
4. limpeza dos nomes das colunas
5. conversão do valor de venda para formato numérico
6. conversão da data de coleta para formato datetime
7. criação de coluna mensal para análise temporal
8. cálculo de KPIs
9. tratamento de outliers com método IQR
10. exportação automatizada para Excel

## Principais análises e KPIs

O projeto gera automaticamente:

- preço médio por estado
- preço médio por mês
- preço médio por estado e mês
- variação de preço por estado
- comparação antes e depois da remoção de outliers

## Estrutura do projeto

```text
anp-fuel-price-report-automation/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── output/
│   └── relatorio_anp_gasolina.xlsx
│
├── scripts/
│   ├── inspect_anp_data.py
│   └── transform_anp_data.py
│
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE