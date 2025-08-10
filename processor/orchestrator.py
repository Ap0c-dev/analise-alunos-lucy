from processor.treatment_dub import process_data
from processor.load_dub import save_to_database
import logging

def main():
    """Orquestrador principal do fluxo de processamento"""
    try:
        logging.info("Iniciando processamento dos dados...")
        df_processed = process_data()

        logging.info("Salvando no banco de dados...")
        save_to_database(df_processed)
        
        logging.info("Pipeline executado com sucesso!")
        
    except Exception as e:
        logging.error(f"Erro durante a execução: {str(e)}")
        raise

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    main()