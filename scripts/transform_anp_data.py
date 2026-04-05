# ============================================================
# SCRIPT: TRANSFORMAÇÃO DOS DADOS DA ANP
# OBJETIVO:
# Preparar base limpa para análise e gerar relatório Excel
# ============================================================

from pathlib import Path
import pandas as pd

# ============================================================
# CAMINHOS DO PROJETO
# ============================================================

RAW_PATH = Path(__file__).resolve().parent.parent / "data" / "raw"
PROCESSED_PATH = Path(__file__).resolve().parent.parent / "data" / "processed"
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "output"

# Garante que as pastas existam
PROCESSED_PATH.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

print("Iniciando transformação dos dados...")

# ============================================================
# LOCALIZAR ARQUIVOS
# ============================================================

arquivos = sorted(RAW_PATH.glob("*.csv"))

print(f"\nArquivos encontrados: {len(arquivos)}")
for arquivo in arquivos:
    print("-", arquivo.name)

# ============================================================
# VERIFICAÇÃO — PASTA NÃO PODE ESTAR VAZIA
# ============================================================

if not arquivos:
    raise FileNotFoundError(
        "Nenhum arquivo CSV encontrado em data/raw/. "
        "Verifique se os arquivos da ANP foram colocados na pasta correta."
    )

# ============================================================
# LER E JUNTAR OS ARQUIVOS
# ============================================================

lista_dfs = []

for arquivo in arquivos:
    print(f"\nLendo arquivo: {arquivo.name}")
    df_temp = pd.read_csv(arquivo, sep=";", encoding="latin1")
    lista_dfs.append(df_temp)

df = pd.concat(lista_dfs, ignore_index=True)

print("\nBase consolidada com sucesso.")
print(f"Dimensão total: {df.shape}")

# ============================================================
# LIMPAR NOMES DAS COLUNAS
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.replace("ï»¿", "", regex=False)
)

print("\nColunas após limpeza:")
for col in df.columns:
    print("-", col)

# ============================================================
# VALIDAR COLUNAS CRÍTICAS
# ============================================================

colunas_criticas = ["Produto", "Valor de Venda", "Data da Coleta", "Estado - Sigla"]
faltantes = [col for col in colunas_criticas if col not in df.columns]

if faltantes:
    raise KeyError(
        f"Colunas críticas ausentes: {faltantes}. "
        f"Colunas disponíveis: {df.columns.tolist()}"
    )

# ============================================================
# FILTRAR APENAS GASOLINA
# ============================================================

df = df[
    df["Produto"]
    .astype(str)
    .str.upper()
    .str.strip() == "GASOLINA"
].copy()

if df.empty:
    raise ValueError(
        "Nenhum registro encontrado para 'GASOLINA'. "
        "Verifique os valores da coluna Produto nos arquivos brutos."
    )

print("\nFiltro aplicado: somente GASOLINA")
print(f"Dimensão após filtro: {df.shape}")

# ============================================================
# TRATAR VALOR DE VENDA
# ============================================================

df["Valor de Venda"] = pd.to_numeric(
    df["Valor de Venda"]
    .astype(str)
    .str.replace(",", ".", regex=False),
    errors="coerce"
)

valores_invalidos = df["Valor de Venda"].isnull().sum()
if valores_invalidos > 0:
    print(f"\nAVISO: {valores_invalidos} valores inválidos em 'Valor de Venda' foram convertidos para NaN.")

df = df.dropna(subset=["Valor de Venda"]).copy()

if df.empty:
    raise ValueError(
        "Todos os registros ficaram inválidos após a conversão de 'Valor de Venda'. "
        "Verifique o formato dessa coluna nos arquivos brutos."
    )

print("\nConversão da coluna Valor de Venda concluída.")
print(f"Tipo atual: {df['Valor de Venda'].dtype}")
print(f"Dimensão após remoção de valores inválidos: {df.shape}")

# ============================================================
# TRATAR DATA DA COLETA
# ============================================================

df["Data da Coleta"] = pd.to_datetime(
    df["Data da Coleta"],
    format="%d/%m/%Y",
    errors="coerce"
)

datas_invalidas = df["Data da Coleta"].isnull().sum()
if datas_invalidas > 0:
    print(f"\nAVISO: {datas_invalidas} datas inválidas foram convertidas para NaT.")

df = df.dropna(subset=["Data da Coleta"]).copy()

if df.empty:
    raise ValueError(
        "Todos os registros ficaram inválidos após a conversão de 'Data da Coleta'. "
        "Verifique o formato dessa coluna nos arquivos brutos."
    )

print("\nConversão da coluna Data da Coleta concluída.")
print(f"Tipo atual: {df['Data da Coleta'].dtype}")
print(f"Dimensão após remoção de datas inválidas: {df.shape}")

# ============================================================
# CRIAR COLUNA DE MÊS
# ============================================================

df["Mes"] = df["Data da Coleta"].dt.to_period("M").astype(str)

print("\nColuna de mês criada com sucesso.")
print(df["Mes"].head())

# ============================================================
# TRATAMENTO DE OUTLIERS (IQR)
# ============================================================

Q1 = df["Valor de Venda"].quantile(0.25)
Q3 = df["Valor de Venda"].quantile(0.75)
IQR = Q3 - Q1

limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

print("\nLimites para outliers (IQR):")
print(f"Inferior: {limite_inferior:.4f}")
print(f"Superior: {limite_superior:.4f}")

registros_antes = df.shape[0]

df = df[
    (df["Valor de Venda"] >= limite_inferior) &
    (df["Valor de Venda"] <= limite_superior)
].copy()

registros_depois = df.shape[0]

print(f"\nRegistros removidos como outliers: {registros_antes - registros_depois}")
print(f"Dimensão após limpeza: {df.shape}")

