# Planejamento Experimental: GraphQL vs REST

## A. Hipóteses Nula e Alternativa
Para avaliar as perguntas de pesquisa, foram definidas as seguintes hipóteses para o **Tempo de Resposta (RQ1)** e **Tamanho da Resposta (RQ2)**:

### RQ1: Tempo de Resposta ($\mu$)
* **$H0_{tempo}$ (Nula):** $\mu_{GraphQL} \geq \mu_{REST}$
    * O tempo de resposta das consultas GraphQL é maior ou igual ao das consultas REST.
* **$H1_{tempo}$ (Alternativa):** $\mu_{GraphQL} < \mu_{REST}$
    * O tempo de resposta das consultas GraphQL é significativamente menor que o das consultas REST.

### RQ2: Tamanho da Resposta ($\mu$)
* **$H0_{tamanho}$ (Nula):** $\mu_{GraphQL} \geq \mu_{REST}$
    * O tamanho do payload das respostas GraphQL é maior ou igual ao das respostas REST.
* **$H1_{tamanho}$ (Alternativa):** $\mu_{GraphQL} < \mu_{REST}$
    * O tamanho do payload das respostas GraphQL é significativamente menor que o das respostas REST (devido à redução de dados desnecessários).

---

## B. Variáveis Dependentes
Variáveis observadas para medir o efeito dos tratamentos:

1.  **Tempo de Resposta (Response Time):** Medido em milissegundos (ms). Refere-se ao tempo total decorrido entre o envio da requisição pelo cliente e o recebimento completo da resposta.
2.  **Tamanho da Resposta (Response Size):** Medido em Bytes. Refere-se ao tamanho exato do corpo (*body*) da resposta JSON recebida.

## C. Variáveis Independentes
Variáveis manipuladas para controlar o experimento:

* **Tipo de API (Tecnologia):** Níveis `{REST, GraphQL}`.
* **Complexidade da Consulta:** Cenários de teste definidos para simular diferentes cargas de dados (ex: busca simples de um recurso vs. busca aninhada com relacionamentos).

## D. Tratamentos
Os tratamentos aplicados consistem na execução das tarefas de busca de dados utilizando as diferentes tecnologias:

* **Tratamento 1 (REST):** Requisição HTTP GET a um endpoint RESTful padrão, retornando a representação completa do recurso.
* **Tratamento 2 (GraphQL):** Requisição HTTP POST contendo uma query GraphQL específica, solicitando apenas os campos estritamente necessários para o cenário.



## E. Objetos Experimentais
Os objetos experimentais são as missões de consulta (*queries*) executadas sobre a base de dados.
> **Exemplo:** Recuperar o "nome" e "email" de um usuário específico e os "títulos" de seus 5 últimos posts.

---

## F. Tipo de Projeto Experimental
* **Fator:** Unifatorial (Fator Principal: Tecnologia da API).
* **Design:** *Randomized Paired Design* (Design Emparelhado). Cada missão de consulta é executada tanto em REST quanto em GraphQL sob as mesmas condições de rede e hardware, permitindo a comparação direta das diferenças (*delta*) entre os pares.

## G. Quantidade de Medições
Para garantir significância estatística e diluir *outliers*:

* **Tamanho da Amostra:** 100 repetições para cada tratamento em cada cenário.
* **Total de Observações:** 200 medições por cenário (100 REST + 100 GraphQL).

## H. Ameaças à Validade
As seguintes ameaças foram identificadas e mitigadas:

* **Latência de Rede (Validade Interna):** Oscilações na conexão de internet podem introduzir ruído nos dados de tempo.
    * *Mitigação:* Execução do Cliente e Servidor em ambiente local (`localhost`) para isolar o teste de variáveis de rede externa.
* **Cold Start (Validade Interna):** A primeira requisição a uma API geralmente é mais lenta devido à inicialização de processos/caches.
    * *Mitigação:* Implementação de rotina de *Warm-up* (aquecimento), onde as 5 primeiras requisições de cada tipo são descartadas antes do início da medição.
* **Interferência de Processos (Validade de Construto):** Outros processos rodando na máquina hospedeira podem consumir CPU/RAM.
    * *Mitigação:* Execução em ambiente controlado, evitando o uso de outros softwares pesados durante o experimento.