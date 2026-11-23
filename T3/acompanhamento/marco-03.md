# Marco 3 — Rastreamento manual

Este marco rastreia a execução do Dijkstra do algs4 (`DijkstraSP`) sobre a instância pequena definida no Marco 2 (n = 3 cidades, m = 4 voos, um cupom de 50%).

---

## 1. Mapeamento dos estados para o algs4

No Marco 2, cada cidade `v` passou a ter dois estados: `(v, 0)` (cupom disponível) e `(v, 1)` (cupom já utilizado).

A classe `EdgeWeightedDigraph` do algs4 identifica os vértices por inteiros sequenciais de `0` a `2n - 1`. Por isso, cada estado `(v, cupom)` recebe um índice único:

- Estado `(v, 0)`: índice `v - 1`
- Estado `(v, 1)`: índice `(v - 1) + n`

Para n = 3, o grafo tem 2n = 6 vértices:

| Estado | Significado | Índice no algs4 |
|:------:|-------------|:---------------:|
| (1, 0) | Cidade 1 com cupom disponível (**origem**) | 0 |
| (2, 0) | Cidade 2 com cupom disponível | 1 |
| (3, 0) | Cidade 3 com cupom disponível | 2 |
| (1, 1) | Cidade 1 com cupom utilizado | 3 |
| (2, 1) | Cidade 2 com cupom utilizado | 4 |
| (3, 1) | Cidade 3 com cupom utilizado (**destino**) | 5 |

### Transições criadas no `EdgeWeightedDigraph`

Para cada voo `a → b` de custo `c`, são inseridos três objetos `DirectedEdge`:

- `(a, 0) → (b, 0)` com custo `c`
- `(a, 1) → (b, 1)` com custo `c`
- `(a, 0) → (b, 1)` com custo `floor(c / 2)` (uso do cupom)

Com a entrada do Marco 2 (n = 3, m = 4), são geradas 3m = 12 arestas direcionadas:

```text
Voo 1 → 2 (custo 3):
  0 → 1  (peso 3)   |  (1, 0) → (2, 0)
  3 → 4  (peso 3)   |  (1, 1) → (2, 1)
  0 → 4  (peso 1)   |  (1, 0) → (2, 1) [cupom]

Voo 2 → 3 (custo 1):
  1 → 2  (peso 1)   |  (2, 0) → (3, 0)
  4 → 5  (peso 1)   |  (2, 1) → (3, 1)
  1 → 5  (peso 0)   |  (2, 0) → (3, 1) [cupom]

Voo 1 → 3 (custo 7):
  0 → 2  (peso 7)   |  (1, 0) → (3, 0)
  3 → 5  (peso 7)   |  (1, 1) → (3, 1)
  0 → 5  (peso 3)   |  (1, 0) → (3, 1) [cupom]

Voo 2 → 1 (custo 5):
  1 → 0  (peso 5)   |  (2, 0) → (1, 0)
  4 → 3  (peso 5)   |  (2, 1) → (1, 1)
  1 → 3  (peso 2)   |  (2, 0) → (1, 1) [cupom]
```

---

## 2. Alterações identificadas na implementação de referência (Python)

Durante o rastreamento, o código de `algs4-py` foi lido linha a linha para que as estruturas reproduzissem o comportamento real. Foram identificados cinco pontos que precisam ser corrigidos na adaptação (a integração e os testes de execução ficam no Marco 4):

| Arquivo | Alteração | Justificativa |
|---------|-----------|---------------|
| `dijkstra_sp.py` | `POSITIVE_INFINITY = 999999.0` substituído por `float("inf")` | Cada voo pode custar até 10⁹, acima do limite fixo de 999999.0. |
| `index_min_pq.py` | `contains(i)` alterado de `i in self.keys` para `self.qp[i] != -1` | `keys` guarda distâncias, não índices de vértices, e não é limpo em `del_min`. Usar `qp` evita falsos positivos e reduz a consulta de O(V) para O(1). |
| `index_min_pq.py` | Atualização de `qp` a cada troca em `swim()` e `sink()` | O código original troca elementos em `pq` sem atualizar o vetor inverso `qp`, invalidando chamadas futuras de `change()`. |
| `index_min_pq.py` | Atualização de `qp` do elemento levado à raiz em `del_min()` | Se esse elemento não afundar, seu `qp` continua apontando para a posição antiga (o fim do heap). Um `change()` posterior acessa uma posição inexistente e gera `IndexError`. |
| `index_min_pq.py` | `self.pq = self.pq[:-1]` substituído por `self.pq.pop()` | O fatiamento copia a lista inteira a cada remoção (O(V) por `del_min`), tornando o algoritmo O(V²) no pior caso. `pop()` remove o último elemento em O(1). |

