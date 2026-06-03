"""
SENTINEL AGRO — Força Bruta
"""

import time
import itertools


class ForcaBruta:


    def __init__(self, grafo):
        self.grafo = grafo
        self.contador_chamadas = 0
        self.contador_caminhos = 0
        self.historico_custos = []

    def resetar_contadores(self):
        self.contador_chamadas = 0
        self.contador_caminhos = 0
        self.historico_custos = []

    def encontrar_caminho_minimo(self, origem, destino):
        """
        Encontra o caminho de menor custo entre origem e destino
        enumerando TODOS os caminhos possíveis.

        Complexidade: O(V!) no pior caso — inviável para N > 12.
        """
        self.resetar_contadores()
        melhor = {'custo': float('inf'), 'caminho': []}
        visitados = set()

        self._backtrack(origem, destino, visitados, [origem], 0, melhor)

        return melhor['caminho'], melhor['custo'], {
            'chamadas_recursivas': self.contador_chamadas,
            'caminhos_avaliados': self.contador_caminhos,
            'custos': self.historico_custos
        }

    def _backtrack(self, atual, destino, visitados, caminho_atual, custo_atual, melhor):
        self.contador_chamadas += 1
        visitados.add(atual)

        if atual == destino:
            self.contador_caminhos += 1
            self.historico_custos.append(custo_atual)
            if custo_atual < melhor['custo']:
                melhor['custo'] = custo_atual
                melhor['caminho'] = list(caminho_atual)
            visitados.remove(atual)
            return

        for vizinho, peso in self.grafo.vizinhos(atual):
            if vizinho not in visitados:
                caminho_atual.append(vizinho)
                self._backtrack(vizinho, destino, visitados,
                                caminho_atual, custo_atual + peso, melhor)
                caminho_atual.pop()

        visitados.remove(atual)

    def mst_forca_bruta(self, vertices_ids):
        """
        Encontra a MST ótima por enumeração de todas as árvores geradoras.
        Apenas para N ≤ 10 vértices.
        """
        self.resetar_contadores()

        arestas_subgrafo = []
        ids_set = set(vertices_ids)
        for u, v, peso in self.grafo.arestas:
            if u in ids_set and v in ids_set:
                arestas_subgrafo.append((u, v, peso))

        n = len(vertices_ids)
        melhor_mst = {'custo': float('inf'), 'arestas': []}

        for combo in itertools.combinations(arestas_subgrafo, n - 1):
            self.contador_chamadas += 1
            if self._forma_arvore_geradora(list(combo), vertices_ids):
                custo = sum(e[2] for e in combo)
                self.contador_caminhos += 1
                self.historico_custos.append(custo)
                if custo < melhor_mst['custo']:
                    melhor_mst['custo'] = custo
                    melhor_mst['arestas'] = list(combo)

        return melhor_mst['arestas'], melhor_mst['custo'], {
            'combinacoes_avaliadas': self.contador_chamadas,
            'arvores_validas': self.contador_caminhos
        }

    def _forma_arvore_geradora(self, arestas, vertices_ids):
        """Verifica se as arestas formam uma árvore geradora (conectada e acíclica)."""
        if not arestas:
            return False
        pai = {v: v for v in vertices_ids}

        def encontrar(x):
            while pai[x] != x:
                pai[x] = pai[pai[x]]
                x = pai[x]
            return x

        def unir(x, y):
            rx, ry = encontrar(x), encontrar(y)
            if rx == ry:
                return False  
            pai[rx] = ry
            return True

        for u, v, _ in arestas:
            if not unir(u, v):
                return False

        raizes = {encontrar(v) for v in vertices_ids}
        return len(raizes) == 1