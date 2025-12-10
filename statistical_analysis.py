"""
Análise Estatística dos resultados do experimento GraphQL vs REST
"""
import json
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List


class StatisticalAnalysis:
    """Classe para análise estatística dos resultados"""
    
    def __init__(self, results_file: str = "results.json"):
        """Carrega os resultados do arquivo JSON"""
        with open(results_file, 'r') as f:
            self.data = json.load(f)
    
    def calculate_statistics(self, values: List[float]) -> Dict:
        """Calcula estatísticas descritivas"""
        return {
            'mean': np.mean(values),
            'median': np.median(values),
            'std': np.std(values, ddof=1),
            'min': np.min(values),
            'max': np.max(values),
            'q25': np.percentile(values, 25),
            'q75': np.percentile(values, 75)
        }
    
    def perform_t_test(self, rest_values: List[float], graphql_values: List[float]) -> Dict:
        """
        Realiza teste t pareado (paired t-test)
        H0: μ_GraphQL >= μ_REST
        H1: μ_GraphQL < μ_REST
        """
        # Teste t pareado (one-tailed)
        # alternative='less' testa se GraphQL < REST
        t_statistic, p_value_two_tailed = stats.ttest_rel(graphql_values, rest_values)
        
        # Para teste unilateral (one-tailed), dividimos p-value por 2
        # Mas precisamos verificar se a diferença está na direção esperada
        if np.mean(graphql_values) < np.mean(rest_values):
            p_value = p_value_two_tailed / 2
        else:
            p_value = 1 - (p_value_two_tailed / 2)
        
        return {
            't_statistic': t_statistic,
            'p_value': p_value,
            'significant_at_0.05': p_value < 0.05,
            'significant_at_0.01': p_value < 0.01
        }
    
    def analyze_scenario(self, scenario_data: Dict) -> Dict:
        """Analisa um cenário específico"""
        scenario_name = scenario_data['scenario']
        
        rest_times = scenario_data['rest']['times']
        rest_sizes = scenario_data['rest']['sizes']
        graphql_times = scenario_data['graphql']['times']
        graphql_sizes = scenario_data['graphql']['sizes']
        
        print(f"\n{'='*70}")
        print(f"ANÁLISE: {scenario_name.upper().replace('_', ' ')}")
        print(f"{'='*70}")
        
        # Análise de Tempo de Resposta
        print("\n--- TEMPO DE RESPOSTA (ms) ---")
        rest_time_stats = self.calculate_statistics(rest_times)
        graphql_time_stats = self.calculate_statistics(graphql_times)
        
        print(f"\nREST:")
        print(f"  Média: {rest_time_stats['mean']:.2f} ms")
        print(f"  Mediana: {rest_time_stats['median']:.2f} ms")
        print(f"  Desvio Padrão: {rest_time_stats['std']:.2f} ms")
        print(f"  Min/Max: {rest_time_stats['min']:.2f} / {rest_time_stats['max']:.2f} ms")
        
        print(f"\nGraphQL:")
        print(f"  Média: {graphql_time_stats['mean']:.2f} ms")
        print(f"  Mediana: {graphql_time_stats['median']:.2f} ms")
        print(f"  Desvio Padrão: {graphql_time_stats['std']:.2f} ms")
        print(f"  Min/Max: {graphql_time_stats['min']:.2f} / {graphql_time_stats['max']:.2f} ms")
        
        time_improvement = ((rest_time_stats['mean'] - graphql_time_stats['mean']) / 
                           rest_time_stats['mean'] * 100)
        print(f"\nMelhoria GraphQL: {time_improvement:+.2f}%")
        
        # Teste estatístico para tempo
        time_test = self.perform_t_test(rest_times, graphql_times)
        print(f"\nTeste t pareado (Tempo):")
        print(f"  t-statistic: {time_test['t_statistic']:.4f}")
        print(f"  p-value: {time_test['p_value']:.6f}")
        print(f"  Significante (α=0.05): {'SIM' if time_test['significant_at_0.05'] else 'NÃO'}")
        print(f"  Significante (α=0.01): {'SIM' if time_test['significant_at_0.01'] else 'NÃO'}")
        
        if time_test['significant_at_0.05']:
            print("  ✓ Rejeitamos H0: GraphQL é significativamente mais rápido que REST")
        else:
            print("  ✗ Não rejeitamos H0: Diferença não é estatisticamente significativa")
        
        # Análise de Tamanho da Resposta
        print("\n--- TAMANHO DA RESPOSTA (bytes) ---")
        rest_size_stats = self.calculate_statistics(rest_sizes)
        graphql_size_stats = self.calculate_statistics(graphql_sizes)
        
        print(f"\nREST:")
        print(f"  Média: {rest_size_stats['mean']:.0f} bytes")
        print(f"  Mediana: {rest_size_stats['median']:.0f} bytes")
        print(f"  Desvio Padrão: {rest_size_stats['std']:.2f} bytes")
        
        print(f"\nGraphQL:")
        print(f"  Média: {graphql_size_stats['mean']:.0f} bytes")
        print(f"  Mediana: {graphql_size_stats['median']:.0f} bytes")
        print(f"  Desvio Padrão: {graphql_size_stats['std']:.2f} bytes")
        
        size_reduction = ((rest_size_stats['mean'] - graphql_size_stats['mean']) / 
                         rest_size_stats['mean'] * 100)
        print(f"\nRedução GraphQL: {size_reduction:+.2f}%")
        
        # Teste estatístico para tamanho
        size_test = self.perform_t_test(rest_sizes, graphql_sizes)
        print(f"\nTeste t pareado (Tamanho):")
        print(f"  t-statistic: {size_test['t_statistic']:.4f}")
        print(f"  p-value: {size_test['p_value']:.6f}")
        print(f"  Significante (α=0.05): {'SIM' if size_test['significant_at_0.05'] else 'NÃO'}")
        print(f"  Significante (α=0.01): {'SIM' if size_test['significant_at_0.01'] else 'NÃO'}")
        
        if size_test['significant_at_0.05']:
            print("  ✓ Rejeitamos H0: GraphQL tem payload significativamente menor que REST")
        else:
            print("  ✗ Não rejeitamos H0: Diferença não é estatisticamente significativa")
        
        return {
            'scenario': scenario_name,
            'time': {
                'rest': rest_time_stats,
                'graphql': graphql_time_stats,
                'improvement_percent': time_improvement,
                'test': time_test
            },
            'size': {
                'rest': rest_size_stats,
                'graphql': graphql_size_stats,
                'reduction_percent': size_reduction,
                'test': size_test
            }
        }
    
    def generate_report(self) -> List[Dict]:
        """Gera relatório completo de todos os cenários"""
        print("\n" + "="*70)
        print("RELATÓRIO DE ANÁLISE ESTATÍSTICA: GraphQL vs REST")
        print("="*70)
        
        analysis_results = []
        
        for scenario_data in self.data:
            result = self.analyze_scenario(scenario_data)
            analysis_results.append(result)
        
        return analysis_results
    
    def create_visualizations(self, analysis_results: List[Dict]):
        """Cria visualizações dos resultados"""
        num_scenarios = len(analysis_results)
        
        # Criar figura com subplots
        fig, axes = plt.subplots(num_scenarios, 2, figsize=(14, 5*num_scenarios))
        if num_scenarios == 1:
            axes = axes.reshape(1, -1)
        
        for idx, result in enumerate(analysis_results):
            scenario_name = result['scenario'].replace('_', ' ').title()
            
            # Gráfico de Tempo de Resposta
            ax_time = axes[idx, 0]
            rest_time = result['time']['rest']['mean']
            gql_time = result['time']['graphql']['mean']
            rest_time_std = result['time']['rest']['std']
            gql_time_std = result['time']['graphql']['std']
            
            bars_time = ax_time.bar(['REST', 'GraphQL'], [rest_time, gql_time], 
                                   yerr=[rest_time_std, gql_time_std],
                                   color=['#FF6B6B', '#4ECDC4'], capsize=5)
            ax_time.set_ylabel('Tempo de Resposta (ms)')
            ax_time.set_title(f'{scenario_name}\nTempo de Resposta')
            ax_time.grid(axis='y', alpha=0.3)
            
            # Adicionar valores nas barras
            for bar in bars_time:
                height = bar.get_height()
                ax_time.text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.2f}',
                           ha='center', va='bottom')
            
            # Gráfico de Tamanho da Resposta
            ax_size = axes[idx, 1]
            rest_size = result['size']['rest']['mean']
            gql_size = result['size']['graphql']['mean']
            rest_size_std = result['size']['rest']['std']
            gql_size_std = result['size']['graphql']['std']
            
            bars_size = ax_size.bar(['REST', 'GraphQL'], [rest_size, gql_size],
                                   yerr=[rest_size_std, gql_size_std],
                                   color=['#FF6B6B', '#4ECDC4'], capsize=5)
            ax_size.set_ylabel('Tamanho da Resposta (bytes)')
            ax_size.set_title(f'{scenario_name}\nTamanho da Resposta')
            ax_size.grid(axis='y', alpha=0.3)
            
            # Adicionar valores nas barras
            for bar in bars_size:
                height = bar.get_height()
                ax_size.text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.0f}',
                           ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('analysis_results.png', dpi=300, bbox_inches='tight')
        print("\n✓ Gráficos salvos em: analysis_results.png")
        plt.close()
    
    def create_summary_table(self, analysis_results: List[Dict]):
        """Cria tabela resumo dos resultados"""
        summary_data = []
        
        for result in analysis_results:
            scenario = result['scenario'].replace('_', ' ').title()
            
            summary_data.append({
                'Cenário': scenario,
                'REST Tempo (ms)': f"{result['time']['rest']['mean']:.2f} ± {result['time']['rest']['std']:.2f}",
                'GraphQL Tempo (ms)': f"{result['time']['graphql']['mean']:.2f} ± {result['time']['graphql']['std']:.2f}",
                'Melhoria Tempo (%)': f"{result['time']['improvement_percent']:+.2f}%",
                'P-value Tempo': f"{result['time']['test']['p_value']:.6f}",
                'REST Size (bytes)': f"{result['size']['rest']['mean']:.0f}",
                'GraphQL Size (bytes)': f"{result['size']['graphql']['mean']:.0f}",
                'Redução Size (%)': f"{result['size']['reduction_percent']:+.2f}%",
                'P-value Size': f"{result['size']['test']['p_value']:.6f}"
            })
        
        df = pd.DataFrame(summary_data)
        
        print("\n" + "="*70)
        print("TABELA RESUMO DOS RESULTADOS")
        print("="*70)
        print(df.to_string(index=False))
        
        # Salvar em CSV
        df.to_csv('summary_results.csv', index=False)
        print("\n✓ Tabela resumo salva em: summary_results.csv")
        
        return df


def main():
    """Função principal"""
    print("Iniciando análise estatística...")
    
    analysis = StatisticalAnalysis("results.json")
    results = analysis.generate_report()
    
    print("\n" + "="*70)
    print("GERANDO VISUALIZAÇÕES E TABELAS")
    print("="*70)
    
    analysis.create_visualizations(results)
    analysis.create_summary_table(results)
    
    print("\n" + "="*70)
    print("ANÁLISE CONCLUÍDA!")
    print("="*70)
    print("\nArquivos gerados:")
    print("  - analysis_results.png (gráficos)")
    print("  - summary_results.csv (tabela resumo)")


if __name__ == "__main__":
    main()
