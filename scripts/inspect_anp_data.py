# ============================================================
# SCRIPT: INSPEÇÃO INICIAL DOS DADOS DA ANP
# OBJETIVO:
# Entender a estrutura da base antes de qualquer transformação
# ============================================================

from pathlib import Path
import pandas as pd

# ============================================================
# DEFINIR CAMINHO DOS DADOS
# ============================================================

RAW_PATH = Path(__file__).resolve().parent.parent / "data" / "raw"

# ============================================================
# INÍCIO DA EXECUÇÃO
# ============================================================

print("Iniciando inspeção dos arquivos...")
print(f"Pasta analisada: {RAW_PATH.resolve()}")

# ============================================================
# LOCALIZAR ARQUIVOS CSV
# ============================================================

arquivos = sorted(RAW_PATH.glob("*.csv"))

print(f"\nArquivos CSV encontrados: {len(arquivos)}")
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
# LER APENAS O PRIMEIRO ARQUIVO COMO AMOSTRA
# ============================================================

primeiro_arquivo = arquivos[0]

print(f"\nInspecionando arquivo: {primeiro_arquivo.name}")
print("(amostra — apenas o primeiro arquivo da lista)")

df = pd.read_csv(primeiro_arquivo, sep=";", encoding="latin1")

print("\nLeitura realizada com sucesso.")

# ============================================================
# LIMPAR NOMES DAS COLUNAS (BOM + ESPAÇOS)
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.replace("ï»¿", "", regex=False)
)

# ============================================================
# VISÃO GERAL
# ============================================================

print("\n--- INFO GERAL ---")
df.info()

print("\n--- VALORES NULOS POR COLUNA ---")
nulos = df.isnull().sum()
nulos_relevantes = nulos[nulos > 0]
print(nulos_relevantes if not nulos_relevantes.empty else "Nenhum valor nulo encontrado.")

print("\n--- PRIMEIRAS LINHAS ---")
print(df.head())

# ============================================================
# LISTAR COLUNAS
# ============================================================

print("\nColunas encontradas:")
for coluna in df.columns:
    print("-", coluna)

# ============================================================
# VALIDAR COLUNAS CRÍTICAS
# ============================================================

colunas_criticas = ["Produto", "Valor de Venda", "Data da Coleta"]
faltantes = [col for col in colunas_criticas if col not in df.columns]

if faltantes:
    raise KeyError(
        f"Colunas críticas ausentes: {faltantes}. "
        f"Colunas disponíveis: {df.columns.tolist()}"
    )

# ============================================================
# ANALISAR PRODUTOS
# ============================================================

print("\nValores únicos da coluna Produto:")
print(df["Produto"].unique())

# ============================================================
# FILTRAR APENAS GASOLINA (ALINHADO AO ESCOPO DO PROJETO)
# ============================================================

df_gasolina = df[
    df["Produto"]
    .astype(str)
    .str.upper()
    .str.strip() == "GASOLINA"
].copy()

if df_gasolina.empty:
    raise ValueError(
        "Nenhum registro encontrado para 'GASOLINA'. "
        "Verifique os valores únicos da coluna Produto."
    )

print("\nApós filtro (somente GASOLINA):")
print(df_gasolina["Produto"].unique())
print(f"Quantidade de registros: {df_gasolina.shape[0]}")

# ============================================================
# INSPECIONAR DATA
# ============================================================

print("\nExemplos da coluna Data da Coleta:")
print(df_gasolina["Data da Coleta"].head(10))

print("\n--- TESTE DE CONVERSÃO DE DATA ---")
try:
    datas_convertidas = pd.to_datetime(
        df_gasolina["Data da Coleta"].head(5),
        format="%d/%m/%Y"
    )
    print(datas_convertidas.tolist())
except Exception as e:
    print(f"AVISO: erro na conversão de datas → {e}")

# ============================================================
# INSPECIONAR VALOR DE VENDA
# ============================================================

print("\nExemplos da coluna Valor de Venda:")
print(df_gasolina["Valor de Venda"].head(10))
print(f"Tipo atual: {df_gasolina['Valor de Venda'].dtype}")

print("\n--- TESTE DE CONVERSÃO DE PREÇO ---")
try:
    valores_convertidos = pd.to_numeric(
        df_gasolina["Valor de Venda"]
        .astype(str)
        .str.replace(",", ".", regex=False),
        errors="coerce"
    )

    print(valores_convertidos.describe())

    invalidos = valores_convertidos.isnull().sum()
    if invalidos > 0:
        print(f"\nAVISO: {invalidos} valores inválidos detectados em 'Valor de Venda'.")

    print("\nAmostra convertida:")
    print(valores_convertidos.head(5).tolist())

except Exception as e:
    print(f"Erro na conversão de preços: {e}")