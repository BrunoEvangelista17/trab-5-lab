"""
Cliente de teste para comparar performance REST vs GraphQL
"""
import requests
import time
import json
from typing import List, Dict, Tuple


class BenchmarkClient:
    """Cliente para realizar benchmarks entre REST e GraphQL"""
    
    def __init__(self, rest_url: str = "http://localhost:5000", 
                 graphql_url: str = "http://localhost:5001/graphql"):
        self.rest_url = rest_url
        self.graphql_url = graphql_url
    
    def warmup(self, repetitions: int = 5):
        """
        Executa warm-up para evitar cold start
        """
        print(f"Executando warm-up ({repetitions} repetições)...")
        for i in range(repetitions):
            # Warm-up REST
            try:
                requests.get(f"{self.rest_url}/api/users/1")
            except:
                pass
            
            # Warm-up GraphQL
            try:
                query = '{ user(id: 1) { name } }'
                requests.post(self.graphql_url, json={'query': query})
            except:
                pass
        
        print("Warm-up concluído!")
    
    def measure_rest_request(self, endpoint: str) -> Tuple[float, int]:
        """
        Mede tempo de resposta e tamanho da resposta para REST
        Retorna: (tempo_ms, tamanho_bytes)
        """
        start_time = time.perf_counter()
        response = requests.get(f"{self.rest_url}{endpoint}")
        end_time = time.perf_counter()
        
        response_time_ms = (end_time - start_time) * 1000
        response_size_bytes = len(response.content)
        
        return response_time_ms, response_size_bytes
    
    def measure_graphql_request(self, query: str, variables: dict = None) -> Tuple[float, int]:
        """
        Mede tempo de resposta e tamanho da resposta para GraphQL
        Retorna: (tempo_ms, tamanho_bytes)
        """
        payload = {'query': query}
        if variables:
            payload['variables'] = variables
        
        start_time = time.perf_counter()
        response = requests.post(self.graphql_url, json=payload)
        end_time = time.perf_counter()
        
        response_time_ms = (end_time - start_time) * 1000
        response_size_bytes = len(response.content)
        
        return response_time_ms, response_size_bytes
    
    def run_scenario_simple_user(self, repetitions: int = 100) -> Dict:
        """
        Cenário 1: Busca simples - Nome e email do usuário
        """
        print(f"\n=== Cenário 1: Busca Simples (Nome e Email) ===")
        print(f"Executando {repetitions} repetições...\n")
        
        rest_times = []
        rest_sizes = []
        graphql_times = []
        graphql_sizes = []
        
        # REST: retorna todos os campos do usuário
        rest_endpoint = "/api/users/1"
        
        # GraphQL: solicita apenas nome e email
        graphql_query = """
        {
            user(id: 1) {
                name
                email
            }
        }
        """
        
        for i in range(repetitions):
            # Teste REST
            try:
                rest_time, rest_size = self.measure_rest_request(rest_endpoint)
                rest_times.append(rest_time)
                rest_sizes.append(rest_size)
            except Exception as e:
                print(f"Erro REST na iteração {i+1}: {e}")
            
            # Teste GraphQL
            try:
                gql_time, gql_size = self.measure_graphql_request(graphql_query)
                graphql_times.append(gql_time)
                graphql_sizes.append(gql_size)
            except Exception as e:
                print(f"Erro GraphQL na iteração {i+1}: {e}")
            
            if (i + 1) % 20 == 0:
                print(f"Progresso: {i+1}/{repetitions}")
        
        return {
            'scenario': 'simple_user',
            'rest': {'times': rest_times, 'sizes': rest_sizes},
            'graphql': {'times': graphql_times, 'sizes': graphql_sizes}
        }
    
    def run_scenario_user_with_posts(self, repetitions: int = 100) -> Dict:
        """
        Cenário 2: Busca complexa - Usuário com títulos de 5 posts
        """
        print(f"\n=== Cenário 2: Busca Complexa (Usuário + Posts) ===")
        print(f"Executando {repetitions} repetições...\n")
        
        rest_times = []
        rest_sizes = []
        graphql_times = []
        graphql_sizes = []
        
        # REST: retorna usuário completo com posts completos e comentários
        rest_endpoint = "/api/users/1/full"
        
        # GraphQL: solicita apenas campos específicos
        graphql_query = """
        {
            user(id: 1) {
                name
                email
                posts(limit: 5) {
                    title
                }
            }
        }
        """
        
        for i in range(repetitions):
            # Teste REST
            try:
                rest_time, rest_size = self.measure_rest_request(rest_endpoint)
                rest_times.append(rest_time)
                rest_sizes.append(rest_size)
            except Exception as e:
                print(f"Erro REST na iteração {i+1}: {e}")
            
            # Teste GraphQL
            try:
                gql_time, gql_size = self.measure_graphql_request(graphql_query)
                graphql_times.append(gql_time)
                graphql_sizes.append(gql_size)
            except Exception as e:
                print(f"Erro GraphQL na iteração {i+1}: {e}")
            
            if (i + 1) % 20 == 0:
                print(f"Progresso: {i+1}/{repetitions}")
        
        return {
            'scenario': 'user_with_posts',
            'rest': {'times': rest_times, 'sizes': rest_sizes},
            'graphql': {'times': graphql_times, 'sizes': graphql_sizes}
        }
    
    def run_scenario_nested_data(self, repetitions: int = 100) -> Dict:
        """
        Cenário 3: Busca aninhada - Usuário com posts e comentários
        """
        print(f"\n=== Cenário 3: Busca Aninhada (Usuário + Posts + Comentários) ===")
        print(f"Executando {repetitions} repetições...\n")
        
        rest_times = []
        rest_sizes = []
        graphql_times = []
        graphql_sizes = []
        
        # REST: retorna tudo
        rest_endpoint = "/api/users/1/full"
        
        # GraphQL: solicita estrutura aninhada específica
        graphql_query = """
        {
            user(id: 1) {
                name
                email
                posts(limit: 5) {
                    title
                    likes
                    comments(limit: 3) {
                        author
                        text
                    }
                }
            }
        }
        """
        
        for i in range(repetitions):
            # Teste REST
            try:
                rest_time, rest_size = self.measure_rest_request(rest_endpoint)
                rest_times.append(rest_time)
                rest_sizes.append(rest_size)
            except Exception as e:
                print(f"Erro REST na iteração {i+1}: {e}")
            
            # Teste GraphQL
            try:
                gql_time, gql_size = self.measure_graphql_request(graphql_query)
                graphql_times.append(gql_time)
                graphql_sizes.append(gql_size)
            except Exception as e:
                print(f"Erro GraphQL na iteração {i+1}: {e}")
            
            if (i + 1) % 20 == 0:
                print(f"Progresso: {i+1}/{repetitions}")
        
        return {
            'scenario': 'nested_data',
            'rest': {'times': rest_times, 'sizes': rest_sizes},
            'graphql': {'times': graphql_times, 'sizes': graphql_sizes}
        }
    
    def save_results(self, results: List[Dict], filename: str = "results.json"):
        """Salva resultados em arquivo JSON"""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResultados salvos em: {filename}")


if __name__ == "__main__":
    # Exemplo de uso
    client = BenchmarkClient()
    
    # Warm-up
    client.warmup(5)
    
    # Executar cenários
    results = []
    results.append(client.run_scenario_simple_user(100))
    results.append(client.run_scenario_user_with_posts(100))
    results.append(client.run_scenario_nested_data(100))
    
    # Salvar resultados
    client.save_results(results)
    
    print("\n✓ Benchmark concluído!")
