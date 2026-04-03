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

```text
data/raw → data/processed → output
```

* **raw**: dados brutos da ANP
* **processed**: base tratada e pronta para análise
* **output**: relatório final em Excel

## Dataset

* Fonte: ANP (Agência Nacional do Petróleo)
* Produto analisado: Gasolina
* Período: meses recentes (amostra controlada)

## Principais análises

* preço médio por estado
* preço médio por mês
* variação de preço por estado
* análise por estado e período
* impacto de outliers nos resultados

## Entrega

O script gera automaticamente:

* base tratada em CSV
* relatório Excel com múltiplas abas

Abas do Excel:

* `Base_Dados`
* `KPI_Estado`
* `KPI_Mensal`
* `KPI_Variacao`

## Tecnologias

* Python
* pandas
* xlsxwriter
* openpyxl

## Como executar

```bash
pip install -r requirements.txt
python scripts/transform_anp_data.py
```

## Screenshots

### Base de dados tratada

![Base\_Dados](assets/excel_base_dados.png)

### KPI por estado

![KPI\_Estado](assets/excel_kpi_estado.png)

### KPI mensal

![KPI\_Mensal](assets/excel_kpi_mensal.png)

## Resultado

* redução de trabalho manual
* maior consistência nos dados
* geração rápida de relatórios analíticos

## Autor

Raphael Guardiano

Projeto desenvolvido como parte do portfólio em análise e automação de dados.
