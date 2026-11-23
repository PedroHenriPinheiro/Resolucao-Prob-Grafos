# Marco 1 — Formulação

## Resumo do problema

Precisamos encontrar a rota de menor custo entre a cidade `1` (Syrjälä) e a cidade `n` (Metsälä).

Existe um único cupom que pode ser utilizado em um dos voos da rota. Ao utilizá-lo em um voo de preço `c`, seu custo passa a ser:

`floor(c / 2)`

O cupom só pode ser utilizado uma vez.

## Entrada

- `n`: número de cidades;
- `m`: número de voos;
- `a b c`: voo direcionado de `a` para `b` com custo `c`.

Restrições principais:

- `2 ≤ n ≤ 10⁵`
- `1 ≤ m ≤ 2 · 10⁵`
- `1 ≤ c ≤ 10⁹`
- É garantida a existência de uma rota de `1` até `n`.

## Saída

Um inteiro representando o menor custo possível para viajar de `1` até `n`, utilizando o cupom uma vez.

## Modelagem como grafo

- **Vértices:** cidades;
- **Arestas:** voos;
- **Direção:** `a → b`;
- **Peso:** preço `c` do voo;
- **Origem:** vértice `1`;
- **Destino:** vértice `n`.

Ao utilizar o cupom em uma aresta de custo `c`:

`c → floor(c / 2)`

## Objetivo

Minimizar o custo total de um caminho entre `1` e `n`, escolhendo uma das arestas do caminho para receber o desconto.

## Família do problema

O problema pertence à família de **caminho mínimo em grafos direcionados e ponderados**, com uma restrição adicional: o uso único de um cupom que altera o peso de uma aresta.

Não é um problema de árvore geradora mínima, pois não precisamos conectar todos os vértices, apenas encontrar o menor caminho entre dois vértices específicos.