# ANP Fuel Price Report Automation

Projeto de portfólio focado na automação de relatório de preços de combustíveis com dados públicos da ANP.

## Objetivo

Automatizar o processo de:

- leitura dos dados públicos da ANP
- limpeza e padronização
- transformação dos dados
- cálculo de KPIs
- geração de relatório final em Excel

## Problema de negócio

Empresas e analistas precisam monitorar preços de combustíveis por região, mas esse processo costuma ser manual, repetitivo e sujeito a erro.

A automação reduz tempo operacional e melhora a consistência da análise.

## Escopo inicial

- Fonte: dados públicos da ANP
- Produto: gasolina
- Período: meses recentes
- Estrutura: tabela única
- Saída final: arquivo Excel com base tratada e KPIs

## Estrutura do projeto

```text
data/raw
data/processed
scripts
output