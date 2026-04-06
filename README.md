# ANP Fuel Price Report Automation

Automação de análise de preços de combustíveis com Python utilizando
dados públicos da ANP.

Este projeto transforma arquivos brutos da ANP em uma base tratada e um
relatório analítico em Excel, reduzindo trabalho manual e aumentando a
consistência da análise.

------------------------------------------------------------------------

## Problema

Bases públicas como as da ANP não vêm prontas para análise.

Antes de qualquer insight, é necessário:

-   consolidar múltiplos arquivos
-   padronizar colunas
-   tratar valores inconsistentes
-   corrigir formatos de data e número

Esse processo manual é demorado, sujeito a erro e dificulta análises
recorrentes.

------------------------------------------------------------------------

## Solução

Foi desenvolvido um pipeline automatizado em Python que:

-   lê múltiplos arquivos CSV da ANP
-   consolida os dados em uma única base
-   realiza limpeza e padronização
-   filtra apenas registros de gasolina
-   trata valores inválidos
-   converte datas e preços
-   remove outliers
-   calcula indicadores
-   gera automaticamente um relatório em Excel

------------------------------------------------------------------------

## 🔍 Hipóteses de Análise

Embora o foco principal do projeto seja a automação do tratamento e da geração do relatório, a estrutura final também permite explorar algumas hipóteses analíticas relevantes sobre os preços de combustíveis.

### 1. Existe variação relevante de preços entre estados e regiões
A consolidação da base permite comparar preços médios por recorte geográfico, facilitando a identificação de diferenças regionais de comportamento.

### 2. Existe dispersão significativa de preços dentro de um mesmo recorte geográfico
A análise de dispersão ajuda a observar se os preços se mantêm relativamente homogêneos ou se apresentam alta variação dentro de estados ou regiões.

### 3. Os preços apresentam comportamento recorrente ao longo do tempo
A visualização por período permite acompanhar oscilações e identificar padrões temporais no comportamento dos preços.

### 4. A diferença entre valores mínimos e máximos pode indicar pontos de atenção para monitoramento
A análise de extremos ajuda a destacar recortes com maior amplitude de preços, o que pode ser útil para acompanhamento periódico e comparação de mercado.

------------------------------------------------------------------------

## Pipeline

data/raw → data/processed → output

------------------------------------------------------------------------

## Dataset

-   Fonte: ANP (Agência Nacional do Petróleo)
-   Produto analisado: Gasolina
-   Período analisado: Jan/2026 a Fev/2026
-   Registros finais após tratamento: 33.942

------------------------------------------------------------------------

## Principais análises

O relatório foi estruturado para responder:

-   qual o preço médio da gasolina por estado
-   como o preço evolui ao longo do tempo
-   quais estados apresentam maior dispersão de preços
-   como o comportamento muda por estado e período

------------------------------------------------------------------------

## Principais descobertas

-   Estados da região Norte apresentaram os maiores preços médios, com
    destaque para AM (\~6,95), RO (\~6,91) e RR (\~6,90)

-   Houve leve queda no preço médio entre janeiro e fevereiro de 2026
    (de 6,3119 para 6,3004)

-   Estados como PA, AL e MA apresentaram maior dispersão de preços,
    indicando maior variação interna

-   São Paulo apresentou preço médio inferior (6,17), sugerindo maior
    estabilidade e competitividade no mercado

------------------------------------------------------------------------

## Entregas

-   Base tratada em CSV
-   Relatório Excel com abas:
    -   Base_Dados
    -   KPI_Estado
    -   KPI_Mensal
    -   KPI_Dispersao
    -   KPI_Estado_Mes

------------------------------------------------------------------------

## Estrutura do projeto

anp-fuel-price-report-automation/ ├── assets/ ├── data/ ├── scripts/ ├──
output/ └── README.md

------------------------------------------------------------------------

## Como executar

pip install -r requirements.txt

python scripts/transform_anp_data.py

------------------------------------------------------------------------

## Screenshots

![Base_Dados](assets/excel_base_dados.png)
![KPI_Estado](assets/excel_kpi_estado.png)
![KPI_Mensal](assets/excel_kpi_mensal.png)
![KPI_Dispersao](assets/excel_kpi_dispersao.png)
![KPI_Estado_Mes](assets/excel_kpi_estado_mes.png)

------------------------------------------------------------------------

## Tecnologias

-   Python
-   pandas
-   xlsxwriter
-   openpyxl

------------------------------------------------------------------------

## Aprendizados

-   a maior parte do trabalho em dados está na preparação da base
-   automação só gera valor com lógica consistente
-   dados não tratados levam a análises erradas
-   consistência entre métricas é essencial

------------------------------------------------------------------------

## Autor

Raphael Guardiano

Projeto desenvolvido como parte da transição para a área de análise de
dados, com foco em automação e geração de insights a partir de dados
reais.
