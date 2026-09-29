# Marco 3 — Estratégia algorítmica

## 1. Propriedade estrutural central

A propriedade estrutural central utilizada neste problema é a **conectividade do grafo**.

O objetivo é determinar quais vértices pertencem à mesma componente conexa. Para isso, utiliza-se a ideia de que, partindo de um vértice, todos os vértices que podem ser alcançados por caminhos pertencem à mesma componente.

O critério utilizado para reconhecer uma componente é:

> dois vértices pertencem à mesma componente conexa se, e somente se, existe um caminho entre eles.

A estratégia escolhida para identificar essas componentes é a **Busca em Profundidade (DFS — Depth-First Search)**.

Durante a execução, cada vértice visitado recebe um identificador de componente. Quando o algoritmo encontra um vértice ainda não visitado após finalizar uma busca anterior, uma nova componente é iniciada.

Para a instância utilizada no Marco 2:

```text
V = {0, 1, 2, 3, 4, 5}

E = {
    (0,1),
    (1,2),
    (2,3),
    (3,0),
    (0,2),
    (4,5)
}
```

a DFS identifica:

```text
C0 = {0, 1, 2, 3}

C1 = {4, 5}
```

Portanto, o número de componentes conexas é:

```text
2
```

---

## 2. Estratégia algorítmica

A estratégia consiste em percorrer todo o grafo utilizando DFS.

Inicialmente, todos os vértices estão marcados como não visitados. O algoritmo percorre os vértices em ordem e, sempre que encontra um vértice ainda não visitado, inicia uma DFS a partir dele.

Todos os vértices alcançados nessa busca recebem o mesmo identificador de componente.

Uma representação simplificada da estratégia é:

```text
para cada vértice v:

    se v ainda não foi visitado:

        iniciar DFS(v)

        atribuir o mesmo identificador
        de componente aos vértices alcançados
```

Na instância escolhida, o processo ocorre da seguinte maneira:

```text
0 → inicia componente 0

DFS(0)
 ├── 1
 │   └── 2
 │       └── 3
 └── demais vértices já visitados

4 → inicia componente 1

DFS(4)
 └── 5
```

Ao final:

```text
componente[0] = 0
componente[1] = 0
componente[2] = 0
componente[3] = 0
componente[4] = 1
componente[5] = 1
```

---

## 3. Implementação de referência do `algs4`

A implementação de referência utilizada como base será a classe **`CC` (Connected Components)** da biblioteca `algs4`.

Essa implementação é responsável por identificar as componentes conexas de um grafo não dirigido utilizando DFS.

A ideia utilizada pela implementação de referência é compatível com a estratégia adotada neste projeto:

```text
CC(G)

    para cada vértice v:
        se v não foi marcado:
            DFS(G, v)
            incrementar identificador da componente
```

Entre as principais operações oferecidas pela implementação estão:

```text
count()
```

para obter a quantidade de componentes conexas;

e:

```text
connected(v, w)
```

para verificar se dois vértices pertencem à mesma componente.

Também é utilizado o conceito de identificador de componente, que permite associar cada vértice à componente encontrada durante a DFS.

### Adaptações previstas

Nesta etapa não será realizada a implementação do código definitivo.

A implementação do `algs4` será utilizada como referência para a solução final, com possíveis adaptações para:

* adequar a entrada ao formato da instância utilizada;
* preservar a representação do grafo por listas de adjacência;
* apresentar os identificadores das componentes;
* permitir a análise das componentes individualmente;
* posteriormente calcular as propriedades solicitadas para cada componente.

A estratégia de busca em profundidade permanece a mesma da implementação de referência.

---

## 4. Obtenção das propriedades das componentes

A identificação das componentes conexas não é suficiente para obter todas as informações solicitadas.

Depois de identificar uma componente, é necessário analisar as distâncias entre seus vértices.

Para isso, pode-se utilizar uma **BFS a partir de cada vértice da componente**.

A BFS permite obter as menores distâncias, em número de arestas, entre um vértice de origem e os demais vértices alcançáveis.

Para cada vértice `v`, calcula-se:

```text
ecc(v) = maior distância entre v e qualquer outro
         vértice pertencente à mesma componente
```

Depois:

