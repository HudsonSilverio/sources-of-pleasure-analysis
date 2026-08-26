# Fase 3 — Analise Exploratoria (EDA)

**Dataset:** `data/processed/clean.csv` — 6,587 respondentes completos

**Principio:** esta fase explora **relacoes entre variaveis** para gerar
observacoes e pistas. Nenhuma conclusao — apenas hipoteses candidatas
para a Fase 4.

---

## Metodologia — metodos aplicados nesta fase

### 1. Correlacoes
| Metodo | Descricao | Aplicado a |
|--------|-----------|------------|
| Correlacao de Spearman | Mede relacoes monotonicas entre pares. Adequada para Likert (ordinal tratado como intervalar). Mais robusta a assimetria que Pearson | Matriz 37x37 itens e 6x6 fatores |
| Identificacao de pares extremos | Top 15 positivas, top 10 negativas, 10 mais proximas de zero | Todos os 666 pares de itens |
| Deteccao de redundancia | Pares com \|rho\| > 0.60 — candidatos a medir a mesma coisa | Todos os pares |

### 2. Grafo de rede de correlacoes
| Metodo | Descricao | Aplicado a |
|--------|-----------|------------|
| Network graph (networkx) | Nos = itens, arestas = correlacoes com \|rho\| >= 0.35. Layout spring com seed fixa. Cor dos nos = fator predefinido | 37 itens |

### 3. Analise de dimensionalidade
| Metodo | Descricao | Aplicado a |
|--------|-----------|------------|
| PCA (Principal Component Analysis) | Decomposicao em componentes ortogonais. Dados padronizados (StandardScaler). Scree plot dos eigenvalues | 37 itens padronizados |
| Analise paralela (Horn) | Compara eigenvalues reais com 100 simulacoes de dados aleatorios (mesmo N e variaveis). Retém componentes cujo eigenvalue real > P95 aleatorio | 37 itens |
| Heatmap de loadings | Pesos de cada item em cada componente. Identifica cross-loadings e itens deslocados | Primeiros componentes retidos |

### 4. Clustering de itens
| Metodo | Descricao | Aplicado a |
|--------|-----------|------------|
| Clustering hierarquico (Ward) | Distancia = 1 - \|correlacao\|. Metodo de ligacao Ward (minimiza variancia intra-cluster). Visualizado como dendrograma | 37 itens |

### 5. Coesao intra-fator
| Metodo | Descricao | Aplicado a |
|--------|-----------|------------|
| Media inter-item (Spearman) | Media das correlacoes entre todos os pares de itens dentro de cada fator (excluindo diagonal). Mede se os itens 'andam juntos' | 6 fatores |

### 6. Distribuicoes comparadas
| Metodo | Descricao | Aplicado a |
|--------|-----------|------------|
| Boxplots | Mediana, quartis, whiskers (1.5x IQR), outliers individuais. Comparacao visual lado a lado | 37 itens e 6 fatores |

### 7. Visualizacao de respondentes
| Metodo | Descricao | Aplicado a |
|--------|-----------|------------|
| t-SNE | Reducao nao-linear para 2D (perplexity=50, 1000 iteracoes). Pre-reducao por PCA para 8 dimensoes. Preserva vizinhancas locais | 6587 respondentes |

### 8. Clustering de respondentes (exploratorio)
| Metodo | Descricao | Aplicado a |
|--------|-----------|------------|
| K-Means | k de 2 a 8, n_init=10, max_iter=300, seed=42. Dados padronizados | 6587 respondentes |
| Silhouette score | Mede coesao intra-cluster vs. separacao entre clusters. Score de -1 a 1 (>0.5 = bom, 0.25-0.5 = razoavel, <0.25 = fraco) | k=2 a k=8 |
| Metodo do cotovelo (Elbow) | Inertia (soma dos quadrados intra-cluster) por k. O 'cotovelo' sugere o k apos o qual adicionar clusters traz pouco ganho | k=2 a k=8 |

### 9. Deteccao de anomalias
| Metodo | Descricao | Aplicado a |
|--------|-----------|------------|
| Straight-lining | Respondentes com a mesma resposta em todos os 37 itens (nunique == 1) | Todos os respondentes |
| Baixa variabilidade | Respondentes com no maximo 2 valores distintos (nunique <= 2) | Todos os respondentes |
| Distancia de Mahalanobis | Distancia multivariada ao centroide. Outliers = acima do P99. Identifica perfis de resposta raros | Todos os respondentes |

