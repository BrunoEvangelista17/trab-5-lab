"""
Script para Visualização de Dados do Experimento REST vs GraphQL
Autor: Especialista em Visualização de Dados
Data: Dezembro 2025

Este script gera boxplots comparativos para análise estatística dos resultados
do experimento REST vs GraphQL, focando em duas questões de pesquisa (RQ):
- RQ1: Tempo de resposta
- RQ2: Tamanho da resposta
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# Configurações de estilo visual
sns.set_theme(style="whitegrid")
sns.set_context("notebook", font_scale=1.1)

# Paleta de cores para diferenciação clara entre REST e GraphQL
COLORS = {
    'REST': '#E74C3C',      # Vermelho
    'GraphQL': '#3498DB'    # Azul
}


def load_experiment_data(filename: str = 'dados_experimento.csv') -> pd.DataFrame:
    """
    Carrega os dados do experimento a partir do arquivo CSV.
    
    Args:
        filename: Nome do arquivo CSV contendo os dados
        
    Returns:
        DataFrame com os dados do experimento
        
    Raises:
        FileNotFoundError: Se o arquivo não for encontrado
    """
    filepath = Path(filename)
    
    if not filepath.exists():
        raise FileNotFoundError(
            f"Arquivo '{filename}' não encontrado. "
            f"Execute primeiro o script 'gerar_dados_experimento.py'."
        )
    
    df = pd.read_csv(filename)
    
    # Validação básica das colunas esperadas
    expected_columns = ['run_id', 'api_type', 'query_scenario', 
                       'response_time_ms', 'response_size_bytes']
    
    missing_columns = set(expected_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Colunas ausentes no dataset: {missing_columns}")
    
    print(f"✓ Dataset carregado com sucesso!")
    print(f"  Total de registros: {len(df)}")
    print(f"  Tipos de API: {', '.join(df['api_type'].unique())}")
    print(f"  Cenários: {', '.join(df['query_scenario'].unique())}")
    
    return df


def create_boxplot_for_scenario(df: pd.DataFrame, scenario: str, metric: str, 
                                 metric_label: str, output_dir: str = 'graficos') -> None:
    """
    Cria um boxplot individual para um cenário específico e métrica.
    
    Args:
        df: DataFrame com os dados do experimento
        scenario: Nome do cenário (ex: 'getUser')
        metric: Nome da coluna da métrica ('response_time_ms' ou 'response_size_bytes')
        metric_label: Label para o eixo Y
        output_dir: Diretório para salvar os gráficos
    """
    # Filtra dados apenas para o cenário específico
    df_scenario = df[df['query_scenario'] == scenario]
    
    # Cria figura
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Define ordem dos tipos de API
    api_order = ['REST', 'GraphQL']
    
    # Cria boxplot
    sns.boxplot(
        data=df_scenario,
        x='api_type',
        y=metric,
        order=api_order,
        palette=COLORS,
        ax=ax,
        showfliers=True,
        linewidth=2,
        width=0.6
    )
    
    # Configurações do gráfico
    title = f'{scenario}: {metric_label}'
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Tipo de API', fontsize=12, fontweight='bold')
    ax.set_ylabel(metric_label, fontsize=12, fontweight='bold')
    ax.tick_params(axis='both', labelsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Adiciona estatísticas descritivas como texto
    stats_text = []
    for api_type in api_order:
        data = df_scenario[df_scenario['api_type'] == api_type][metric]
        mean_val = data.mean()
        median_val = data.median()
        stats_text.append(f"{api_type}: μ={mean_val:.1f}, M={median_val:.1f}")
    
    # Adiciona texto com estatísticas no gráfico
    ax.text(0.02, 0.98, '\n'.join(stats_text), 
            transform=ax.transAxes, 
            fontsize=9, 
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    # Ajusta layout
    plt.tight_layout()
    
    # Cria diretório se não existir
    Path(output_dir).mkdir(exist_ok=True)
    
    # Define nome do arquivo
    metric_name = 'tempo' if 'time' in metric else 'tamanho'
    filename = f"{output_dir}/{scenario}_{metric_name}.png"
    
    # Salva a figura
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    
    plt.close()


def create_all_scenario_charts(df: pd.DataFrame) -> None:
    """
    Cria gráficos individuais para todos os cenários e métricas.
    
    Args:
        df: DataFrame com os dados do experimento
    """
    # Lista de cenários
    scenarios = df['query_scenario'].unique()
    
    print("\n📊 Gerando gráficos individuais por cenário...")
    print("="*70)
    
    # Para cada cenário, cria gráficos de tempo e tamanho
    for i, scenario in enumerate(scenarios, 1):
        # Gráfico de Tempo de Resposta
        create_boxplot_for_scenario(
            df, 
            scenario, 
            'response_time_ms', 
            'Tempo de Resposta (ms)'
        )
        print(f"  [{i}/{len(scenarios)}] ✓ {scenario}_tempo.png")
        
        # Gráfico de Tamanho da Resposta
        create_boxplot_for_scenario(
            df, 
            scenario, 
            'response_size_bytes', 
            'Tamanho da Resposta (bytes)'
        )
        print(f"  [{i}/{len(scenarios)}] ✓ {scenario}_tamanho.png")
    
    print("="*70)
    print(f"✓ Total de gráficos gerados: {len(scenarios) * 2}")


def print_summary_statistics(df: pd.DataFrame) -> None:
    """
    Imprime estatísticas descritivas resumidas dos dados.
    
    Args:
        df: DataFrame com os dados do experimento
    """
    print("\n" + "="*70)
    print("ESTATÍSTICAS DESCRITIVAS POR TIPO DE API")
    print("="*70)
    
    # Estatísticas de tempo de resposta
    print("\n📊 TEMPO DE RESPOSTA (ms):")
    print(df.groupby('api_type')['response_time_ms'].describe().round(2))
    
    # Estatísticas de tamanho da resposta
    print("\n📊 TAMANHO DA RESPOSTA (bytes):")
    print(df.groupby('api_type')['response_size_bytes'].describe().round(2))
    
    # Comparação por cenário
    print("\n📊 COMPARAÇÃO POR CENÁRIO:")
    summary = df.groupby(['query_scenario', 'api_type']).agg({
        'response_time_ms': ['mean', 'median'],
        'response_size_bytes': ['mean', 'median']
    }).round(2)
    print(summary)
    
    # Contagem de outliers (valores além de 1.5 * IQR)
    print("\n📊 ANÁLISE DE OUTLIERS:")
    for api_type in df['api_type'].unique():
        api_data = df[df['api_type'] == api_type]['response_time_ms']
        Q1 = api_data.quantile(0.25)
        Q3 = api_data.quantile(0.75)
        IQR = Q3 - Q1
        outliers = api_data[(api_data < Q1 - 1.5*IQR) | (api_data > Q3 + 1.5*IQR)]
        print(f"  {api_type}: {len(outliers)} outliers detectados ({len(outliers)/len(api_data)*100:.1f}%)")


def main():
    """Função principal para execução do script."""
    print("="*70)
    print("VISUALIZAÇÃO DE RESULTADOS - EXPERIMENTO REST vs GraphQL")
    print("="*70)
    print("\nCarregando dados do experimento...")
    
    try:
        # Carrega os dados
        df = load_experiment_data()
        
        # Imprime estatísticas descritivas
        print_summary_statistics(df)
        
        # Gera gráficos individuais por cenário
        create_all_scenario_charts(df)
        
        print("\n" + "="*70)
        print("Processo concluído!")
        print("="*70)
        print("\n💡 Arquivos gerados no diretório 'graficos/':")
        scenarios = df['query_scenario'].unique()
        for scenario in scenarios:
            print(f"  - {scenario}_tempo.png")
            print(f"  - {scenario}_tamanho.png")
        
    except FileNotFoundError as e:
        print(f"\n❌ Erro: {e}")
        print("Execute primeiro: python gerar_dados_experimento.py")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        raise


if __name__ == "__main__":
    main()
