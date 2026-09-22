# Marco 2 — Componentes Conexas

## 1. Contexto e adaptação do problema

Para este marco, foi utilizado um caso particular baseado no problema **Eulerian Path**, do Kattis. Conforme solicitado, o problema original foi adaptado para trabalhar com um **grafo simples e não dirigido**, utilizando no máximo 6 vértices e 6 arestas.

O objetivo desta etapa é identificar as componentes conexas do grafo utilizando **DFS (Busca em Profundidade)** e analisar cada componente por meio das distâncias entre seus vértices.

A instância utilizada possui:

- **6 vértices:** `V = {0, 1, 2, 3, 4, 5}`
- **6 arestas:** `{(0,1), (1,2), (2,3), (3,0), (0,2), (4,5)}`

Como não existem arestas repetidas nem laços, o grafo é simples.

---

## 2. Descrição do grafo

O grafo possui duas partes que não possuem ligação entre si. A primeira é formada pelos vértices `0, 1, 2 e 3`, enquanto a segunda é formada pelos vértices `4 e 5`.

As arestas utilizadas são:

```text
(0,1)
(1,2)
(2,3)
(3,0)
(0,2)
(4,5)
```

Assim, as componentes encontradas posteriormente são:

```text
C1 = {0, 1, 2, 3}

C2 = {4, 5}
```

---

## 3. Desenho do grafo

Uma representação simplificada do grafo é:

```text
      1
     / \
    0---2
     \ /
      3


    4 ----- 5
```

A parte superior representa a primeira componente, enquanto `4` e `5` formam uma segunda componente isolada.

Não existe nenhuma aresta ligando os vértices da primeira parte aos vértices `4` e `5`.

---

## 4. Listas de adjacência

As listas de adjacência utilizadas para representar o grafo são:

```text
0 → [1, 3, 2]
1 → [0, 2]
2 → [1, 3, 0]
3 → [2, 0]
4 → [5]
5 → [4]
```

Como o grafo é não dirigido, quando existe uma aresta entre dois vértices, ela aparece na lista de adjacência dos dois.

Por exemplo, a aresta `(4,5)` aparece como `5` na lista do vértice `4` e como `4` na lista do vértice `5`.

---

## 5. Identificação das componentes conexas

Uma componente conexa é um conjunto de vértices em que existe um caminho entre qualquer par de vértices pertencentes a esse conjunto.

No grafo utilizado, é possível chegar de `0` a `1`, `2` e `3`, direta ou indiretamente. Portanto, esses quatro vértices pertencem à mesma componente:

```text
C1 = {0, 1, 2, 3}
```

Já os vértices `4` e `5` possuem apenas uma ligação entre si e não possuem ligação com a primeira parte:

```text
C2 = {4, 5}
```

Dessa forma, o grafo possui **2 componentes conexas**.

---

## 6. Excentricidades da primeira componente

A excentricidade de um vértice corresponde à maior distância entre ele e qualquer outro vértice da mesma componente.

Para o vértice `0`:

```text
0 → 1 = 1
0 → 2 = 1
0 → 3 = 1
```

Logo:

```text
ecc(0) = 1
```

Para o vértice `1`:

```text
1 → 0 = 1
1 → 2 = 1
1 → 3 = 2
```

Logo:

```text
ecc(1) = 2
```

Para o vértice `2`:

```text
2 → 0 = 1
2 → 1 = 1
2 → 3 = 1
```

Logo:

```text
ecc(2) = 1
```

Para o vértice `3`:

```text
3 → 0 = 1
3 → 2 = 1
3 → 1 = 2
```

Logo:

```text
ecc(3) = 2
```

Portanto:

```text
Excentricidades:
0 → 1
1 → 2
2 → 1
3 → 2
```

---

## 7. Raio, diâmetro e centro da primeira componente

A partir das excentricidades calculadas, podemos obter o raio e o diâmetro.

O **raio** é a menor excentricidade:

```text
raio = 1
```

O **diâmetro** é a maior excentricidade:

```text
diâmetro = 2
```

Os vértices que possuem excentricidade igual ao raio são `0` e `2`. Portanto, eles formam o centro da componente:

```text
Centro = {0, 2}
```

Assim, para a primeira componente:

