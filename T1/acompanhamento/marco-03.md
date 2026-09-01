# Marco 3 — Aplicação básica de DFS

Este marco aplica manualmente o algoritmo de **Busca em Profundidade (DFS)** sobre uma instância pequena do problema **C. Kefa e Parque**, evidenciando estados de visita, árvore de busca, tempos de descoberta/término, alcançabilidade, predecessores e a adaptação necessária para resolver o problema real.

---

## Instância utilizada

Reaproveitando a instância pequena definida no Marco 1:

```
5 1
1 0 1 0 0
1 2
1 3
2 4
2 5
```

* `n = 5`, `m = 1`
* Gatos: vértice 1 (gato), vértice 2 (sem gato), vértice 3 (gato), vértice 4 (sem gato), vértice 5 (sem gato)
* Raiz: vértice 1

Representação da árvore (rótulo indica se o vértice tem gato):

```
        1 (gato)
       /        \
     2 (—)      3 (gato)
    /    \
  4 (—)  5 (—)
```

Ordem de visita dos vizinhos adotada na execução manual: sempre em ordem crescente de índice (1 → 2 antes de 1 → 3; 2 → 4 antes de 2 → 5), conforme a ordem em que as arestas aparecem na entrada.

---

## 1. Execução manual do DFS

Execução do DFS clássico (sem qualquer adaptação ao problema ainda), partindo da raiz (vértice 1):

| Passo | Ação                          | Pilha de chamadas ativa |
|------:|-------------------------------|--------------------------|
| 1     | Visita 1 (raiz)               | [1]                      |
| 2     | Visita 2 (filho de 1)         | [1, 2]                   |
| 3     | Visita 4 (filho de 2)         | [1, 2, 4]                |
| 4     | 4 não tem filhos → finaliza 4 | [1, 2]                   |
| 5     | Visita 5 (filho de 2)         | [1, 2, 5]                |
| 6     | 5 não tem filhos → finaliza 5 | [1, 2]                   |
| 7     | 2 não tem mais filhos → finaliza 2 | [1]                 |
| 8     | Visita 3 (filho de 1)         | [1, 3]                   |
| 9     | 3 não tem filhos → finaliza 3 | [1]                      |
| 10    | 1 não tem mais filhos → finaliza 1 | []                   |

---

## 2. Estados de visita

Cada vértice passa por três estados clássicos do DFS:

* **Branco** — ainda não descoberto;
* **Cinza** — descoberto, mas com descendentes ainda em processamento (está na pilha de recursão);
* **Preto** — finalizado, todos os descendentes já processados.

| Tempo | Evento          | Estado resultante do vértice |
|------:|-----------------|-------------------------------|
| t=1   | descobre 1      | 1 → cinza                     |
| t=2   | descobre 2      | 2 → cinza                     |
| t=3   | descobre 4      | 4 → cinza                     |
| t=4   | finaliza 4      | 4 → preto                     |
| t=5   | descobre 5      | 5 → cinza                     |
| t=6   | finaliza 5      | 5 → preto                     |
| t=7   | finaliza 2      | 2 → preto                     |
| t=8   | descobre 3      | 3 → cinza                     |
| t=9   | finaliza 3      | 3 → preto                     |
| t=10  | finaliza 1      | 1 → preto                     |

Não há vértices que permaneçam brancos ao final, pois a árvore é conexa e todos os vértices são alcançáveis a partir da raiz.

---

## 3. Árvore de busca (árvore DFS)

Como o grafo de entrada já é uma árvore, a árvore de busca gerada pelo DFS **coincide exatamente** com a árvore original — não existem arestas de retorno (*back edges*), de avanço (*forward edges*) nem de cruzamento (*cross edges*), apenas arestas de árvore (*tree edges*):

```
1
├── 2
│   ├── 4
│   └── 5
└── 3
```

Arestas de árvore identificadas: (1,2), (1,3), (2,4), (2,5).

---

## 4. Tempos de descoberta e término

| Vértice | Descoberta `d[v]` | Término `f[v]` | Intervalo `[d, f]` |
|:-------:|:------------------:|:---------------:|:--------------------:|
| 1       | 1                   | 10               | [1, 10]               |
| 2       | 2                   | 7                | [2, 7]                 |
| 3       | 8                   | 9                | [8, 9]                 |
| 4       | 3                   | 4                | [3, 4]                 |
| 5       | 5                   | 6                | [5, 6]                 |

Observa-se a propriedade de **aninhamento de intervalos** (*parenthesis theorem*): o intervalo de cada filho está totalmente contido no intervalo do pai (ex.: `[2,7]` de 2 contém `[3,4]` de 4 e `[5,6]` de 5; `[1,10]` de 1 contém todos os demais).

---

## 5. Alcançabilidade

A partir da raiz (vértice 1), o conjunto de vértices alcançáveis é:

```
alcançáveis(1) = {1, 2, 3, 4, 5}
```

Ou seja, todos os vértices da árvore são alcançáveis a partir de 1 — resultado esperado, já que a entrada garante que o grafo é uma árvore (conexa por definição).

