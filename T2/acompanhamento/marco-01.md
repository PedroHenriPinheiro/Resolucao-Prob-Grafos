# Marco 1 — Problema e conhecimento prévio

## 1. Descrição do problema

O problema consiste em determinar se um grafo possui um **caminho euleriano** e, caso possua, apresentar uma sequência de vértices que represente esse caminho.

Um caminho euleriano é um caminho que percorre **todas as arestas do grafo exatamente uma vez**. Os vértices podem ser visitados mais de uma vez, desde que nenhuma aresta seja utilizada novamente.

O programa recebe diversos casos de teste. Para cada caso, deve analisar o grafo e encontrar um caminho euleriano quando ele existir.

A entrada é encerrada pela linha:

```text
0 0
```

Essa linha não representa um caso de teste e não deve ser processada.

---

## 2. Entrada

Cada caso de teste começa com dois inteiros `n` e `m`:

* `n` representa a quantidade de vértices do grafo;
* `m` representa a quantidade de arestas.

Os vértices são numerados de `0` até `n - 1`.

Em seguida, são fornecidas `m` linhas contendo dois inteiros `u` e `v`, representando uma aresta entre os vértices `u` e `v`.

Por exemplo:

```text
4 4
0 1
1 2
1 3
2 3
```

representa um grafo com quatro vértices e quatro arestas.

---

## 3. Saída

Para cada caso de teste:

* caso exista um caminho euleriano, deve ser apresentada uma sequência de vértices que representa esse caminho;
* caso não exista, deve ser apresentada a palavra:

```text
Impossible
```

Quando existem vários caminhos eulerianos possíveis, qualquer um deles é considerado uma resposta válida.

---

## 4. Restrições e características da entrada

A entrada possui as seguintes características importantes:

* podem existir vários casos de teste;
* `n` e `m` são inteiros não negativos;
* os vértices são numerados de `0` a `n - 1`;
* cada aresta é informada por um par de vértices;
* o processamento termina quando `n = 0` e `m = 0`;
* o grafo pode possuir mais de um caminho euleriano;
* quando não existe caminho euleriano, a saída deve ser `Impossible`.

O principal requisito algorítmico é verificar a possibilidade de utilizar **todas as arestas exatamente uma vez**.

---

# 5. Modelagem do problema

## Vértices

Cada vértice representa um nó do grafo.

Os vértices são identificados pelos números:

```text
0, 1, 2, ..., n - 1
```

Não existe uma função especial associada a um determinado vértice. Diferentemente de um problema com árvore enraizada, não há necessariamente um vértice raiz.

---

## Arestas

Cada par `(u, v)` representa uma aresta conectando os vértices `u` e `v`.

O objetivo é encontrar uma sequência de vértices na qual cada aresta do grafo seja utilizada exatamente uma vez.

Por exemplo:

```text
0 → 1 → 2 → 3
```

utiliza as arestas:

```text
(0,1), (1,2), (2,3)
```

sem repetir nenhuma delas.

---

# 6. Classificação do grafo

O problema trabalha com um **grafo não direcionado**.

Isso pode ser observado porque uma aresta informada como:

```text
0 1
```

representa uma conexão entre os vértices `0` e `1`, e não necessariamente uma direção de `0` para `1`.

O grafo pode ser representado por uma **lista de adjacência**, pois cada vértice precisa manter as arestas que podem ser utilizadas durante a construção do caminho.

Uma característica importante é que o grafo **não é necessariamente uma árvore**.

Uma árvore possui exatamente `n - 1` arestas e não possui ciclos. Já neste problema podem existir ciclos e uma quantidade arbitrária de arestas de acordo com a entrada.

---

# 7. Conhecimento prévio: Caminho Euleriano

Para determinar se existe um caminho euleriano em um grafo não direcionado, é necessário analisar principalmente o **grau dos vértices** e a conectividade das partes que possuem arestas.

O grau de um vértice corresponde à quantidade de arestas incidentes nele.

Para um grafo conectado considerando apenas os vértices que possuem arestas:

* se **0 vértices possuem grau ímpar**, existe um circuito euleriano e, portanto, também é possível obter um caminho euleriano;
* se **2 vértices possuem grau ímpar**, existe um caminho euleriano que começa em um desses vértices e termina no outro;
* se houver **mais de 2 vértices de grau ímpar**, não existe caminho euleriano.

Assim, a quantidade de vértices com grau ímpar é uma das principais condições utilizadas para determinar a existência da solução.

Além disso, as arestas que serão utilizadas precisam pertencer à mesma componente conexa do grafo.

---

# 8. Participação da DFS/BFS

A DFS ou a BFS pode ser utilizada para verificar a **conectividade** do grafo.

A ideia é escolher um vértice que possua pelo menos uma aresta e realizar uma busca a partir dele.

Por exemplo, utilizando DFS:

```text
DFS(v)
    marca v como visitado
    para cada vizinho de v
        se ainda não foi visitado
            DFS(vizinho)
```

Ao final, podemos verificar se todos os vértices que possuem arestas foram alcançados.

Entretanto, a DFS/BFS sozinha não resolve o problema, pois uma busca comum pode visitar uma mesma aresta várias vezes e não garante que todas as arestas sejam utilizadas exatamente uma vez.

Portanto, a busca é utilizada como parte da análise, principalmente para verificar a conectividade. A construção efetiva do caminho euleriano exige também o controle das arestas já utilizadas.

---

# 9. Instância pequena

Considere o seguinte caso:

```text
3 3
0 1
1 2
2 0
```

O grafo pode ser representado por:

```text
      0
     / \
    1---2
```

Os graus são:

```text
grau(0) = 2
grau(1) = 2
grau(2) = 2
```

Todos os vértices possuem grau par.

Portanto, existe um circuito euleriano.

Uma possível resposta é:

```text
0 1 2 0
```

O caminho utiliza todas as três arestas exatamente uma vez:

```text
0 → 1
1 → 2
2 → 0
```

Logo, o resultado é válido.

---

# 10. Exemplo de instância sem solução

Considere:

```text
4 4
0 1
1 2
1 3
2 3
```

Representação:

```text
    0
    |
    1
   / \
  2 - 3
```

Os graus são:

```text
grau(0) = 1
grau(1) = 3
grau(2) = 1
grau(3) = 1
```

Existem quatro vértices de grau ímpar.

Como um grafo não direcionado precisa possuir exatamente `0` ou `2` vértices de grau ímpar para possuir um caminho euleriano, esse grafo não possui solução.

Resultado:

```text
Impossible
```

---

# 11. Resultado de aprendizagem aferido

O problema permite aplicar os conceitos estudados sobre:

* representação de grafos;
* grau de vértices;
* conectividade;
* caminhos;
* ciclos;
* busca em profundidade (DFS);
* busca em largura (BFS);
* caminhos eulerianos;
* construção de percursos utilizando as arestas do grafo.

O principal conhecimento avaliado é a capacidade de identificar as condições necessárias para a existência de um caminho euleriano e utilizar uma estratégia de busca para construir esse caminho quando ele existir.

---

# 12. Hipótese inicial da solução

A hipótese inicial é utilizar uma representação do grafo por lista de adjacência, calcular o grau de cada vértice e verificar a quantidade de vértices de grau ímpar.

Em seguida, deve-se verificar se todas as arestas pertencem à mesma componente conexa.

Caso as condições para a existência de um caminho euleriano sejam satisfeitas, será utilizado um algoritmo baseado em DFS...


```text
Impossible
```