---

## 3. Estruturas de dados e estados iniciais

Ao executar `DijkstraSP(g, 0)`:

- **`g` (`EdgeWeightedDigraph`)**: `g.V = 6` vértices e `g.E = 12` arestas, em listas de adjacência `g.adj[0..5]` do tipo `Bag`.
- **`distTo`**: lista de tamanho 6 com o menor custo acumulado conhecido a partir do índice 0, `(1, 0)`.
- **`edgeTo`**: lista de tamanho 6 com a última `DirectedEdge` usada para chegar a cada índice.
- **`pq` (`IndexMinPQ`)**: heap binário mínimo indexado. Na versão Python ele usa três listas: `pq` (heap com índices de vértices, raiz na posição 0), `qp` (posição de cada vértice no heap, `-1` se fora) e `keys` (prioridade, isto é, a distância).

### Ordem das listas de adjacência

O `Bag` do algs4 insere cada item no **início** de uma lista encadeada (`add` cria um novo `Node` apontando para o antigo `first`). Por isso, `for e in g.adj[v]` percorre as arestas na **ordem inversa à de inserção**. Com as arestas inseridas na ordem da seção 1, as listas ficam:

| Índice | Estado | `g.adj[v]` (ordem de iteração) |
|:------:|:------:|--------------------------------|
| 0 | (1, 0) | 0→5 (3), 0→2 (7), 0→4 (1), 0→1 (3) |
| 1 | (2, 0) | 1→3 (2), 1→0 (5), 1→5 (0), 1→2 (1) |
| 2 | (3, 0) | vazia |
| 3 | (1, 1) | 3→5 (7), 3→4 (3) |
| 4 | (2, 1) | 4→3 (5), 4→5 (1) |
| 5 | (3, 1) | vazia |

### Estado inicial (antes do laço `while`)

```text
Índices:   0      1      2      3      4      5
Estados: (1,0)  (2,0)  (3,0)  (1,1)  (2,1)  (3,1)
--------------------------------------------------
distTo:  [  0 ,  inf ,  inf ,  inf ,  inf ,  inf ]
edgeTo:  [None, None , None , None , None , None ]
pq.pq:   [  0  ]
```

---

## 4. Rastreamento passo a passo

O laço `while not self.pq.is_empty()` remove `v = pq.del_min()` (menor `distTo`) e relaxa as arestas de `g.adj[v]` na ordem da tabela acima. `pq.pq` é mostrado da raiz (posição 0) ao fim.

O rastreamento foi conferido executando a implementação de referência, com as correções da seção 2, sobre esta mesma instância.

### Iteração 1 — remove índice 0 | estado (1, 0) | custo 0

- `0 → 5` (peso 3): 0 + 3 < inf → `distTo[5] = 3`, `edgeTo[5] = 0→5`, `pq.insert(5, 3)` → `[5]`
- `0 → 2` (peso 7): 0 + 7 < inf → `distTo[2] = 7`, `edgeTo[2] = 0→2`, `pq.insert(2, 7)` → `[5, 2]`
- `0 → 4` (peso 1): 0 + 1 < inf → `distTo[4] = 1`, `edgeTo[4] = 0→4`, `pq.insert(4, 1)`. O 4 sobe para a raiz → `[4, 2, 5]`
- `0 → 1` (peso 3): 0 + 3 < inf → `distTo[1] = 3`, `edgeTo[1] = 0→1`, `pq.insert(1, 3)`. O 1 troca com o pai 2 (custo 7) e para abaixo do 4 → `[4, 1, 5, 2]`

```text
distTo:  [  0 ,   3  ,   7  ,  inf ,   1  ,   3  ]
edgeTo:  [None,  0→1 ,  0→2 , None ,  0→4 ,  0→5 ]
pq.pq:   [  4 ,   1  ,   5  ,   2  ]
```

