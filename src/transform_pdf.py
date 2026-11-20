import re
from pathlib import Path
import pdfplumber

# Definição dos diretórios principais do projeto
BASE = Path(__file__).resolve().parent.parent
RAW_DIR = BASE / "raw"

def transform_pdf_to_csv(pdf_path: Path) -> Path:
    """Extrai transações financeiras de uma fatura em PDF específica e a converte para CSV."""
    # Define o caminho do CSV resultante com base no nome do PDF
    csv_path = pdf_path.with_suffix(".csv")

    # Abre o PDF e extrai o texto da página relevante (página 2, índice 1)
    with pdfplumber.open(pdf_path) as pdf:
        texto = pdf.pages[1].extract_text() or ""

    # Isola o bloco de transações entre o cabeçalho e a palavra 'Total'
    bloco = texto.split("Data Movimentações Valor em R$")[-1].split("Total")[0]

    rows = []
    # Processa linha por linha do bloco extraído
    for linha in filter(None, map(str.strip, bloco.splitlines())):
        # Padroniza o formato do valor monetário (ex: "R$ 512,62" -> ",512.62")
        linha = re.sub(r"\s*R\$\s*([\d.]+),(\d{2})", r",\1.\2", linha)
        # Insere vírgulas separando data, descrição e valor
        rows.append(linha.replace(" ", ",", 1))

    # Salva o resultado em formato CSV na pasta raw
    csv_path.write_text("Data,Movimentações,Valor em R$\n" + "\n".join(rows), encoding="utf-8")
    print(f"PDF transformado com sucesso: {pdf_path.name} -> {csv_path.name} ({len(rows)} linhas)")
    return csv_path

def process_raw_pdfs():
    """Varre a pasta raw em busca de PDFs novos que ainda não foram transformados em CSV."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    
    # Busca todos os arquivos PDF na pasta raw
    pdf_files = list(RAW_DIR.glob("*.pdf"))
    if not pdf_files:
        print("Nenhum PDF encontrado na pasta raw.")
        return

    # Percorre cada PDF encontrado na pasta raw
    for pdf_path in pdf_files:
        # Define o arquivo CSV correspondente esperado
        csv_path = pdf_path.with_suffix(".csv")
        
        # Verifica se o PDF já foi transformado anteriormente (se o arquivo CSV já existe)
        if csv_path.exists():
            print(f"PDF já transformado anteriormente (ignorado): {pdf_path.name}")
            continue
            
        # Se for um PDF novo, executa a transformação
        print(f"Novo PDF detectado: {pdf_path.name}. Iniciando transformação...")
        try:
            transform_pdf_to_csv(pdf_path)
        except Exception as e:
            print(f"Erro ao transformar o PDF {pdf_path.name}: {e}")

if __name__ == "__main__":
    process_raw_pdfs()
