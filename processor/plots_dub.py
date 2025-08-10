import matplotlib.pyplot as plt

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
    ax = mensalidades.plot(kind='barh', color='lightgreen')
    
    plt.title('Total de Mensalidades por Professor')
    plt.xlabel('Valor Total (R$)')
    plt.ylabel('Professor')
    
    # Adiciona os valores nas barras
    for i, v in enumerate(mensalidades):
        ax.text(v + 0.5, i, f'R$ {v:,.2f}', color='black', va='center')
    
    plt.tight_layout()
    plt.show()
    
if __name__=='__main__':
    plot_alunos_por_professor(df_final)
    plot_mensalidade_por_professor(df_final)