if df.empty:
    raise ValueError(
        "A base ficou vazia após o tratamento de outliers. "
        "Revise os limites calculados e a qualidade dos dados."
    )

# ============================================================
# KPIs — TODOS CALCULADOS APÓS LIMPEZA
# ============================================================

# KPI 1 — Preço médio por estado
preco_medio_estado = (
    df.groupby("Estado - Sigla")["Valor de Venda"]
    .mean()
    .round(4)
    .sort_values(ascending=False)
)

print("\nPreço médio por estado (dados limpos):")
print(preco_medio_estado.head(10))

# KPI 2 — Preço médio por mês
preco_medio_mes = (
    df.groupby("Mes")["Valor de Venda"]
    .mean()
    .round(4)
    .sort_index()
)

print("\nPreço médio por mês (dados limpos):")
print(preco_medio_mes)

# KPI 3 — Preço médio por estado e mês
preco_estado_mes = (
    df.groupby(["Estado - Sigla", "Mes"])["Valor de Venda"]
    .mean()
    .round(4)
    .sort_values(ascending=False)
)

print("\nPreço médio por estado e mês (dados limpos):")
print(preco_estado_mes.head(15))

# KPI 4 — Dispersão de preço por estado (desvio padrão)
dispersao_estado = (
    df.groupby("Estado - Sigla")["Valor de Venda"]
    .std()
    .round(4)
    .sort_values(ascending=False)
)

print("\nEstados com maior dispersão de preço (desvio padrão):")
print(dispersao_estado.head(10))

# ============================================================
# INVESTIGAÇÃO — ESTADO SP
# ============================================================

df_sp = df[df["Estado - Sigla"] == "SP"]

print("\nEstatísticas SP (dados limpos):")
if df_sp.empty:
    print("Nenhum registro encontrado para SP após os tratamentos.")
else:
    print(df_sp["Valor de Venda"].describe())

# ============================================================
# SALVAR BASE TRATADA
# ============================================================

output_csv = PROCESSED_PATH / "base_anp_gasolina_tratada.csv"
df.to_csv(output_csv, index=False, sep=";", encoding="utf-8-sig")

print("\nBase tratada salva com sucesso.")
print(f"Caminho: {output_csv}")

# ============================================================
# PREPARAR DATAFRAMES PARA EXPORTAÇÃO
# ============================================================

df_estado_export = preco_medio_estado.reset_index()
df_estado_export.columns = ["Estado - Sigla", "Valor de Venda"]

df_mensal_export = preco_medio_mes.reset_index()
df_mensal_export.columns = ["Mes", "Valor de Venda"]

df_dispersao_export = dispersao_estado.reset_index()
df_dispersao_export.columns = ["Estado - Sigla", "Desvio Padrao"]

df_estado_mes_export = preco_estado_mes.reset_index()
df_estado_mes_export.columns = ["Estado - Sigla", "Mes", "Valor de Venda"]

# ============================================================
# EXPORTAR RELATÓRIO EM EXCEL
# ============================================================

OUTPUT_FILE = OUTPUT_PATH / "relatorio_anp_gasolina.xlsx"

with pd.ExcelWriter(OUTPUT_FILE, engine="xlsxwriter") as writer:
    # Exportar abas
    df.to_excel(writer, sheet_name="Base_Dados", index=False)
    df_estado_export.to_excel(writer, sheet_name="KPI_Estado", index=False)
    df_mensal_export.to_excel(writer, sheet_name="KPI_Mensal", index=False)
    df_dispersao_export.to_excel(writer, sheet_name="KPI_Dispersao", index=False)
    df_estado_mes_export.to_excel(writer, sheet_name="KPI_Estado_Mes", index=False)

    workbook = writer.book

    # Formatos reutilizáveis
    currency_format = workbook.add_format({
        "num_format": "R$ #,##0.00"
    })

    header_format = workbook.add_format({
        "bold": True,
        "text_wrap": False,
        "valign": "top",
        "bg_color": "#1F4E78",
        "font_color": "white",
        "align": "center",
        "border": 1
    })

    # ========================================================
    # FUNÇÃO AUXILIAR DE FORMATAÇÃO
    # ========================================================

    def formatar_aba(worksheet, dataframe):
        # Congelar primeira linha
        worksheet.freeze_panes(1, 0)

        # Aplicar formato no cabeçalho
        for col_num, value in enumerate(dataframe.columns):
            worksheet.write(0, col_num, value, header_format)

        # Formatar moeda, se existir coluna monetária
        if "Valor de Venda" in dataframe.columns:
            col_idx = dataframe.columns.get_loc("Valor de Venda")
            worksheet.set_column(col_idx, col_idx, 14, currency_format)

        # Ajustar largura das colunas
        for i, col in enumerate(dataframe.columns):
            valores_como_texto = dataframe[col].fillna("").astype(str)
            max_len = max(
                len(str(col)),
                valores_como_texto.str.len().max()
            )
            worksheet.set_column(i, i, min(max_len + 2, 30))

    # Aplicar formatação em cada aba
    formatar_aba(writer.sheets["Base_Dados"], df)
    formatar_aba(writer.sheets["KPI_Estado"], df_estado_export)
    formatar_aba(writer.sheets["KPI_Mensal"], df_mensal_export)
    formatar_aba(writer.sheets["KPI_Dispersao"], df_dispersao_export)
    formatar_aba(writer.sheets["KPI_Estado_Mes"], df_estado_mes_export)

print("\nRelatório Excel gerado com sucesso.")
print(f"Caminho: {OUTPUT_FILE}")
print("\nAbas geradas:")
print("  - Base_Dados")
print("  - KPI_Estado")
print("  - KPI_Mensal")
print("  - KPI_Dispersao")
print("  - KPI_Estado_Mes")