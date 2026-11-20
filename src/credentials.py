import json
import logging
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from auth import get_credentials

# Configuração do sistema de logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# Definição de diretórios principais e identificador da pasta no Drive
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
RAW_DIR = BASE_DIR / "raw"
MANIFEST_PATH = CONFIG_DIR / "manifest.json"
FOLDER_ID = "1GVchYD8NybFSkFU8jFGVZO8J-zKvpU1s"

def main():
    log.info("=== Iniciando pipeline ===")
    
    # Autenticação e construção do cliente da API do Google Drive
    creds = get_credentials()
    service = build("drive", "v3", credentials=creds)

    # Carrega o manifesto de arquivos já baixados anteriormente
    processed = set(json.loads(MANIFEST_PATH.read_text())) if MANIFEST_PATH.exists() else set()
    
    # Lista arquivos presentes na pasta monitorada do Google Drive
    files = service.files().list(q=f"'{FOLDER_ID}' in parents and trashed = false", fields="files(id, name)").execute().get("files", [])
    
    # Filtra apenas arquivos que ainda não foram baixados
    novos = [f for f in files if f["id"] not in processed]
    log.info("%d arquivos novos para baixar.", len(novos))
    
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # Faz o download de cada novo arquivo e atualiza o manifesto
    for f in novos:
        log.info("Baixando '%s'...", f["name"])
        request = service.files().get_media(fileId=f["id"])
        path = RAW_DIR / f["name"]
        with open(path, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request)
            while not downloader.next_chunk()[1]: pass
        processed.add(f["id"])

    # Salva o manifesto atualizado com os novos IDs processados
    MANIFEST_PATH.write_text(json.dumps(sorted(processed), indent=2))
    log.info("=== Fim do pipeline ===")

if __name__ == "__main__":
    main()
