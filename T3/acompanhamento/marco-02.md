# Marco 2 — Escolha do algoritmo

## 1. Escolha do algoritmo

O problema foi classificado como um problema de **caminho mínimo em grafo direcionado e ponderado**, pois precisamos encontrar a rota de menor custo entre dois vértices específicos: a cidade `1` e a cidade `n`.

Entre os algoritmos estudados, temos:

| Algoritmo | Aplicação | Justificativa |
|---|---|---|
| Kruskal | Árvore geradora mínima | Não se aplica, pois não precisamos conectar todas as cidades. |
| Prim | Árvore geradora mínima | Não se aplica pelo mesmo motivo. |
| Dijkstra | Caminho mínimo | Adequado porque todos os pesos são não negativos. |
| Ford-Fulkerson | Fluxo máximo | Não se aplica, pois não estamos calculando fluxo em uma rede. |
| Edmonds-Karp | Fluxo máximo | Também não se aplica, pois não existe uma demanda de fluxo a maximizar. |

A escolha inicial é o algoritmo de **Dijkstra**, pois os preços dos voos são positivos e queremos minimizar o custo de um caminho entre dois vértices.

Entretanto, existe uma particularidade: o cupom pode ser utilizado em apenas um voo. Portanto, precisamos considerar não apenas a cidade em que estamos, mas também se o cupom já foi utilizado.

## 2. Adaptação: grafo de estados

Para representar essa condição, cada cidade passa a possuir dois estados:

- `(v, 0)`: estamos na cidade `v` e ainda temos o cupom disponível.
- `(v, 1)`: estamos na cidade `v` e já utilizamos o cupom.

Dessa maneira, uma mesma cidade pode representar duas situações diferentes.

### Exemplo

Considere o seguinte voo:

```text
1 --10--> 2
```

Existem duas possibilidades para chegar à cidade 2:

**Sem utilizar o cupom:**

```text
(1, 0) --10--> (2, 0)
```

**Utilizando o cupom:**

```text
(1, 0) --5--> (2, 1)
```

Observe que chegamos à mesma cidade, mas em estados diferentes. No primeiro caso, ainda podemos utilizar o cupom; no segundo, ele já foi utilizado.

### Transições entre os estados

Para cada voo `a → b` de custo `c`, existem três possibilidades:

| Situação | Transição | Custo |
|---|---|---|
| Cupom disponível, sem utilizá-lo | `(a, 0) → (b, 0)` | `c` |
| Cupom disponível, utilizando-o | `(a, 0) → (b, 1)` | `floor(c / 2)` |
| Cupom já utilizado | `(a, 1) → (b, 1)` | `c` |

Não existe transição de `(a, 1)` para `(b, 0)`, pois não podemos recuperar o cupom depois de utilizá-lo.

## 3. Representação da instância

Considere a entrada:

```text
3 4
1 2 3
2 3 1
1 3 7
2 1 5
```

O grafo original possui três cidades e quatro voos:

```text
       3         1
  1 ------> 2 ------> 3
   \                  ^
    \                 |
     ------ 7 --------
```

Agora podemos observar algumas rotas possíveis.

### Rota A: 1 → 3

O voo possui custo 7.

Utilizando o cupom:

```text
floor(7 / 2) = 3
```

Custo total: `3`.

### Rota B: 1 → 2 → 3

Os voos possuem custos 3 e 1.

Sem utilizar o cupom:

```text
3 + 1 = 4
```

Utilizando o cupom no primeiro voo:

```text
floor(3 / 2) + 1
1 + 1 = 2
```

Utilizando o cupom no segundo voo:

```text
3 + floor(1 / 2)
3 + 0 = 3
```

Portanto, a melhor alternativa é utilizar o cupom no primeiro voo, resultando em custo total igual a `2`.

### Resultado esperado

```text
2
```

## 4. Aplicação do Dijkstra

O algoritmo será executado sobre os estados, e não apenas sobre as cidades originais.

Utilizaremos uma estrutura de distâncias:

```text
dist[cidade][cupom]
```

Onde:

- `dist[v][0]`: menor custo conhecido para chegar à cidade `v` sem utilizar o cupom.
- `dist[v][1]`: menor custo conhecido para chegar à cidade `v` após utilizar o cupom.

O estado inicial será:

```text
dist[1][0] = 0
```

Todos os demais estados começam com distância infinita.

O objetivo será encontrar:

```text
dist[n][1]
```

Isso garante que o resultado considere uma rota na qual o cupom foi utilizado exatamente uma vez.

## 5. Complexidade

O grafo original possui:

- `n` vértices;
- `m` arestas.

Com a criação dos dois estados para cada cidade, teremos:

- `2n` vértices;
- `3m` transições.

Cada aresta original gera até três transições no grafo de estados.

Utilizando Dijkstra com fila de prioridade, temos:

**Complexidade de tempo:**

```text
O((2n + 3m) log(2n))
```

Desconsiderando constantes:

```text
O((n + m) log n)
```

**Complexidade de espaço:**

```text
O(n + m)
```

Isso ocorre porque precisamos armazenar o grafo de estados, as distâncias e a fila de prioridade.

Considerando as restrições:

- `n ≤ 100.000`
- `m ≤ 200.000`

O grafo de estados terá até 200.000 vértices e 600.000 transições, mantendo uma complexidade adequada para os limites apresentados.

## 6. Conclusão

A solução escolhida utiliza **Dijkstra com uma adaptação baseada em grafo de estados**.

Essa adaptação permite representar as duas situações possíveis para cada cidade: cupom disponível ou cupom utilizado.

Como todos os pesos continuam sendo não negativos, Dijkstra permanece adequado para encontrar o menor caminho.

A complexidade final é `O((n + m) log n)` em tempo e `O(n + m)` em espaço.