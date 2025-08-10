import sqlite3
from processor.treatment_dub import process_data

def save_to_database(df):
    df = process_data()
    
    conn = sqlite3.connect('/home/tiago/banco_lucy')
    
    try:
        df.to_sql('alunos', conn, if_exists='replace', index=False)
        print("Dados salvos com sucesso no banco de dados!")
    except Exception as e:
        print(f"Erro ao salvar no banco de dados: {e}")
        raise
    finally:
        conn.close()
    
    conn.close()
    
    if __name__=='__main__':
        save_to_database()