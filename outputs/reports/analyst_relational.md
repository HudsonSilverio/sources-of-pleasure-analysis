# Relatorio do Analista Relacional

**Data:** 2026-08-28 09:49
**Hipoteses analisadas:** 5
**Respondentes:** N = 6,587
**Seed aleatoria:** 42

## Resumo de vereditos

| Hipotese | Titulo | Veredito |
|----------|--------|----------|
| H05 | Alguns prazeres sao realmente incompativeis? | confirmada |
| H06 | Mentes curiosas sao indiferentes a status? | confirmada |
| H07 | Existe um superfator 'quem cuida'? | confirmada |
| H08 | Prazer sexual: emocao ou sensacao? | confirmada |
| H09 | Amor prediz conexao e tempo de qualidade? | confirmada |

## Analises detalhadas

---

### H05 — Alguns prazeres sao realmente incompativeis?

**Manchete:** Quem ama natureza nao liga pra status — alguns prazeres sao incompativeis

**Veredito:** [CONFIRMADA]

**Tecnica utilizada:** Correlacao de Spearman de um lado so (testa se e realmente negativa) para todos os pares de itens com correlacao negativa. Correcao FDR de Benjamini-Hochberg para evitar falsos positivos quando se testa muitos pares ao mesmo tempo.

**Premissas verificadas:** Spearman nao exige normalidade. Total de pares testados: 55. Alpha apos correcao: 0.05.

**Resultado:** Total de pares com correlacao negativa: 55
Pares que sobreviveram a correcao FDR (alpha=0.05): 26

Top 5 pares negativos significativos:
  Being in nature × High status: rho = -0.098, p_corr = 0.0000
  Competition / winning × Being in nature: rho = -0.084, p_corr = 0.0000
  Competition / winning × Creativity: rho = -0.083, p_corr = 0.0000
  High intensity situations × Relaxation: rho = -0.075, p_corr = 0.0000
  Interacting with animals × High status: rho = -0.074, p_corr = 0.0000


**Interpretacao:** 26 de 55 pares negativos sobreviveram a correcao para multiplas comparacoes (FDR). O par mais forte: Being in nature × High status (rho = -0.098). Existem prazeres genuinamente incompativeis.

**Relevancia (o efeito importa na pratica?):** Mesmo os pares significativos tem correlacoes fracas (|rho| < 0.15). A incompatibilidade existe mas e sutil — nao e como se gostar de natureza impedisse de gostar de status.

**Limitacoes:** Correlacoes negativas fracas podem ser artefato da escala (-3 a +3) e do tipo de amostra. Amostra de conveniencia.

**Graficos:**
- `outputs\figures\exploratory\phase56\H05_negative_correlations.png`


---

### H06 — Mentes curiosas sao indiferentes a status?

**Manchete:** Mentes curiosas nao buscam status — as duas dimensoes sao independentes

**Veredito:** [CONFIRMADA]

**Tecnica utilizada:** Teste de equivalencia TOST (Two One-Sided Tests — testa se a correlacao e tao perto de zero que nao importa). Faixa de equivalencia: |rho| < 0.1.

**Premissas verificadas:** Fisher z-transform para a correlacao. Faixa de equivalencia definida como |rho| < 0.1 (efeitos menores que isso sao triviais).

**Resultado:** Correlacao Spearman entre intellectual e reputational: rho = 0.023
Teste TOST (faixa de equivalencia: |rho| < 0.1):
  p_upper = 0.0000, p_lower = 0.0000
  p_TOST = 0.0000 (< 0.05 → equivalente a zero)

**Interpretacao:** A correlacao entre intellectual e reputational (rho = 0.023) esta dentro da faixa de equivalencia a zero (|rho| < 0.1). Sao mundos realmente independentes.

**Relevancia (o efeito importa na pratica?):** rho = 0.023 — praticamente zero. Os dois fatores sao independentes na pratica.

**Limitacoes:** Amostra de conveniencia. Dados de autorrelato.

**Graficos:**
- `outputs\figures\exploratory\phase56\H06_equivalence_tost.png`


---

### H07 — Existe um superfator 'quem cuida'?

**Manchete:** Quem cuida de pessoas tambem cuida de causas

**Veredito:** [CONFIRMADA]

