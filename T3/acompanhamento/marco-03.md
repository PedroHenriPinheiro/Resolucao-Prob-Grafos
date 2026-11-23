# Marco 3 — Rastreamento manual

## 1. Mapeamento dos estados para o `algs4`

No Marco 2, definimos que cada cidade v possui dois estados: `(v, 0) (cupom disponível)` e `(v, 1) (cupom já utilizado)`.   

Como a classe `EdgeWeightedDigraph` da biblioteca `algs4` identifica vértices por inteiros sequenciais a partir de 0 `(0 até 2n - 1)`, mapeamos cada estado `(v, cupom)` para um índice único:   
- **Estado (v, 0) (cupom disponível):** índice v - 1
- **Estado (v, 1) (cupom utilizado):** índice (v - 1) + n

Para a instância com `n = 3 cidades`, temos `2n = 6 vértices` no grafo do `algs4`:  

| Estado | Significado | Índice no algs4 |
|---|---|---|
| `(1, 0)` | Cidade 1 com cupom disponível (Origem)| 0 |
| `(2, 0)` | Cidade 2 com cupom disponível | 1 | 
| `(3, 0)` | Cidade 3 com cupom disponível | 2 | 
| `(1, 1)` | Cidade 1 com cupom utilizado | 3 | 
| `(2, 1)` | Cidade 2 com cupom utilizado | 4 | 
| `(3, 1)` | Cidade 3 com cupom utilizado (Destino) | 5 | 

### Transições criadas no EdgeWeightedDigraph

Para cada voo `a → b de custo c`, inserimos três objetos `DirectedEdge`:   
- (a, 0) → (b, 0) com custo c   
- (a, 1) → (b, 1) com custo c   
- (a, 0) → (b, 1) com custo floor(c / 2)   

Aplicando à entrada do Marco 2 `(n = 3, m = 4)`, geramos `3m = 12 arestas direcionadas`:   

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

## 2. Alterações registradas na implementação `algs4` (Python)

Ao adaptar os arquivos de referência `dijkstra_sp.py` e `index_min_pq.py` para o problema, foram necessárias três correções pontuais:

| Arquivo | Alteração realizada | Justificativa |
|---|---|---|
| `dijkstra_sp.py` | Substituição de `POSITIVE_INFINITY = 999999.0` por `float("inf")`| As restrições do problema permitem custos de até `10⁹` por voo, ultrapassando o limite fixo de `999999.0`. |
| `index_min_pq.py` | Correção de `contains(i) de i in self.keys` para `self.qp[i] != -1` | O vetor `keys` armazena distâncias e não índices de vértices; usar `qp` evita falsos positivos e reduz a consulta de `O(V)` para `O(1)` | 
| `index_min_pq.py` | Atualização de `self.qp[self.pq[k]] = k` dentro de `swim()` e `sink()` | O código original trocava elementos no `heap pq` sem atualizar suas posições no vetor inverso `qp`, invalidando chamadas futuras de `change()`. | 

## 3. Estruturas de dados e estados iniciais

Ao executar `DijkstraSP(g, 0)`, as estruturas internas são inicializadas da seguinte forma:   
- **`g (EdgeWeightedDigraph)`:** grafo com g.V = 6 vértices e g.E = 12 arestas, armazenadas em listas de adjacência g.adj[0..5] do tipo Bag.   
- **`distTo`:** lista de tamanho 6 com o menor custo acumulado conhecido desde o índice 0 ((1, 0)).   
- **`edgeTo`:** lista de tamanho 6 com a última aresta DirectedEdge utilizada para alcançar cada índice.   
- **`pq (IndexMinPQ)`:** fila de prioridade indexada (heap binário mínimo) que mantém os vértices abertos ordenados pelo menor valor em distTo.   

### Estado inicial (antes do laço while)

```text
Índices:   0      1      2      3      4      5
Estados: (1,0)  (2,0)  (3,0)  (1,1)  (2,1)  (3,1)
--------------------------------------------------
distTo:  [  0 ,  inf ,  inf ,  inf ,  inf ,  inf ]
edgeTo:  [None, None , None , None , None , None ]
pq.pq:   [  0  ]
```

## 4. Rastreamento passo a passo das operações

O algoritmo executa o laço while not self.pq.is_empty() removendo o vértice v = pq.del_min() de menor distância e relaxando todas as arestas em g.adj[v].   

