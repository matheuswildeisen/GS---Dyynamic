
import pytest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / 'src'))

from data_structures import (GrafoMunicipios, BinarySearchTree,
                              criar_municipio, Node)
from brute_force import ForcaBruta
from greedy import Dijkstra, Prim
from performance_monitor import PerformanceMonitor


@pytest.fixture
def grafo_simples():
    """Grafo com 5 nós — controlável para validação exata."""
    g = GrafoMunicipios()
    muns = [
        criar_municipio(1, 'A', 0.9, 1000, 50000),
        criar_municipio(2, 'B', 0.5, 1200, 30000),
        criar_municipio(3, 'C', 0.7, 1100, 20000),
        criar_municipio(4, 'D', 0.3, 900,  15000),
        criar_municipio(5, 'E', 0.8, 1300, 40000),
    ]
    for m in muns:
        g.adicionar_vertice(m)
    g.adicionar_aresta(1, 2, 4)
    g.adicionar_aresta(1, 3, 2)
    g.adicionar_aresta(2, 4, 5)
    g.adicionar_aresta(3, 4, 1)
    g.adicionar_aresta(3, 5, 8)
    g.adicionar_aresta(4, 5, 3)
    return g

@pytest.fixture
def bst_simples():
    bst = BinarySearchTree()
    muns = [
        criar_municipio(10, 'X', 0.5, 1000, 10000),
        criar_municipio(20, 'Y', 0.8, 1500, 20000),
        criar_municipio(30, 'Z', 0.3, 800,  5000),
        criar_municipio(40, 'W', 0.9, 2000, 30000),
        criar_municipio(50, 'V', 0.6, 1200, 15000),
    ]
    for m in muns:
        bst.inserir(m)
    return bst

class TestGrafo:

    def test_adicionar_vertices(self, grafo_simples):
        assert len(grafo_simples.vertices) == 5

    def test_adjacencia_bidirecional(self, grafo_simples):
        vizinhos_1 = [v for v, _ in grafo_simples.vizinhos(1)]
        assert 2 in vizinhos_1 and 3 in vizinhos_1

    def test_bfs_conectado(self, grafo_simples):
        ordem, dist = grafo_simples.bfs(1)
        assert set(ordem) == {1, 2, 3, 4, 5}

    def test_risco_retornado(self, grafo_simples):
        assert grafo_simples.get_risco(1) == pytest.approx(0.9)


class TestBST:

    def test_tamanho(self, bst_simples):
        assert len(bst_simples) == 5

    def test_in_order_crescente(self, bst_simples):
        ordem = bst_simples.percurso_in_order()
        riscos = [m[2] for m in ordem]
        assert riscos == sorted(riscos)

    def test_altura(self, bst_simples):
        assert bst_simples.altura() == 3

    def test_buscar_intervalo(self, bst_simples):
        resultado = bst_simples.buscar_intervalo(0.5, 0.8)
        nomes = {m[1] for m in resultado}
        assert nomes == {'X', 'Y', 'V'}

    def test_remover(self, bst_simples):
        removido = bst_simples.remover(20)
        assert removido is True
        assert len(bst_simples) == 4