### Iteração 2 — remove índice 4 | estado (2, 1) | custo 1

`del_min` troca a raiz (4) com o último (2) e remove o 4. O 2 (custo 7) afunda trocando com o filho de menor custo, 1 (custo 3; empate com 5 favorece o filho da esquerda). Heap: `[1, 2, 5]`.

- `4 → 3` (peso 5): 1 + 5 = 6 < inf → `distTo[3] = 6`, `edgeTo[3] = 4→3`, `pq.insert(3, 6)` → `[1, 3, 5, 2]` (3 troca com o pai 2, de custo 7)
- `4 → 5` (peso 1): 1 + 1 = 2 < 3 → `distTo[5] = 2`, `edgeTo[5] = 4→5`, `pq.change(5, 2)`. O 5 sobe para a raiz → `[5, 3, 1, 2]`

```text
distTo:  [  0 ,   3  ,   7  ,   6  ,   1  ,   2  ]
edgeTo:  [None,  0→1 ,  0→2 ,  4→3 ,  0→4 ,  4→5 ]
pq.pq:   [  5 ,   3  ,   1  ,   2  ]
```

### Iteração 3 — remove índice 5 | estado (3, 1) | custo 2

- `del_min` leva o 2 (custo 7) para a raiz; ele afunda trocando com o filho de menor custo, 1 (custo 3).
- `g.adj[5]` está vazia (não há voos saindo da cidade 3).

```text
distTo:  [  0 ,   3  ,   7  ,   6  ,   1  ,   2  ]
edgeTo:  [None,  0→1 ,  0→2 ,  4→3 ,  0→4 ,  4→5 ]
pq.pq:   [  1 ,   3  ,   2  ]
```

### Iteração 4 — remove índice 1 | estado (2, 0) | custo 3

`del_min` leva o 2 (custo 7) para a raiz; ele afunda trocando com 3 (custo 6). Heap: `[3, 2]`.

- `1 → 3` (peso 2): 3 + 2 = 5 < 6 → `distTo[3] = 5`, `edgeTo[3] = 1→3`, `pq.change(3, 5)` (3 já está na raiz) → `[3, 2]`
- `1 → 0` (peso 5): 3 + 5 = 8, não melhora `distTo[0] = 0` → ignora
- `1 → 5` (peso 0): 3 + 0 = 3, não melhora `distTo[5] = 2` → ignora
- `1 → 2` (peso 1): 3 + 1 = 4 < 7 → `distTo[2] = 4`, `edgeTo[2] = 1→2`, `pq.change(2, 4)`. O 2 sobe para a raiz → `[2, 3]`

```text
distTo:  [  0 ,   3  ,   4  ,   5  ,   1  ,   2  ]
edgeTo:  [None,  0→1 ,  1→2 ,  1→3 ,  0→4 ,  4→5 ]
pq.pq:   [  2 ,   3  ]
```

### Iteração 5 — remove índice 2 | estado (3, 0) | custo 4

- `g.adj[2]` está vazia (não há voos saindo da cidade 3).

```text
distTo:  [  0 ,   3  ,   4  ,   5  ,   1  ,   2  ]
edgeTo:  [None,  0→1 ,  1→2 ,  1→3 ,  0→4 ,  4→5 ]
pq.pq:   [  3  ]
```

### Iteração 6 — remove índice 3 | estado (1, 1) | custo 5

- `3 → 5` (peso 7): 5 + 7 = 12, não melhora `distTo[5] = 2` → ignora
- `3 → 4` (peso 3): 5 + 3 = 8, não melhora `distTo[4] = 1` → ignora

```text
distTo:  [  0 ,   3  ,   4  ,   5  ,   1  ,   2  ]
edgeTo:  [None,  0→1 ,  1→2 ,  1→3 ,  0→4 ,  4→5 ]
pq.pq:   [ ]   (fila vazia — fim do laço)
```

### Resumo das iterações

