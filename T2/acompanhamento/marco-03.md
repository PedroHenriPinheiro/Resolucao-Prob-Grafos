# Marco 3 — Estratégia algorítmica

## 1. Propriedade estrutural central

O problema consiste em encontrar um **caminho euleriano em um grafo direcionado**, ou seja, uma sequência de vértices que percorra **todas as arestas exatamente uma vez**, sempre respeitando a direção de cada aresta.

A propriedade estrutural central utilizada para determinar se um caminho euleriano pode existir é a relação entre o **grau de entrada (`indegree`)** e o **grau de saída (`outdegree`)** de cada vértice.

### Condições para existência do caminho

Em um grafo direcionado, um caminho euleriano pode assumir duas formas:

#### Caminho euleriano aberto

Deve existir:

* exatamente um vértice com:

```text
outdegree(v) = indegree(v) + 1
```

Esse será o vértice inicial.

* exatamente um vértice com:

```text
indegree(v) = outdegree(v) + 1
```

Esse será o vértice final.

* todos os demais vértices devem possuir:

```text
indegree(v) = outdegree(v)
```

#### Ciclo euleriano

Caso todos os vértices possuam:

```text
indegree(v) = outdegree(v)
```

o grafo pode possuir um ciclo euleriano, desde que as arestas pertençam à mesma componente relevante do grafo.

### Conectividade

Além das condições de grau, as arestas precisam estar conectadas de forma que possam ser percorridas em uma única sequência.

Para essa verificação, a conectividade pode ser analisada desconsiderando a direção das arestas.

Caso existam componentes distintas contendo arestas, não é possível construir um único caminho que percorra todas elas.

### Estratégia para obtenção da resposta

Depois de verificar as condições estruturais, será utilizado o algoritmo de **Hierholzer** para construir o caminho.

A estratégia utiliza uma pilha:

1. Escolher o vértice inicial.
2. Seguir uma aresta ainda não utilizada.
3. Adicionar o próximo vértice à pilha.
4. Continuar enquanto existirem arestas disponíveis.
5. Quando o vértice atual não possuir mais arestas disponíveis, removê-lo da pilha e adicioná-lo ao caminho.
6. Continuar o processo até a pilha ficar vazia.
7. Verificar se foram utilizadas todas as arestas.

Como um caminho que utiliza `E` arestas possui `E + 1` vértices, essa propriedade será utilizada como verificação final:

```text
path.size() == E + 1
```

Caso essa condição não seja satisfeita, a resposta será:

```text
Impossible
```

---

# 2. Implementações de referência do `algs4`

## 2.1. `DirectedEulerianPath`

A principal implementação de referência será a classe:

```text
DirectedEulerianPath
```

do `algs4`.

Essa classe implementa a busca de um caminho euleriano em um **grafo direcionado** e utiliza uma estratégia iterativa baseada em pilha.

Ela será utilizada como referência para:

* análise de `indegree` e `outdegree`;
* escolha do vértice inicial;
* representação por listas de adjacência;
* construção do caminho com uma pilha;
* aplicação do algoritmo de Hierholzer;
* verificação de que o caminho contém `E + 1` vértices.

A implementação será adaptada para o formato de entrada e saída do problema atribuído.

A classe original possui estruturas e funcionalidades específicas do `algs4`, além de códigos utilizados para testes. Esses elementos não serão necessariamente incorporados à solução final.

---

## 2.2. `Digraph`

A classe:

```text
Digraph
```

será utilizada como referência para a representação de um grafo direcionado por **listas de adjacência**.

Para cada aresta:

```text
u → v
```

o vértice `v` será armazenado na lista de adjacência de `u`.

Além da lista de adjacência, serão mantidos os graus de entrada e saída dos vértices.

---

## 2.3. `Stack`

A estrutura:

```text
Stack
```

será utilizada como referência para a implementação iterativa do Hierholzer.

A pilha armazena os vértices do percurso atual.

Quando o vértice do topo ainda possui uma aresta disponível, o algoritmo segue essa aresta e adiciona o próximo vértice à pilha.

Quando não existem mais arestas disponíveis, o vértice é retirado da pilha e inserido no caminho final.

---

## 2.4. `BreadthFirstDirectedPaths`

A classe:

```text
BreadthFirstDirectedPaths
```

pode ser utilizada como referência para a verificação de conectividade dos vértices que possuem arestas.

Como o problema possui arestas direcionadas, a conectividade necessária para essa condição pode ser analisada considerando uma representação direcionada das arestas.

---

# 3. Adaptações previstas

