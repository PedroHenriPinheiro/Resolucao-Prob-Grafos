# Representação Computacional

## Escolha da Representação Computacional

Para a modelagem do problema, analisou-se as três abordagens clássicas de representação de grafos:

| Representação | Adequação ao Problema |
| :--- | :--- |
| **Matriz de Adjacência** | **Inviável**: Com $N = 10^5$, alocaria $\approx 10^{10}$ posições de memória, estourando o limite de recursos (*Memory Limit Exceeded*). |
| **Representação Implícita** | **Inviável**: Aplicável apenas a grafos com padrões geométricos ou matemáticos fixos (ex: grades 2D, árvores binárias completas). A topologia deste problema é arbitrária. |
| **Lista de Adjacência** | **Ideal**: Armazena apenas as arestas existentes. Como em árvores $E = N - 1$, o consumo espacial e o tempo de construção são estritamente lineares, adequando-se às restrições. |

**Decisão:** Utilização de **Lista de Adjacência** dinâmica baseada em vetores.

---

## Leitura da Entrada e Construção do Grafo

A construção do grafo consiste em converter a entrada de texto não estruturada em uma estrutura navegável em memória:

**1. Ajuste de Indexação (*1-based*):** Como os vértices do problema são numerados de $1$ a $N$, aloca-se o vetor de listas com tamanho $N + 1$, preservando o índice $0$ como elemento nulo.

**2. Atribuição de Atributos:** O vetor $a$ armazena a presença de gatos ($0$ ou $1$) associado diretamente ao índice de cada vértice.

**3. Inserção Bidirecional de Arestas:** Sendo um grafo não direcionado, cada linha $(u, v)$ resulta na inserção de $v$ na lista de $u$ e de $u$ na lista de $v$.

O código realiza a leitura da entrada, constrói a lista de adjacência e calcula as principais medidas estruturais do grafo (número de vértices, arestas, graus e identificação de folhas).

### Entrada

```text
5 1
1 0 1 0 0
1 2
1 3
2 4
2 5
```

### Saída 

```text
=== SAÍDA / RESULTADOS ===
Número de vértices (N): 5
Número de arestas (E): 4
Grau mínimo: 1
Grau máximo: 3
Grau médio: 1.60
Densidade: 0.40
Quantidade de folhas (restaurantes): 3
Vértices folha: [3, 4, 5]

--- Lista de Adjacência ---
Vértice 1 (Gato: 1): [2, 3]
Vértice 2 (Gato: 0): [1, 4, 5]
Vértice 3 (Gato: 1): [1]
Vértice 4 (Gato: 0): [2]
Vértice 5 (Gato: 0): [2]
```

---

## Medidas Estruturais Pertinentes (Unidade I)

1. **Vértices ($N = 5$) e Arestas ($E = 4$):** Confirma a relação $E = N - 1$, validando que a estrutura é uma árvore.

2. **Grau mínimo ($min = 1$) e Grau máximo ($máx = 3$):**

    1. **Vértice 1 (Raiz):** possui grau $2$ (vizinhos: 2 e 3);
    2. **Vértice 2:** possui grau $3$ (vizinhos: 1, 4 e 5);
    3. **Vértices 3, 4 e 5:** possuem grau $1$ cada, sendo mapeados corretamente como folhas (restaurantes do problema).

4. **Grau Médio ($1.60$):** Calculado dividindo a soma dos graus de todos os vértices pelo número total de vértices

5. **Densidade ($0.40$):** Mostra que sua densidade é de 40%. É um grafo esparso, pois toda árvore, por definição estrutural, é um grafo esparso.

---

## Validação da Representação com a Instância Pequena

**1. Validação das Arestas (Conexões):** 

**No enunciado:** 
O vértice 1 se conecta com 2 e 3. 
O vértice 2 se conecta com 4 e 5.

**Na saída:** 
```text
Vértice 1: [2, 3]
Vértice 2: [1, 4, 5]
```

**Conclusão:** As conexões bidirecionais foram inseridas sem perdas.

**2. Validação dos Atributos (Gatos):**

**No enunciado:**
O vetor de gatos é 1 0 1 0 0 (gatos nos vértices 1 e 3).

**Na saída:**
```text
Vértice 1 (Gato: 1)
Vértice 2 (Gato: 0)
Vértice 3 (Gato: 1)
```

**Conclusão:** Os atributos foram vinculados aos vértices corretos (sem erros de offset ou deslocamento de índices).

**3. Validação dos Restaurantes (Folhas):**

**No enunciado:**
Os vértices do fim da árvore (restaurantes) são 3, 4 e 5.

**Na saída:**
```text
Vértices folha: [3, 4, 5]
```

**Conclusão:** O cálculo de grau identificou com $100\%$ de precisão onde estão as folhas do grafo.
