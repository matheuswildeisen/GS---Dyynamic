"""
SENTINEL AGRO — Monitoramento de Desempenho
"""

import time
import tracemalloc
import sys
from functools import wraps


class PerformanceMonitor:
    """
    Instrumenta algoritmos para coleta de métricas de desempenho.
    Métricas: tempo (ms), memória (MB), operações elementares.
    """

    def __init__(self):
        self.resultados = []

    def medir(self, nome_algoritmo, func, *args, **kwargs):
        """
        Executa uma função instrumentada e registra as métricas.
        Retorna (resultado_da_funcao, metricas_dict).
        """
        tracemalloc.start()
        inicio = time.perf_counter()

        resultado = func(*args, **kwargs)

        fim = time.perf_counter()
        mem_atual, mem_pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        metricas = {
            'algoritmo': nome_algoritmo,
            'tempo_ms': (fim - inicio) * 1000,
            'memoria_mb': mem_pico / (1024 * 1024),
        }
        self.resultados.append(metricas)

        print(f"\n[{nome_algoritmo}]")
        print(f"  Tempo de execução : {metricas['tempo_ms']:.4f} ms")
        print(f"  Memória pico      : {metricas['memoria_mb']:.4f} MB")

        return resultado, metricas

    def comparar_algoritmos(self, tamanhos_n, func_fb, func_guloso, grafo_factory):
        """
        Executa ambos os algoritmos para diferentes tamanhos N e registra
        os resultados para o gráfico comparativo de escalabilidade.
        """
        dados = {'N': [], 'tempo_FB': [], 'tempo_Guloso': [],
                 'mem_FB': [], 'mem_Guloso': []}

        for n in tamanhos_n:
            grafo_n = grafo_factory(n)
            print(f"\n--- N = {n} vértices ---")

            _, m_fb = self.medir(f"Força Bruta (N={n})", func_fb, grafo_n)
            _, m_g  = self.medir(f"Dijkstra (N={n})",   func_guloso, grafo_n)

            dados['N'].append(n)
            dados['tempo_FB'].append(m_fb['tempo_ms'])
            dados['tempo_Guloso'].append(m_g['tempo_ms'])
            dados['mem_FB'].append(m_fb['memoria_mb'])
            dados['mem_Guloso'].append(m_g['memoria_mb'])

        return dados

    def calcular_gap_otimalidade(self, custo_fb, custo_guloso):
        """
        Calcula o gap percentual entre a solução ótima (FB) e a Gulosa.
        Gap = 0% significa que o Guloso encontrou a solução ótima.
        """
        if custo_fb == 0:
            return 0.0
        return abs(custo_guloso - custo_fb) / custo_fb * 100