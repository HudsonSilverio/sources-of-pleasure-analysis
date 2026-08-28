# Relatorio do Analista Estrutural

**Data:** 2026-08-28 09:49
**Hipoteses analisadas:** 1
**Respondentes:** N = 6,587
**Seed aleatoria:** 42

## Resumo de vereditos

| Hipotese | Titulo | Veredito |
|----------|--------|----------|
| H10 | Os 6 itens avulsos se conectam entre si? | inconclusiva |

## Analises detalhadas

---

### H10 — Os 6 itens avulsos se conectam entre si?

**Manchete:** Humor e musica, natureza e animais: pares naturais entre os itens avulsos

**Veredito:** [INCONCLUSIVA]

**Tecnica utilizada:** Matriz de correlacao Spearman entre os 6 itens avulsos (que nao pertencem a nenhum fator). Visualizacao em heatmap e rede de conexoes. Limite para 'conexao moderada': rho > 0.3. Limite para considerar novo grupo: rho > 0.5.

**Premissas verificadas:** Spearman nao exige normalidade. Esta analise NAO tenta corrigir os 6 fatores — apenas explora se os itens avulsos tem conexoes entre si.

**Resultado:** Matriz de correlacao dos 6 itens avulsos:

  Laughing / humor × Being in nature: rho = 0.176
  Laughing / humor × Sound / music: rho = 0.356 ** (moderada)
  Laughing / humor × Interacting with animals: rho = 0.177
  Laughing / humor × Playing games: rho = 0.165
  Laughing / humor × Sexual arousal: rho = 0.154
  Being in nature × Sound / music: rho = 0.188
  Being in nature × Interacting with animals: rho = 0.245
  Being in nature × Playing games: rho = -0.009
  Being in nature × Sexual arousal: rho = 0.062
  Sound / music × Interacting with animals: rho = 0.159
  Sound / music × Playing games: rho = 0.104
  Sound / music × Sexual arousal: rho = 0.123
  Interacting with animals × Playing games: rho = 0.080
  Interacting with animals × Sexual arousal: rho = -0.005
  Playing games × Sexual arousal: rho = 0.131

Pares com rho > 0.3: 1
Pares com rho > 0.5: 0

**Interpretacao:** Encontramos 1 par(es) com correlacao moderada (rho > 0.3), mas nenhum forte o bastante (rho > 0.5) para criar um novo grupo. Existem conexoes, mas nao um grupo coeso.

**Relevancia (o efeito importa na pratica?):** Correlacao mais forte entre avulsos: 0.356. Sao conexoes reais mas nao formam um fator coeso.

**Limitacoes:** Com apenas 6 itens, uma analise fatorial nao seria confiavel. A analise se limita a correlacoes entre pares.

**Graficos:**
- `outputs\figures\exploratory\phase56\H10_standalone_correlations.png`


---

*Relatorio gerado automaticamente por `src/analysts/structural.py`*
*Dados: Sources of Pleasure (ClearerThinking.org) — N = 6,587*
