# Relatorio do Analista Segmentacao

**Data:** 2026-08-28 09:51
**Hipoteses analisadas:** 5
**Respondentes:** N = 6,587
**Seed aleatoria:** 42

## Resumo de vereditos

| Hipotese | Titulo | Veredito |
|----------|--------|----------|
| H11 | Somos especialistas ou generalistas do prazer? | confirmada |
| H12 | Perfis de prazer sao um espectro ou existem tipos reais? | confirmada |
| H13 | Quem busca emocao forte tem perfil completamente diferente? | confirmada |
| H14 | Quem gosta de espiritualidade e uma tribo a parte? | confirmada |
| H15 | Existe um grupo puramente intelectual? | confirmada |

## Analises detalhadas

---

### H11 — Somos especialistas ou generalistas do prazer?

**Manchete:** Especialistas vs. generalistas: como as pessoas organizam seu prazer

**Veredito:** [CONFIRMADA]

**Tecnica utilizada:** Entropia de Shannon dos 6 scores de fator (mede se o perfil de prazer e equilibrado ou concentrado). Divisao pela mediana em generalistas e especialistas. Mann-Whitney U para comparar o prazer medio geral entre os dois grupos.

**Premissas verificadas:** Entropia ja calculada na Fase 2 (respondent_profiles). Mann-Whitney nao exige normalidade.

**Resultado:** Generalistas: N = 3,294, prazer medio = 1.21
Especialistas: N = 3,293, prazer medio = 0.58
Mann-Whitney U = 8802914, p = 0.00e+00
Cohen's d = 1.201

**Interpretacao:** Os generalistas reportam mais prazer geral (d = 1.201, p < 0.001). Generalistas: media = 1.21, Especialistas: media = 0.58.

**Relevancia (o efeito importa na pratica?):** |d| = 1.201. Efeito grande.

**Limitacoes:** A divisao pela mediana e arbitraria. Amostra de conveniencia.

**Graficos:**
- `outputs\figures\exploratory\phase56\H11_entropy_groups.png`


---

### H12 — Perfis de prazer sao um espectro ou existem tipos reais?

**Manchete:** Nao existem tipos claros — prazer e um espectro

**Veredito:** [CONFIRMADA]

**Tecnica utilizada:** Tres metodos de agrupamento (K-Means, hierarquico, mistura gaussiana) com k de 2 a 8. Silhouette mede a qualidade da separacao (0 = sem separacao, 1 = perfeita). Estabilidade verificada com 100 sub-amostras.

**Premissas verificadas:** Dados padronizados (z-score) antes do agrupamento. Limite para 'grupos claros': silhouette > 0.25.

**Resultado:** Silhouette por metodo e k:
  kmeans k=2: 0.218
  kmeans k=3: 0.152
  kmeans k=4: 0.152
  kmeans k=5: 0.143
  kmeans k=6: 0.139
  kmeans k=7: 0.134
  kmeans k=8: 0.133
  hierarchical k=2: 0.228 ← melhor
  hierarchical k=3: 0.103
  hierarchical k=4: 0.076
  hierarchical k=5: 0.077
  hierarchical k=6: 0.078
  hierarchical k=7: 0.074
  hierarchical k=8: 0.076
  gmm k=2: 0.193
  gmm k=3: 0.123
  gmm k=4: 0.113
  gmm k=5: 0.103
  gmm k=6: 0.106
  gmm k=7: 0.095
  gmm k=8: 0.100

Melhor: hierarchical k=2, silhouette = 0.228
Estabilidade (bootstrap): 0.183 ± 0.039

**Interpretacao:** O melhor agrupamento encontrado (hierarchical, k=2) tem silhouette = 0.228 — abaixo do limite de 0.25. Nenhum metodo encontrou grupos claros. Prazer e um espectro, nao tipos separados.

**Relevancia (o efeito importa na pratica?):** Silhouette = 0.228 — fraco, grupos mal definidos.

**Limitacoes:** Agrupamento depende da escolha de variaveis e metodo. Silhouette < 0.25 nao prova que grupos nao existem — apenas que estes metodos nao os encontram nestes dados.

**Graficos:**
- `outputs\figures\exploratory\phase56\H12_clustering_validation.png`


---

### H13 — Quem busca emocao forte tem perfil completamente diferente?

**Manchete:** Quem busca adrenalina: um perfil de prazer completamente diferente

**Veredito:** [CONFIRMADA]

**Tecnica utilizada:** Divisao da amostra em Top 25% e Bottom 25% do fator thrilling. Mann-Whitney U (compara grupos sem assumir normalidade) para cada um dos outros 5 fatores. Cohen's d mede o tamanho da diferenca. Correcao FDR para multiplas comparacoes.

