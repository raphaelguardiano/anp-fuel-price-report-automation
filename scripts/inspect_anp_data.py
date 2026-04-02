# ============================================================
# SCRIPT: INSPEÇÃO INICIAL DOS DADOS DA ANP
# OBJETIVO:
# Entender a estrutura da base antes de qualquer transformação
# ============================================================

# Importa ferramentas para trabalhar com caminhos de arquivos
from pathlib import Path

# Importa a biblioteca principal de dados
import pandas as pd


# ============================================================
# DEFINIR CAMINHO DOS DADOS
# ============================================================

# __file__ → caminho do arquivo atual (inspect_anp_data.py)
# .resolve() → transforma em caminho absoluto
# .parent → sobe para pasta "scripts"
# .parent → sobe para raiz do projeto
# depois entra em: data/raw

RAW_PATH = Path(__file__).resolve().parent.parent / "data" / "raw"


# ============================================================
# INÍCIO DA EXECUÇÃO
# ============================================================

print("Iniciando inspeção dos arquivos...")
print(f"Pasta analisada: {RAW_PATH.resolve()}")


# ============================================================
# LOCALIZAR ARQUIVOS CSV
# ============================================================

# Procura todos os arquivos .csv dentro da pasta
arquivos = sorted(RAW_PATH.glob("*.csv"))

print("\nArquivos CSV encontrados:")
for arquivo in arquivos:
    print("-", arquivo.name)


# ============================================================
# VERIFICAR SE EXISTEM ARQUIVOS
# ============================================================

if not arquivos:
    print("\nNenhum arquivo CSV foi encontrado em data/raw/")


# ============================================================
# SE EXISTIR ARQUIVO → LER O PRIMEIRO
# ============================================================

else:
    # Pega o primeiro arquivo da lista
    primeiro_arquivo = arquivos[0]

    print(f"\nTentando ler o arquivo: {primeiro_arquivo.name}")

    # Lê o CSV usando pandas
    # sep=";" → separador de colunas
    # encoding="latin1" → para lidar com acentos
    df = pd.read_csv(primeiro_arquivo, sep=";", encoding="latin1")

    print("\nLeitura realizada com sucesso.")


    # ========================================================
    # TAMANHO DO DATASET
    # ========================================================

    # shape → (linhas, colunas)
    print(f"Dimensão do arquivo: {df.shape}")


    # ========================================================
    # LISTAR COLUNAS
    # ========================================================

    print("\nColunas encontradas:")
    for coluna in df.columns:
        print("-", coluna)


    # ========================================================
    # VER VALORES ÚNICOS DO PRODUTO
    # ========================================================

    print("\nValores únicos da coluna Produto:")
    print(df["Produto"].unique())
    
    # ========================================================
    # FILTRAR APENAS GASOLINA
    # ========================================================

    df_gasolina = df[df["Produto"] == "GASOLINA"]

    print("\nApós filtro (somente GASOLINA):")
    print(df_gasolina["Produto"].unique())
    print(f"Quantidade de registros: {df_gasolina.shape[0]}")
    
    # ========================================================
    # VER EXEMPLOS DA DATA DA COLETA
    # ========================================================

    print("\nExemplos da coluna Data da Coleta:")
    print(df_gasolina["Data da Coleta"].head(10))

    # ========================================================
    # VER EXEMPLOS DO VALOR DE VENDA
    # ========================================================

    print("\nExemplos da coluna Valor de Venda:")
    print(df_gasolina["Valor de Venda"].head(10))
    print(f"Tipo atual da coluna Valor de Venda: {df_gasolina['Valor de Venda'].dtype}")