**Tecnica utilizada:** Correlacao Spearman entre os dois fatores + alpha de Cronbach (mede se os dois fatores funcionam juntos como uma dimensao unica). Alpha > 0.60 = aceitavel, > 0.70 = bom.

**Premissas verificadas:** Alpha de Cronbach com apenas 2 itens (fatores) e uma simplificacao. Uma analise fatorial confirmatoria seria mais rigorosa, mas para uma exploracao inicial e suficiente.

**Resultado:** Correlacao entre interpersonal e noble: rho = 0.460, p = 0.00e+00
Alpha de Cronbach como dimensao unica: 0.67
> 0.60 — aceitavel

**Interpretacao:** Os fatores interpersonal e noble tem correlacao forte (rho = 0.460) e funcionam bem como uma dimensao unica (alpha de Cronbach = 0.67). Faz sentido falar de um superfator 'quem cuida'.

**Relevancia (o efeito importa na pratica?):** rho = 0.460 e uma correlacao forte.

**Limitacoes:** Alpha de Cronbach com 2 itens tende a ser baixo. Uma analise fatorial de segunda ordem com todos os itens dos dois fatores seria mais precisa.

**Graficos:**
- `outputs\figures\exploratory\phase56\H07_second_order_factor.png`


---

### H08 — Prazer sexual: emocao ou sensacao?

**Manchete:** Prazer sexual: mais emocao e ego do que pura sensacao?

**Veredito:** [CONFIRMADA]

**Tecnica utilizada:** Teste de Steiger — compara duas correlacoes que compartilham os mesmos dados (o item sexual esta nas duas). Testa se a diferenca entre as correlacoes e real.

**Premissas verificadas:** Steiger assume normalidade bivariada (simplificacao). Usamos Spearman para as correlacoes base.

**Resultado:** Correlacoes do item Sexual arousal com cada fator:
  Emocionante: rho = 0.250
  Reputacional: rho = 0.212
  Sensorial: rho = 0.174
  Interpessoal: rho = 0.167
  Intelectual: rho = 0.117
  Nobre: rho = 0.066

Teste de Steiger (thrilling vs sensorial): Z = 7.62, p = 0.0000

**Interpretacao:** O item Sexual arousal correlaciona significativamente mais com thrilling (rho = 0.250) do que com sensorial (rho = 0.174). Teste de Steiger: Z = 7.62, p = 0.0000.

**Relevancia (o efeito importa na pratica?):** Diferenca de correlacao: 0.077. Pequena mas mensuravel.

**Limitacoes:** O item sexual esta avulso (nao pertence a nenhum fator). Amostra de conveniencia.

**Graficos:**
- `outputs\figures\exploratory\phase56\H08_steiger_comparison.png`


---

### H09 — Amor prediz conexao e tempo de qualidade?

**Manchete:** Amor gera conexao: quem ama tambem valoriza tempo de qualidade

**Veredito:** [CONFIRMADA]

**Tecnica utilizada:** Regressao linear com divisao treino (70%) / teste (30%). R² mede quanto da variacao o modelo explica — quanto mais perto de 1, melhor a previsao.

**Premissas verificadas:** Regressao linear assume relacao linear entre as variaveis. Divisao treino/teste garante que o resultado nao e inflado pela mesma amostra.

**Resultado:** Regressao: Deep personal connection ~ Loving / being loved + Quality time with loved ones
R² treino: 0.264
R² teste: 0.245
Coeficientes: {'Loving / being loved': '0.249', 'Quality time with loved ones': '0.310'}

**Interpretacao:** O modelo consegue prever Deep personal connection a partir de Loving / being loved, Quality time with loved ones com R² = 0.245 fora da amostra de treino. A associacao e real e funciona em dados novos.

**Relevancia (o efeito importa na pratica?):** R² = 0.245 — o modelo explica mais de 15% da variacao, o que e relevante.

**Limitacoes:** Correlacao != causalidade. Saber que amor e conexao andam juntos nao significa que um causa o outro.

**Graficos:**
- `outputs\figures\exploratory\phase56\H09_predictive_correlation.png`


---

*Relatorio gerado automaticamente por `src/analysts/relational.py`*
*Dados: Sources of Pleasure (ClearerThinking.org) — N = 6,587*