| Iteração | Vértice removido | Estado | `distTo[0..5]` | `pq.pq` ao final |
|:--------:|:----------------:|:------:|----------------|------------------|
| Início | — | — | [0, inf, inf, inf, inf, inf] | [0] |
| 1 | 0 | (1, 0) | [0, 3, 7, inf, 1, 3] | [4, 1, 5, 2] |
| 2 | 4 | (2, 1) | [0, 3, 7, 6, 1, 2] | [5, 3, 1, 2] |
| 3 | 5 | (3, 1) | [0, 3, 7, 6, 1, 2] | [1, 3, 2] |
| 4 | 1 | (2, 0) | [0, 3, 4, 5, 1, 2] | [2, 3] |
| 5 | 2 | (3, 0) | [0, 3, 4, 5, 1, 2] | [3] |
| 6 | 3 | (1, 1) | [0, 3, 4, 5, 1, 2] | [] |

A ordem de remoção (0, 4, 5, 1, 2, 3) segue sempre custo não decrescente (0, 1, 2, 3, 4, 5), como o Dijkstra garante.

---

## 5. Justificativa das decisões e resultado

### Por que as decisões garantem o caminho mínimo

A cada passo, a `IndexMinPQ` entrega o estado `(v, cupom)` com menor custo acumulado. Como todos os pesos são não negativos (`c ≥ 1` e `floor(c / 2) ≥ 0`), nenhum caminho que passe por vértices ainda na fila consegue produzir custo menor para um estado já removido.

Na Iteração 1, o algoritmo encontrou o voo direto 1 → 3 com cupom (`0 → 5`), registrando custo 3 para o destino `(3, 1)`. Mas o estado `(2, 1)` (índice 4) tinha custo menor (1) e foi expandido antes, na Iteração 2. Ali foi descoberta a transição `4 → 5` de peso 1, que reduziu o custo do destino para 2.

O destino é removido da fila na Iteração 3, com custo 2. A partir daí, seu valor não muda mais: todos os estados restantes na fila já custam pelo menos 3.

### Reconstrução do caminho e resultado

O destino é `(3, 1)`, índice `2n - 1 = 5`. `distTo[5] = 2`.

Seguindo `edgeTo` de trás para frente a partir do índice 5:

```text
edgeTo[5] = 4 → 5   (voo 2 → 3 sem cupom, custo 1)
edgeTo[4] = 0 → 4   (voo 1 → 2 com cupom, custo floor(3 / 2) = 1)
```

Caminho ótimo:

```text
(1, 0) --[cupom: 1]--> (2, 1) --[normal: 1]--> (3, 1)
```

**Resultado final: 2**, igual à saída esperada definida no Marco 2.

---

## 6. Explicação individual de uma etapa no código algs4

Cada etapa abaixo detalha uma parte diferente do código.

### 6.1 `relax`

Etapa escolhida: o método `relax(self, g, v)` da classe `DijkstraSP` (`dijkstra_sp.py`).

```python
def relax(self, g, v):
    for e in g.adj[v]:
        w = e.To()
        if self.distTo[w] > self.distTo[v] + e.weight:
            self.distTo[w] = self.distTo[v] + e.weight
            self.edgeTo[w] = e
            if self.pq.contains(w):
                self.pq.change(w, self.distTo[w])
            else:
                self.pq.insert(w, self.distTo[w])
```

- **`for e in g.adj[v]:` e `w = e.To()`**
  Percorre todas as `DirectedEdge` da `Bag` do vértice `v` recém-removido da fila e obtém o destino `w`. No grafo de estados, esse laço avalia ao mesmo tempo os voos comuns (que mantêm o nível de cupom) e o uso do cupom (salto de `(a, 0)` para `(b, 1)`).

- **`if self.distTo[w] > self.distTo[v] + e.weight:`**
  Condição de relaxamento: testa se chegar a `w` passando por `v` pela aresta `e` custa estritamente menos que a melhor distância já registrada para `w`.

- **`self.distTo[w] = ...` e `self.edgeTo[w] = e`**
  Se o caminho novo é mais barato, atualiza o custo acumulado até `w` e registra `e` como aresta predecessora na árvore de caminhos mínimos (SPT).

