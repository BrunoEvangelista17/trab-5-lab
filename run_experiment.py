"""
Script principal para executar o experimento completo
"""
import subprocess
import sys
import time
import os


def run_servers():
    """Inicia os servidores REST e GraphQL"""
    print("Iniciando servidores...")
    
    # Obter o executável Python correto
    python_exe = sys.executable
    
    # Iniciar servidor REST
    rest_process = subprocess.Popen(
        [python_exe, "rest_server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Iniciar servidor GraphQL
    graphql_process = subprocess.Popen(
        [python_exe, "graphql_server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Aguardar servidores iniciarem
    print("Aguardando servidores iniciarem...")
    time.sleep(3)
    
    return rest_process, graphql_process


def run_benchmark():
    """Executa o benchmark"""
    print("\nExecutando benchmark...")
    
    python_exe = sys.executable
    result = subprocess.run(
        [python_exe, "benchmark_client.py"],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print("Erros:", result.stderr)
    
    return result.returncode == 0


def run_analysis():
    """Executa a análise estatística"""
    print("\nExecutando análise estatística...")
    
    python_exe = sys.executable
    result = subprocess.run(
        [python_exe, "statistical_analysis.py"],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print("Erros:", result.stderr)
    
    return result.returncode == 0


def main():
    """Função principal"""
    print("="*70)
    print("EXPERIMENTO: GraphQL vs REST")
    print("="*70)
    
    rest_proc = None
    graphql_proc = None
    
    try:
        # Passo 1: Iniciar servidores
        rest_proc, graphql_proc = run_servers()
        
        # Passo 2: Executar benchmark
        benchmark_success = run_benchmark()
        
        if not benchmark_success:
            print("\n❌ Erro ao executar benchmark!")
            return
        
        # Passo 3: Executar análise
        analysis_success = run_analysis()
        
        if not analysis_success:
            print("\n❌ Erro ao executar análise!")
            return
        
        print("\n" + "="*70)
        print("✓ EXPERIMENTO CONCLUÍDO COM SUCESSO!")
        print("="*70)
        print("\nArquivos gerados:")
        print("  - results.json (dados brutos)")
        print("  - analysis_results.png (gráficos)")
        print("  - summary_results.csv (tabela resumo)")
        
    except KeyboardInterrupt:
        print("\n\n⚠ Experimento interrompido pelo usuário")
    
    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
    
    finally:
        # Encerrar servidores
        print("\nEncerrando servidores...")
        if rest_proc:
            rest_proc.terminate()
        if graphql_proc:
            graphql_proc.terminate()
        
        time.sleep(1)
        print("✓ Servidores encerrados")


if __name__ == "__main__":
    main()
