from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Definição de caminhos e escopos de acesso à API do Google Drive
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
CREDENTIALS_PATH = next(CONFIG_DIR.glob("client_secret_*.json"))
TOKEN_PATH = CONFIG_DIR / "token.json"
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

def get_credentials():
    """Obtém, renova ou gera novas credenciais OAuth2 para acessar o Google Drive."""
    # Carrega o token existente se ele já estiver salvo
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES) if TOKEN_PATH.exists() else None
    
    # Se as credenciais não existirem ou forem inválidas, renova ou executa o fluxo de autenticação local
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES).run_local_server(port=0)
        # Salva o token atualizado em disco
        TOKEN_PATH.write_text(creds.to_json())
    return creds
