"""
SENTINEL AGRO — Global Solution 2026
"""

import heapq
from collections import deque


def criar_municipio(id_mun, nome, indice_risco, custo_atendimento, populacao):
    """
    Cria um vértice do grafo como tupla imutável.
    Tupla escolhida pela imutabilidade e eficiência de memória.
    """
    return (id_mun, nome, indice_risco, custo_atendimento, populacao)


def criar_aresta(origem, destino, peso):
    """
    Cria uma aresta como tupla (u, v, peso).
    Peso = distância km entre municípios (dados sintéticos baseados em rotas reais).
    """
    return (origem, destino, peso)

class GrafoMunicipios:
    """
    Grafo ponderado não-direcionado representando municípios e rotas.
    Implementado como dicionário de listas de adjacência.

    Justificativa da representação:
    - Lista de adjacência: O(V + E) de espaço — eficiente para grafos esparsos
      como redes viárias municipais (cada município conecta a poucos vizinhos).
    - Matriz de adjacência exigiria O(V²), inviável para os 337 municípios do MATOPIBA.
    """

    def __init__(self):
        self.vertices = {}
        self.adjacencia = {}
        self.arestas = []

    def adicionar_vertice(self, municipio_tupla):
        """Adiciona município ao grafo. O(1)"""
        id_mun = municipio_tupla[0]
        self.vertices[id_mun] = municipio_tupla
        if id_mun not in self.adjacencia:
            self.adjacencia[id_mun] = []

    def adicionar_aresta(self, u, v, peso):
        """Adiciona aresta bidirecional. O(1)"""
        self.adjacencia[u].append((v, peso))
        self.adjacencia[v].append((u, peso))
        self.arestas.append((u, v, peso))

    def vizinhos(self, u):
        """Retorna lista de vizinhos de u. O(grau(u))"""
        return self.adjacencia.get(u, [])

    def bfs(self, origem):
        """
        Busca em largura — usa deque (fila) para O(V+E).
        Retorna ordem de visita e distâncias em saltos.
        """
        visitados = set()
        fila = deque([origem])
        ordem = []
        distancias = {origem: 0}

        while fila:
            atual = fila.popleft()
            if atual in visitados:
                continue
            visitados.add(atual)
            ordem.append(atual)

            for vizinho, _ in self.vizinhos(atual):
                if vizinho not in visitados:
                    fila.append(vizinho)
                    if vizinho not in distancias:
                        distancias[vizinho] = distancias[atual] + 1

        return ordem, distancias

    def get_risco(self, id_mun):
        return self.vertices[id_mun][2]

    def get_custo(self, id_mun):
        return self.vertices[id_mun][3]

    def get_nome(self, id_mun):
        return self.vertices[id_mun][1]


class Node:
    """Nó da BST com chave = índice_risco e valor = tupla do município."""

    def __init__(self, municipio_tupla):
        self.risco = municipio_tupla[2]
        self.municipio = municipio_tupla
        self.esquerda = None
        self.direita = None


class BinarySearchTree:
    """
    BST de municípios ordenada por índice de risco (0.0 a 1.0).
    Permite consultas eficientes por faixa de risco — O(log N) no caso médio.

    Propriedade mantida: r_esquerda < r_pai < r_direita
    """

    def __init__(self):
        self.raiz = None
        self._tamanho = 0

    def inserir(self, municipio_tupla):
        """Insere município mantendo propriedade BST. O(log N) médio, O(N) pior caso."""
        self.raiz = self._inserir_rec(self.raiz, municipio_tupla)
        self._tamanho += 1

    def _inserir_rec(self, no, municipio_tupla):
        if no is None:
            return Node(municipio_tupla)
        risco = municipio_tupla[2]
        if risco < no.risco:
            no.esquerda = self._inserir_rec(no.esquerda, municipio_tupla)
        elif risco > no.risco:
            no.direita = self._inserir_rec(no.direita, municipio_tupla)
        else:
            no.direita = self._inserir_rec(no.direita, municipio_tupla)
        return no

    def buscar_intervalo(self, r_min, r_max):
        """
        Retorna todos os municípios com índice de risco em [r_min, r_max].
        O(log N + K) onde K = número de resultados.
        """
        resultado = []
        self._buscar_intervalo_rec(self.raiz, r_min, r_max, resultado)
        return resultado

    def _buscar_intervalo_rec(self, no, r_min, r_max, resultado):
        if no is None:
            return
        if no.risco >= r_min:
            self._buscar_intervalo_rec(no.esquerda, r_min, r_max, resultado)
        if r_min <= no.risco <= r_max:
            resultado.append(no.municipio)
        if no.risco <= r_max:
            self._buscar_intervalo_rec(no.direita, r_min, r_max, resultado)

    def percurso_in_order(self):
        """
        Retorna municípios em ordem crescente de risco.
        Usado para priorização na cobertura de atendimento. O(N).
        """
        resultado = []
        self._in_order_rec(self.raiz, resultado)
        return resultado

    def _in_order_rec(self, no, resultado):
        if no is None:
            return
        self._in_order_rec(no.esquerda, resultado)
        resultado.append(no.municipio)
        self._in_order_rec(no.direita, resultado)

    def altura(self):
        """Calcula altura da árvore. O(N)."""
        return self._altura_rec(self.raiz)

    def _altura_rec(self, no):
        if no is None:
            return 0
        return 1 + max(self._altura_rec(no.esquerda), self._altura_rec(no.direita))

    def remover(self, id_municipio):
        """Remove nó pelo id do município. O(log N) médio."""
        self.raiz, removido = self._remover_rec(self.raiz, id_municipio)
        if removido:
            self._tamanho -= 1
        return removido

    def _remover_rec(self, no, id_municipio):
        if no is None:
            return no, False

        removido = False
        if no.municipio[0] == id_municipio:
            removido = True

            if no.esquerda is None and no.direita is None:
                return None, removido

            if no.esquerda is None:
                return no.direita, removido
            if no.direita is None:
                return no.esquerda, removido

            sucessor = self._minimo(no.direita)
            no.risco = sucessor.risco
            no.municipio = sucessor.municipio
            no.direita, _ = self._remover_rec(no.direita, sucessor.municipio[0])
        elif id_municipio < no.municipio[0]:
            no.esquerda, removido = self._remover_rec(no.esquerda, id_municipio)
        else:
            no.direita, removido = self._remover_rec(no.direita, id_municipio)

        return no, removido

    def _minimo(self, no):
        while no.esquerda is not None:
            no = no.esquerda
        return no

    def __len__(self):
        return self._tamanho