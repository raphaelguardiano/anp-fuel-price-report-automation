# ============================================================
# SCRIPT: TRANSFORMAÇÃO DOS DADOS DA ANP
# OBJETIVO:
# Preparar base limpa para análise
# ============================================================

from pathlib import Path
import pandas as pd

# Caminhos do projeto
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

print("\nArquivos encontrados:")
for arquivo in arquivos:
    print("-", arquivo.name)

# ============================================================
# LER E JUNTAR OS ARQUIVOS
# ============================================================

lista_dfs = []

for arquivo in arquivos:
    print(f"\nLendo arquivo: {arquivo.name}")
    df_temp = pd.read_csv(arquivo, sep=";", encoding="latin1")
    lista_dfs.append(df_temp)

# Junta todos os DataFrames em um só
df = pd.concat(lista_dfs, ignore_index=True)

print("\nBase consolidada com sucesso.")
print(f"Dimensão final: {df.shape}")

# ============================================================
# LIMPAR NOMES DAS COLUNAS
# ============================================================

df.columns = df.columns.str.replace("ï»¿", "", regex=False)

print("\nColunas após limpeza:")
for col in df.columns:
    print("-", col)

# ============================================================
# TRATAR VALOR DE VENDA
# ============================================================

df["Valor de Venda"] = df["Valor de Venda"].str.replace(",", ".", regex=False)
df["Valor de Venda"] = df["Valor de Venda"].astype(float)

print("\nTipo da coluna Valor de Venda após conversão:")
print(df["Valor de Venda"].dtype)

# ============================================================
# FILTRAR APENAS GASOLINA
# ============================================================

df = df[df["Produto"] == "GASOLINA"].copy()

print("\nFiltro aplicado: somente GASOLINA")
print(f"Dimensão após filtro: {df.shape}")

# ============================================================
# TRATAR DATA DA COLETA
# ============================================================

df["Data da Coleta"] = pd.to_datetime(
    df["Data da Coleta"],
    format="%d/%m/%Y"
)

print("\nTipo da coluna Data da Coleta:")
print(df["Data da Coleta"].dtype)

# ============================================================
# CRIAR COLUNA DE MÊS
# ============================================================

df["Mes"] = df["Data da Coleta"].dt.to_period("M")

print("\nColuna de mês criada com sucesso.")
print(df["Mes"].head())

# ============================================================
# KPI 1 — PREÇO MÉDIO POR ESTADO
# ============================================================

preco_medio_estado = (
    df.groupby("Estado - Sigla")["Valor de Venda"]
    .mean()
    .sort_values(ascending=False)
)

print("\nPreço médio por estado:")
print(preco_medio_estado.head(10))

# ============================================================
# KPI 2 — PREÇO MÉDIO POR MÊS
# ============================================================

preco_medio_mes = (
    df.groupby("Mes")["Valor de Venda"]
    .mean()
    .sort_index()
)

print("\nPreço médio por mês:")
print(preco_medio_mes)

# ============================================================
# KPI 3 — PREÇO MÉDIO POR ESTADO E MÊS
# ============================================================

preco_estado_mes = (
    df.groupby(["Estado - Sigla", "Mes"])["Valor de Venda"]
    .mean()
    .sort_values(ascending=False)
)

print("\nPreço médio por estado e mês:")
print(preco_estado_mes.head(15))

# ============================================================
# KPI 4 — VARIAÇÃO DE PREÇO POR ESTADO
# ============================================================

variacao_estado = (
    df.groupby("Estado - Sigla")["Valor de Venda"]
    .agg(lambda x: x.max() - x.min())
    .sort_values(ascending=False)
)

print("\nEstados com maior variação de preço:")
print(variacao_estado.head(10))

# ============================================================
# INVESTIGAÇÃO — ESTADO SP
# ============================================================

df_sp = df[df["Estado - Sigla"] == "SP"]

print("\nEstatísticas SP:")
print(df_sp["Valor de Venda"].describe())

# ============================================================
# TRATAMENTO DE OUTLIERS (IQR)
# ============================================================

Q1 = df["Valor de Venda"].quantile(0.25)
Q3 = df["Valor de Venda"].quantile(0.75)
IQR = Q3 - Q1

limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

print("\nLimites para outliers:")
print(f"Inferior: {limite_inferior}")
print(f"Superior: {limite_superior}")

df = df[
    (df["Valor de Venda"] >= limite_inferior) &
    (df["Valor de Venda"] <= limite_superior)
].copy()

print("\nDimensão após remoção de outliers:")
print(df.shape)

# ============================================================
# KPI 1 (APÓS LIMPEZA) — PREÇO MÉDIO POR ESTADO
# ============================================================

preco_medio_estado_clean = (
    df.groupby("Estado - Sigla")["Valor de Venda"]
    .mean()
    .sort_values(ascending=False)
)

print("\nPreço médio por estado (dados limpos):")
print(preco_medio_estado_clean.head(10))

# ============================================================
# SALVAR BASE TRATADA
# ============================================================

output_csv = PROCESSED_PATH / "base_anp_gasolina_tratada.csv"

df.to_csv(output_csv, index=False, sep=";", encoding="utf-8-sig")

print("\nBase tratada salva com sucesso.")
print(f"Caminho: {output_csv}")

# ============================================================
# EXPORTAR RELATÓRIO EM EXCEL (MULTI-ABAS)
# ============================================================

OUTPUT_FILE = OUTPUT_PATH / "relatorio_anp_gasolina.xlsx"

with pd.ExcelWriter(OUTPUT_FILE, engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="Base_Dados", index=False)
    preco_medio_estado_clean.to_excel(writer, sheet_name="KPI_Estado")
    preco_medio_mes.to_excel(writer, sheet_name="KPI_Mensal")
    variacao_estado.to_excel(writer, sheet_name="KPI_Variacao")

print("\nRelatório Excel completo gerado com sucesso.")
print(f"Caminho do arquivo: {OUTPUT_FILE}")