```text
raio = menor excentricidade

diâmetro = maior excentricidade

centro = vértices cuja excentricidade é igual ao raio
```

Assim, a estratégia completa possui duas etapas:

```text
1. DFS
   ↓
   identifica as componentes

2. BFS a partir de cada vértice
   ↓
   calcula as distâncias
   ↓
   calcula excentricidades
   ↓
   calcula raio, diâmetro e centro
```

Essa separação é importante porque **DFS resolve a identificação das componentes**, enquanto **BFS fornece as menores distâncias necessárias para as propriedades métricas**.

---

## 5. Rastreamento manual da estratégia

Será utilizado o grafo definido no Marco 2:

```text
      1
     / \
    0---2
     \ /
      3

    4 ----- 5
```

com as listas de adjacência:

```text
0 → [1, 3, 2]
1 → [0, 2]
2 → [1, 3, 0]
3 → [2, 0]
4 → [5]
5 → [4]
```

### 5.1 Estado inicial

```text
visitado = [F, F, F, F, F, F]

componente = [-1, -1, -1, -1, -1, -1]
```

O algoritmo começa pelo vértice `0`.

```text
DFS(0)
```

Marca:

```text
visitado = [V, F, F, F, F, F]

componente = [0, -1, -1, -1, -1, -1]
```

O primeiro vizinho de `0` é `1`.

```text
DFS(1)
```

Estado:

```text
visitado = [V, V, F, F, F, F]

componente = [0, 0, -1, -1, -1, -1]
```

A partir de `1`, o vértice `2` ainda não foi visitado.

```text
DFS(2)
```

Estado:

```text
visitado = [V, V, V, F, F, F]

componente = [0, 0, 0, -1, -1, -1]
```

A partir de `2`, encontramos o vértice `3`.

```text
DFS(3)
```

Estado:

```text
visitado = [V, V, V, V, F, F]

componente = [0, 0, 0, 0, -1, -1]
```

Os demais vizinhos encontrados durante esse percurso já foram visitados.

A primeira componente está concluída:

```text
C0 = {0, 1, 2, 3}
```

### 5.2 Segunda componente

O algoritmo continua percorrendo os vértices.

Os vértices `1`, `2` e `3` já foram visitados.

Ao chegar em `4`:

```text
visitado[4] = F
```

uma nova componente é iniciada:

```text
DFS(4)
```

Estado:

```text
visitado = [V, V, V, V, V, F]

componente = [0, 0, 0, 0, 1, -1]
```

O vizinho de `4` é `5`.

```text
DFS(5)
```

Estado final:

```text
visitado = [V, V, V, V, V, V]

componente = [0, 0, 0, 0, 1, 1]
```

Portanto:

```text
C0 = {0, 1, 2, 3}

C1 = {4, 5}
```

e:

```text
count = 2
```

---

## 6. Rastreamento do cálculo das distâncias

Depois da identificação das componentes, a primeira componente é:

```text
C0 = {0, 1, 2, 3}
```

Partindo de `0`, uma BFS produz:

```text
distância:

0 → 0 = 0
0 → 1 = 1
0 → 2 = 1
0 → 3 = 1
```

Logo:

```text
ecc(0) = 1
```

Partindo de `1`:

```text
1 → 0 = 1
1 → 2 = 1
1 → 3 = 2
```

Logo:

```text
ecc(1) = 2
```

Partindo de `2`:

```text
2 → 0 = 1
2 → 1 = 1
2 → 3 = 1
```

Logo:

```text
ecc(2) = 1
```

Partindo de `3`:

```text
3 → 0 = 1
3 → 2 = 1
3 → 1 = 2
```

Logo:

```text
ecc(3) = 2
```

Tabela resultante:

| Vértice | Excentricidade |
| ------- | -------------: |
| 0       |              1 |
| 1       |              2 |
| 2       |              1 |
| 3       |              2 |

Consequentemente:

```text
raio = 1

diâmetro = 2

centro = {0, 2}
```

Para a segunda componente:

```text
C1 = {4, 5}
```

temos:

```text
4 → 5 = 1
5 → 4 = 1
```

Logo:

```text
ecc(4) = 1
ecc(5) = 1

raio = 1

diâmetro = 1

centro = {4, 5}
```

