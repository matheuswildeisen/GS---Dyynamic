"""
SENTINEL AGRO — Algoritmo Guloso

"""

import heapq


class Dijkstra:


    def __init__(self, grafo, bst=None):
        self.grafo = grafo
        self.bst = bst             
        self.passos_gulosos = []   
    def executar(self, origem):
        """
        Executa Dijkstra a partir da origem.
        Retorna distâncias mínimas e predecessores para reconstrução de caminho.
        """
        self.passos_gulosos = []

        dist = {v: float('inf') for v in self.grafo.vertices}
        dist[origem] = 0

        pred = {v: None for v in self.grafo.vertices}

        heap = [(0, origem)]

        finalizados = set()

        while heap:
            custo_atual, u = heapq.heappop(heap)  

            if u in finalizados:
                continue
            finalizados.add(u)

            self.passos_gulosos.append({
                'municipio': self.grafo.get_nome(u),
                'custo_chegada': custo_atual,
                'risco': self.grafo.get_risco(u)
            })

            for vizinho, peso in self.grafo.vizinhos(u):
                if vizinho not in finalizados:
                    novo_custo = custo_atual + peso
                    if novo_custo < dist[vizinho]:
                        dist[vizinho] = novo_custo
                        pred[vizinho] = u
                        heapq.heappush(heap, (novo_custo, vizinho))

        return dist, pred

    def reconstruir_caminho(self, pred, destino):
        """Reconstrói o caminho mínimo usando o dicionário de predecessores."""
        caminho = []
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = pred[atual]
        return list(reversed(caminho))

    def municipios_criticos_priorizados(self, r_min=0.7):
        """
        Consulta BST para obter municípios com alto risco (>= r_min).
        Retorna lista ordenada por risco decrescente para priorização do atendimento.
        """
        if self.bst is None:
            return []
        criticos = self.bst.buscar_intervalo(r_min, 1.0)
        return sorted(criticos, key=lambda m: m[2], reverse=True)

    def rota_atendimento_prioritario(self, origem, r_min=0.7):
        """
        Calcula a rota de menor custo da origem até cada município crítico,
        integrando BST (identificação de alvos) + Dijkstra (rota mínima).

        Retorna lista de (município, custo, caminho) ordenada por custo.
        """
        dist, pred = self.executar(origem)
        criticos = self.municipios_criticos_priorizados(r_min)

        rotas = []
        for mun in criticos:
            id_mun = mun[0]
            if dist[id_mun] < float('inf'):
                caminho = self.reconstruir_caminho(pred, id_mun)
                rotas.append({
                    'municipio': mun[1],
                    'id': id_mun,
                    'risco': mun[2],
                    'custo_rota': dist[id_mun],
                    'caminho': caminho
                })

        rotas.sort(key=lambda r: (-r['risco'], r['custo_rota']))
        return rotas


class Prim:


    def __init__(self, grafo):
        self.grafo = grafo

    def executar(self, inicio):
        """Constrói a MST a partir do vértice inicial."""
        visitados = set([inicio])
        mst_arestas = []
        custo_total = 0

        candidatas = []
        for vizinho, peso in self.grafo.vizinhos(inicio):
            heapq.heappush(candidatas, (peso, inicio, vizinho))

        while candidatas and len(visitados) < len(self.grafo.vertices):
            peso, u, v = heapq.heappop(candidatas)   # decisão gulosa

            if v in visitados:
                continue

            visitados.add(v)
            mst_arestas.append((u, v, peso))
            custo_total += peso

            for vizinho, p in self.grafo.vizinhos(v):
                if vizinho not in visitados:
                    heapq.heappush(candidatas, (p, v, vizinho))

        return mst_arestas, custo_total