- **`if self.pq.contains(w): self.pq.change(...) else: self.pq.insert(...)`**
  Mantém a `IndexMinPQ` sincronizada com `distTo`:
  - Se `w` já está na fila, `pq.change` atualiza sua prioridade e reorganiza o heap em O(log V). Isso ocorreu na Iteração 2, quando `distTo[5]` caiu de 3 para 2, e na Iteração 4, com os índices 3 e 2.
  - Senão, `w` foi descoberto agora e entra no heap com `pq.insert`. Isso ocorreu na Iteração 1 para os índices 5, 2, 4 e 1, e na Iteração 2 para o índice 3.

  Esse trecho depende das correções da seção 2: `contains` precisa consultar `qp` e `swim`/`sink` precisam manter `qp` atualizado para que `change` encontre `w` na posição certa do heap.

### 6.2 `del_min` e `sink`

Arquivo `index_min_pq.py`, já com as correções da seção 2:

```python
def del_min(self):
    m = self.pq[0]
    last = self.pq.pop()
    if self.pq:
        self.pq[0] = last
        self.qp[last] = 0
        self.sink(0)
    self.qp[m] = -1
    return m
```

- **`m = self.pq[0]`**: a raiz do heap guarda o vértice com menor `distTo`. É ele que o Dijkstra vai fixar nesta iteração.
- **`last = self.pq.pop()`**: retira o último elemento em O(1). O código original usava `self.pq[:-1]`, que copiava a lista inteira a cada remoção.
- **`self.pq[0] = last` e `self.qp[last] = 0`**: o último elemento ocupa a raiz, e sua posição é registrada em `qp`. Sem essa linha, um `change()` posterior procuraria esse vértice numa posição que não existe mais.
- **`self.sink(0)`**: o elemento novo na raiz pode ser maior que os filhos. O `sink` desce com ele, trocando sempre com o filho de menor custo, até o heap voltar a ficar ordenado (O(log V)).
- **`self.qp[m] = -1`**: marca que `m` saiu da fila, para `contains(m)` passar a responder falso.

No rastreamento, na Iteração 2, a raiz 4 saiu, o 2 (custo 7) foi para o topo e afundou trocando com o 1 (custo 3), resultando em `[1, 2, 5]`.

### 6.3 `change` e `swim`

```python
def change(self, i, item):
    self.keys[i] = item
    self.sink(self.qp[i])
    self.swim(self.qp[i])

def swim(self, k):
    while k > 0 and self.greater((k - 1) // 2, k):
        p = (k - 1) // 2
        self.pq[k], self.pq[p] = self.pq[p], self.pq[k]
        self.qp[self.pq[k]] = k
        self.qp[self.pq[p]] = p
        k = p
```

- **`self.keys[i] = item`**: grava a nova distância do vértice `i`.
- **`self.qp[i]`**: informa em O(1) onde `i` está no heap. Por isso `qp` precisa estar sempre correto.
- **`sink` e depois `swim`**: a nova chave pode ter aumentado ou diminuído. No Dijkstra ela só diminui, então na prática é o `swim` que age.
- **`swim`**: enquanto o pai `(k - 1) // 2` tiver custo maior, troca os dois e sobe um nível. As duas linhas com `qp` atualizam a posição de ambos após a troca (correção da seção 2).

No rastreamento, na Iteração 2, `change(5, 2)` fez o 5 subir até a raiz, porque passou a ter o menor custo da fila.

### 6.4 `path_to` e reconstrução da resposta

```python
def path_to(self, v):
    if not self.has_path_to(v):
        return None
    edges = []
    e = self.edgeTo[v]
    while e != None:
        edges.append(e)
        e = self.edgeTo[e.From()]
    return reversed(edges)
```

- **`has_path_to(v)`**: verifica se `distTo[v]` é finito, isto é, se o estado foi alcançado.
- **`e = self.edgeTo[v]`**: começa pela aresta que chegou ao destino.
- **`e = self.edgeTo[e.From()]`**: volta para a aresta que chegou à origem de `e`, repetindo até a origem do grafo, onde `edgeTo` é `None`.
- **`reversed(edges)`**: as arestas foram coletadas do fim para o começo, então são invertidas.

No problema, a resposta pedida é apenas o custo `distTo[2n - 1]`. O caminho serve para justificar o resultado: `edgeTo[5] = 4→5` e `edgeTo[4] = 0→4`, ou seja, `(1, 0) → (2, 1) → (3, 1)`.

