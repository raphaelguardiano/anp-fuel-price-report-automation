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