---

## 7. Complexidade de tempo

A identificação das componentes utilizando DFS possui complexidade:

```text
O(V + E)
```

quando o grafo é representado por listas de adjacência.

Isso ocorre porque cada vértice é visitado uma vez e cada aresta é examinada durante os percursos.

Entretanto, para calcular as excentricidades é necessário obter as menores distâncias entre os vértices de cada componente.

Utilizando uma BFS para cada vértice, o custo é:

```text
O(V(V + E))
```

no pior caso.

Portanto, considerando a estratégia completa:

```text
DFS para componentes:
O(V + E)

BFS para cálculo das distâncias:
O(V(V + E))

Custo total:
O(V + E) + O(V(V + E))

= O(V(V + E))
```

Para a instância pequena utilizada neste trabalho, esse custo é baixo. A análise é importante principalmente para compreender como o algoritmo se comportaria à medida que o número de vértices e arestas aumentasse.

---

## 8. Complexidade de memória

É importante separar a memória utilizada para **representar o grafo** da memória **auxiliar do algoritmo**.

### 8.1 Representação do grafo

Utilizando listas de adjacência:

```text
O(V + E)
```

A estrutura armazena cada vértice e suas respectivas adjacências.

Como o grafo é não dirigido, cada aresta aparece nas listas de seus dois extremos.

### 8.2 Memória auxiliar da DFS

A DFS utiliza:

```text
visitado → O(V)

componente → O(V)

pilha de recursão → O(V)
```

Portanto, a memória auxiliar da identificação das componentes é:

```text
O(V)
```

### 8.3 Memória auxiliar das BFS

Para uma BFS são necessárias estruturas como:

```text
fila → O(V)

distâncias → O(V)

marcação de visitados → O(V)
```

Assim, a memória auxiliar continua sendo:

```text
O(V)
```

por execução da BFS.

Portanto, podemos separar:

```text
Representação do grafo:
O(V + E)

Memória auxiliar:
O(V)
```

Essa distinção evita considerar a estrutura de entrada como memória auxiliar do algoritmo.

---

## 9. Justificativa da estratégia

A utilização da DFS é adequada para identificar componentes conexas porque uma única busca iniciada em um vértice alcança exatamente os vértices que estão conectados a ele por algum caminho.

Assim, cada nova DFS iniciada a partir de um vértice ainda não visitado representa uma nova componente.

Para as propriedades relacionadas às distâncias, a BFS é adequada porque, em um grafo não ponderado, ela encontra as menores distâncias em número de arestas a partir de uma origem.

Dessa maneira, a combinação das duas estratégias permite resolver as duas necessidades do problema:

```text
DFS
→ identificar a estrutura de conectividade

BFS
→ obter menores distâncias

Excentricidades
→ obter raio, diâmetro e centro
```

A estratégia também mantém a representação do grafo por listas de adjacência, que é apropriada para grafos esparsos e permite percorrer eficientemente os vizinhos de cada vértice.

---

## 10. Conclusão

A estratégia algorítmica definida para o problema utiliza **DFS para identificação das componentes conexas** e **BFS para obtenção das menores distâncias necessárias ao cálculo das propriedades métricas**.

Na instância analisada, a DFS encontrou:

```text
C0 = {0, 1, 2, 3}

C1 = {4, 5}
```

A primeira componente apresentou:

```text
raio = 1

diâmetro = 2

centro = {0, 2}
```

enquanto a segunda apresentou:

```text
raio = 1

diâmetro = 1

centro = {4, 5}
```

A implementação `CC` do `algs4` será utilizada como referência para a identificação das componentes conexas, enquanto a lógica de busca em largura servirá como base para o cálculo das distâncias.

A identificação das componentes possui custo `O(V + E)`, enquanto o cálculo das propriedades por BFS a partir de cada vértice possui custo `O(V(V + E))`. A representação do grafo ocupa `O(V + E)` e a memória auxiliar utilizada pelos algoritmos é `O(V)`.

Dessa forma, o Marco 3 estabelece a estratégia que será utilizada na implementação, relacionando a propriedade estrutural do problema às estruturas de dados, às implementações de referência do `algs4` e às complexidades envolvidas.

