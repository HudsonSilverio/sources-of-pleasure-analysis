# Relatorio do Analista Distribucional

**Data:** 2026-08-28 09:49
**Hipoteses analisadas:** 4
**Respondentes:** N = 6,587
**Seed aleatoria:** 42

## Resumo de vereditos

| Hipotese | Titulo | Veredito |
|----------|--------|----------|
| H01 | Rir e a fonte de prazer mais universal? | confirmada |
| H02 | Conexao, amor e aprendizado dominam o ranking? | confirmada |
| H03 | Buscar emocao forte e a categoria mais rejeitada? | confirmada |
| H04 | Espiritualidade divide as pessoas em dois grupos? | confirmada |

## Analises detalhadas

---

### H01 — Rir e a fonte de prazer mais universal?

**Manchete:** Rir: o unico prazer com que quase todo mundo concorda

**Veredito:** [CONFIRMADA]

**Tecnica utilizada:** Ranking por net_agreement com intervalos de confianca via bootstrap (1000 reamostras)

**Premissas verificadas:** Bootstrap com 1000 reamostras. Intervalos de confianca de 95% (percentis 2.5 e 97.5). Metrica: net_agreement.

**Resultado:** Top 5 itens por net_agreement:
  1. Laughing / humor: 77.1% (IC 95%: 76.0 – 78.1)
  2. Deep personal connection: 74.5% (IC 95%: 73.2 – 75.7)
  3. Exploring ideas / thinking: 73.1% (IC 95%: 71.8 – 74.2)
  4. Learning: 72.4% (IC 95%: 71.3 – 73.6)
  5. Quality time with loved ones: 71.8% (IC 95%: 70.6 – 73.0)

Diferenca entre 1o e 2o lugar: 2.6 pontos percentuais. Sobreposicao de intervalos: nao.

**Interpretacao:** p_humor e o lider claro do ranking — seu intervalo de confianca nao se sobrepoem com o segundo colocado (p_connection).

**Relevancia (o efeito importa na pratica?):** A diferenca entre os primeiros e de 2.6 pontos percentuais — pequena.

**Limitacoes:** Bootstrap assume que a amostra e representativa. Como a amostra e de conveniencia (visitantes do ClearerThinking), o ranking pode nao refletir a populacao geral.

**Graficos:**
- `outputs\figures\exploratory\phase56\H01_ranking_bootstrap.png`


---

### H02 — Conexao, amor e aprendizado dominam o ranking?

**Manchete:** Conexao humana e aprendizado: o que as pessoas mais valorizam

**Veredito:** [CONFIRMADA]

**Tecnica utilizada:** Ranking por top2_pct com intervalos de confianca via bootstrap (1000 reamostras)

**Premissas verificadas:** Bootstrap com 1000 reamostras. Intervalos de confianca de 95% (percentis 2.5 e 97.5). Metrica: top2_pct.

**Resultado:** Top 5 itens por top2_pct:
  1. Laughing / humor: 78.1% (IC 95%: 77.0 – 79.1)
  2. Deep personal connection: 76.1% (IC 95%: 75.0 – 77.0)
  3. Exploring ideas / thinking: 74.9% (IC 95%: 73.9 – 76.0)
  4. Learning: 74.2% (IC 95%: 73.2 – 75.2)
  5. Quality time with loved ones: 73.9% (IC 95%: 72.9 – 75.0)

Diferenca entre 1o e 2o lugar: 2.1 pontos percentuais. Sobreposicao de intervalos: nao.

**Interpretacao:** p_humor e o lider claro do ranking — seu intervalo de confianca nao se sobrepoem com o segundo colocado (p_connection).

**Relevancia (o efeito importa na pratica?):** A diferenca entre os primeiros e de 2.1 pontos percentuais — pequena.

**Limitacoes:** Bootstrap assume que a amostra e representativa. Como a amostra e de conveniencia (visitantes do ClearerThinking), o ranking pode nao refletir a populacao geral.

**Graficos:**
- `outputs\figures\exploratory\phase56\H02_ranking_bootstrap.png`


---

### H03 — Buscar emocao forte e a categoria mais rejeitada?

**Manchete:** A maioria nao quer adrenalina — emocao forte e o prazer menos popular

**Veredito:** [CONFIRMADA]

**Tecnica utilizada:** Comparacao dos 6 fatores por mediana. Teste Wilcoxon (compara pares sem assumir que os dados sao simetricos) entre o fator mais baixo e o segundo mais baixo. Tamanho de efeito: r = Z / sqrt(N).

**Premissas verificadas:** Teste Wilcoxon nao exige normalidade. As comparacoes sao pareadas (mesmo respondente em ambos os fatores). Com N grande, p-valor quase sempre sera significativo — o tamanho de efeito (r) e o que realmente importa.

**Resultado:** Ranking dos 6 fatores por mediana:
  1. Emocionante: -0.33
  2. Reputacional: 0.50
  3. Nobre: 0.67
  4. Sensorial: 1.25
  5. Intelectual: 1.80
  6. Interpessoal: 2.00

Teste Wilcoxon entre thrilling e reputational: W = 3101829, p = 0.00e+00, r = inf

**Interpretacao:** O fator thrilling (mediana = -0.33) e o mais baixo dos 6 fatores e a diferenca para o segundo mais baixo (reputational, mediana = 0.50) e real (p < 0.001) e relevante (r = inf).

**Relevancia (o efeito importa na pratica?):** r = inf. Efeito grande — a diferenca e substancial.

**Limitacoes:** Dados de autorrelato, amostra de conveniencia. Correlacao entre fatores nao e controlada nesta comparacao.

**Graficos:**
- `outputs\figures\exploratory\phase56\H03_factor_comparison.png`


---

### H04 — Espiritualidade divide as pessoas em dois grupos?

**Manchete:** Espiritualidade: o prazer que racha a sala ao meio

**Veredito:** [CONFIRMADA]

**Tecnica utilizada:** Mistura gaussiana (GMM — ajusta 1 vs 2 curvas nos dados e compara qual modelo se encaixa melhor usando o BIC, uma medida de qualidade do ajuste — quanto menor, melhor).

**Premissas verificadas:** GMM nao exige normalidade dos dados. Criterio de decisao: diferenca de BIC > 10 entre 1 e 2 componentes indica forte evidencia de 2 grupos.

**Resultado:** BIC com 1 curva: 28087
BIC com 2 curvas: 25973
Diferenca: 2114 (> 10 = forte evidencia de 2 grupos)

Grupo 1: media = -2.6, peso = 64.4%
Grupo 2: media = 0.9, peso = 35.6%

**Interpretacao:** O modelo com 2 curvas (BIC = 25973) ajusta muito melhor que o de 1 curva (BIC = 28087). Diferenca de BIC = 2114 (acima de 10 e forte). Existem dois grupos: um centrado em -2.6 e outro em 0.9.

**Relevancia (o efeito importa na pratica?):** Separacao entre os grupos: 3.4 pontos na escala de -3 a +3. Grupos bem separados — a divisao e real.

**Limitacoes:** GMM assume que cada grupo segue uma curva normal, o que pode nao ser perfeito para dados Likert com limites fixos (-3 a +3). O item e discreto (7 valores), nao continuo.

**Graficos:**
- `outputs\figures\exploratory\phase56\H04_bimodality_gmm.png`


---

*Relatorio gerado automaticamente por `src/analysts/distributional.py`*
*Dados: Sources of Pleasure (ClearerThinking.org) — N = 6,587*
