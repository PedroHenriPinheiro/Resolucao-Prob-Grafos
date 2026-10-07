# Marco 4 — Implementação final e conclusão

## 1. Reutilização e Modificação das Estruturas de Referência `(algs4)`

A solução foi desenvolvida em Python, traduzindo os conceitos originais do repositório algs4 (Java) e aplicando adaptações orientadas na plataforma Kattis.

## 1.1. `Digraph`

**Status no Projeto:** Reutilizado e Adaptado.

**Justificativa e Adaptações:** Implementado como classe nativa em Python. Substituiu-se a coleção `Bag<Integer>[]` por listas nativas do Python `(list[list])` e o array fixo de graus de entrada por `list[int]` para eliminar overhead e otimizar acessos à memória.

## 1.2. `DirectedEulerianPath`

**Status no Projeto:** Reutilizado e Adaptado.

**Justificativa e Adaptações:** Implementa o Algoritmo de Hierholzer `O(V + E)`. Utilizou-se geradores iterativos `(iter())` para garantir o consumo de cada aresta em tempo constante `O(1)`.

## 1.3. `Stack`

**Status no Projeto:** Substituído (Nativo)

**Justificativa e Adaptações:** Em vez de instanciar uma classe `Stack` com nós encadeados, utilizou-se a lista nativa do Python `(stack = [])` aproveitando os métodos `.append()` e `.pop()`.

## 1.4. `BreadthFirstDirectedPaths`

**Status no Projeto:** Omitido / Otimizado

**Justificativa e Adaptações:** A verificação prévia de conectividade por `BFS` foi desestimada por redundância. A validação de alcance de todas as arestas foi transferida para a verificação do tamanho final do caminho `(len(self._path) != digraph.E + 1)` em `O(1)` no término da reconstrução por DFS/Hierholzer.

## 2. Análise do Algoritmo e Critério Estrutural (DFS vs BFS)

A solução utiliza uma Busca em Profundidade (DFS) modificada acoplada a uma pilha para costurar subciclos através do `Algoritmo de Hierholzer`.

**Por que não utilizar BFS?** A BFS explora o grafo em largura (camadas por Fila/Queue), sendo inadequada para compor sequencialmente os circuitos eulerianos. A verificação de conectividade por BFS antes da DFS exigiria uma varredura duplicada sobre o grafo (`O(V+E)` adicional). 

## 3. Resultados dos Testes Executados e Evidência de Accepted

## 3.1. Casos de Teste

**Exemplo de Caso de Teste:**

```text
4 4
0 1
1 2
1 3
2 3
2 2
0 1
1 0
2 1
0 1
0 0
```

**Saída Esperada:**

```text
Impossible
0 1 0
0 1
```

## 3.2. Accepted

**Plataforma:** Kattis

**Problema:** Eulerian Path

**Resultado:** `Accepted`

**Linguagem:** Python 3

**Tempo de Execução / Desempenho:** Aprovado em todos os casos de teste utilizando a leitura otimizada `sys.stdin.read().split()`

<img width="1116" height="162" alt="image" src="https://github.com/user-attachments/assets/f0496a83-e8e0-49fc-9882-c9ea07e0fe83" />
