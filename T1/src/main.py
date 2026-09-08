import sys
sys.setrecursionlimit(200000)

n, m = map(int, input().split())

cats = [0] + list(map(int, input().split()))

adj = [[] for _ in range(n + 1)]

for _ in range(n - 1):
    u, v = map(int, input().split())
    adj[u].append(v)
    adj[v].append(u)

ans = 0

def dfs(v, pai, consecutivos):
    global ans

    if cats[v]:
        consecutivos += 1
    else:
        consecutivos = 0

    if consecutivos > m:
        return

    folha = True

    for viz in adj[v]:
        if viz != pai:
            folha = False
            dfs(viz, v, consecutivos)

    if folha:
        ans += 1

dfs(1, 0, 0)

print(ans)