```text
C1 = {0, 1, 2, 3}
raio = 1
diâmetro = 2
centro = {0, 2}
```

---

## 8. Análise da segunda componente

A segunda componente é formada somente pelos vértices `4` e `5`:

```text
4 — 5
```

Existe apenas uma distância entre os dois vértices:

```text
4 → 5 = 1
5 → 4 = 1
```

Portanto:

```text
ecc(4) = 1
ecc(5) = 1
```

Como as duas excentricidades são iguais:

```text
raio = 1
diâmetro = 1
centro = {4, 5}
```

Assim:

```text
C2 = {4, 5}
raio = 1
diâmetro = 1
centro = {4, 5}
```

---

## 9. Algoritmo DFS e estruturas utilizadas

Para identificar as componentes conexas foi utilizada uma **DFS recursiva**.

A ideia é marcar cada vértice visitado e continuar o percurso pelos seus vizinhos. Quando o algoritmo encontra um vértice que ainda não foi visitado, uma nova componente é iniciada.

Uma representação simplificada do algoritmo é:

```text
DFS(v):
    visitado[v] = verdadeiro

    para cada u em adj[v]:
        se visitado[u] == falso:
            DFS(u)
```

Além das listas de adjacência, são utilizadas duas estruturas principais:

```text
visitado = [false, false, false, false, false, false]

componente = [-1, -1, -1, -1, -1, -1]
```

O vetor `visitado` indica quais vértices já foram percorridos. O vetor `componente` armazena o número da componente à qual cada vértice pertence.

---

## 10. Rastreamento manual do DFS

Inicialmente, nenhum vértice foi visitado:

```text
visitado = [false, false, false, false, false, false]
```

O algoritmo começa pelo vértice `0`. A partir dele, segue pelas listas de adjacência:

```text
DFS(0)
 └── DFS(1)
      └── DFS(2)
           └── DFS(3)
```

Durante esse percurso, os vértices `0, 1, 2 e 3` são marcados como pertencentes à primeira componente.

Depois, o algoritmo continua verificando os demais vértices. Ao chegar ao vértice `4`, inicia uma nova busca:

```text
DFS(4)
 └── DFS(5)
```

Nesse momento, `4` e `5` são classificados como pertencentes à segunda componente.

Ao final do processo:

```text
visitado = [true, true, true, true, true, true]

componente = [0, 0, 0, 0, 1, 1]
```

O resultado confirma que foram encontradas duas componentes conexas.

---

## 11. Complexidade e consultas de conectividade

Considerando a representação por listas de adjacência, o DFS visita cada vértice uma vez e percorre as arestas existentes.

A complexidade de tempo do algoritmo é:

```text
O(V + E)
```

O espaço utilizado também é:

```text
O(V + E)
```

considerando as listas de adjacência, o vetor `visitado`, o vetor `componente` e a pilha de chamadas da recursão.

Depois que as componentes foram identificadas, é possível verificar se dois vértices pertencem à mesma componente comparando seus identificadores:

```text
componente[u] == componente[v]
```

Essa consulta possui custo `O(1)`.

Sem esse pré-processamento, seria necessário realizar uma busca para cada consulta, podendo chegar a `O(V + E)` por consulta.

---

## 12. Conclusão

A partir da adaptação do problema, foi possível representar um grafo simples e não dirigido com duas componentes conexas.

O uso do DFS permitiu identificar quais vértices pertencem a cada componente:

```text
C1 = {0, 1, 2, 3}

C2 = {4, 5}
```

Também foram calculadas manualmente as excentricidades, o raio, o diâmetro e o centro de cada componente.

Para a primeira componente, o raio é `1`, o diâmetro é `2` e o centro é formado pelos vértices `{0, 2}`. Para a segunda, o raio e o diâmetro são `1`, e os dois vértices pertencem ao centro.

Por fim, a análise da complexidade mostrou que a identificação das componentes utilizando listas de adjacência e DFS possui custo `O(V + E)`, enquanto as consultas de conectividade, após o pré-processamento, podem ser realizadas em `O(1)`.

Essa análise complementa o estudo do problema original de caminho Euleriano, permitindo compreender primeiro a estrutura de conectividade do grafo utilizado.
