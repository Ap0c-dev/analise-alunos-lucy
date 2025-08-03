from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from io import BytesIO
import pandas as pd
from params.drive_params import SERVICE_ACCOUNT_FILE, GOOGLE_DRIVE_FILE_ID, SCOPES

def get_data_from_drive():
    """Obtém dados do Google Drive"""
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=SCOPES
        )
        
        service = build('drive', 'v3', credentials=creds)
        
        request = service.files().get_media(fileId=GOOGLE_DRIVE_FILE_ID)
        content = BytesIO()
        downloader = MediaIoBaseDownload(content, request)
        
        done = False
        while not done:
            _, done = downloader.next_chunk()

        content.seek(0)

        df = pd.read_excel(content, engine='openpyxl')
        return df
    
    except Exception as e:
        print(f"Erro ao acessar arquivo: {e}")
        return None

if __name__ == "__main__":
    # Teste da função
    dados = get_data_from_drive()
    if dados is not None:
        print("Dados carregados com sucesso!")
        print(dados.head())