### Ferramentas utilizadas
- **Python 3.13** com pandas, numpy, scipy, scikit-learn, matplotlib, networkx
- **scipy**: stats.spearmanr, cluster.hierarchy (linkage, dendrogram)
- **scikit-learn**: PCA, KMeans, TSNE, StandardScaler, silhouette_score
- **networkx**: spring_layout, draw_networkx
- **Seed fixa**: 42 para reprodutibilidade
- **Script reproduzivel**: `scripts/phase3_eda.py`

---

## Observacoes

Cada observacao e uma pista, nao uma conclusao. O formato e:
> O-nn: [observacao] → [possivel pergunta]

### O-01
**Observacao:** Os fatores mais correlacionados sao Interpessoal e Nobre (rho=0.46). Os menos correlacionados sao Reputacional e Intelectual (rho=0.02).

**Possivel pergunta:** A estrutura de 6 fatores captura dimensoes realmente independentes ou ha sobreposicao?

### O-02
**Observacao:** O grafo de correlacoes (limiar |rho| >= 0.35) tem 37 arestas. Itens do mesmo fator tendem a se agrupar visualmente, mas ha conexoes entre fatores.

**Possivel pergunta:** A estrutura fatorial predefinida e confirmada pela rede de correlacoes ou ha itens que se conectam mais com outros fatores?

### O-03
**Observacao:** O par mais fortemente correlacionado e Supporting community ↔ Charity / altruism (rho=0.60). A correlacao negativa mais forte e Being in nature ↔ High status (rho=-0.10).

**Possivel pergunta:** Os pares mais correlacionados sao redundantes (medem a mesma coisa) ou sao genuinamente relacionados?

### O-04
**Observacao:** A analise paralela sugere reter 8 componentes (eigenvalue real > P95 aleatorio). O instrumento usa 6 fatores, que explicam 46.2% da variancia. Os primeiros 8 componentes explicam 52.7%.

**Possivel pergunta:** A estrutura de 6 fatores e adequada ou os dados sugerem 8 dimensoes?

### O-05
**Observacao:** No heatmap de loadings, os itens tendem a carregar nos componentes esperados pelos seus fatores, mas ha cross-loadings que merecem investigacao na analise estrutural.

**Possivel pergunta:** A estrutura empirica dos dados confirma ou desafia a organizacao dos 6 fatores do instrumento?

### O-06
**Observacao:** O dendrograma mostra como os itens se agrupam empiricamente com base em suas correlacoes. Comparar os clusters emergentes com os 6 fatores predefinidos revela concordancias e divergencias.

**Possivel pergunta:** Quais itens estao 'mal classificados' nos fatores originais segundo o agrupamento empirico?

### O-07
**Observacao:** O fator mais coeso e Interpessoal (media inter-item r = 0.39). O menos coeso e Intelectual (media inter-item r = 0.29).

**Possivel pergunta:** O fator menos coeso deveria ser reorganizado? Algum item esta deslocado?

### O-08
**Observacao:** Thrilling e o unico fator com mediana negativa, indicando que a maioria dos respondentes nao obtem prazer substancial de atividades emocionantes/arriscadas. Interpessoal e Intelectual dominam com medianas acima de 1.5.

**Possivel pergunta:** O perfil dominante (alto interpessoal/intelectual, baixo thrilling) e uma caracteristica da amostra ClearerThinking ou seria universal?

### O-09
**Observacao:** A projecao t-SNE mostra a distribuicao dos respondentes no espaco reduzido. Regioes com concentracao de uma cor sugerem perfis com predominancia de um fator.

**Possivel pergunta:** Existem clusters discretos de respondentes ou e uma distribuicao continua?

### O-10
**Observacao:** O melhor k pelo silhouette e k=2 (score=0.114). Score baixo (<0.25) sugere que os clusters nao sao bem separados — a distribuicao pode ser mais continua do que discreta.

**Possivel pergunta:** Com k=2, quais sao os perfis dos clusters? Eles contam uma historia interpretavel?

### O-11
**Observacao:** 3 respondentes deram a mesma resposta para todos os 37 itens (straight-lining). Isso pode indicar falta de engajamento.

**Possivel pergunta:** Respondentes com padrao de resposta suspeito deveriam ser removidos?

### O-12
**Observacao:** 28 respondentes usaram no maximo 2 valores diferentes nos 37 itens. Padrao de resposta com baixissima variabilidade.

**Possivel pergunta:** Esses respondentes devem ser investigados como potenciais respostas descuidadas?

### O-13
**Observacao:** Deteccao de outliers multivariados por distancia de Mahalanobis: 66 respondentes acima do P99 (dist > 10.1). Esses sao perfis de resposta raros, nao necessariamente errados.

