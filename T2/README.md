# README

# Problema G* — Kattis Eulerian Path (Caminho Euleriano)

**Disciplina:** T290-09 - Resolução de Problemas com Grafos

**Professor:** Ricardo Kassner Carubbi

## Objetivo

Este repositório contém a modelagem e desenvolvimento da solução para o **Problema G — Kattis Eulerian Path (Caminho Euleriano)**, proposto na disciplina **Resolução de Problemas com Grafos**

## Equipe

|Integrantes | RA |
|------------|----|
|Carlos Andrey Silveira Silva | 2420515 |
|Juliana Martins Ribeiro | 2420516 |
|Pedro Henrique Pinheiro de Oliveira | 2420509 |

## 1. Problema

**Problema G — Kattis Eulerian Path**

**Link oficial:** https://open.kattis.com/problems/eulerianpath.

**Resumo:** Dado um grafo direcionado com `n` vértices e `m` arestas, o objetivo é encontrar um caminho euleriano — um caminho que visita cada aresta do grafo exatamente uma vez. Caso não seja possível construir tal caminho, deve-se indicar que a solução é `impossível`.

## 2. Linguagem e Execução

**Linguagem:** Python 3.x

**Instruções de Execução**:

Para executar o código passando um arquivo de entrada de testes:

  * **Linux / macOS:**
    ```bash
    python3 src/main.py < casos-de-teste.txt
    ```

  * **Windows (PowerShell):**
    ```powershell
    Get-Content casos-de-teste.txt | python src/main.py
    ```

  * **Windows (Prompt de Comando / CMD):**
    ```cmd
    python src/main.py < casos-de-teste.txt
    ```

## 3. Modelagem

O problema é modelado como a busca por um **Caminho Euleriano** em um **Grafo Direcionado (Digrafo)** $G = (V, E)$, onde:
* $V$ representa o conjunto de vértices (índices de $0$ a $V-1$).
* $E$ representa o conjunto de arestas direcionadas $(u, v)$, indicando uma transição orientada do vértice $u$ para o vértice $v$.


## 4. Propriedade Estrutural

Um digrafo $G = (V, E)$ possui um Caminho Euleriano se, e somente se, satisfaz as seguintes condições estruturais:

4.1. **Condição de Graus (In-degree e Out-degree):**
   * **Caminho Euleriano (Aberto):** Existe exatamente um vértice $s$ com $\text{outdegree}(s) - \text{indegree}(s) = 1$ (vértice inicial) e exatamente um vértice $t$ com $\text{indegree}(t) - \text{outdegree}(t) = 1$ (vértice final). Para todos os demais vértices $v$, $\text{outdegree}(v) == \text{indegree}(v)$.
   * **Circuito Euleriano (Fechado):** Para todos os vértices $v$, $\text{outdegree}(v) == \text{indegree}(v)$. Nesses casos, qualquer vértice não isolado pode atuar como ponto de partida.

4.2. **Conectividade das Arestas:**
   * Todas as arestas com grau maior que zero pertencem a uma única componente fortemente/fracamente conectada que pode ser alcançada a partir do vértice inicial $s$.

## 5. Algoritmo

A solução utiliza o **Algoritmo de Hierholzer**, executado em tempo linear $\mathcal{O}(V + E)$:

**5.1. Validação Preliminar de Graus:** Varre os vértices verificando os graus de entrada e saída para identificar o nó de partida $s$ e garantir que as condições de desbalanceamento de graus não sejam violadas.

**5.2. Exploração em Profundidade (DFS com Pilha):** A partir do nó de partida $s$, o algoritmo percorre as arestas utilizando uma pilha (`Stack`). Cada aresta visitada é consumida e removida da lista de adjacências via iteradores locais.

**5.3. Backtracking:** Quando a busca atinge um nó sem arestas de saída disponíveis, o nó é desempilhado e inserido na lista do caminho final. 

**5.4. Reversão e Cobertura:** A lista do caminho é invertida. Se o total de vértices no caminho for exatamente $E + 1$, todas as arestas foram percorridas e o caminho é válido; caso contrário, o grafo possui arestas desconexas e o resultado é considerado impossível (`Impossible`).


## 6. Implementação de Referência

A implementação baseia-se nos módulos do repositório de referência `algs4`:
* `Digraph.java` (Estrutura do digrafo)
* `DirectedEulerianPath.java` (Algoritmo de Hierholzer)
* `Stack.java` (Estrutura de dados auxiliar)

## 7. Alterações e Justificativas

| Módulo de Referência (`algs4`) | Modificação / Adaptação no Python | Justificativa Técnica |
| :--- | :--- | :--- |
| **`Digraph`** | Convertido para classe Python usando listas de adjacência nativas (`list[list]`) e lista de graus (`list[int]`). | Elimina a necessidade da classe `Bag<Integer>` do Java, aproveitando o desempenho nativo das listas dinâmicas no Python. |
| **`Stack`** | Substituído pelo uso de uma lista nativa do Python (`stack = []`) com `.append()` e `.pop()`. | A lista nativa do Python opera como uma pilha LIFO otimizada diretamente na máquina virtual, descartando a criação de uma classe com nós encadeados. |
| **`BreadthFirstDirectedPaths`** | **Omitido/Removido.** | A BFS prévia para checar conectividade exigia um percurso $\mathcal{O}(V+E)$ adicional. A verificação foi unificada no final do Hierholzer checando `len(path) == E + 1` em $\mathcal{O}(1)$, garantindo que nenhuma aresta ficou isolada. |
| **Leitura de Entrada (I/O)** | Uso de `sys.stdin.read().split()`. | Reduz drasticamente o tempo de I/O na plataforma Kattis para lidar com grandes volumes de dados de entrada de uma só vez. |

## 8. Complexidade

* **Complexidade de Tempo:** $\mathcal{O}(V + E)$
  * A verificação de graus consome $\mathcal{O}(V)$.
  * Cada aresta $E$ é visitada e consumida exatamente uma vez pelo iterador no Algoritmo de Hierholzer.
  * A verificação final do tamanho do caminho é feita em $\mathcal{O}(1)$.

* **Complexidade de Espaço:** $\mathcal{O}(V + E)$
  * Guarda as listas de adjacência de tamanho $V + E$.
  * A pilha e a lista do caminho final armazenam até $E + 1$ elementos.

## 9. Casos Especiais

* **Grafo sem arestas ($E = 0$):** O algoritmo trata antecipadamente e encerra a verificação.
* **Grafo com componentes desconexos contendo arestas:** O algoritmo de Hierholzer constrói um caminho parcial. A checagem `len(path) != E + 1` captura essa desconexão e retorna `Impossible`.
* **Vértices isolados (grau 0):** Ignorados na busca, pois não impactam o percurso de arestas.
* **Self-loops e Multigrafos:** Suportados naturalmente pela lista de adjacências e pelo controle de iteradores por aresta.


## 10. Evidência do Accepted

* **Plataforma:** Kattis
* **Problema:** Eulerian Path
* **Linguagem:** Python 3
* **Status:** **Accepted**

<img width="1116" height="162" alt="image" src="https://github.com/user-attachments/assets/f0496a83-e8e0-49fc-9882-c9ea07e0fe83" />

