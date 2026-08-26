# Fase 4 — Registro de Hipoteses

**Total:** 41 hipoteses registradas

**Viaveis:** 41 | **Estacionadas:** 0

**Fontes:** 14 observacoes da Fase 3 + artefatos numericos das Fases 2-3 + objetivo editorial (blog) + experiencia em ciencia de dados

**Principio:** cada hipotese e uma pergunta testavel com os dados que temos. Nenhuma exige dados externos ou demograficos.

---

## Resumo por categoria

| Categoria | Descricao | Analista | Qtd |
|-----------|-----------|---------|-----|
| DISTRIBUTIONAL | Forma das distribuicoes, polarizacao, universalidade | distributional | 7 |
| RELATIONAL | Correlacoes, associacoes, redundancias, incompatibilidades | relational | 9 |
| STRUCTURAL | Estrutura fatorial, dimensionalidade, coesao | structural | 7 |
| SEGMENTATION | Clustering, perfis de respondentes, subgrupos | segmentation | 7 |
| PREDICTIVE | Modelos preditivos, feature importance | predictive | 6 |
| COMPARATIVE | Comparacoes entre grupos derivados | comparative | 5 |
| **Total** | | | **41** |

## Resumo por prioridade

| Prioridade | Qtd |
|------------|-----|
| Alta | 21 |
| Media | 16 |
| Baixa | 4 |

---

## Distribucional — forma, universalidade e polarizacao

### H01 — Humor e a fonte de prazer com maior consenso positivo entre os respondentes (net agreement > 75%)?

- **Origem:** Fase 2 stats (net_agreement humor = 77.1%)
- **Categoria:** DISTRIBUTIONAL
- **Prioridade:** ***Alta***
- **Viabilidade:** Viavel
- **Notas:** Verificar se a diferenca para o segundo item (thinking, 73%) e significativa. Manchete potencial: 'Rir e o prazer mais universal'.

### H02 — Loving/being loved, Deep connection, Quality time e Learning sao as fontes de prazer mais universalmente valorizadas (top-2 box > 65%)?

- **Origem:** Fase 2 stats (top-2 box: connection 76%, learning 74%, quality time 74%, loving 71%)
- **Categoria:** DISTRIBUTIONAL
- **Prioridade:** ***Alta***
- **Viabilidade:** Viavel
- **Notas:** Ranking dos itens por top-2 box. Manchete: 'Conexao humana e aprendizado dominam o prazer'.

### H03 — Atividades emocionantes/arriscadas (fator Thrilling) sao a categoria de prazer mais rejeitada — unico fator com mediana negativa?

- **Origem:** O-08
- **Categoria:** DISTRIBUTIONAL
- **Prioridade:** ***Alta***
- **Viabilidade:** Viavel
- **Notas:** Comparar mediana, net agreement e bottom-2 box de Thrilling vs demais fatores.

### H04 — Sentimentos espirituais/religiosos sao a fonte de prazer mais polarizadora (maior desvio-padrao entre todos os itens)?

- **Origem:** Fase 2 stats (SD spiritual = 2.04, maior de todos os 37 itens)
- **Categoria:** DISTRIBUTIONAL
- **Prioridade:** ***Alta***
- **Viabilidade:** Viavel
- **Notas:** Spiritual tem moda = -3 mas 10.5% no +3. Manchete: 'Espiritualidade: o prazer que mais divide'.

### H05 — Itens com coeficiente de bimodalidade > 0.555 revelam populacoes com preferencias opostas, nao apenas alta dispersao?

- **Origem:** Fase 2 stats (bimodality_coeff)
- **Categoria:** DISTRIBUTIONAL
- **Prioridade:** **Media**
- **Viabilidade:** Viavel
- **Notas:** Verificar quais itens sao bimodais e se isso se traduz em subgrupos reais.

### H06 — A maioria dos respondentes concentra seu prazer em 2-3 fatores dominantes (especializacao) em vez de distribuir igualmente entre todos?

- **Origem:** Experiencia DS
- **Categoria:** DISTRIBUTIONAL
- **Prioridade:** ***Alta***
- **Viabilidade:** Viavel
- **Notas:** Calcular entropia do perfil individual (Shannon sobre os 6 scores de fator normalizados). Manchete: 'Somos especialistas ou generalistas do prazer?'

### H07 — Itens com forte efeito de teto (>30% no +3) tem menor poder discriminativo entre respondentes?

