# 🌾 SENTINEL AGRO
### Inteligência Satelital para Monitoramento de Riscos Ambientais

> Global Solution 2026 — Space Connect | FIAP  
> Disciplina: Dynamic Programming — Estruturas de Dados e Algoritmos  
> Prof. André Marques | 1º Semestre de 2026

---

## 👥 Equipe

| RM | Nome |
|---|---|
| 564880 | Gabriel Ciriaco |
| 565916 | Vinicius Mafra Paiva |
| 561539 | Matheus Von Koss Wildeisen |

---

## 📡 Sobre o Projeto

O **SENTINEL AGRO** é uma plataforma de inteligência satelital que processa dados 
orbitais de missões como **Landsat 8/9 (NASA)**, **Sentinel-2 (ESA)** e **MODIS 
(NASA Terra/Aqua)** para monitorar riscos ambientais em municípios brasileiros em 
tempo real.

Nesta entrega da Global Solution, o projeto é implementado como um **sistema de 
monitoramento e triagem de riscos** utilizando **grafos ponderados**, **árvores 
binárias de busca (BST)**, **algoritmos de Força Bruta** e **algoritmos Gulosos 
(Dijkstra + Prim)**, aplicados a dois cenários brasileiros reais:

- 🌵 **Cenário B — Seca no MATOPIBA** (MA, TO, PI, BA): rota de atendimento 
  prioritário com base em índice de risco NDVI/INMET
- 🌊 **Cenário A — Enchentes no RS**: cobertura mínima de municípios afetados 
  via MST (Prim)

### Conexão com os ODS da ONU

| ODS | Contribuição |
|---|---|
| 🌾 ODS 2 — Fome Zero | Priorização de atendimento a municípios em risco de seca protege a produção de alimentos |
| 🏭 ODS 9 — Inovação | Integração de dados satelitais (MODIS/NASA) com algoritmos de grafos para decisão em tempo real |
| 🏙️ ODS 11 — Cidades Sustentáveis | MST minimiza custo de cobertura das rotas de defesa civil em regiões de enchente |
| 🌍 ODS 13 — Ação Climática | Monitoramento contínuo de NDVI permite detectar seca antes da perda irreversível da lavoura |

---

## 🗂️ Estrutura do Repositório

GS - Dyynamic/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── data_structures.py
│   ├── brute_force.py
│   ├── greedy.py
│   ├── performance_monitor.py
│   └── visualizations.py
├── notebooks/
│   └── analise_resultados.ipynb
├── tests/
│   └── test_algorithms.py
└── report/
    └── relatorio_final.pdf

    
## ⚙️ Como Executar

### 1. Clone o repositório


bash
Copiar

git clone https://github.com/seu-usuario/GS-Dyynamic.git
cd GS-Dyynamic




### 2. Crie um ambiente virtual e instale as dependências


bash
Copiar

python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

pip install -r requirements.txt




### 3. Execute os módulos principais


bash
Copiar

# Estruturas de dados e algoritmos
python src/data_structures.py

# Força Bruta (validação baseline)
python src/brute_force.py

# Algoritmo Guloso (Dijkstra + Prim)
python src/greedy.py

# Monitoramento de desempenho
python src/performance_monitor.py




### 4. Execute os testes automatizados


bash
Copiar

pytest tests/test_algorithms.py -v




### 5. Abra o notebook de análise


bash
Copiar

jupyter notebook notebooks/analise_resultados.ipynb




---

## 📦 Dependências
networkx>=3.0 matplotlib>=3.7 seaborn>=0.12 numpy>=1.24 pandas>=2.0 scipy>=1.10 jupyter>=1.0 pytest>=7.3 tracemalloc # nativa Python 3.4+ heapq # nativa Python

> Instale tudo com: `pip install -r requirements.txt`

---

## 🧠 Algoritmos Implementados

| Algoritmo | Papel | Complexidade |
|---|---|---|
| **Força Bruta** (backtracking) | Solução exata para N ≤ 12 — baseline de validação | O(V!) |
| **Dijkstra** (Guloso) | Rota de menor custo de atendimento a municípios críticos | O((V+E) log V) |
| **Prim** (Guloso) | Árvore geradora mínima — cobertura com menor custo total | O(E log V) |
| **BST** | Consulta eficiente de municípios por faixa de risco | O(log N) médio |
| **BFS** | Percurso em largura no grafo de municípios | O(V+E) |

---

## 📊 Estruturas de Dados Utilizadas

| Estrutura | Onde foi usada | Justificativa |
|---|---|---|
| **Tupla** | Vértices e arestas do grafo | Imutabilidade garante integridade dos dados de municípios |
| **Dicionário** | Lista de adjacência, custos acumulados, predecessores | Acesso O(1) por ID de município |
| **Lista** | Adjacência, caminhos reconstruídos, heap | Inserção e iteração eficientes |
| **Conjunto (set)** | Nós visitados em BFS/DFS | Verificação de pertencimento em O(1) |
| **Heap (heapq)** | Fila de prioridade em Dijkstra e Prim | Extração do mínimo em O(log N) |
| **BST** | Municípios ordenados por índice de risco | Busca por intervalo em O(log N + K) |
| **Grafo (dict of lists)** | Rede de municípios e rotas | Lista de adjacência eficiente para grafos esparsos |

---

## 📈 Cenários Brasileiros

### 🌵 Cenário B — Seca no MATOPIBA
Municípios dos estados do Maranhão, Tocantins, Piauí e Bahia com índice de risco 
derivado de dados NDVI/MODIS (NASA) e pluviometria INMET. A BST organiza os 
municípios por grau de criticidade e o Dijkstra calcula a rota de menor custo de 
atendimento a partir do hub de Palmas-TO.

**Fonte dos dados:** NDVI MODIS/NASA + INMET (dados sintéticos baseados em 
fontes reais, devidamente justificados no relatório)

### 🌊 Cenário A — Enchentes no RS
Municípios afetados pelas enchentes do Rio Grande do Sul em 2024. A MST calculada 
pelo algoritmo de Prim determina a rede de cobertura mínima para posicionamento de 
equipes de resposta da defesa civil.

**Fonte dos dados:** Malha viária DNIT + Defesa Civil RS (dados sintéticos baseados 
em fontes reais)

---

## 🔬 Figuras Obrigatórias

Todas as figuras são geradas automaticamente pelo módulo `src/visualizations.py` 
e salvas na pasta `report/`:

- `fig1_grafo_mst.png` — Grafo de municípios com arestas da MST destacadas
- `fig2_bst.png` — Representação visual da BST (10–15 nós) com índices de risco
- `fig3_desempenho.png` — Tempo de execução × N para Força Bruta e Dijkstra
- `fig4_gap_otimalidade.png` — Gap percentual entre solução FB (ótima) e Gulosa


<div align="center">
  <sub>FIAP — Bacharelado em Sistemas de Informação | Global Solution 2026</sub><br>
  <sub>Dynamic Programming — Prof. André Marques</sub>
</div>