### Iteração 1 — Remove índice 0 | Estado (1, 0) (custo 0)

Relaxamento das arestas de saída de 0:   

- 0 → 1 (peso 3): 0 + 3 < inf → distTo[1] = 3, edgeTo[1] = 0→1, pq.insert(1, 3)   
- 0 → 4 (peso 1): 0 + 1 < inf → distTo[4] = 1, edgeTo[4] = 0→4, pq.insert(4, 1) (4 sobe para a raiz do heap)   
- 0 → 2 (peso 7): 0 + 7 < inf → distTo[2] = 7, edgeTo[2] = 0→2, pq.insert(2, 7)   
- 0 → 5 (peso 3): 0 + 3 < inf → distTo[5] = 3, edgeTo[5] = 0→5, pq.insert(5, 3)  

```text
distTo:  [  0 ,   3  ,   7  ,  inf ,   1  ,   3  ]
edgeTo:  [None,  0→1 ,  0→2 , None ,  0→4 ,  0→5 ]
pq.pq:   [  4 ,   1  ,   2  ,   5  ]
```

### Iteração 2 — Remove índice 4 | Estado (2, 1) (custo 1)

Relaxamento das arestas de saída de 4:   
- 4 → 5 (peso 1): 1 + 1 = 2 < 3 (distTo[5]) → atualiza distTo[5] = 2, edgeTo[5] = 4→5, pq.change(5, 2) (5 sobe para a raiz)
- 4 → 3 (peso 5): 1 + 5 = 6 < inf → distTo[3] = 6, edgeTo[3] = 4→3, pq.insert(3, 6)   

```text
distTo:  [  0 ,   3  ,   7  ,   6  ,   1  ,   2  ]
edgeTo:  [None,  0→1 ,  0→2 ,  4→3 ,  0→4 ,  4→5 ]
pq.pq:   [  5 ,   1  ,   3  ,   2  ]
```

### Iteração 3 — Remove índice 5 | Estado (3, 1) (custo 2)

- g.adj[5] está vazia (não há voos saindo da cidade 3).
- Ao remover 5 da raiz, o último elemento (2) vai para o topo e afunda (sink), promovendo 1 para a raiz.   

```text
distTo:  [  0 ,   3  ,   7  ,   6  ,   1  ,   2  ]
edgeTo:  [None,  0→1 ,  0→2 ,  4→3 ,  0→4 ,  4→5 ]
pq.pq:   [  1 ,   2  ,   3  ]
```

### Iteração 4 — Remove índice 1 | Estado (2, 0) (custo 3)

Relaxamento das arestas de saída de 1:   
- 1 → 2 (peso 1): 3 + 1 = 4 < 7 (distTo[2]) → atualiza distTo[2] = 4, edgeTo[2] = 1→2, pq.change(2, 4)
- 1 → 5 (peso 0): 3 + 0 = 3 (não melhora distTo[5] = 2) → ignora
- 1 → 0 (peso 5): 3 + 5 = 8 (não melhora distTo[0] = 0) → ignora
- 1 → 3 (peso 2): 3 + 2 = 5 < 6 (distTo[3]) → atualiza distTo[3] = 5, edgeTo[3] = 1→3, pq.change(3, 5)

```text
distTo:  [  0 ,   3  ,   4  ,   5  ,   1  ,   2  ]
edgeTo:  [None,  0→1 ,  1→2 ,  1→3 ,  0→4 ,  4→5 ]
pq.pq:   [  2 ,   3  ]
```

### Iteração 5 — Remove índice 2 | Estado (3, 0) (custo 4)

- g.adj[2] está vazia (não há voos saindo da cidade 3)

```text
distTo:  [  0 ,   3  ,   4  ,   5  ,   1  ,   2  ]
edgeTo:  [None,  0→1 ,  1→2 ,  1→3 ,  0→4 ,  4→5 ]
pq.pq:   [  3  ]
```

### Iteração 6 — Remove índice 3 | Estado (1, 1) (custo 5)

Relaxamento das arestas de saída de 3:   
- 3 → 4 (peso 3): 5 + 3 = 8 (não melhora distTo[4] = 1) → ignora
- 3 → 5 (peso 7): 5 + 7 = 12 (não melhora distTo[5] = 2) → ignora

