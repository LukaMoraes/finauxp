import re
from pathlib import Path
import pdfplumber

BASE = Path(__file__).resolve().parent.parent
RAW_DIR = BASE / "raw"
PDF, CSV = RAW_DIR / "faturanov26.pdf", RAW_DIR / "fatura_nov2026.csv"

with pdfplumber.open(PDF) as pdf:
    texto = pdf.pages[1].extract_text() or ""

# Bloco do cartão: após o segundo cabeçalho, antes do "Total"
bloco = texto.split("Data Movimentações Valor em R$")[-1].split("Total")[0]

rows = []
for linha in filter(None, map(str.strip, bloco.splitlines())):
    # "R$ 512,62" -> ",512.62" (vírgula decimal -> ponto)
    linha = re.sub(r"\s*R\$\s*([\d.]+),(\d{2})", r",\1.\2", linha)
    # "31/10 DESCRIÇÃO,512.62" -> "31/10,DESCRIÇÃO,512.62"
    rows.append(linha.replace(" ", ",", 1))

CSV.parent.mkdir(parents=True, exist_ok=True)
CSV.write_text("Data,Movimentações,Valor em R$\n" + "\n".join(rows), encoding="utf-8")
print(f"{len(rows)} linhas salvas em {CSV}")