A solução do problema não utilizará diretamente toda a estrutura da classe `DirectedEulerianPath`.

As principais adaptações previstas são:

### Entrada

O problema possui vários casos de teste.

Cada caso começa com:

```text
V E
```

seguido por `E` arestas.

A entrada termina quando:

```text
0 0
```

for encontrado.

Portanto, a solução deverá processar os casos sequencialmente.

### Representação

Será utilizada uma lista de adjacência direcionada.

Para uma entrada:

```text
u v
```

será registrada a aresta:

```text
u → v
```

Também serão atualizados:

```text
outdegree[u]++
indegree[v]++
```

### Saída

Para cada caso:

* se existir um caminho euleriano, será impressa uma sequência de vértices;
* caso contrário, será impresso:

```text
Impossible
```

Quando existirem múltiplos caminhos eulerianos válidos, qualquer um deles poderá ser utilizado.

### Construção do caminho

A construção será baseada no algoritmo de Hierholzer, utilizando uma pilha e percorrendo cada aresta no máximo uma vez.

---

# 4. Estratégia algorítmica

A solução será dividida em duas etapas principais.

## 4.1. Verificação das condições

Para cada caso de teste:

1. Ler `V` e `E`.
2. Criar a lista de adjacência.
3. Ler cada aresta `u → v`.
4. Adicionar `v` à lista de adjacência de `u`.
5. Incrementar `outdegree(u)`.
6. Incrementar `indegree(v)`.
7. Analisar a diferença entre os graus de entrada e saída.
8. Determinar o possível vértice inicial.
9. Verificar a conectividade das regiões que possuem arestas.

Se as condições necessárias não forem satisfeitas, o caso será considerado impossível.

---

## 4.2. Construção com Hierholzer

Depois da validação, será utilizado o algoritmo de Hierholzer.

A estrutura principal será uma pilha de vértices.

Inicialmente:

```text
stack = [s]
path = []
```

onde `s` é o vértice inicial.

Enquanto a pilha não estiver vazia:

* observar o vértice no topo;
* caso exista uma aresta não utilizada, seguir essa aresta e colocar o destino na pilha;
* caso não existam mais arestas disponíveis, retirar o vértice da pilha e colocá-lo no caminho.

Ao final, o caminho é obtido na ordem inversa em que os vértices foram retirados da pilha.

A sequência final será então verificada.

Se:

```text
path.size() = E + 1
```

todas as arestas foram incorporadas ao caminho.

Caso contrário:

```text
Impossible
```

---

# 5. Rastreamento manual

Será utilizada a seguinte instância:

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

As arestas direcionadas são:

```text
0 → 1
1 → 2
2 → 3
3 → 0
0 → 2
4 → 5
```

A representação por lista de adjacência é:

```text
0 → [1, 2]
1 → [2]
2 → [3]
3 → [0]
4 → [5]
5 → []
```

---

## 5.1. Identificação das componentes

Uma DFS utilizada para analisar a conectividade identifica:

```text
C0 = {0, 1, 2, 3}

C1 = {4, 5}
```

A primeira componente contém cinco arestas:

```text
0 → 1
1 → 2
2 → 3
3 → 0
0 → 2
```

A segunda contém:

```text
4 → 5
```

Portanto, existe uma região do grafo contendo uma aresta que não pode ser incorporada ao mesmo percurso das arestas de `C0`.

---

# 6. Análise dos graus

Os graus de entrada e saída são:

| Vértice | Indegree | Outdegree |
| ------- | -------- | --------- |
| 0       | 1        | 2         |
| 1       | 1        | 1         |
| 2       | 2        | 1         |
| 3       | 1        | 1         |
| 4       | 0        | 1         |
| 5       | 1        | 0         |

No componente `C0`:

```text
0: outdegree = indegree + 1
2: indegree = outdegree + 1
1: indegree = outdegree
3: indegree = outdegree
```

Assim, os graus de `C0` são compatíveis com um caminho euleriano aberto.

O vértice:

```text
0
```

seria o candidato a início.

O vértice:

```text
2
```

seria o candidato a final.

Entretanto, existem também os vértices `4` e `5`, que possuem a aresta:

```text
4 → 5
```

Essa aresta pertence a uma segunda componente.

Consequentemente, não existe um único caminho que utilize todas as seis arestas da instância.

---

# 7. Rastreamento do Hierholzer

Mesmo iniciando no vértice `0`, o algoritmo ficará restrito às arestas do componente `C0`.

Estado inicial:

```text
Stack:
[0]

Path:
[]
```

### Passo 1

A partir de `0`, existe a aresta:

```text
0 → 1
```

