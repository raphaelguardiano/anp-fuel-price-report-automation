# ANP Fuel Price Report Automation

Automação de análise de preços de combustíveis com Python utilizando
dados públicos da ANP.

Este projeto foi desenvolvido para transformar arquivos brutos da ANP em
uma base tratada e em um relatório final em Excel, reduzindo trabalho
manual e aumentando a consistência do processo de análise.

------------------------------------------------------------------------

## Problema

Acompanhar preços de combustíveis com dados públicos normalmente exige
etapas manuais repetitivas, como:

-   leitura de múltiplos arquivos CSV
-   consolidação da base
-   padronização de colunas
-   tratamento de datas e valores numéricos
-   organização da saída final para análise

Esse processo é demorado, sujeito a erro e dificulta análises
recorrentes.

------------------------------------------------------------------------

## Solução

O projeto automatiza o pipeline de dados com Python, realizando:

-   leitura de múltiplos arquivos CSV da ANP
-   consolidação da base em um único DataFrame
-   limpeza e padronização dos dados
-   filtro dos registros de gasolina
-   tratamento de valores inválidos
-   conversão de datas e preços
-   remoção de outliers
-   cálculo de indicadores
-   geração automática de relatório em Excel

------------------------------------------------------------------------

## Pipeline

data/raw → data/processed → output

------------------------------------------------------------------------

## Dataset

-   Fonte: ANP (Agência Nacional do Petróleo)
-   Produto analisado: Gasolina
-   Origem dos arquivos: CSVs públicos da ANP

------------------------------------------------------------------------

## Principais análises

-   preço médio por estado
-   evolução mensal dos preços
-   dispersão de preços por estado
-   análise por estado e período

------------------------------------------------------------------------

## Entregas

-   Base tratada em CSV
-   Relatório Excel com abas:
    -   Base_Dados
    -   KPI_Estado
    -   KPI_Mensal
    -   KPI_Variacao

------------------------------------------------------------------------

## Estrutura do projeto

anp-fuel-price-report-automation/ ├── assets/ ├── data/ ├── scripts/ ├──
README.md

------------------------------------------------------------------------

## Como executar

pip install -r requirements.txt

python scripts/transform_anp_data.py

------------------------------------------------------------------------

## Screenshots

![Base_Dados](assets/excel_base_dados.png)
![KPI_Estado](assets/excel_kpi_estado.png)
![KPI_Mensal](assets/excel_kpi_mensal.png)

------------------------------------------------------------------------

## Tecnologias

-   Python
-   pandas
-   xlsxwriter
-   openpyxl

------------------------------------------------------------------------

## Aprendizados

-   preparação de dados é a etapa mais crítica
-   automação reduz erro manual
-   consistência entre dados e output é essencial

------------------------------------------------------------------------

## Autor

Raphael Guardiano
