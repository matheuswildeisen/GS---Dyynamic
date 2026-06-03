"""Notebook analysis script for SENTINEL AGRO."""

import sys
import random
import time
import tracemalloc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / 'src'))

import numpy as np
import matplotlib.pyplot as plt
from data_structures import GrafoMunicipios, BinarySearchTree, criar_municipio, criar_aresta
from brute_force import ForcaBruta
from greedy import Dijkstra, Prim
from performance_monitor import PerformanceMonitor
from visualizations import (plotar_grafo_com_mst, plotar_bst,
                             plotar_desempenho_comparativo, plotar_gap_otimalidade)


def grafo_aleatorio(n, seed=42):
    random.seed(seed + n)
    g = GrafoMunicipios()
    for i in range(n):
        mun = criar_municipio(i, f'Mun_{i}', round(random.uniform(0.3, 0.95), 2),
                              random.randint(1000, 3000), random.randint(10000, 500000))
        g.adicionar_vertice(mun)
    ids = list(range(n))
    for i in range(n - 1):
        g.adicionar_aresta(ids[i], ids[i+1], random.randint(50, 500))
    for _ in range(n):
        u, v = random.sample(ids, 2)
        g.adicionar_aresta(u, v, random.randint(50, 500))
    return g


def main():
    monitor = PerformanceMonitor()
    print("SENTINEL AGRO — Análise de Resultados")
    print("Global Solution 2026 | FIAP — Dynamic Programming")

    municipios_matopiba = [
        criar_municipio(2111300, 'Balsas-MA',        0.85, 2100.0, 95000),
        criar_municipio(2113700, 'Imperatriz-MA',    0.60, 1800.0, 260000),
        criar_municipio(1721000, 'Palmas-TO',        0.30, 1200.0, 310000),
        criar_municipio(1712504, 'Araguaína-TO',     0.55, 1600.0, 180000),
        criar_municipio(2207702, 'Parnaíba-PI',      0.78, 1950.0, 150000),
        criar_municipio(2910727, 'Barreiras-BA',     0.92, 2400.0, 160000),
        criar_municipio(2919207, 'Luís Eduardo-BA',  0.88, 2300.0, 75000),
        criar_municipio(1706003, 'Guaraí-TO',        0.45, 1400.0, 25000),
        criar_municipio(2109007, 'Barra do Corda-MA',0.72, 1750.0, 85000),
        criar_municipio(2203909, 'Floriano-PI',      0.65, 1700.0, 58000),
        criar_municipio(2915401, 'Ibotirama-BA',     0.80, 2000.0, 22000),
        criar_municipio(1716109, 'Tocantinópolis-TO',0.58, 1550.0, 23000),
    ]

    rotas_matopiba = [
        (1721000, 1712504, 380),
        (1721000, 1706003, 210),
        (1712504, 2111300, 620),
        (1712504, 1716109, 180),
        (2111300, 2113700, 440),
        (2111300, 2109007, 350),
        (2109007, 2203909, 410),
        (2203909, 2207702, 320),
        (2910727, 2919207, 100),
        (2910727, 2111300, 900),
        (2910727, 2915401, 280),
        (1706003, 2109007, 530),
        (2113700, 1716109, 220),
    ]

    grafo_matopiba = GrafoMunicipios()
    for mun in municipios_matopiba:
        grafo_matopiba.adicionar_vertice(mun)
    for u, v, p in rotas_matopiba:
        grafo_matopiba.adicionar_aresta(u, v, p)

    bst_matopiba = BinarySearchTree()
    for mun in municipios_matopiba:
        bst_matopiba.inserir(mun)

    print(f"Grafo MATOPIBA: {len(grafo_matopiba.vertices)} vértices, {len(grafo_matopiba.arestas)} arestas")
    print(f"BST: {len(bst_matopiba)} municípios | Altura: {bst_matopiba.altura()}")

    print("\n--- Municípios em Risco CRÍTICO (risco >= 0.80) ---")
    criticos = bst_matopiba.buscar_intervalo(0.80, 1.0)
    for m in criticos:
        print(f"  {m[1]:<25} risco={m[2]:.2f}  custo=R${m[3]:,.0f}")

    print("\n--- Percurso In-Order (crescente por risco) ---")
    ordenados = bst_matopiba.percurso_in_order()
    for m in ordenados:
        print(f"  {m[1]:<25} risco={m[2]:.2f}")

    HUB = 1721000

    dijkstra = Dijkstra(grafo_matopiba, bst_matopiba)
    rotas, _ = monitor.medir(
        "Dijkstra — MATOPIBA",
        dijkstra.rota_atendimento_prioritario,
        HUB, 0.70
    )

    print("\n--- ROTAS DE ATENDIMENTO (Palmas → Municípios Críticos) ---")
    print(f"{'Município':<25} {'Risco':>6} {'Distância km':>14} {'Caminho'}")
    print('-' * 70)
    for r in rotas:
        nomes_caminho = [grafo_matopiba.get_nome(i) for i in r['caminho']]
        print(f"{r['municipio']:<25} {r['risco']:>6.2f} {r['custo_rota']:>14.0f}  {' → '.join(nomes_caminho)}")

    ids_subgrafo = [1721000, 1712504, 2111300, 2113700,
                    2109007, 2203909, 2207702, 1706003]

    fb = ForcaBruta(grafo_matopiba)

    print("\n--- FORÇA BRUTA: Palmas → Balsas ---")
    caminho_fb, custo_fb, stats_fb = monitor.medir(
        "Força Bruta — Palmas→Balsas",
        fb.encontrar_caminho_minimo,
        1721000, 2111300
    )[0]

    nomes_fb = [grafo_matopiba.get_nome(i) for i in caminho_fb]
    print(f"  Caminho ótimo: {' → '.join(nomes_fb)}")
    print(f"  Custo: {custo_fb} km")
    print(f"  Chamadas recursivas: {stats_fb['chamadas_recursivas']}")
    print(f"  Caminhos avaliados : {stats_fb['caminhos_avaliados']}")

    dist_dij, pred_dij = dijkstra.executar(1721000)
    caminho_dij = dijkstra.reconstruir_caminho(pred_dij, 2111300)
    custo_dij = dist_dij[2111300]
    gap = monitor.calcular_gap_otimalidade(custo_fb, custo_dij)

    print(f"\n  Dijkstra: {custo_dij} km | Gap de otimalidade: {gap:.2f}%")
    print(f"  → Dijkstra {'encontrou a solução ótima' if gap == 0 else f'divergiu {gap:.2f}% do ótimo'}")

    municipios_rs = [
        criar_municipio(4314902, 'Porto Alegre',  0.72, 1850, 1400000),
        criar_municipio(4300406, 'Alegrete',      0.68, 1600, 77000),
        criar_municipio(4316808, 'Santa Maria',   0.55, 1500, 280000),
        criar_municipio(4307005, 'Caxias do Sul', 0.40, 1400, 520000),
        criar_municipio(4309209, 'Ijuí',          0.62, 1550, 83000),
        criar_municipio(4312401, 'Pelotas',       0.75, 1700, 342000),
        criar_municipio(4303905, 'Canoas',        0.35, 1300, 350000),
        criar_municipio(4318705, 'Uruguaiana',    0.80, 1900, 126000),
    ]

    rotas_rs = [
        (4314902, 4316808, 1.8), (4314902, 4307005, 2.5),
        (4314902, 4312401, 2.0), (4314902, 4303905, 0.5),
        (4316808, 4309209, 2.1), (4316808, 4300406, 3.5),
        (4300406, 4318705, 2.8), (4300406, 4309209, 2.3),
        (4307005, 4309209, 1.5), (4312401, 4318705, 4.2),
    ]

    grafo_rs = GrafoMunicipios()
    for m in municipios_rs:
        grafo_rs.adicionar_vertice(m)
    for u, v, p in rotas_rs:
        grafo_rs.adicionar_aresta(u, v, p)

    bst_rs = BinarySearchTree()
    for m in municipios_rs:
        bst_rs.inserir(m)

    prim = Prim(grafo_rs)
    mst_rs, custo_mst_rs = monitor.medir(
        "Prim MST — RS",
        prim.executar,
        4314902
    )[0]

    print("\n--- MST RS (Prim) — Cobertura mínima de municípios afetados ---")
    print(f"  Custo total MST: {custo_mst_rs:.1f} h de deslocamento")
    for u, v, p in mst_rs:
        print(f"  {grafo_rs.get_nome(u):<20} → {grafo_rs.get_nome(v):<20} {p:.1f}h")

    tamanhos_fb = [5, 6, 7, 8, 9, 10, 11, 12]
    tempos_fb, tempos_dij = [], []
    mems_fb, mems_dij = [], []
    gaps = []

    print("\n--- EXPERIMENTO DE ESCALABILIDADE ---")
    print(f"{'N':>4} | {'FB (ms)':>10} | {'Dijkstra (ms)':>14} | {'Gap (%)':>8}")
    print('-' * 45)

    for n in tamanhos_fb:
        g = grafo_aleatorio(n)
        fb_exp = ForcaBruta(g)
        dij_exp = Dijkstra(g)
        ids = list(g.vertices.keys())

        tracemalloc.start()
        t0 = time.perf_counter()
        _, custo_fb_exp, _ = fb_exp.encontrar_caminho_minimo(ids[0], ids[-1])
        t_fb = (time.perf_counter() - t0) * 1000
        _, mem_fb_pico = tracemalloc.get_traced_memory(); tracemalloc.stop()

        tracemalloc.start()
        t0 = time.perf_counter()
        dist_exp, pred_exp = dij_exp.executar(ids[0])
        t_dij = (time.perf_counter() - t0) * 1000
        _, mem_dij_pico = tracemalloc.get_traced_memory(); tracemalloc.stop()
        custo_dij_exp = dist_exp.get(ids[-1], float('inf'))

        gap_n = monitor.calcular_gap_otimalidade(custo_fb_exp, custo_dij_exp)

        tempos_fb.append(t_fb)
        tempos_dij.append(t_dij)
        mems_fb.append(mem_fb_pico / 1024**2)
        mems_dij.append(mem_dij_pico / 1024**2)
        gaps.append(gap_n)

        print(f"{n:>4} | {t_fb:>10.3f} | {t_dij:>14.3f} | {gap_n:>8.2f}")

    for n in [20, 50, 100]:
        g = grafo_aleatorio(n)
        dij_exp = Dijkstra(g)
        ids = list(g.vertices.keys())
        tracemalloc.start()
        t0 = time.perf_counter()
        dij_exp.executar(ids[0])
        t_dij = (time.perf_counter() - t0) * 1000
        _, mem_dij_pico = tracemalloc.get_traced_memory(); tracemalloc.stop()
        tempos_dij.append(t_dij)
        mems_dij.append(mem_dij_pico / 1024**2)
        print(f"{n:>4} | {'N/A (inviável)':>10} | {t_dij:>14.3f} | {'N/A':>8}")

    prim_mat = Prim(grafo_matopiba)
    mst_mat, _ = prim_mat.executar(1721000)
    plotar_grafo_com_mst(grafo_matopiba, mst_mat,
                         "SENTINEL AGRO — Grafo MATOPIBA com MST (Prim)")

    plotar_bst(bst_matopiba, "BST MATOPIBA — Municípios por Índice de Risco (NDVI/INMET)")

    dados_perf = {
        'N': tamanhos_fb,
        'tempo_FB': tempos_fb,
        'tempo_Guloso': tempos_dij[:len(tamanhos_fb)],
        'mem_FB': mems_fb,
        'mem_Guloso': mems_dij[:len(tamanhos_fb)]
    }
    plotar_desempenho_comparativo(dados_perf)
    plotar_gap_otimalidade(tamanhos_fb, gaps)

    print("""
╔══════════════════════════════════════════════════════════════════════╗
║         ESCALA DE DECISÃO — SENTINEL AGRO                           ║
╠══════════════════════════════════════════════════════════════════════╣
║  Nível 1 — ÓTIMO GARANTIDO (N ≤ 8)                                  ║
║  Algoritmo: Força Bruta                                              ║
║  Uso: validação de rotas críticas em pequenas cooperativas           ║
║  Qualidade: 100% ótimo | Custo: exponencial — inviável acima de N=12 ║
╠══════════════════════════════════════════════════════════════════════╣
║  Nível 2 — QUASI-ÓTIMO EFICIENTE (N = 9..50)                        ║
║  Algoritmo: Dijkstra (Guloso) + BST para priorização                 ║
║  Uso: rotas de atendimento por hub regional (ex.: Palmas → MATOPIBA) ║
║  Qualidade: gap 0–5% vs FB | Custo: O((V+E)log V) — escalável        ║
╠══════════════════════════════════════════════════════════════════════╣
║  Nível 3 — COBERTURA MÍNIMA REGIONAL (N > 50)                        ║
║  Algoritmo: Prim MST + BST                                           ║
║  Uso: planejamento de rede de monitoramento para todo o MATOPIBA     ║
║  Qualidade: solução estrutural, não por rota | Custo: O(E log V)     ║
╠══════════════════════════════════════════════════════════════════════╣
║  Nível 4 — ESCALA NACIONAL (N > 500)                                 ║
║  Algoritmo: Dijkstra com poda por BST (consulta r >= 0.8 primeiro)   ║
║  Uso: SENTINEL AGRO em escala nacional — 500 mil propriedades        ║
║  Qualidade: aceitável | Custo: gerenciável com heap + early stopping  ║
╚══════════════════════════════════════════════════════════════╝
""")

    print("""
CONEXÃO COM ODS:
  ODS 2  — Fome Zero: a priorização por BST permite atender primeiro os
            municípios com maior risco de seca, protegendo a produção de alimentos.
  ODS 9  — Inovação: a plataforma SENTINEL AGRO integra satélites (MODIS/NASA)
            com algoritmos de grafos para decisão em tempo real.
  ODS 11 — Cidades Sustentáveis: a MST minimiza o custo de cobertura das rotas
            de defesa civil em regiões de enchente (RS).
  ODS 13 — Ação Climática: o monitoramento contínuo de NDVI via BST permite
            detectar seca antes da perda irreversível da lavoura.
""")


if __name__ == '__main__':
    main()