```text
distTo:  [  0 ,   3  ,   4  ,   5  ,   1  ,   2  ]
edgeTo:  [None,  0→1 ,  1→2 ,  1→3 ,  0→4 ,  4→5 ]
pq.pq:   [     ]  (fila vazia — encerramento)
```

### Resumo geral das iterações

| Iteração | Vértice removido | Estado | distTo[0..5] | Fila pq.pq |
|---|---|---|---|---|
|Início | — | — | [0, inf, inf, inf, inf, inf] | [0] |
| 1 | 0 | (1, 0) | [0, 3, 7, inf, 1, 3] | [4, 1, 2, 5] |
| 2 | 4 | (2, 1) | [0, 3, 7, 6, 1, 2] | [5, 1, 3, 2] | 
| 3 | 5 | (3, 1) | [0, 3, 7, 6, 1, 2] | [1, 2, 3] | 
| 4 | 1 | (2, 0) | [0, 3, 4, 5, 1, 2] | [2, 3] | 
| 5 | 2 | (3, 0) | [0, 3, 4, 5, 1, 2] | [3] | 
| 6 | 3 | (1, 1) | [0, 3, 4, 5, 1, 2] | [] | 

## 5. Justificativa das decisões e resultado

### Por que as decisões garantem o caminho mínimo

Em cada passo, a IndexMinPQ extrai o estado (v, cupom) com menor custo acumulado conhecido. Como todos os pesos das transições são não negativos (c ≥ 1 e floor(c / 2) ≥ 0), nenhum caminho futuro passando por vértices ainda na fila poderá produzir um custo menor para um estado já removido.   Na Iteração 1, o algoritmo encontrou o voo direto 1 → 3 utilizando o cupom (0 → 5), registrando custo inicial 3 para o destino (3, 1). Porém, como o estado (2, 1) (índice 4) possuía custo menor (1), ele foi expandido antes na Iteração 2, descobrindo a transição 4 → 5 de custo 1 e reduzindo o custo total do destino para 2.

### Reconstrução do caminho e resultado final

O destino desejado é (3, 1), correspondente ao índice 2n - 1 = 5. Consultando distTo[5], obtemos o custo mínimo 2.   

Seguindo o vetor edgeTo de trás para frente a partir do índice 5: 

```text
edgeTo[5] = 4 → 5   (voo 2 → 3 sem cupom, custo 1)
edgeTo[4] = 0 → 4   (voo 1 → 2 com cupom, custo floor(3 / 2) = 1)
```

Caminho ótimo obtido:

```text
(1, 0) --[cupom: 1]--> (2, 1) --[normal: 1]--> (3, 1)
```

Resultado final: 2 (idêntico à saída esperada definida no Marco 2).

## 6. Explicação individual de uma etapa no código `algs4`

A etapa selecionada é o método relax(self, g, v) da classe DijkstraSP (dijkstra_sp.py):

```text
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

`for e in g.adj[v]: e w = e.To()`   
- Percorre todas as arestas direcionadas (DirectedEdge) armazenadas na Bag do vértice v recém-removido da fila, obtendo o vértice de destino w. No grafo de estados, esse laço avalia simultaneamente voos comuns (permanecendo no mesmo nível de cupom) e o uso do cupom (saltando de (a, 0) para (b, 1)).   

`if self.distTo[w] > self.distTo[v] + e.weight:`   
- Verifica a condição de relaxamento: testa se chegar a w passando por v e atravessando a aresta e resulta em um custo estritamente menor que a melhor distância registrada anteriormente para w.   

`self.distTo[w] = self.distTo[v] + e.weight e self.edgeTo[w] = e`  
- Caso o novo caminho seja mais barato, atualiza o menor custo acumulado até w e registra a aresta e como predecessora na árvore de caminhos mínimos (SPT).   

`if self.pq.contains(w): self.pq.change(...) else: self.pq.insert(...)`   
- Mantém a fila de prioridade indexada (IndexMinPQ) sincronizada:
  - Se w já estava na fila de fronteira (contains(w) verdadeiro), pq.change reduz sua prioridade e reorganiza o heap em tempo O(log V) — como ocorreu na Iteração 2, quando distTo[5] foi reduzido de 3 para 2.   
  - Caso contrário, w é descoberto pela primeira vez e inserido no heap via pq.insert — como ocorreu na Iteração 1 para os índices 1, 4, 2 e 5.    
