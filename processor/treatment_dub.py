import unicodedata
import pandas as pd
import re

def get_professor_name():
    df = pd.read_excel('data/CONTROLE DE ALUNOS DUBLAGEM.xlsx', sheet_name='DUBLAGEM', header=[0,1]) 
    professores = list(df.columns.get_level_values(0).unique())

    lista_dfs = []
    for professor in professores:
        try:
            df_professor = df.xs(professor, axis=1, level=0).copy()
            df_professor['professor'] = professor
            if 'ALUNO' in df_professor.columns:
                lista_dfs.append(df_professor)
        except Exception as e:
            print(f"Erro ao processar {professor}: {e!r}")

    if lista_dfs:
        df_final = pd.concat(lista_dfs, ignore_index=True)
        df_final = df_final.dropna(subset=['ALUNO'])
    else:
        df_final = pd.DataFrame()
    return df_final

def clean_column_names(df):
    df = df.rename(columns={'PGT': 'dia_pagamento'})
    df.columns = [str(col).strip().lower().replace(' ', '_').translate(str.maketrans('áéíóú', 'aeiou')) 
                for col in df.columns]
    
    if 'dia_pagamento' in df.columns:
        def clean_day(value):
            try:
                day = int(float(str(value)))
                return day if 1 <= day <= 31 else None
            except (ValueError, TypeError):
                value_str = str(value).strip()
                clean_str = re.sub(r'[^\d\-/]', '', value_str)
                
                if '-' in clean_str:
                    first_num = clean_str.split('-')[0]
                    try:
                        day = int(first_num)
                        return day if 1 <= day <= 31 else None
                    except ValueError:
                        return None
                
                numbers = re.findall(r'\d+', clean_str)
                if numbers:
                    day = int(numbers[0])
                    return day if 1 <= day <= 31 else None
                
                return None
        
        df['dia_pagamento'] = (
            df['dia_pagamento']
            .map(clean_day)
            .astype('Int64')
        )
    
    return df

def clean_columns_data(df):
    df['professor'] = df['professor'].str.split().str[:2].str.join(' ').str.title()
    df['aluno'] = df['aluno'].str.title()
    df['dia_aula'] = df['dia_aula'].str.split().str[:1].str.join(' ')
    df['modalidade'] = df['modalidade'].str.split().str[:1].str.join(' ').str.lower()
    return df

def normalize_dia_aula(dia):
    if pd.isna(dia):
        return None
    
    dias_map = {
        'SEG': ['segunda', '2a', '2ª', 'segunda-feira', 'seg'],
        'TER': ['terca', 'terça', '3a', '3ª', 'terca-feira', 'ter'],
        'QUA': ['quarta', '4a', '4ª', 'quarta-feira', 'qua'],
        'QUI': ['quinta', '5a', '5ª', 'quinta-feira', 'qui'],
        'SEX': ['sexta', '6a', '6ª', 'sexta-feira', 'sex'],
        'SAB': ['sabado', 'sábado', 'sab'],
        'DOM': ['domingo', 'dom']
    }
    
    dia_str = str(dia).strip().lower()
    dia_str = unicodedata.normalize('NFKD', dia_str)
    dia_str = ''.join([c for c in dia_str if not unicodedata.combining(c)])
    dia_str = re.sub(r'[-_ ]', '', dia_str)
    
    for normalized, variants in dias_map.items():
        if any(variant.replace('-', '').replace('ç', 'c') in dia_str for variant in variants):
            return normalized
    
    return None

def process_data():
    """Função principal que executa todo o processamento"""
    df = get_professor_name()
    df = clean_column_names(df)
    df = clean_columns_data(df)
    df['dia_aula'] = df['dia_aula'].apply(normalize_dia_aula)
    return df

if __name__ == "__main__":
    df_processed = process_data()
    df_processed.to_excel('data/controle_dublagem_todos_professores.xlsx', index=False)
    print(f"DataFrame retornado: {type(df_processed)}")