**Premissas verificadas:** Top 25%: N = 1,709. Bottom 25%: N = 1,692. Mann-Whitney nao exige normalidade.

**Resultado:** Comparacao Top 25% vs Bottom 25% do fator thrilling:

  Interpessoal: d = 0.538, p_corr = 0.0000 ***
  Emocionante: d = 6.086, p_corr = 0.0000 ***
  Nobre: d = 0.577, p_corr = 0.0000 ***
  Reputacional: d = 0.887, p_corr = 0.0000 ***
  Sensorial: d = 0.456, p_corr = 0.0000 ***
  Intelectual: d = 0.275, p_corr = 0.0000 ***


**Interpretacao:** Quem busca emocao forte difere em 5 dos outros 5 fatores. O maior efeito e d = 0.887. O perfil de prazer e realmente diferente.

**Relevancia (o efeito importa na pratica?):** Maior efeito: d = 0.887. d < 0.2 = trivial, 0.2-0.5 = pequeno, 0.5-0.8 = medio, > 0.8 = grande.

**Limitacoes:** Quartis sao uma divisao arbitraria. Amostra de conveniencia. Correlacao, nao causalidade.

**Graficos:**
- `outputs\figures\exploratory\phase56\H13_quartile_comparison.png`


---

### H14 — Quem gosta de espiritualidade e uma tribo a parte?

**Manchete:** A minoria espiritual: um perfil de prazer distinto

**Veredito:** [CONFIRMADA]

**Tecnica utilizada:** Divisao por pontuacao no item Spiritual / religious feelings: alto (>= 1) vs baixo (<= -1). Mann-Whitney U + Cohen's d para cada fator. Correcao FDR.

**Premissas verificadas:** Alto: N = 2,469, Baixo: N = 3,180. Mann-Whitney nao exige normalidade.

**Resultado:** Grupo alto (Spiritual / religious feelings >= 1): N = 2,469
Grupo baixo (Spiritual / religious feelings <= -1): N = 3,180

  Interpessoal: d = 0.474, p_corr = 0.0000 ***
  Emocionante: d = 0.289, p_corr = 0.0000 ***
  Nobre: d = 1.308, p_corr = 0.0000 ***
  Reputacional: d = 0.249, p_corr = 0.0000 ***
  Sensorial: d = 0.496, p_corr = 0.0000 ***
  Intelectual: d = 0.383, p_corr = 0.0000 ***


**Interpretacao:** Quem pontua alto em Spiritual / religious feelings difere em 6 dos 6 fatores. O perfil de prazer e realmente diferente.

**Relevancia (o efeito importa na pratica?):** Maior efeito: d = 1.308. d < 0.2 = trivial, 0.2-0.5 = pequeno, > 0.5 = medio.

**Limitacoes:** Pontos de corte arbitrarios. Correlacao, nao causalidade. Amostra de conveniencia.

**Graficos:**
- `outputs\figures\exploratory\phase56\H14_group_comparison.png`


---

### H15 — Existe um grupo puramente intelectual?

**Manchete:** A vida da mente: existem pessoas que so sentem prazer em pensar?

**Veredito:** [CONFIRMADA]

**Tecnica utilizada:** K-Means com k de 3 a 6. Para cada solucao, procurar um grupo onde o fator intellectual seja o mais alto e todos os outros fiquem abaixo da media geral. Criterio minimo: pelo menos 50 pessoas no grupo.

**Premissas verificadas:** Dados padronizados. A busca por um perfil especifico e exploratoria — o grupo pode nao existir como tipo natural.

**Resultado:** Busca por perfil 'intellectual-dominante' em k=3 a 6:
Encontrado.
  k = 3, grupo 0, N = 1,712
  interpersonal: 0.79
  thrilling: -0.80
  noble: -0.52
  reputational: 0.05
  sensorial: 0.26
  intellectual: 1.12

**Interpretacao:** Encontrado um grupo de 1,712 pessoas (k=3) com intellectual como fator dominante e todos os outros abaixo da media geral.

**Relevancia (o efeito importa na pratica?):** Grupo com 1712 pessoas — pequeno mas real.

**Limitacoes:** Buscar um perfil pre-definido e enviesado. O grupo pode ser um artefato do agrupamento. Resultado depende do k escolhido.

**Graficos:**
- `outputs\figures\exploratory\phase56\H15_profile_search.png`


---

*Relatorio gerado automaticamente por `src/analysts/segmentation.py`*
*Dados: Sources of Pleasure (ClearerThinking.org) — N = 6,587*
