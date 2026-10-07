import sys

sys.setrecursionlimit(300000)


class Digraph:

    def __init__(self, V):
        self.V = V
        self.E = 0
        self._adj = [[] for _ in range(V)]
        self._indegree = [0] * V

    def add_edge(self, v, w):
        if 0 <= v < self.V and 0 <= w < self.V:
            self._adj[v].append(w)
            self._indegree[w] += 1
            self.E += 1

    def adj(self, v):
        return self._adj[v]

    def outdegree(self, v):
        return len(self._adj[v])

    def indegree(self, v):
        return self._indegree[v]


class DirectedEulerianPath:
    # calcula usando Algoritmo de Hierholzer em O(V + E)

    def __init__(self, digraph: Digraph):
        self._path = None

        if digraph.E == 0:
            return

        # indegree e outdegree
        deficit = 0
        s = self._non_isolated_vertex(digraph)

        for v in range(digraph.V):
            out_deg = digraph.outdegree(v)
            in_deg = digraph.indegree(v)

            if out_deg > in_deg:
                deficit += out_deg - in_deg
                s = v
            elif in_deg > out_deg + 1:
                return

        if deficit > 1:
            return

        if s == -1:
            s = 0

        adj_iterators = [iter(digraph.adj(v)) for v in range(digraph.V)]

        # Algoritmo de Hierholzer
        stack = [s]
        self._path = []

        while stack:
            v = stack.pop()
            while True:
                try:
                    w = next(adj_iterators[v])
                    stack.append(v)
                    v = w
                except StopIteration:
                    break
            self._path.append(v)

        self._path.reverse()

        # substitui o uso da BreadthFirstPaths/BreadthFirstDirectedPaths
        if len(self._path) != digraph.E + 1:
            self._path = None

    def path(self):
        return self._path

    def has_eulerian_path(self):
        return self._path is not None

    @staticmethod
    def _non_isolated_vertex(digraph: Digraph):
        for v in range(digraph.V):
            if digraph.outdegree(v) > 0:
                return v
        return -1


def solve():
    
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    idx = 0
    while idx < len(input_data):
        V = int(input_data[idx])
        E = int(input_data[idx + 1])
        idx += 2

        # condição de encerramento do problema
        if V == 0 and E == 0:
            break

        g = Digraph(V)
        for _ in range(E):
            u = int(input_data[idx])
            v = int(input_data[idx + 1])
            g.add_edge(u, v)
            idx += 2

        eulerian = DirectedEulerianPath(g)

        if eulerian.has_eulerian_path():
            print(" ".join(map(str, eulerian.path())))
        else:
            print("Impossible")


if __name__ == "__main__":
    solve()