**Possivel pergunta:** Os outliers multivariados representam perfis genuinamente atipicos ou erros de resposta?

---

## Detalhes — Correlacoes entre fatores

| Fator A | Fator B | Spearman rho |
|---------|---------|-------------|
| Interpessoal | Nobre | 0.460 |
| Interpessoal | Sensorial | 0.393 |
| Nobre | Sensorial | 0.334 |
| Emocionante | Reputacional | 0.332 |
| Interpessoal | Reputacional | 0.299 |
| Nobre | Intelectual | 0.249 |
| Sensorial | Intelectual | 0.220 |
| Emocionante | Nobre | 0.219 |
| Interpessoal | Emocionante | 0.204 |
| Reputacional | Sensorial | 0.177 |
| Interpessoal | Intelectual | 0.170 |
| Emocionante | Sensorial | 0.164 |
| Nobre | Reputacional | 0.156 |
| Emocionante | Intelectual | 0.089 |
| Reputacional | Intelectual | 0.023 |

## Detalhes — Top 15 correlacoes positivas entre itens

| Item A | Item B | Spearman rho | Mesmo fator? |
|--------|--------|-------------|-------------|
| Supporting community | Charity / altruism | 0.599 | Sim |
| Taking care of others | Supporting family | 0.594 | Sim |
| Authority / power | High status | 0.573 | Sim |
| Learning | Exploring ideas / thinking | 0.522 | Sim |
| Helping others | Charity / altruism | 0.483 | Sim |
| Using imagination | Creativity | 0.481 | Sim |
| Belonging to a group | Being liked | 0.477 | Nao |
| Social recognition | High status | 0.472 | Sim |
| Helping others | Taking care of others | 0.451 | Sim |
| Loving / being loved | Quality time with loved ones | 0.443 | Sim |
| High-adrenaline activities | Escaping risky situations | 0.441 | Sim |
| Being liked | Social recognition | 0.440 | Sim |
| High-adrenaline activities | Frightening but fun | 0.430 | Sim |
| Quality time with loved ones | Deep personal connection | 0.428 | Sim |
| Being attractive | High status | 0.422 | Sim |

## Detalhes — Top 10 correlacoes negativas entre itens

| Item A | Item B | Spearman rho |
|--------|--------|-------------|
| Being in nature | High status | -0.098 |
| Competition / winning | Being in nature | -0.084 |
| Competition / winning | Creativity | -0.083 |
| High intensity situations | Relaxation | -0.075 |
| Interacting with animals | High status | -0.074 |
| Being liked | Exploring ideas / thinking | -0.068 |
| Learning | Partying / letting loose | -0.063 |
| Interacting with animals | Authority / power | -0.060 |
| Relaxation | Exploring ideas / thinking | -0.055 |
| Learning | Escaping risky situations | -0.051 |

## Detalhes — Perfis dos 2 clusters (exploratorio)

| Cluster | N | % | Interpessoal | Emocionante | Nobre | Reputacional | Sensorial | Intelectual |
|---------|---|---|---|---|---|---|---|---|
| 0 | 2646 | 40.2% | 1.08 | -0.96 | -0.24 | -0.02 | 0.57 | 1.38 |
| 1 | 3941 | 59.8% | 2.23 | -0.02 | 1.07 | 0.85 | 1.64 | 1.93 |

Silhouette score para k=2: **0.114**
(Analise formal de segmentacao sera feita nas Fases 5-6 pelo analista SEGMENTATION)

---

## Graficos exploratorios

Todos em `outputs/figures/exploratory/`:

- `11_correlation_heatmap_items.png` — Quais fontes de prazer andam juntas?
- `12_correlation_heatmap_factors.png` — Como as categorias de prazer se relacionam?
- `13_correlation_network.png` — Quais comunidades de itens emergem?
- `14_top_bottom_correlations.png` — Quais sao as relacoes mais fortes e mais fracas?
- `15_pca_scree_parallel.png` — Quantas dimensoes reais existem nos dados?
- `16_pca_loadings_heatmap.png` — Quais itens carregam em quais componentes?
- `17_dendrogram_items.png` — Os itens se agrupam como os fatores predefinidos?
- `18_within_factor_cohesion.png` — Os itens dentro de cada fator sao coesos?
- `19_boxplots_items.png` — Como as distribuicoes se comparam visualmente?
- `20_boxplots_factors.png` — Como os fatores se comparam entre si?
- `21_tsne_respondents.png` — Existem perfis naturais de respondentes?
- `22_silhouette_elbow.png` — Qual o numero otimo de clusters de respondentes?

---

*Gerado a partir de `data/processed/clean.csv` — N = 6,587 | Seed = 42*
