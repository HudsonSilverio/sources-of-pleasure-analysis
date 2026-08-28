# Relatorio do Analista Preditivo

**Data:** 2026-08-28 09:51
**Hipoteses analisadas:** 2
**Respondentes:** N = 6,587
**Seed aleatoria:** 42

## Resumo de vereditos

| Hipotese | Titulo | Veredito |
|----------|--------|----------|
| H16 | Adrenalina e serenidade sao caminhos opostos? | inconclusiva |
| H17 | Qual fator mais contribui pro prazer geral? | confirmada |

## Analises detalhadas

---

### H16 — Adrenalina e serenidade sao caminhos opostos?

**Manchete:** Adrenalina vs. serenidade: dois caminhos opostos para o prazer

**Veredito:** [INCONCLUSIVA]

**Tecnica utilizada:** Regressao linear com divisao treino (70%) / teste (30%). Verifica se itens de adrenalina preveem relaxamento (e vice-versa). R² mede quanto da variacao o modelo explica.

**Premissas verificadas:** Regressao linear assume relacao linear. Divisao treino/teste evita resultado inflado.

**Resultado:** Modelo: Relaxation ~ High-adrenaline activities + Frightening but fun + Escaping risky situations
R² treino: 0.0058
R² teste: 0.0062
MAE teste: 1.24

Coeficientes:
  High-adrenaline activities: -0.0079
  Frightening but fun: 0.0682
  Escaping risky situations: -0.0057
  Intercepto: 1.4472

Modelo reverso (relaxamento → adrenalina):
  High-adrenaline activities: R² = -0.0012
  Frightening but fun: R² = 0.0062
  Escaping risky situations: R² = -0.0017


**Interpretacao:** Alguns itens de adrenalina tem efeito negativo, mas o poder de previsao e muito fraco (R² = 0.006).

**Relevancia (o efeito importa na pratica?):** R² = 0.006 — previsao muito fraca. Os dois caminhos existem mas sao quase independentes.

**Limitacoes:** R² baixo nao significa que nao existe relacao — significa que outros fatores tambem influenciam. Correlacao nao e causalidade.

**Graficos:**
- `outputs\figures\exploratory\phase56\H16_regression.png`


---

### H17 — Qual fator mais contribui pro prazer geral?

**Manchete:** O maior motor do prazer geral pode te surpreender

**Veredito:** [CONFIRMADA]

**Tecnica utilizada:** Regressao multipla com coeficientes padronizados (betas). Padronizar permite comparar o peso de cada fator na mesma escala — o maior beta e o fator que mais contribui.

**Premissas verificadas:** Variaveis padronizadas (media 0, desvio 1). IMPORTANTE: os fatores sao medias de subconjuntos dos 37 itens, e o prazer geral e a media de todos os 37. Entao existe circularidade parcial — o R² alto nao e uma descoberta independente, mas os pesos relativos sao informativos.

**Resultado:** Modelo: prazer medio geral ~ 6 fatores
R² = 0.9738

Betas padronizados (maiores = mais peso):
  Emocionante: 0.3540
  Nobre: 0.3005
  Reputacional: 0.2873
  Sensorial: 0.2424
  Intelectual: 0.2237
  Interpessoal: 0.1918


**Interpretacao:** O fator que mais contribui para o prazer geral e 'Emocionante' (beta = 0.354). R² total = 0.974 — os 6 fatores explicam 97.4% da variacao no prazer geral. NOTA: como os fatores fazem parte dos 37 itens, essa analise mostra pesos relativos, nao uma descoberta independente.

**Relevancia (o efeito importa na pratica?):** O fator 'Emocionante' tem o maior peso. Isso indica que, entre os 6 tipos de prazer, este e o que mais 'puxa' a media geral pra cima ou pra baixo.

**Limitacoes:** Circularidade parcial: fatores sao parte da media geral. R² alto e esperado por construcao. O valor real esta nos pesos relativos, nao no R² absoluto.

**Graficos:**
- `outputs\figures\exploratory\phase56\H17_multiple_regression.png`


---

*Relatorio gerado automaticamente por `src/analysts/predictive.py`*
*Dados: Sources of Pleasure (ClearerThinking.org) — N = 6,587*
