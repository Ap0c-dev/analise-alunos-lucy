import pandas as pd
from extract.extract import extract_data

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
    else:
        df_final = pd.DataFrame()
    output_path = 'data/controle_dublagem_todos_professores.xlsx'
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df_final.to_excel(writer, index=False)
    print(f"Arquivo escrito em: {output_path}")
    return df_final

if __name__ == "__main__":
    df_final = get_professor_name()
    print(df_final.head())