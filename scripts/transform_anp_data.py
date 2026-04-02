# ============================================================
# SCRIPT: TRANSFORMAÇÃO DOS DADOS DA ANP
# OBJETIVO:
# Preparar base limpa para análise
# ============================================================

from pathlib import Path
import pandas as pd

# Caminho dos dados brutos
RAW_PATH = Path(__file__).resolve().parent.parent / "data" / "raw"

print("Iniciando transformação dos dados...")

# ============================================================
# SCRIPT: TRANSFORMAÇÃO DOS DADOS DA ANP
# OBJETIVO:
# Preparar base limpa para análise
# ============================================================

from pathlib import Path
import pandas as pd

# Caminho dos dados brutos
RAW_PATH = Path(__file__).resolve().parent.parent / "data" / "raw"

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