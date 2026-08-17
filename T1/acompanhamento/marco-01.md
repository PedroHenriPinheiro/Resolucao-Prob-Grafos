# Modelagem do Problema

## Entrada

A entrada é composta por:

* Dois inteiros `n` e `m`, em que:

  * `n` representa a quantidade de vértices da árvore;
  * `m` representa o número máximo de vértices consecutivos com gatos permitido em um caminho.
* Um vetor `a` de tamanho `n`, onde:

  * `a[i] = 1` indica que o vértice `i` possui um gato;
  * `a[i] = 0` indica que o vértice `i` não possui gato.
* `n - 1` linhas contendo pares de inteiros `(u, v)`, representando as arestas da árvore.

## Saída

A saída consiste em um único número inteiro correspondente à quantidade de restaurantes (vértices folha) que podem ser alcançados a partir da raiz sem que o caminho contenha mais de `m` vértices consecutivos com gatos.

## Restrições

* `2 ≤ n ≤ 10^5`
* `1 ≤ m ≤ n`
* O grafo possui exatamente `n - 1` arestas.
* Cada vértice possui valor `0` (sem gato) ou `1` (com gato).
* Devido ao limite de `n`, a solução deve possuir complexidade linear, aproximadamente **O(n)**.

## Vértices

Os vértices representam os locais do parque:

* O vértice `1` representa a casa de Kefa e é a raiz da árvore.
* Os demais vértices representam pontos do parque.
* Os vértices folha representam os restaurantes.

## Arestas

Cada aresta representa um caminho entre dois locais do parque.

Como o grafo possui `n - 1` arestas e é conexo, ele caracteriza uma árvore.

## Tipo do Grafo

O problema é modelado como uma:

* Árvore;
* Não direcionada;
* Conexa;
* Enraizada no vértice `1`.

Embora a entrada forneça arestas não direcionadas, durante a resolução a árvore é tratada como enraizada no vértice `1`.

## Instância Pequena

### Entrada

```text
5 1
1 0 1 0 0
1 2
1 3
2 4
2 5
```

### Representação da árvore

```text
      1(gato)
     / \
    2   3(gato) Como aqui já ficou consecutivo, nem precisariamos percorrer o restante caso houvessem...
   / \  
  4   5
```

## Resultado Esperado

As folhas da árvore são os vértices `3`, `4` e `5`.

* Caminho `1 → 3`: possui dois gatos consecutivos (`1` e `3`), excedendo `m = 1`. Portanto, o restaurante não pode ser visitado.
* Caminho `1 → 2 → 4`: a sequência de gatos é interrompida no vértice `2`, resultando em no máximo um gato consecutivo. O restaurante pode ser visitado.
* Caminho `1 → 2 → 5`: segue a mesma condição do caminho anterior e também é válido.

**Resposta esperada:**

```text
2
```

## Hipótese Inicial

A solução proposta consiste em percorrer a árvore utilizando **Busca em Profundidade (DFS)** a partir da raiz.

Durante o percurso, mantém-se a quantidade de vértices consecutivos com gatos no caminho atual. Quando um vértice sem gato é encontrado, essa contagem é reiniciada. Caso o número de gatos consecutivos ultrapasse o limite `m`, o ramo é descartado, pois nenhum de seus descendentes poderá gerar um caminho válido.

Ao alcançar um vértice folha cujo caminho permaneça dentro da restrição, esse restaurante é contabilizado na resposta.

Essa estratégia percorre cada vértice apenas uma vez, resultando em complexidade de tempo **O(n)**, adequada para os limites do problema.
