# Marco 4 – Aplicação básica de BFS e conclusão

## Execução manual utilizando BFS

Embora a solução final utilize Busca em Profundidade (DFS), é importante verificar como a Busca em Largura (BFS) percorreria a árvore.

Considerando a instância:

```text
4 1
1 1 0 0

1 2
1 3
1 4
```

A árvore pode ser representada como:

```text
      1(gato)
    /   |   \
 2(gato) 3   4
```

A BFS visita os vértices por níveis.

### Passo a passo

Inicialmente:

```text
Fila = [1]
```

Remove-se o vértice 1 da fila e visitam-se seus filhos:

```text
Fila = [2, 3, 4]
```

Em seguida:

* visita o vértice 2;
* depois o vértice 3;
* por último o vértice 4.

A ordem de visita é:

```text
1 → 2 → 3 → 4
```

Durante essa execução:

* o caminho até o vértice 2 possui dois gatos consecutivos, ultrapassando o limite m = 1;
* os caminhos até os vértices 3 e 4 possuem apenas um gato consecutivo.

Assim, apenas os restaurantes representados pelos vértices 3 e 4 podem ser visitados.

Resultado:

```text
2
```

---

# Níveis, distâncias e predecessores

A BFS permite calcular naturalmente os níveis da árvore, as distâncias em número de arestas e o predecessor de cada vértice.

| Vértice | Nível | Distância da raiz | Predecessor |
| ------- | ----- | ----------------- | ----------- |
| 1       | 0     | 0                 | —           |
| 2       | 1     | 1                 | 1           |
| 3       | 1     | 1                 | 1           |
| 4       | 1     | 1                 | 1           |

Como a árvore é percorrida em largura, todos os vértices do mesmo nível são visitados antes dos níveis seguintes.

---

# Comparação entre DFS e BFS

As duas estratégias percorrem todos os vértices da árvore em tempo linear, porém apresentam características diferentes.

| DFS                                                                | BFS                                                                                 |
| ------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| Explora um ramo até o fim antes de retornar.                       | Explora a árvore por níveis.                                                        |
| Pode ser implementada com recursão ou pilha.                       | Utiliza obrigatoriamente uma fila.                                                  |
| Facilita o controle de informações acumuladas ao longo do caminho. | É indicada para problemas envolvendo menores distâncias em grafos não ponderados.   |
| Permite interromper imediatamente um ramo inválido.                | Mesmo que um ramo seja inválido, outros vértices do mesmo nível permanecem na fila. |

---

# Justificativa da escolha da DFS

Neste problema, a principal informação que precisa ser mantida é a quantidade de gatos consecutivos no caminho atual.

A DFS é mais adequada porque acompanha naturalmente um único caminho da raiz até uma folha. Dessa forma:

* a contagem de gatos consecutivos é atualizada à medida que o percurso avança;
* quando um vértice sem gato é encontrado, a contagem é reiniciada;
* se a quantidade de gatos consecutivos ultrapassar o limite `m`, o restante daquele ramo é descartado imediatamente (poda), evitando visitas desnecessárias.

Embora a BFS também possa resolver o problema armazenando, para cada vértice da fila, a quantidade de gatos consecutivos até aquele ponto, ela exige manter mais informações simultaneamente e não oferece vantagem para esse tipo de percurso.

Assim, a DFS apresenta uma implementação mais simples e direta para este problema.

---

# Adaptação e integração da solução

A implementação final foi baseada em uma Busca em Profundidade (DFS) sobre a árvore enraizada no vértice 1.

Durante o percurso foram realizadas as seguintes adaptações:

* construção da lista de adjacência para representar a árvore;
* controle do vértice pai para evitar retornar pelo mesmo caminho;
* atualização da quantidade de gatos consecutivos;
* reinicialização dessa contagem quando um vértice sem gato é encontrado;
* interrupção da exploração quando o limite `m` é ultrapassado;
* contabilização apenas dos vértices folha cujo caminho permaneceu válido.

Cada vértice é visitado apenas uma única vez, garantindo eficiência mesmo para os maiores casos de teste.

---

# Testes realizados

Foram realizados testes utilizando:

* os exemplos fornecidos pelo enunciado;
* árvores contendo apenas um caminho;
* árvores onde todos os vértices possuem gatos;
* árvores sem gatos;
* árvores em que apenas alguns ramos ultrapassam o limite de gatos consecutivos.

Em todos os casos, a quantidade de restaurantes encontrada coincidiu com o resultado esperado.

---

# Complexidade

A lista de adjacência é construída em tempo O(n).

Durante a DFS, cada vértice e cada aresta são visitados apenas uma vez.

Assim, a complexidade da solução é:

* Tempo: **O(n)**
* Espaço: **O(n)**

Essa complexidade atende às restrições do problema, em que `n` pode assumir valores de até `10^5`.

---

# Submissão

Após a implementação, o programa foi submetido ao sistema de avaliação do Codeforces.

Resultado obtido:

```text
Accepted
```

Isso confirma que a solução produz respostas corretas para todos os casos de teste utilizados pela plataforma, respeitando também os limites de tempo e memória.

---

# Conclusão

A análise do problema mostrou que tanto a Busca em Largura (BFS) quanto a Busca em Profundidade (DFS) são capazes de percorrer toda a árvore em tempo linear.

Entretanto, devido à necessidade de acompanhar continuamente a sequência de gatos ao longo de cada caminho da raiz até uma folha e de interromper imediatamente ramos que violam a restrição estabelecida, a DFS mostrou-se mais adequada. Sua implementação é mais simples, exige menos controle de estado durante a execução e permite realizar podas de forma natural.

Os testes realizados confirmaram o correto funcionamento da solução, e a submissão com resultado **Accepted** comprova que o algoritmo atende integralmente aos requisitos do problema.
