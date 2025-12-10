# Experimento: GraphQL vs REST

Este projeto implementa um experimento controlado para comparar o desempenho entre APIs GraphQL e REST em termos de **tempo de resposta** e **tamanho do payload**.

## 📋 Estrutura do Projeto

```
trab-5-/
├── data.py                    # Base de dados simulada
├── rest_server.py             # Servidor REST (Flask)
├── graphql_server.py          # Servidor GraphQL (Graphene + Flask)
├── benchmark_client.py        # Cliente para medições de performance
├── statistical_analysis.py    # Análise estatística dos resultados
├── run_experiment.py          # Script principal para executar o experimento
├── requirements.txt           # Dependências Python
└── README.md                  # Este arquivo
```

## 🚀 Instalação

1. **Clone o repositório:**
```bash
git clone <repo-url>
cd trab-5-
```

2. **Crie um ambiente virtual (recomendado):**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

## 📊 Execução do Experimento

### Opção 1: Execução Automática (Recomendado)

Execute o script principal que gerencia todo o processo:

```bash
python run_experiment.py
```

Este script irá:
1. Iniciar os servidores REST e GraphQL
2. Executar os benchmarks (100 repetições por cenário)
3. Realizar a análise estatística
4. Gerar gráficos e relatórios

### Opção 2: Execução Manual

#### Passo 1: Iniciar os Servidores

Em terminais separados:

```bash
# Terminal 1 - Servidor REST
python rest_server.py

# Terminal 2 - Servidor GraphQL
python graphql_server.py
```

#### Passo 2: Executar Benchmark

```bash
python benchmark_client.py
```

#### Passo 3: Analisar Resultados

```bash
python statistical_analysis.py
```

## 🎯 Cenários de Teste

### Cenário 1: Busca Simples
- **REST**: Retorna usuário completo com todos os campos
- **GraphQL**: Solicita apenas nome e email
- **Objetivo**: Medir overhead de dados desnecessários

### Cenário 2: Busca Complexa
- **REST**: Retorna usuário com posts completos e comentários
- **GraphQL**: Solicita apenas nome, email e títulos de 5 posts
- **Objetivo**: Avaliar eficiência em queries relacionais

### Cenário 3: Busca Aninhada
- **REST**: Retorna estrutura completa (usuário + posts + comentários)
- **GraphQL**: Solicita estrutura específica com limites
- **Objetivo**: Testar performance em dados aninhados

## 📈 Resultados

Após a execução, os seguintes arquivos são gerados:

- **`results.json`**: Dados brutos das medições
- **`analysis_results.png`**: Gráficos comparativos
- **`summary_results.csv`**: Tabela resumo com estatísticas

## 🔬 Metodologia

### Hipóteses

**RQ1 - Tempo de Resposta:**
- H0: μ_GraphQL ≥ μ_REST
- H1: μ_GraphQL < μ_REST

**RQ2 - Tamanho da Resposta:**
- H0: μ_GraphQL ≥ μ_REST
- H1: μ_GraphQL < μ_REST

### Variáveis

**Dependentes:**
- Tempo de resposta (ms)
- Tamanho da resposta (bytes)

**Independentes:**
- Tipo de API (REST vs GraphQL)
- Complexidade da consulta

### Design Experimental

- **Tipo**: Randomized Paired Design
- **Repetições**: 100 por tratamento/cenário
- **Warm-up**: 5 requisições iniciais descartadas
- **Ambiente**: localhost (elimina variação de rede)

### Análise Estatística

- Teste t pareado (paired t-test)
- Nível de significância: α = 0.05
- Estatísticas descritivas (média, mediana, desvio padrão)

## 🛠️ Tecnologias Utilizadas

- **Python 3.11+**
- **Flask**: Framework web
- **Graphene**: Implementação GraphQL
- **Requests**: Cliente HTTP
- **SciPy**: Testes estatísticos
- **NumPy**: Cálculos numéricos
- **Pandas**: Manipulação de dados
- **Matplotlib**: Visualizações

## 📝 Endpoints

### REST API (porta 5000)

- `GET /api/users/{id}` - Buscar usuário
- `GET /api/users/{id}/posts` - Posts do usuário
- `GET /api/posts/{id}/comments` - Comentários do post
- `GET /api/users/{id}/full` - Usuário com posts e comentários

### GraphQL API (porta 5001)

Endpoint único: `POST /graphql`

**Exemplo de query:**
```graphql
{
  user(id: 1) {
    name
    email
    posts(limit: 5) {
      title
      comments(limit: 3) {
        author
        text
      }
    }
  }
}
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📄 Licença

Este projeto é parte de um trabalho acadêmico.

## 👥 Autores

- Bruno Evangelista

## 📚 Referências

- [GraphQL Specification](https://graphql.org/)
- [REST API Best Practices](https://restfulapi.net/)
- [Statistical Testing in Python](https://docs.scipy.org/doc/scipy/reference/stats.html)
