# Teremos um código muito bom aqui, vrau vrau
import sys

def carregar_grafo_e_medidas():
    print("--- DIGITE A ENTRADA ---")
    
    # 1. Lê N e M
    n, m = map(int, sys.stdin.readline().split())
    
    # 2. Lê a presença de gatos (1-based index)
    a = [0] + list(map(int, sys.stdin.readline().split()))
    
    # 3. Lê exatamente N - 1 arestas
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, sys.stdin.readline().split())
        adj[u].append(v)
        adj[v].append(u)
        
    # --- MEDIDAS ESTRUTURAIS ---
    num_vertices = n
    num_arestas = n - 1
    graus = [len(adj[i]) for i in range(1, n + 1)]
    
    # Folhas: grau 1 (desconsiderando a raiz 1 se N > 1)
    folhas = [i for i in range(1, n + 1) if len(adj[i]) == 1 and i != 1]
    
    print("\n=== SAÍDA / RESULTADOS ===")
    print(f"Número de vértices (N): {num_vertices}")
    print(f"Número de arestas (E): {num_arestas}")
    print(f"Grau mínimo: {min(graus)}")
    print(f"Grau máximo: {max(graus)}")
    print(f"Grau médio: {sum(graus) / num_vertices:.2f}")
    print(f"Densidade: {2 / n:.2f}")
    print(f"Quantidade de folhas (restaurantes): {len(folhas)}")
    print(f"Vértices folha: {folhas}")
    print("\n--- Lista de Adjacência ---")
    for i in range(1, n + 1):
        print(f"Vértice {i} (Gato: {a[i]}): {adj[i]}")

if __name__ == "__main__":
    carregar_grafo_e_medidas()