- **Origem:** Fase 2 stats (ceiling_pct: humor 42%, thinking 42%, connection 43%)
- **Categoria:** DISTRIBUTIONAL
- **Prioridade:** *Baixa*
- **Viabilidade:** Viavel
- **Notas:** Correlacionar ceiling_pct com desvio-padrao e entropia do item.

## Relacional — associacoes, redundancias e incompatibilidades

### H08 — Supporting community e Charity/altruism sao redundantes — medem essencialmente a mesma coisa (rho > 0.55)?

- **Origem:** O-03 (rho = 0.60)
- **Categoria:** RELATIONAL
- **Prioridade:** **Media**
- **Viabilidade:** Viavel
- **Notas:** Testar redundancia: correlacao parcial controlando os demais itens do fator Noble.

### H09 — Taking care of others e Supporting family sao redundantes (rho > 0.55)?

- **Origem:** Fase 3 corr (rho = 0.59)
- **Categoria:** RELATIONAL
- **Prioridade:** **Media**
- **Viabilidade:** Viavel
- **Notas:** Mesmo teste de redundancia que H08, para o fator Noble.

### H10 — Being liked correlaciona mais fortemente com itens do fator Reputacional (recognition, status, attractive) do que com os demais itens do Interpessoal?

- **Origem:** O-02, Fase 3 top correlations (Being liked ↔ Social recognition rho=0.44, Being liked ↔ Belonging rho=0.48)
- **Categoria:** RELATIONAL
- **Prioridade:** **Media**
- **Viabilidade:** Viavel
- **Notas:** Comparar correlacoes medias de Being liked com itens Interpessoal vs Reputacional.

### H11 — Existem pares de prazer 'incompativeis': nature vs status, learning vs partying, creativity vs competition representam oposicoes significativas?

- **Origem:** Fase 3 negative correlations (nature↔status rho=-0.10, competition↔creativity rho=-0.08)
- **Categoria:** RELATIONAL
- **Prioridade:** ***Alta***
- **Viabilidade:** Viavel
- **Notas:** Manchete: 'Prazeres incompativeis: quem ama natureza rejeita status'. Testar se as correlacoes negativas sao significativamente < 0.

### H12 — Humor e Musica (Sound) compartilham uma dimensao hedonica que nao pertence a nenhum fator (rho = 0.36)?

- **Origem:** O-14
- **Categoria:** RELATIONAL
- **Prioridade:** **Media**
- **Viabilidade:** Viavel
- **Notas:** Ambos sao standalone. Verificar se sua correlacao e mais forte do que com qualquer fator.

### H13 — O prazer intelectual (learning, thinking) e praticamente ortogonal ao prazer reputacional (status, power, recognition) — rho proximo de zero?

- **Origem:** O-01 (Reputacional-Intelectual rho = 0.02)
- **Categoria:** RELATIONAL
- **Prioridade:** ***Alta***
- **Viabilidade:** Viavel
- **Notas:** Manchete: 'Mentes curiosas nao buscam status — as duas dimensoes sao independentes'. Testar se rho nao e significativamente diferente de zero.

### H14 — A correlacao interpessoal-nobre (rho = 0.46) reflete uma orientacao prossocial — um superfator que agrupa quem se importa com pessoas e causas?

- **Origem:** O-01
- **Categoria:** RELATIONAL
- **Prioridade:** ***Alta***
- **Viabilidade:** Viavel
- **Notas:** Verificar se interpessoal + nobre formam um fator de segunda ordem. Manchete: 'O superfator prossocial: quem cuida de pessoas tambem cuida de causas'.

### H15 — Gostar de uma fonte de prazer dentro de um fator prediz significativamente gostar das outras do mesmo fator (consistencia intra-fator)?

- **Origem:** O-07 (coesao intra-fator: Interpessoal r=0.39, Intelectual r=0.29)
- **Categoria:** RELATIONAL
- **Prioridade:** **Media**
- **Viabilidade:** Viavel
- **Notas:** Quantificar a preditibilidade intra-fator por regressao item→demais do fator.

### H16 — Sexo (item standalone) correlaciona mais com Thrilling e Reputacional do que com Sensorial — contrariando a intuicao?

