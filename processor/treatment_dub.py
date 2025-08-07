import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt


def get_professor_name():
    df = pd.read_excel('CONTROLE DE ALUNOS DUBLAGEM.xlsx', sheet_name='DUBLAGEM', header=[0,1]) 
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
    df.columns = (
        str(col)
        .strip()
        .lower()
        .replace(' ', '_')
        .translate(str.maketrans('áéíóú', 'aeiou'))
        for col in df.columns
    )
    return df

def clean_columns_data(df):
    df['professor'] = df['professor'].str.split().str[:2].str.join(' ')
    df['professor'] = df['professor'].str.title()
    df['aluno'] = df['aluno'].str.title()
    df['dia_aula'] = df['dia_aula'].str.split().str[:1].str.join(' ')
    return df
    
def plot_alunos_por_professor(df):
    
    alunos_por_professor = df['professor'].value_counts()
    
    plt.figure(figsize=(10,6))
    alunos_por_professor.plot(kind='barh', color='skyblue')
    
    plt.title('Quantidade de alunos por professor')
    plt.xlabel('Número de Alunos', fontsize=12)
    plt.ylabel('Professor', fontsize=12)
    
    for index, value in enumerate(alunos_por_professor):
        plt.text(value, index, f'{value}', va='center')
    
    plt.tight_layout()
    plt.show()

def calcular_mensalidades_por_professor(df):
    if 'valor' not in df.columns:
        print("Aviso: Coluna 'valor' não encontrada no DataFrame.")
        print("Colunas disponíveis:", df.columns.tolist())
        return None
    
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce').fillna(0)
    
    mensalidades = df.groupby('professor')['valor'].sum()
    
    return mensalidades

def plot_mensalidade_por_professor(df):
    mensalidades = calcular_mensalidades_por_professor(df)
    
    if mensalidades is None:
        return
    
    plt.figure(figsize=(10,6))
    ax = mensalidades.plot(kind='barh', color='lightgreen')  # Mudei para barh (horizontal)
    
    plt.title('Total de Mensalidades por Professor')
    plt.xlabel('Valor Total (R$)')
    plt.ylabel('Professor')
    
    # Adiciona os valores nas barras
    for i, v in enumerate(mensalidades):
        ax.text(v + 0.5, i, f'R$ {v:,.2f}', color='black', va='center')  # Formata com 2 decimais
    
    plt.tight_layout()
    plt.show()
        
if __name__ == "__main__":
    df_final = get_professor_name()
    df_final = clean_column_names(df_final)
    df_final = clean_columns_data(df_final)

    plot_alunos_por_professor(df_final)
    plot_mensalidade_por_professor(df_final)

    #output_path = 'data/controle_dublagem_todos_professores.xlsx'
    #df_final.to_excel(output_path, index=False)