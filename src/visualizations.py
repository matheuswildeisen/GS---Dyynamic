"""
SENTINEL AGRO — Visualizações Obrigatórias
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np


def plotar_grafo_com_mst(grafo, mst_arestas, titulo="Grafo de Municípios — MST SENTINEL AGRO"):

    G = nx.Graph()

    for id_mun, dados in grafo.vertices.items():
        G.add_node(id_mun, nome=dados[1], risco=dados[2])

    for u, v, peso in grafo.arestas:
        G.add_edge(u, v, weight=peso)

    mst_set = set()
    for u, v, _ in mst_arestas:
        mst_set.add((min(u, v), max(u, v)))

    pos = nx.spring_layout(G, seed=42)
    riscos = [G.nodes[n]['risco'] for n in G.nodes()]
    nomes  = {n: G.nodes[n]['nome'] for n in G.nodes()}

    fig, ax = plt.subplots(figsize=(14, 10))

    arestas_normais = [(u, v) for u, v in G.edges()
                       if (min(u,v), max(u,v)) not in mst_set]
    nx.draw_networkx_edges(G, pos, edgelist=arestas_normais,
                           edge_color='#cccccc', width=1, ax=ax)

    arestas_mst = [(u, v) for u, v in G.edges()
                   if (min(u,v), max(u,v)) in mst_set]
    nx.draw_networkx_edges(G, pos, edgelist=arestas_mst,
                           edge_color='#e74c3c', width=2.5,
                           label='MST — Cobertura Mínima', ax=ax)

    nc = nx.draw_networkx_nodes(G, pos, node_color=riscos,
                                cmap=plt.cm.RdYlGn_r,
                                node_size=400, ax=ax)
    nx.draw_networkx_labels(G, pos, labels=nomes, font_size=7, ax=ax)

    plt.colorbar(nc, ax=ax, label='Índice de Risco (0=baixo, 1=crítico)')
    patch_mst = mpatches.Patch(color='#e74c3c', label='Arestas MST')
    ax.legend(handles=[patch_mst])
    ax.set_title(titulo, fontsize=14, fontweight='bold')
    ax.set_xlabel("Fonte: dados sintéticos baseados em malha viária DNIT + NDVI MODIS/NASA")
    plt.tight_layout()
    plt.savefig('report/fig1_grafo_mst.png', dpi=150)
    plt.show()


def plotar_bst(bst, titulo="BST — Municípios por Índice de Risco"):
    """
    Desenha a árvore BST para instâncias de 10–15 nós.
    Exibe o índice de risco em cada nó.
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_title(titulo, fontsize=13, fontweight='bold')
    ax.axis('off')

    posicoes = {}
    labels = {}

    def _calcular_pos(no, x, y, dx):
        if no is None:
            return
        posicoes[id(no)] = (x, y)
        labels[id(no)] = f"{no.municipio[1][:8]}\nr={no.risco:.2f}"
        _calcular_pos(no.esquerda, x - dx, y - 1, dx / 2)
        _calcular_pos(no.direita,  x + dx, y - 1, dx / 2)

    _calcular_pos(bst.raiz, 0, 0, 4)

    def _desenhar_arestas(no):
        if no is None:
            return
        if no.esquerda:
            x1, y1 = posicoes[id(no)]
            x2, y2 = posicoes[id(no.esquerda)]
            ax.plot([x1, x2], [y1, y2], 'k-', lw=1.2, zorder=1)
            _desenhar_arestas(no.esquerda)
        if no.direita:
            x1, y1 = posicoes[id(no)]
            x2, y2 = posicoes[id(no.direita)]
            ax.plot([x1, x2], [y1, y2], 'k-', lw=1.2, zorder=1)
            _desenhar_arestas(no.direita)

    _desenhar_arestas(bst.raiz)

    for node_id, (x, y) in posicoes.items():
        risco = float(labels[node_id].split('r=')[1])
        cor = plt.cm.RdYlGn_r(risco)
        circle = plt.Circle((x, y), 0.35, color=cor, zorder=2)
        ax.add_patch(circle)
        ax.text(x, y, labels[node_id], ha='center', va='center',
                fontsize=7, zorder=3)

    if posicoes:
        xs = [p[0] for p in posicoes.values()]
        ys = [p[1] for p in posicoes.values()]
        ax.set_xlim(min(xs) - 1, max(xs) + 1)
        ax.set_ylim(min(ys) - 1, max(ys) + 1)

    ax.set_xlabel("Fonte: dados sintéticos — índices de risco derivados de NDVI MODIS/NASA + INMET")
    plt.tight_layout()
    plt.savefig('report/fig2_bst.png', dpi=150)
    plt.show()


def plotar_desempenho_comparativo(dados, titulo="Desempenho: Força Bruta vs Dijkstra (Guloso)"):
    """
    Gráfico tempo × N para os dois algoritmos.
    Identifica o cruzamento das curvas (ponto onde FB se torna inviável).
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    N = dados['N']

    axes[0].plot(N, dados['tempo_FB'],    'r-o', label='Força Bruta', linewidth=2)
    axes[0].plot(N, dados['tempo_Guloso'],'b-s', label='Dijkstra (Guloso)', linewidth=2)
    axes[0].set_xlabel("N (número de municípios)", fontsize=11)
    axes[0].set_ylabel("Tempo de execução (ms)", fontsize=11)
    axes[0].set_title("Tempo × N", fontsize=12)
    axes[0].legend()
    axes[0].set_yscale('log')
    axes[0].grid(True, alpha=0.4)
    axes[0].set_xlabel("N — Fonte: execuções instrumentadas com time.perf_counter()")

    axes[1].plot(N, dados['mem_FB'],    'r-o', label='Força Bruta', linewidth=2)
    axes[1].plot(N, dados['mem_Guloso'],'b-s', label='Dijkstra (Guloso)', linewidth=2)
    axes[1].set_xlabel("N (número de municípios)", fontsize=11)
    axes[1].set_ylabel("Memória pico (MB)", fontsize=11)
    axes[1].set_title("Memória × N", fontsize=12)
    axes[1].legend()
    axes[1].grid(True, alpha=0.4)

    fig.suptitle(titulo, fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig('report/fig3_desempenho.png', dpi=150)
    plt.show()


def plotar_gap_otimalidade(ns, gaps, titulo="Gap de Otimalidade: Força Bruta vs Dijkstra"):
    """
    Gráfico do gap percentual entre solução FB (ótima) e Gulosa em função de N.
    Gap = 0% indica que o Dijkstra encontrou a solução exata.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(ns, gaps, color=['#2ecc71' if g < 5 else '#e74c3c' for g in gaps],
           edgecolor='black', width=0.6)
    ax.axhline(y=5, color='orange', linestyle='--', label='Limiar aceitável (5%)')
    ax.set_xlabel("N (número de municípios)", fontsize=11)
    ax.set_ylabel("Gap de Otimalidade (%)", fontsize=11)
    ax.set_title(titulo, fontsize=13, fontweight='bold')
    ax.legend()
    ax.grid(True, axis='y', alpha=0.4)
    ax.set_xlabel("N — Fonte: comparação direta FB (exato) × Dijkstra (guloso)")
    plt.tight_layout()
    plt.savefig('report/fig4_gap_otimalidade.png', dpi=150)
    plt.show()