- **Origem:** O-14 (sex↔thrilling rho=0.25, sex↔reputational rho=0.21, sex↔sensorial rho=0.17)
- **Categoria:** RELATIONAL
- **Prioridade:** ***Alta***
- **Viabilidade:** Viavel
- **Notas:** Manchete: 'Prazer sexual: mais emocao e status do que sensacao?'

## Estrutural — dimensionalidade e organizacao dos fatores

### H17 — A estrutura empirica dos dados e melhor descrita por 8 dimensoes do que pelos 6 fatores do instrumento?

- **Origem:** O-04 (analise paralela sugere 8 componentes)
- **Categoria:** STRUCTURAL
- **Prioridade:** ***Alta***
- **Viabilidade:** Viavel
- **Notas:** Aplicar EFA com rotacao obliqua para 6, 7 e 8 fatores. Comparar fit indices.

### H18 — O fator Intelectual e o menos coeso (r inter-item = 0.29) e contem itens que carregam em componentes diferentes?

- **Origem:** O-07
- **Categoria:** STRUCTURAL
- **Prioridade:** **Media**
- **Viabilidade:** Viavel
- **Notas:** Analisar loadings dos 5 itens intelectuais na PCA. Algum carrega em PC inesperado?

### H19 — Being liked e Belonging to group carregam empiricamente mais no componente Reputacional do que no Interpessoal?

- **Origem:** O-05, O-06, Fase 3 top correlations (belonging↔being liked rho=0.48, cross-factor)
- **Categoria:** STRUCTURAL
- **Prioridade:** **Media**
- **Viabilidade:** Viavel
- **Notas:** Verificar loadings desses itens na EFA e no dendrograma.

### H20 — Uma EFA com rotacao obliqua produz uma solucao de 8 fatores interpretavel e superior a de 6?

- **Origem:** O-04
- **Categoria:** STRUCTURAL
- **Prioridade:** ***Alta***
- **Viabilidade:** Viavel
- **Notas:** Rodar EFA para 6 e 8 fatores. Comparar interpretabilidade e variancia explicada.

### H21 — Os itens standalone (humor, nature, sound, animals) formam ao menos um agrupamento empirico coeso quando incluidos na analise fatorial?

- **Origem:** O-14 (humor↔sound rho=0.36, nature↔animals rho=0.25)
- **Categoria:** STRUCTURAL
- **Prioridade:** ***Alta***
- **Viabilidade:** Viavel
- **Notas:** Manchete: 'Um setimo fator: a dimensao dos prazeres sensoriais-naturais'.

### H22 — Remover itens com cross-loadings altos (>0.30 em dois componentes) melhora a clareza da estrutura fatorial?

- **Origem:** O-05
- **Categoria:** STRUCTURAL
- **Prioridade:** *Baixa*
- **Viabilidade:** Viavel
- **Notas:** Identificar itens com cross-loading e re-rodar a EFA sem eles.

### H23 — A inclusao dos 6 itens standalone na EFA revela dimensoes nao capturadas pelos 6 fatores originais?

- **Origem:** O-14, experiencia DS
- **Categoria:** STRUCTURAL
- **Prioridade:** ***Alta***
- **Viabilidade:** Viavel
- **Notas:** EFA com todos os 37 itens e comparar com EFA apenas dos 31 itens dos fatores.

## Segmentacao — perfis e subgrupos de respondentes

### H24 — Os respondentes nao formam clusters discretos bem separados — a distribuicao de perfis de prazer e essencialmente continua?

- **Origem:** O-09, O-10 (silhouette k=2 = 0.114)
- **Categoria:** SEGMENTATION
- **Prioridade:** ***Alta***
- **Viabilidade:** Viavel
- **Notas:** Testar K-Means, hierarquico e GMM. Se todos dao silhouette < 0.25, a hipotese e sustentada.

### H25 — Com k=2, os clusters representam perfis interpretaveis: 'seletivos' (prazer concentrado em poucos fatores) vs 'amplos' (prazer distribuido)?

- **Origem:** O-10 (cluster 0: 40%, cluster 1: 60%)
- **Categoria:** SEGMENTATION
- **Prioridade:** ***Alta***
- **Viabilidade:** Viavel
- **Notas:** Manchete: 'Dois tipos de pessoa: quem concentra prazer vs quem gosta de tudo'.

### H26 — Existe um subgrupo identificavel de respondentes primariamente intelectuais (alto intelectual, relativamente baixo nos demais fatores)?

