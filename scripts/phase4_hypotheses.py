"""
Phase 4 — Hypothesis Registration.
Transforms EDA observations + item/factor stats + editorial goals
into a structured list of testable hypotheses, categorized and prioritized.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_PATH = PROJECT_ROOT / "outputs" / "reports" / "phase4_hypotheses.md"

# ---------------------------------------------------------------------------
# Hypothesis registry — each tuple:
#   (id, question_pt, origin, category, priority, viable, notes)
# ---------------------------------------------------------------------------

hypotheses = [
    # ===================================================================
    # DISTRIBUTIONAL (7)
    # ===================================================================
    ("H01",
     "Humor e a fonte de prazer com maior consenso positivo entre os respondentes "
     "(net agreement > 75%)?",
     "Fase 2 stats (net_agreement humor = 77.1%)",
     "DISTRIBUTIONAL", "alta", True,
     "Verificar se a diferenca para o segundo item (thinking, 73%) e significativa. "
     "Manchete potencial: 'Rir e o prazer mais universal'."),

    ("H02",
     "Loving/being loved, Deep connection, Quality time e Learning sao as fontes de "
     "prazer mais universalmente valorizadas (top-2 box > 65%)?",
     "Fase 2 stats (top-2 box: connection 76%, learning 74%, quality time 74%, loving 71%)",
     "DISTRIBUTIONAL", "alta", True,
     "Ranking dos itens por top-2 box. Manchete: 'Conexao humana e aprendizado dominam o prazer'."),

    ("H03",
     "Atividades emocionantes/arriscadas (fator Thrilling) sao a categoria de prazer "
     "mais rejeitada — unico fator com mediana negativa?",
     "O-08",
     "DISTRIBUTIONAL", "alta", True,
     "Comparar mediana, net agreement e bottom-2 box de Thrilling vs demais fatores."),

    ("H04",
     "Sentimentos espirituais/religiosos sao a fonte de prazer mais polarizadora "
     "(maior desvio-padrao entre todos os itens)?",
     "Fase 2 stats (SD spiritual = 2.04, maior de todos os 37 itens)",
     "DISTRIBUTIONAL", "alta", True,
     "Spiritual tem moda = -3 mas 10.5% no +3. Manchete: 'Espiritualidade: o prazer que mais divide'."),

    ("H05",
     "Itens com coeficiente de bimodalidade > 0.555 revelam populacoes com preferencias "
     "opostas, nao apenas alta dispersao?",
     "Fase 2 stats (bimodality_coeff)",
     "DISTRIBUTIONAL", "media", True,
     "Verificar quais itens sao bimodais e se isso se traduz em subgrupos reais."),

    ("H06",
     "A maioria dos respondentes concentra seu prazer em 2-3 fatores dominantes "
     "(especializacao) em vez de distribuir igualmente entre todos?",
     "Experiencia DS",
     "DISTRIBUTIONAL", "alta", True,
     "Calcular entropia do perfil individual (Shannon sobre os 6 scores de fator normalizados). "
     "Manchete: 'Somos especialistas ou generalistas do prazer?'"),

    ("H07",
     "Itens com forte efeito de teto (>30% no +3) tem menor poder discriminativo "
     "entre respondentes?",
     "Fase 2 stats (ceiling_pct: humor 42%, thinking 42%, connection 43%)",
     "DISTRIBUTIONAL", "baixa", True,
     "Correlacionar ceiling_pct com desvio-padrao e entropia do item."),

    # ===================================================================
    # RELATIONAL (9)
    # ===================================================================
    ("H08",
     "Supporting community e Charity/altruism sao redundantes — medem essencialmente "
     "a mesma coisa (rho > 0.55)?",
     "O-03 (rho = 0.60)",
     "RELATIONAL", "media", True,
     "Testar redundancia: correlacao parcial controlando os demais itens do fator Noble."),

    ("H09",
     "Taking care of others e Supporting family sao redundantes (rho > 0.55)?",
     "Fase 3 corr (rho = 0.59)",
     "RELATIONAL", "media", True,
     "Mesmo teste de redundancia que H08, para o fator Noble."),

    ("H10",
     "Being liked correlaciona mais fortemente com itens do fator Reputacional "
     "(recognition, status, attractive) do que com os demais itens do Interpessoal?",
     "O-02, Fase 3 top correlations (Being liked ↔ Social recognition rho=0.44, "
     "Being liked ↔ Belonging rho=0.48)",
     "RELATIONAL", "media", True,
     "Comparar correlacoes medias de Being liked com itens Interpessoal vs Reputacional."),

    ("H11",
     "Existem pares de prazer 'incompativeis': nature vs status, learning vs partying, "
     "creativity vs competition representam oposicoes significativas?",
     "Fase 3 negative correlations (nature↔status rho=-0.10, competition↔creativity rho=-0.08)",
     "RELATIONAL", "alta", True,
     "Manchete: 'Prazeres incompativeis: quem ama natureza rejeita status'. "
     "Testar se as correlacoes negativas sao significativamente < 0."),

    ("H12",
     "Humor e Musica (Sound) compartilham uma dimensao hedonica que nao pertence a "
     "nenhum fator (rho = 0.36)?",
     "O-14",
     "RELATIONAL", "media", True,
     "Ambos sao standalone. Verificar se sua correlacao e mais forte do que com qualquer fator."),

    ("H13",
     "O prazer intelectual (learning, thinking) e praticamente ortogonal ao prazer "
     "reputacional (status, power, recognition) — rho proximo de zero?",
     "O-01 (Reputacional-Intelectual rho = 0.02)",
     "RELATIONAL", "alta", True,
     "Manchete: 'Mentes curiosas nao buscam status — as duas dimensoes sao independentes'. "
     "Testar se rho nao e significativamente diferente de zero."),

    ("H14",
     "A correlacao interpessoal-nobre (rho = 0.46) reflete uma orientacao prossocial "
     "— um superfator que agrupa quem se importa com pessoas e causas?",
     "O-01",
     "RELATIONAL", "alta", True,
     "Verificar se interpessoal + nobre formam um fator de segunda ordem. "
     "Manchete: 'O superfator prossocial: quem cuida de pessoas tambem cuida de causas'."),

    ("H15",
     "Gostar de uma fonte de prazer dentro de um fator prediz significativamente "
     "gostar das outras do mesmo fator (consistencia intra-fator)?",
     "O-07 (coesao intra-fator: Interpessoal r=0.39, Intelectual r=0.29)",
     "RELATIONAL", "media", True,
     "Quantificar a preditibilidade intra-fator por regressao item→demais do fator."),

    ("H16",
     "Sexo (item standalone) correlaciona mais com Thrilling e Reputacional do que "
     "com Sensorial — contrariando a intuicao?",
     "O-14 (sex↔thrilling rho=0.25, sex↔reputational rho=0.21, sex↔sensorial rho=0.17)",
     "RELATIONAL", "alta", True,
     "Manchete: 'Prazer sexual: mais emocao e status do que sensacao?'"),

    # ===================================================================
    # STRUCTURAL (7)
    # ===================================================================
    ("H17",
     "A estrutura empirica dos dados e melhor descrita por 8 dimensoes do que "
     "pelos 6 fatores do instrumento?",
     "O-04 (analise paralela sugere 8 componentes)",
     "STRUCTURAL", "alta", True,
     "Aplicar EFA com rotacao obliqua para 6, 7 e 8 fatores. Comparar fit indices."),

    ("H18",
     "O fator Intelectual e o menos coeso (r inter-item = 0.29) e contem itens "
     "que carregam em componentes diferentes?",
     "O-07",
     "STRUCTURAL", "media", True,
     "Analisar loadings dos 5 itens intelectuais na PCA. Algum carrega em PC inesperado?"),

    ("H19",
     "Being liked e Belonging to group carregam empiricamente mais no componente "
     "Reputacional do que no Interpessoal?",
     "O-05, O-06, Fase 3 top correlations (belonging↔being liked rho=0.48, cross-factor)",
     "STRUCTURAL", "media", True,
     "Verificar loadings desses itens na EFA e no dendrograma."),

    ("H20",
     "Uma EFA com rotacao obliqua produz uma solucao de 8 fatores interpretavel "
     "e superior a de 6?",
     "O-04",
     "STRUCTURAL", "alta", True,
     "Rodar EFA para 6 e 8 fatores. Comparar interpretabilidade e variancia explicada."),

    ("H21",
     "Os itens standalone (humor, nature, sound, animals) formam ao menos um "
     "agrupamento empirico coeso quando incluidos na analise fatorial?",
     "O-14 (humor↔sound rho=0.36, nature↔animals rho=0.25)",
     "STRUCTURAL", "alta", True,
     "Manchete: 'Um setimo fator: a dimensao dos prazeres sensoriais-naturais'."),

    ("H22",
     "Remover itens com cross-loadings altos (>0.30 em dois componentes) melhora "
     "a clareza da estrutura fatorial?",
     "O-05",
     "STRUCTURAL", "baixa", True,
     "Identificar itens com cross-loading e re-rodar a EFA sem eles."),

    ("H23",
     "A inclusao dos 6 itens standalone na EFA revela dimensoes nao capturadas "
     "pelos 6 fatores originais?",
     "O-14, experiencia DS",
     "STRUCTURAL", "alta", True,
     "EFA com todos os 37 itens e comparar com EFA apenas dos 31 itens dos fatores."),

    # ===================================================================
    # SEGMENTATION (7)
    # ===================================================================
    ("H24",
     "Os respondentes nao formam clusters discretos bem separados — a distribuicao "
     "de perfis de prazer e essencialmente continua?",
     "O-09, O-10 (silhouette k=2 = 0.114)",
     "SEGMENTATION", "alta", True,
     "Testar K-Means, hierarquico e GMM. Se todos dao silhouette < 0.25, a hipotese "
     "e sustentada."),

    ("H25",
     "Com k=2, os clusters representam perfis interpretaveis: 'seletivos' (prazer "
     "concentrado em poucos fatores) vs 'amplos' (prazer distribuido)?",
     "O-10 (cluster 0: 40%, cluster 1: 60%)",
     "SEGMENTATION", "alta", True,
     "Manchete: 'Dois tipos de pessoa: quem concentra prazer vs quem gosta de tudo'."),

    ("H26",
     "Existe um subgrupo identificavel de respondentes primariamente intelectuais "
     "(alto intelectual, relativamente baixo nos demais fatores)?",
     "Experiencia DS",
     "SEGMENTATION", "media", True,
     "Verificar se algum cluster (k=3 a 6) isola um perfil intelectual puro."),

    ("H27",
     "Respondentes com alto score em Thrilling (quartil superior) diferem "
     "sistematicamente em todos os outros fatores?",
     "O-08",
     "SEGMENTATION", "alta", True,
     "Manchete: 'Quem busca adrenalina: um perfil de prazer fundamentalmente diferente'."),

    ("H28",
     "Respondentes com alto score espiritual (>+1) formam um subgrupo com "
     "perfil de prazer distinto dos demais?",
     "Fase 2 stats (spiritual: moda=-3 mas 23% >= +2)",
     "SEGMENTATION", "media", True,
     "Spiritual e bimodal — os que gostam muito sao um grupo a parte?"),

    ("H29",
     "GMM (Gaussian Mixture Model) identifica uma solucao de clusters mais "
     "interpretavel que K-Means para estes dados?",
     "Experiencia DS",
     "SEGMENTATION", "media", True,
     "GMM permite clusters elipticos e sobrepostos, mais adequado para distribuicao continua."),

    ("H30",
     "A estabilidade dos clusters (bootstrap/subamostra) e baixa, confirmando "
     "que a segmentacao e fraca?",
     "O-10, experiencia DS",
     "SEGMENTATION", "media", True,
     "Rodar K-Means em 100 subamostras de 80% e medir concordancia (ARI)."),

    # ===================================================================
    # PREDICTIVE (6)
    # ===================================================================
    ("H31",
     "Os 6 scores de fator sao preditores significativos do prazer medio geral "
     "(media dos 37 itens)?",
     "Experiencia DS",
     "PREDICTIVE", "alta", True,
     "Regressao multipla: mean_all_items ~ f_interpersonal + f_thrilling + ... + f_intellectual. "
     "Reportar R2, betas padronizados. Qual fator contribui mais?"),

    ("H32",
     "O score Interpessoal e o preditor individual mais forte do prazer geral?",
     "Fase 2 stats (interpessoal: media mais alta = 1.77)",
     "PREDICTIVE", "media", True,
     "Regressao simples de cada fator → prazer medio. Comparar R2 individuais."),

    ("H33",
     "Um modelo parcimonioso com menos de 10 itens consegue prever o perfil "
     "completo de prazer (37 itens) com R2 > 0.70?",
     "Experiencia DS",
     "PREDICTIVE", "media", True,
     "Feature selection (Lasso ou stepwise) para encontrar itens-chave."),

    ("H34",
     "Gostar de Loving/being loved prediz significativamente gostar de "
     "Deep connection e Quality time (cadeia interpessoal)?",
     "Fase 3 correlations (loving↔quality rho=0.44, quality↔connection rho=0.43)",
     "PREDICTIVE", "alta", True,
     "Manchete: 'Amor gera conexao: quem ama tambem valoriza tempo de qualidade'. "
     "Distinguir associacao de capacidade preditiva (split treino/teste)."),

    ("H35",
     "O perfil de 6 fatores de um respondente pode ser predito com boa acuracia "
     "a partir de apenas seus 5 itens mais extremos (top/bottom)?",
     "Experiencia DS",
     "PREDICTIVE", "baixa", True,
     "Simular: pegar os 5 itens com |score| mais alto e prever os 6 scores de fator."),

    ("H36",
     "Gostar de atividades de alto risco (adrenaline, scary, risk) prediz "
     "negativamente o prazer em relaxamento e natureza?",
     "Fase 3 negative correlations (exciting↔relaxation rho=-0.08)",
     "PREDICTIVE", "alta", True,
     "Manchete: 'Adrenalina vs. serenidade: dois caminhos opostos para o prazer'. "
     "Regressao: relaxation ~ adrenaline + scary + risk."),

    # ===================================================================
    # COMPARATIVE (5)
    # ===================================================================
    ("H37",
     "Respondentes no quartil superior de Thrilling tem perfis de prazer "
     "significativamente diferentes dos do quartil inferior em todos os fatores?",
     "O-08",
     "COMPARATIVE", "alta", True,
     "Mann-Whitney (ou teste t) por fator: Q4 Thrilling vs Q1 Thrilling. "
     "Tamanho de efeito (d de Cohen)."),

    ("H38",
     "Respondentes no quartil superior de Intelectual tem scores significativamente "
     "menores em Reputacional do que os demais?",
     "O-01 (rho Reputacional-Intelectual = 0.02)",
     "COMPARATIVE", "media", True,
     "Se rho≈0, os quartis extremos podem ainda divergir."),

    ("H39",
     "Os 66 outliers multivariados (Mahalanobis P99) tem perfis de prazer "
     "qualitativamente diferentes do restante da amostra?",
     "O-13",
     "COMPARATIVE", "media", True,
     "Comparar medias dos 6 fatores: outliers vs nao-outliers. "
     "Que tipo de pessoa e um outlier no espaco do prazer?"),

    ("H40",
     "Respondentes com alta diversidade de prazer (entropia individual alta) diferem "
     "dos com baixa diversidade em fatores especificos?",
     "Experiencia DS",
     "COMPARATIVE", "alta", True,
     "Manchete: 'Generalistas vs especialistas do prazer: quem e mais feliz?'"),

    ("H41",
     "Remover os 31 respondentes com padrao de resposta suspeito (3 straight-liners + "
     "28 baixa variabilidade) nao altera significativamente os resultados descritivos?",
     "O-11, O-12",
     "COMPARATIVE", "baixa", True,
     "Comparar medias e SDs com e sem esses respondentes. Se nao muda, confirma qualidade."),
]

# ---------------------------------------------------------------------------
# Category counts and summary
# ---------------------------------------------------------------------------
from collections import Counter

cat_counts = Counter(h[3] for h in hypotheses)
priority_counts = Counter(h[4] for h in hypotheses)
viable_count = sum(1 for h in hypotheses if h[5])
parked_count = sum(1 for h in hypotheses if not h[5])

# ---------------------------------------------------------------------------
# Generate report
# ---------------------------------------------------------------------------
lines = []
lines.append("# Fase 4 — Registro de Hipoteses\n")
lines.append(f"**Total:** {len(hypotheses)} hipoteses registradas\n")
lines.append(f"**Viaveis:** {viable_count} | **Estacionadas:** {parked_count}\n")
lines.append("**Fontes:** 14 observacoes da Fase 3 + artefatos numericos das Fases 2-3 "
             "+ objetivo editorial (blog) + experiencia em ciencia de dados\n")
lines.append("**Principio:** cada hipotese e uma pergunta testavel com os dados que temos. "
             "Nenhuma exige dados externos ou demograficos.\n")

lines.append("---\n")
lines.append("## Resumo por categoria\n")
lines.append("| Categoria | Descricao | Analista | Qtd |")
lines.append("|-----------|-----------|---------|-----|")
lines.append(f"| DISTRIBUTIONAL | Forma das distribuicoes, polarizacao, universalidade | distributional | {cat_counts['DISTRIBUTIONAL']} |")
lines.append(f"| RELATIONAL | Correlacoes, associacoes, redundancias, incompatibilidades | relational | {cat_counts['RELATIONAL']} |")
lines.append(f"| STRUCTURAL | Estrutura fatorial, dimensionalidade, coesao | structural | {cat_counts['STRUCTURAL']} |")
lines.append(f"| SEGMENTATION | Clustering, perfis de respondentes, subgrupos | segmentation | {cat_counts['SEGMENTATION']} |")
lines.append(f"| PREDICTIVE | Modelos preditivos, feature importance | predictive | {cat_counts['PREDICTIVE']} |")
lines.append(f"| COMPARATIVE | Comparacoes entre grupos derivados | comparative | {cat_counts['COMPARATIVE']} |")
lines.append(f"| **Total** | | | **{len(hypotheses)}** |")

lines.append("\n## Resumo por prioridade\n")
lines.append("| Prioridade | Qtd |")
lines.append("|------------|-----|")
for p in ["alta", "media", "baixa"]:
    lines.append(f"| {p.capitalize()} | {priority_counts[p]} |")

lines.append("\n---\n")

# Group hypotheses by category
categories_order = [
    ("DISTRIBUTIONAL", "Distribucional — forma, universalidade e polarizacao"),
    ("RELATIONAL", "Relacional — associacoes, redundancias e incompatibilidades"),
    ("STRUCTURAL", "Estrutural — dimensionalidade e organizacao dos fatores"),
    ("SEGMENTATION", "Segmentacao — perfis e subgrupos de respondentes"),
    ("PREDICTIVE", "Preditivo — o que prediz o que?"),
    ("COMPARATIVE", "Comparativo — diferencas entre grupos derivados"),
]

for cat_key, cat_title in categories_order:
    cat_hyps = [h for h in hypotheses if h[3] == cat_key]
    lines.append(f"## {cat_title}\n")

    for h_id, question, origin, category, priority, viable, notes in cat_hyps:
        status = "Viavel" if viable else "Estacionada"
        priority_emoji = {"alta": "***Alta***", "media": "**Media**", "baixa": "*Baixa*"}[priority]

        lines.append(f"### {h_id} — {question}\n")
        lines.append(f"- **Origem:** {origin}")
        lines.append(f"- **Categoria:** {category}")
        lines.append(f"- **Prioridade:** {priority_emoji}")
        lines.append(f"- **Viabilidade:** {status}")
        lines.append(f"- **Notas:** {notes}")
        lines.append("")

lines.append("---\n")

# Methodology
lines.append("## Metodologia — como as hipoteses foram formuladas\n")
lines.append("### Fontes de inspiracao\n")
lines.append("1. **14 observacoes da Fase 3 (EDA)** — cada observacao termina com uma "
             "'possivel pergunta' que foi transformada em hipotese testavel.")
lines.append("2. **Artefatos numericos das Fases 2-3** — revisao dos CSVs de estatisticas "
             "descritivas (item_stats, factor_stats) e das matrizes de correlacao e loadings "
             "da PCA para identificar padroes nao capturados pelas observacoes.")
lines.append("3. **Objetivo editorial** — perguntas formuladas com potencial de gerar "
             "manchetes publicaveis em blog (ex: 'Rir e o prazer mais universal', "
             "'Adrenalina vs serenidade').")
lines.append("4. **Experiencia em ciencia de dados** — tecnicas e perguntas que costumam "
             "gerar insights valiosos (entropia individual, modelos preditivos parcimoniosos, "
             "estabilidade de clusters).\n")

lines.append("### Criterios de priorizacao\n")
lines.append("- **Alta:** alto potencial de gerar insight publicavel + viavel com os dados")
lines.append("- **Media:** interessante mas menos impactante ou mais tecnico")
lines.append("- **Baixa:** verificacao metodologica ou resultado esperado\n")

lines.append("### Categorias e roteamento\n")
lines.append("Cada hipotese foi categorizada para ser roteada ao analista especialista "
             "correto nas Fases 5-6. As categorias seguem o PRD:\n")
lines.append("- **DISTRIBUTIONAL** → analisa formas de distribuicao, padroes de resposta")
lines.append("- **RELATIONAL** → correlacoes, associacoes entre variaveis")
lines.append("- **STRUCTURAL** → estrutura fatorial, dimensionalidade, EFA/PCA")
lines.append("- **SEGMENTATION** → clustering, perfis, tipologias")
lines.append("- **PREDICTIVE** → modelos preditivos, feature selection")
lines.append("- **COMPARATIVE** → comparacoes entre grupos (derivados dos dados)\n")

lines.append("### Viabilidade\n")
lines.append("Todas as 41 hipoteses sao viaveis com os dados disponiveis. "
             "Nenhuma requer dados demograficos ou externos. Hipoteses COMPARATIVE "
             "usam grupos derivados (quartis, clusters, flags de anomalia).\n")

lines.append("---\n")
lines.append(f"*Gerado por `scripts/phase4_hypotheses.py` — {len(hypotheses)} hipoteses*\n")

report_text = "\n".join(lines)
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(report_text)

print(f"Fase 4 concluida!")
print(f"  Relatorio: {REPORT_PATH}")
print(f"  Total de hipoteses: {len(hypotheses)}")
print(f"  Por categoria: {dict(cat_counts)}")
print(f"  Por prioridade: {dict(priority_counts)}")
print(f"  Viaveis: {viable_count} | Estacionadas: {parked_count}")