Essa noção "genérica" de alcançabilidade (existe ou não caminho) não é, sozinha, suficiente para o problema: o que importa não é apenas *se* o restaurante é alcançável, mas se ele é alcançável **respeitando a restrição de gatos consecutivos**. Isso é tratado na adaptação da Seção 7.

---

## 6. Predecessores

A tabela de predecessores (pai de cada vértice na árvore de busca) é:

| Vértice | Predecessor (`pai`) |
|:-------:|:---------------------:|
| 1       | — (raiz)               |
| 2       | 1                      |
| 3       | 1                      |
| 4       | 2                      |
| 5       | 2                      |

Esses predecessores permitem reconstruir o caminho da raiz até qualquer vértice, por exemplo:
- caminho até 4: `4 → 2 → 1` (invertido: `1 → 2 → 4`)
- caminho até 3: `3 → 1` (invertido: `1 → 3`)

---

## 7. Aplicabilidade ao problema

O DFS é diretamente aplicável ao problema porque:

* O parque **é** uma árvore enraizada em 1 (a casa de Kefa), então o DFS percorre naturalmente todo caminho da raiz até cada vértice exatamente uma vez;
* Os **predecessores** gerados pelo DFS correspondem exatamente ao caminho único da casa de Kefa até qualquer restaurante (folha), permitindo verificar a condição de gatos consecutivos ao longo desse caminho;
* Como cada vértice é visitado uma única vez, o DFS garante a complexidade linear `O(n)` exigida pelas restrições do problema (`n ≤ 10^5`);
* As **folhas** identificadas durante o DFS (vértices sem filhos) são exatamente os candidatos a restaurante que precisam ser contabilizados.

Entretanto, o DFS "puro" (estados de visita, tempos de descoberta/término) resolve apenas alcançabilidade genérica — ele não sabe, por si só, quando um caminho deve ser descartado por causa dos gatos. Por isso é necessária uma adaptação pontual.

---

## 8. Adaptação parcial do DFS

Adaptação proposta em relação ao DFS clássico:

1. **Estado extra por chamada**: além do vértice atual, a recursão carrega o valor `gatosConsecutivos`, representando quantos vértices com gato apareceram em sequência no caminho da raiz até o vértice atual.
   - Se `a[v] == 1`: `gatosConsecutivos = gatosConsecutivos(pai) + 1`
   - Se `a[v] == 0`: `gatosConsecutivos = 0`

2. **Poda antecipada (early pruning)**: se, ao visitar um vértice `v`, `gatosConsecutivos > m`, a recursão **não desce mais** para os filhos de `v` — o ramo inteiro é descartado, pois nenhum descendente poderia gerar um caminho válido (a contagem de gatos consecutivos só aumenta ou reinicia, nunca "corrige" o excesso já ocorrido no caminho).

3. **Contagem da resposta**: se `v` é folha (não tem filhos) **e** `gatosConsecutivos ≤ m` no momento em que `v` é alcançado, `v` é um restaurante válido e o contador de resposta é incrementado.

Essa é uma adaptação **parcial**: a estrutura de percurso (ordem de visita, uso de pilha de recursão, marcação de vértices visitados, geração da árvore de busca e dos predecessores) permanece idêntica ao DFS clássico. O que muda é apenas a informação extra carregada em cada chamada e uma condição de corte. Os tempos de descoberta/término, por si, não são usados na solução final — servem aqui apenas para evidenciar didaticamente o funcionamento do DFS (Seções 1–6); o que realmente importa na resolução é a ordem de visita e os predecessores/caminho.

### Simulação da adaptação na instância pequena (m = 1)

| Vértice | `a[v]` | gatosConsecutivos | ≤ m? | É folha? | Restaurante válido? |
|:-------:|:------:|:-------------------:|:----:|:--------:|:---------------------:|
| 1       | 1      | 1                    | sim  | não      | —                      |
| 2       | 0      | 0                    | sim  | não      | —                      |
| 4       | 0      | 0                    | sim  | **sim**  | ✅ válido               |
| 5       | 0      | 0                    | sim  | **sim**  | ✅ válido               |
| 3       | 1      | 2                    | não  | **sim**  | ❌ inválido             |

**Resultado da simulação: 2 restaurantes válidos**, coincidindo com o resultado esperado do Marco 1.

---

## 9. Pseudocódigo do DFS adaptado

```
DFS(v, pai, gatosConsecutivos):
    se a[v] == 1:
        gatosConsecutivos = gatosConsecutivos + 1
    senão:
        gatosConsecutivos = 0

    se gatosConsecutivos > m:
        return   // poda: nenhum descendente pode ser válido

    se v é folha (sem filhos além do pai):
        resposta = resposta + 1
        return

    para cada vizinho u de v:
        se u != pai:
            DFS(u, v, gatosConsecutivos)

// chamada inicial:
DFS(1, -1, 0)
```

Complexidade: `O(n)`, pois cada vértice é visitado exatamente uma vez, com trabalho constante por vértice.