Estado:

```text
Stack:
[0, 1]

Path:
[]
```

### Passo 2

A partir de `1`:

```text
1 → 2
```

Estado:

```text
Stack:
[0, 1, 2]

Path:
[]
```

### Passo 3

A partir de `2`:

```text
2 → 3
```

Estado:

```text
Stack:
[0, 1, 2, 3]

Path:
[]
```

### Passo 4

A partir de `3`:

```text
3 → 0
```

Estado:

```text
Stack:
[0, 1, 2, 3, 0]

Path:
[]
```

### Passo 5

A partir de `0`, ainda existe a aresta:

```text
0 → 2
```

Estado:

```text
Stack:
[0, 1, 2, 3, 0, 2]

Path:
[]
```

Agora o vértice `2` não possui mais arestas de saída disponíveis.

O vértice é retirado da pilha e adicionado ao caminho.

```text
Stack:
[0, 1, 2, 3, 0]

Path:
[2]
```

O processo continua retirando os vértices que não possuem mais arestas disponíveis.

Ao final, o caminho parcial será equivalente a:

```text
0 1 2 3 0 2
```

As cinco arestas do componente `C0` foram utilizadas:

```text
0 → 1
1 → 2
2 → 3
3 → 0
0 → 2
```

Porém, a aresta:

```text
4 → 5
```

permanece sem utilização.

---

# 8. Verificação final

O grafo possui:

```text
E = 6
```

Portanto, um caminho euleriano válido precisaria possuir:

```text
E + 1 = 7
```

vértices.

O caminho construído a partir do vértice `0` utiliza somente as cinco arestas de `C0`, produzindo:

```text
0 1 2 3 0 2
```

Esse caminho possui:

```text
6
```

vértices, em vez dos `7` necessários.

Além disso, a aresta:

```text
4 → 5
```

não foi utilizada.

Logo:

```text
path.size() != E + 1
```

e a resposta para essa instância será:

```text
Impossible
```

---

# 9. Complexidade

Sejam:

* `V` o número de vértices;
* `E` o número de arestas.

## 9.1. Representação do grafo

A lista de adjacência armazena cada vértice e cada aresta uma vez.

Portanto:

```text
O(V + E)
```

de memória é utilizada para a representação do grafo.

Os vetores de `indegree` e `outdegree` utilizam:

```text
O(V)
```

memória adicional.

---

## 9.2. Tempo

A construção da lista de adjacência percorre as `E` arestas:

```text
O(E)
```

A análise dos graus percorre os `V` vértices:

```text
O(V)
```

A verificação de conectividade percorre os vértices e as arestas:

```text
O(V + E)
```

O algoritmo de Hierholzer percorre cada aresta no máximo uma vez:

```text
O(E)
```

Assim, o tempo total permanece:

```text
O(V + E)
```

---

## 9.3. Memória auxiliar

Separando a memória utilizada para representar o grafo da memória utilizada pelo algoritmo:

### Representação do grafo

```text
O(V + E)
```

### Memória auxiliar

Vetores de graus:

```text
O(V)
```

Pilha:

```text
O(V + E)
```

Caminho:

```text
O(E + 1)
```

Portanto, a memória auxiliar é:

```text
O(V + E)
```

e a memória total também é:

```text
O(V + E)
```

---

# 10. Justificativa da estratégia

O problema exige que cada aresta seja utilizada **exatamente uma vez**. Por isso, uma DFS tradicional não é suficiente para construir diretamente a resposta, pois seu objetivo principal é explorar os vértices e determinar alcançabilidade.

O algoritmo de **Hierholzer** é adequado porque foi desenvolvido especificamente para construir caminhos eulerianos.

A utilização de uma pilha permite percorrer as arestas disponíveis e retornar a vértices anteriores quando ainda existem arestas que precisam ser incorporadas ao caminho.

A análise de `indegree` e `outdegree` permite identificar previamente a estrutura necessária para a existência do caminho.

A verificação final de:

```text
path.size() == E + 1
```

garante que todas as arestas foram efetivamente utilizadas na construção.

Dessa forma, a estratégia combina:

* **lista de adjacência** para representar o grafo;
* **indegree/outdegree** para reconhecer a propriedade estrutural;
* **DFS/conectividade** para verificar se as arestas pertencem à mesma região relevante;
* **pilha** para a execução iterativa;
* **Hierholzer** para construir o caminho;
* **verificação de `E + 1` vértices** para validar a solução.

A estratégia possui complexidade linear:

```text
O(V + E)
```

tanto para o processamento do grafo quanto para a construção do caminho.