- **Origem:** Experiencia DS
- **Categoria:** SEGMENTATION
- **Prioridade:** **Media**
- **Viabilidade:** Viavel
- **Notas:** Verificar se algum cluster (k=3 a 6) isola um perfil intelectual puro.

### H27 — Respondentes com alto score em Thrilling (quartil superior) diferem sistematicamente em todos os outros fatores?

- **Origem:** O-08
- **Categoria:** SEGMENTATION
- **Prioridade:** ***Alta***
- **Viabilidade:** Viavel
- **Notas:** Manchete: 'Quem busca adrenalina: um perfil de prazer fundamentalmente diferente'.

### H28 — Respondentes com alto score espiritual (>+1) formam um subgrupo com perfil de prazer distinto dos demais?

- **Origem:** Fase 2 stats (spiritual: moda=-3 mas 23% >= +2)
- **Categoria:** SEGMENTATION
- **Prioridade:** **Media**
- **Viabilidade:** Viavel
- **Notas:** Spiritual e bimodal — os que gostam muito sao um grupo a parte?

### H29 — GMM (Gaussian Mixture Model) identifica uma solucao de clusters mais interpretavel que K-Means para estes dados?

- **Origem:** Experiencia DS
- **Categoria:** SEGMENTATION
- **Prioridade:** **Media**
- **Viabilidade:** Viavel
- **Notas:** GMM permite clusters elipticos e sobrepostos, mais adequado para distribuicao continua.

### H30 — A estabilidade dos clusters (bootstrap/subamostra) e baixa, confirmando que a segmentacao e fraca?

- **Origem:** O-10, experiencia DS
- **Categoria:** SEGMENTATION
- **Prioridade:** **Media**
- **Viabilidade:** Viavel
- **Notas:** Rodar K-Means em 100 subamostras de 80% e medir concordancia (ARI).

## Preditivo — o que prediz o que?

### H31 — Os 6 scores de fator sao preditores significativos do prazer medio geral (media dos 37 itens)?

- **Origem:** Experiencia DS
- **Categoria:** PREDICTIVE
- **Prioridade:** ***Alta***
- **Viabilidade:** Viavel
- **Notas:** Regressao multipla: mean_all_items ~ f_interpersonal + f_thrilling + ... + f_intellectual. Reportar R2, betas padronizados. Qual fator contribui mais?

### H32 — O score Interpessoal e o preditor individual mais forte do prazer geral?

- **Origem:** Fase 2 stats (interpessoal: media mais alta = 1.77)
- **Categoria:** PREDICTIVE
- **Prioridade:** **Media**
- **Viabilidade:** Viavel
- **Notas:** Regressao simples de cada fator → prazer medio. Comparar R2 individuais.

### H33 — Um modelo parcimonioso com menos de 10 itens consegue prever o perfil completo de prazer (37 itens) com R2 > 0.70?

- **Origem:** Experiencia DS
- **Categoria:** PREDICTIVE
- **Prioridade:** **Media**
- **Viabilidade:** Viavel
- **Notas:** Feature selection (Lasso ou stepwise) para encontrar itens-chave.

### H34 — Gostar de Loving/being loved prediz significativamente gostar de Deep connection e Quality time (cadeia interpessoal)?

- **Origem:** Fase 3 correlations (loving↔quality rho=0.44, quality↔connection rho=0.43)
- **Categoria:** PREDICTIVE
- **Prioridade:** ***Alta***
- **Viabilidade:** Viavel
- **Notas:** Manchete: 'Amor gera conexao: quem ama tambem valoriza tempo de qualidade'. Distinguir associacao de capacidade preditiva (split treino/teste).

### H35 — O perfil de 6 fatores de um respondente pode ser predito com boa acuracia a partir de apenas seus 5 itens mais extremos (top/bottom)?

- **Origem:** Experiencia DS
- **Categoria:** PREDICTIVE
- **Prioridade:** *Baixa*
- **Viabilidade:** Viavel
- **Notas:** Simular: pegar os 5 itens com |score| mais alto e prever os 6 scores de fator.

### H36 — Gostar de atividades de alto risco (adrenaline, scary, risk) prediz negativamente o prazer em relaxamento e natureza?

- **Origem:** Fase 3 negative correlations (exciting↔relaxation rho=-0.08)
- **Categoria:** PREDICTIVE
- **Prioridade:** ***Alta***
- **Viabilidade:** Viavel
- **Notas:** Manchete: 'Adrenalina vs. serenidade: dois caminhos opostos para o prazer'. Regressao: relaxation ~ adrenaline + scary + risk.

