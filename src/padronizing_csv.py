import pandas as pd
from pathlib import Path

# Definição dos diretórios de entrada (raw) e saída (processed_raw)
BASE = Path(__file__).resolve().parent.parent
RAW_DIR = BASE / "raw"
PROC_DIR = BASE / "processed_raw"

def clean_amount(val):
    """Limpa e converte valores monetários em formato brasileiro/internacional para float."""
    if pd.isna(val):
        return 0.0
    s = str(val).strip().replace(" ", "").replace("R$", "")
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0

def standardize():
    PROC_DIR.mkdir(parents=True, exist_ok=True)
    
    # Varre todos os arquivos CSV na pasta raw para padronização
    for csv_path in RAW_DIR.glob("*.csv"):
        try:
            df = None
            # Tenta carregar o CSV testando diferentes delimitadores (vírgula ou ponto e vírgula)
            for sep in [",", ";"]:
                try:
                    df = pd.read_csv(csv_path, sep=sep)
                    if len(df.columns) > 1 and any(any(k in str(c).lower() for k in ["data", "date", "release"]) for c in df.columns):
                        break
                except Exception:
                    continue
            
            # Fallback para extratos bancários com cabeçalho nas linhas iniciais (ex: skiprows)
            if df is None or not any(any(k in str(c).lower() for k in ["data", "date", "release"]) for c in df.columns):
                df = pd.read_csv(csv_path, sep=";", skiprows=3)

            cols = {str(c).lower().strip(): c for c in df.columns}
            
            # Identifica dinamicamente as colunas de data, descrição e valor
            date_col = next((cols[c] for c in cols if "data" in c or "date" in c or "release" in c), None)
            desc_col = next((cols[c] for c in cols if "desc" in c or "mov" in c or "title" in c or "type" in c), None)
            amount_col = next((cols[c] for c in cols if "valor" in c or "amount" in c or "net" in c), None)

            if not (date_col and desc_col and amount_col):
                print(f"Aviso: Não foi possível mapear colunas em {csv_path.name}: {df.columns.tolist()}")
                continue

            # Cria o DataFrame padronizado com as colunas essenciais
            new_df = pd.DataFrame()
            new_df["date"] = df[date_col]
            new_df["description"] = df[desc_col]
            new_df["amount"] = df[amount_col].apply(clean_amount)

            # Salva o arquivo padronizado na pasta processed_raw
            out_path = PROC_DIR / csv_path.name
            new_df.to_csv(out_path, index=False, encoding="utf-8")
            print(f"Padronizado com sucesso: {csv_path.name} -> processed_raw/")
        except Exception as e:
            print(f"Erro ao processar {csv_path.name}: {e}")

if __name__ == "__main__":
    standardize()