## Comparativo — diferencas entre grupos derivados

### H37 — Respondentes no quartil superior de Thrilling tem perfis de prazer significativamente diferentes dos do quartil inferior em todos os fatores?

- **Origem:** O-08
- **Categoria:** COMPARATIVE
- **Prioridade:** ***Alta***
- **Viabilidade:** Viavel
- **Notas:** Mann-Whitney (ou teste t) por fator: Q4 Thrilling vs Q1 Thrilling. Tamanho de efeito (d de Cohen).

### H38 — Respondentes no quartil superior de Intelectual tem scores significativamente menores em Reputacional do que os demais?

- **Origem:** O-01 (rho Reputacional-Intelectual = 0.02)
- **Categoria:** COMPARATIVE
- **Prioridade:** **Media**
- **Viabilidade:** Viavel
- **Notas:** Se rho≈0, os quartis extremos podem ainda divergir.

### H39 — Os 66 outliers multivariados (Mahalanobis P99) tem perfis de prazer qualitativamente diferentes do restante da amostra?

- **Origem:** O-13
- **Categoria:** COMPARATIVE
- **Prioridade:** **Media**
- **Viabilidade:** Viavel
- **Notas:** Comparar medias dos 6 fatores: outliers vs nao-outliers. Que tipo de pessoa e um outlier no espaco do prazer?

### H40 — Respondentes com alta diversidade de prazer (entropia individual alta) diferem dos com baixa diversidade em fatores especificos?

- **Origem:** Experiencia DS
- **Categoria:** COMPARATIVE
- **Prioridade:** ***Alta***
- **Viabilidade:** Viavel
- **Notas:** Manchete: 'Generalistas vs especialistas do prazer: quem e mais feliz?'

### H41 — Remover os 31 respondentes com padrao de resposta suspeito (3 straight-liners + 28 baixa variabilidade) nao altera significativamente os resultados descritivos?

- **Origem:** O-11, O-12
- **Categoria:** COMPARATIVE
- **Prioridade:** *Baixa*
- **Viabilidade:** Viavel
- **Notas:** Comparar medias e SDs com e sem esses respondentes. Se nao muda, confirma qualidade.

---

## Metodologia — como as hipoteses foram formuladas

### Fontes de inspiracao

1. **14 observacoes da Fase 3 (EDA)** — cada observacao termina com uma 'possivel pergunta' que foi transformada em hipotese testavel.
2. **Artefatos numericos das Fases 2-3** — revisao dos CSVs de estatisticas descritivas (item_stats, factor_stats) e das matrizes de correlacao e loadings da PCA para identificar padroes nao capturados pelas observacoes.
3. **Objetivo editorial** — perguntas formuladas com potencial de gerar manchetes publicaveis em blog (ex: 'Rir e o prazer mais universal', 'Adrenalina vs serenidade').
4. **Experiencia em ciencia de dados** — tecnicas e perguntas que costumam gerar insights valiosos (entropia individual, modelos preditivos parcimoniosos, estabilidade de clusters).

### Criterios de priorizacao

- **Alta:** alto potencial de gerar insight publicavel + viavel com os dados
- **Media:** interessante mas menos impactante ou mais tecnico
- **Baixa:** verificacao metodologica ou resultado esperado

### Categorias e roteamento

Cada hipotese foi categorizada para ser roteada ao analista especialista correto nas Fases 5-6. As categorias seguem o PRD:

- **DISTRIBUTIONAL** → analisa formas de distribuicao, padroes de resposta
- **RELATIONAL** → correlacoes, associacoes entre variaveis
- **STRUCTURAL** → estrutura fatorial, dimensionalidade, EFA/PCA
- **SEGMENTATION** → clustering, perfis, tipologias
- **PREDICTIVE** → modelos preditivos, feature selection
- **COMPARATIVE** → comparacoes entre grupos (derivados dos dados)

### Viabilidade

Todas as 41 hipoteses sao viaveis com os dados disponiveis. Nenhuma requer dados demograficos ou externos. Hipoteses COMPARATIVE usam grupos derivados (quartis, clusters, flags de anomalia).

---

*Gerado por `scripts/phase4_hypotheses.py` — 41 hipoteses*
