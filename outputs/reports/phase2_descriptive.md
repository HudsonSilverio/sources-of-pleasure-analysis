# Fase 2 — Analise Descritiva

**Dataset:** `data/processed/clean.csv` — 6,587 respondentes completos

**Premissa declarada:** itens Likert de 7 pontos (-3 a +3) tratados como
intervalares, convencao aceita na literatura para escalas de 7+ pontos.
Onde distribuicoes forem muito assimetricas, preferir Spearman nas fases seguintes.

---

## Leitura principal

### Fontes de prazer mais valorizadas (top 5 por media)
| Rank | Item | Media | IC 95% | Net Agreement |
|------|------|-------|--------|---------------|
| 1 | Laughing / humor | 2.11 | [2.08, 2.13] | 77.1% |
| 2 | Deep personal connection | 2.05 | [2.02, 2.08] | 74.5% |
| 3 | Exploring ideas / thinking | 2.02 | [1.99, 2.04] | 73.1% |
| 4 | Learning | 2.00 | [1.97, 2.02] | 72.4% |
| 5 | Quality time with loved ones | 1.96 | [1.93, 1.99] | 71.8% |

### Fontes de prazer menos valorizadas (bottom 5 por media)
| Rank | Item | Media | IC 95% | Net Agreement |
|------|------|-------|--------|---------------|
| 37 | Escaping risky situations | -0.89 | [-0.93, -0.84] | -33.7% |
| 36 | Frightening but fun | -0.79 | [-0.83, -0.74] | -30.8% |
| 35 | High intensity situations | -0.52 | [-0.56, -0.47] | -21.5% |
| 34 | Spiritual / religious feelings | -0.36 | [-0.41, -0.31] | -14.8% |
| 33 | High status | -0.34 | [-0.38, -0.29] | -15.5% |

### Itens mais polarizadores (top 5 por desvio padrao)
| Item | DP | MAD | Entropia norm. | Bimodalidade |
|------|-----|-----|----------------|-------------|
| Spiritual / religious feelings | 2.04 | 2.00 | 0.98 | 0.60 **BIMODAL** |
| High-adrenaline activities | 1.92 | 2.00 | 0.99 | 0.57 **BIMODAL** |
| Partying / letting loose | 1.90 | 2.00 | 0.99 | 0.56 **BIMODAL** |
| Frightening but fun | 1.82 | 1.00 | 0.95 | 0.58 **BIMODAL** |
| Escaping risky situations | 1.81 | 1.00 | 0.94 | 0.60 **BIMODAL** |

### Efeitos de teto (itens com > 25% no +3): 14
| Item | % no +3 | Media |
|------|---------|-------|
| Deep personal connection | 43.0% | 2.05 |
| Exploring ideas / thinking | 42.3% | 2.02 |
| Laughing / humor | 42.2% | 2.11 |
| Loving / being loved | 41.5% | 1.91 |
| Learning | 40.7% | 2.00 |
| Being in nature | 38.7% | 1.89 |
| Quality time with loved ones | 38.6% | 1.96 |
| Sound / music | 31.7% | 1.68 |
| Using imagination | 29.8% | 1.58 |
| Seeing beauty | 29.4% | 1.58 |
| Creativity | 28.8% | 1.37 |
| Non-sexual touch | 27.4% | 1.46 |
| Relaxation | 27.3% | 1.38 |
| Taste (food/beverages) | 25.8% | 1.51 |

### Efeitos de piso (itens com > 25% no -3): 0
Nenhum item com efeito de piso substancial.

### Itens com assimetria substancial (|skewness| > 1): 13
| Item | Skewness | Direcao |
|------|----------|---------|
| Deep personal connection | -1.57 | maioria concorda |
| Laughing / humor | -1.56 | maioria concorda |
| Exploring ideas / thinking | -1.56 | maioria concorda |
| Quality time with loved ones | -1.52 | maioria concorda |
| Learning | -1.51 | maioria concorda |
| Being in nature | -1.47 | maioria concorda |
| Loving / being loved | -1.46 | maioria concorda |
| Helping others | -1.25 | maioria concorda |
| Sound / music | -1.21 | maioria concorda |
| Seeing beauty | -1.19 | maioria concorda |
| Taste (food/beverages) | -1.09 | maioria concorda |
| Non-sexual touch | -1.06 | maioria concorda |
| Using imagination | -1.03 | maioria concorda |

### Itens candidatos a bimodais (BC > 0.555): 18
| Item | BC | Skewness | DP |
|------|-----|----------|-----|
| Spiritual / religious feelings | 0.60 | 0.16 | 2.04 |
| Loving / being loved | 0.60 | -1.46 | 1.28 |
| Interacting with animals | 0.60 | -0.78 | 1.73 |
| Escaping risky situations | 0.60 | 0.55 | 1.81 |
| Relaxation | 0.59 | -0.95 | 1.52 |
| Non-sexual touch | 0.59 | -1.06 | 1.48 |
| Seeing beauty | 0.59 | -1.19 | 1.40 |
| Frightening but fun | 0.58 | 0.47 | 1.82 |
| Being in nature | 0.58 | -1.47 | 1.26 |
| Exploring ideas / thinking | 0.58 | -1.56 | 1.16 |
| Creativity | 0.58 | -0.88 | 1.54 |
| Sexual arousal | 0.58 | -0.89 | 1.62 |
| High-adrenaline activities | 0.57 | 0.01 | 1.92 |
| Quality time with loved ones | 0.57 | -1.52 | 1.17 |
| Deep personal connection | 0.57 | -1.57 | 1.13 |
| Learning | 0.56 | -1.51 | 1.15 |
| Partying / letting loose | 0.56 | 0.12 | 1.90 |
| Competition / winning | 0.56 | -0.28 | 1.80 |

---

## Fatores

| Fator | Media | Mediana | DP | Skewness | Kurtosis | IC 95% |
|-------|-------|---------|-----|----------|----------|--------|
| Interpessoal | 1.77 | 2.00 | 0.95 | -1.25 | 2.50 | [1.74, 1.79] |
| Emocionante | -0.39 | -0.33 | 1.19 | 0.15 | -0.53 | [-0.42, -0.37] |
| Nobre | 0.54 | 0.67 | 1.09 | -0.46 | 0.20 | [0.51, 0.57] |
| Reputacional | 0.51 | 0.50 | 1.11 | -0.23 | -0.25 | [0.48, 0.53] |
| Sensorial | 1.21 | 1.25 | 1.03 | -0.70 | 0.53 | [1.18, 1.23] |
| Intelectual | 1.71 | 1.80 | 0.87 | -0.95 | 1.46 | [1.69, 1.73] |

---

## Tabela completa — 37 itens

### Tendencia central e dispersao

| Item | Media | Mediana | Moda | Trim.Mean | DP | Var | MAD | IQR | CV | SEM | IC 95% |
|------|-------|---------|------|-----------|-----|-----|-----|-----|----|-----|--------|
| Laughing / humor | 2.11 | 2.00 | 3 | 2.22 | 1.01 | 1.02 | 1.00 | 1.00 | 48.0 | 0.012 | [2.08, 2.13] |
| Deep personal connection | 2.05 | 2.00 | 3 | 2.17 | 1.13 | 1.27 | 1.00 | 1.00 | 54.9 | 0.014 | [2.02, 2.08] |
| Exploring ideas / thinking | 2.02 | 2.00 | 3 | 2.15 | 1.16 | 1.35 | 1.00 | 2.00 | 57.6 | 0.014 | [1.99, 2.04] |
| Learning | 2.00 | 2.00 | 3 | 2.12 | 1.15 | 1.31 | 1.00 | 2.00 | 57.4 | 0.014 | [1.97, 2.02] |
| Quality time with loved ones | 1.96 | 2.00 | 3 | 2.09 | 1.17 | 1.36 | 1.00 | 2.00 | 59.5 | 0.014 | [1.93, 1.99] |
| Loving / being loved | 1.91 | 2.00 | 3 | 2.05 | 1.28 | 1.65 | 1.00 | 2.00 | 67.3 | 0.016 | [1.88, 1.94] |
| Being in nature | 1.89 | 2.00 | 3 | 2.03 | 1.26 | 1.58 | 1.00 | 2.00 | 66.6 | 0.015 | [1.86, 1.92] |
| Sound / music | 1.68 | 2.00 | 3 | 1.81 | 1.32 | 1.73 | 1.00 | 2.00 | 78.4 | 0.016 | [1.65, 1.71] |
| Using imagination | 1.58 | 2.00 | 2 | 1.70 | 1.36 | 1.86 | 1.00 | 2.00 | 86.2 | 0.017 | [1.55, 1.61] |
| Seeing beauty | 1.58 | 2.00 | 2 | 1.71 | 1.40 | 1.95 | 1.00 | 2.00 | 88.4 | 0.017 | [1.55, 1.61] |
| Helping others | 1.58 | 2.00 | 2 | 1.69 | 1.24 | 1.54 | 1.00 | 1.00 | 78.9 | 0.015 | [1.55, 1.61] |
| Taste (food/beverages) | 1.51 | 2.00 | 2 | 1.63 | 1.36 | 1.86 | 1.00 | 2.00 | 90.2 | 0.017 | [1.48, 1.55] |
| Non-sexual touch | 1.46 | 2.00 | 2 | 1.58 | 1.48 | 2.19 | 1.00 | 2.00 | 101.6 | 0.018 | [1.42, 1.49] |
| Being liked | 1.41 | 2.00 | 2 | 1.52 | 1.35 | 1.83 | 1.00 | 1.00 | 96.1 | 0.017 | [1.38, 1.44] |
| Relaxation | 1.38 | 2.00 | 2 | 1.50 | 1.52 | 2.32 | 1.00 | 2.00 | 110.1 | 0.019 | [1.35, 1.42] |
| Creativity | 1.37 | 2.00 | 3 | 1.49 | 1.54 | 2.36 | 1.00 | 2.00 | 111.8 | 0.019 | [1.34, 1.41] |
| Sexual arousal | 1.15 | 1.00 | 2 | 1.27 | 1.62 | 2.62 | 1.00 | 2.00 | 140.1 | 0.020 | [1.12, 1.19] |
| Belonging to a group | 1.15 | 1.00 | 2 | 1.25 | 1.51 | 2.27 | 1.00 | 2.00 | 130.8 | 0.019 | [1.12, 1.19] |
| Interacting with animals | 1.03 | 1.00 | 2 | 1.14 | 1.73 | 3.01 | 1.00 | 2.00 | 169.1 | 0.021 | [0.98, 1.07] |
| Social recognition | 1.00 | 1.00 | 2 | 1.09 | 1.55 | 2.41 | 1.00 | 2.00 | 154.9 | 0.019 | [0.97, 1.04] |
| Playing games | 0.92 | 1.00 | 2 | 1.00 | 1.61 | 2.59 | 1.00 | 2.00 | 175.2 | 0.020 | [0.88, 0.96] |
| Being attractive | 0.83 | 1.00 | 1 | 0.90 | 1.52 | 2.30 | 1.00 | 2.00 | 182.3 | 0.019 | [0.80, 0.87] |
| Charity / altruism | 0.65 | 1.00 | 1 | 0.71 | 1.51 | 2.27 | 1.00 | 2.00 | 231.3 | 0.019 | [0.61, 0.69] |
| Taking care of others | 0.64 | 1.00 | 1 | 0.69 | 1.56 | 2.43 | 1.00 | 2.00 | 245.4 | 0.019 | [0.60, 0.67] |
| Supporting family | 0.60 | 1.00 | 1 | 0.66 | 1.57 | 2.47 | 1.00 | 2.00 | 260.6 | 0.019 | [0.57, 0.64] |
| Smell | 0.47 | 1.00 | 1 | 0.52 | 1.63 | 2.66 | 1.00 | 3.00 | 344.1 | 0.020 | [0.43, 0.51] |
| Competition / winning | 0.23 | 1.00 | 1 | 0.26 | 1.80 | 3.22 | 1.00 | 3.00 | 772.8 | 0.022 | [0.19, 0.28] |
| Spontaneity | 0.23 | 0.00 | 1 | 0.25 | 1.78 | 3.17 | 1.00 | 3.00 | 784.6 | 0.022 | [0.18, 0.27] |
| Supporting community | 0.14 | 0.00 | 1 | 0.16 | 1.56 | 2.43 | 1.00 | 2.00 | 1115.6 | 0.019 | [0.10, 0.18] |
| Authority / power | -0.11 | 0.00 | 1 | -0.12 | 1.73 | 2.99 | 1.00 | 3.00 | 1633.2 | 0.021 | [-0.15, -0.06] |
| High-adrenaline activities | -0.15 | 0.00 | 1 | -0.17 | 1.92 | 3.70 | 2.00 | 3.00 | 1281.9 | 0.024 | [-0.20, -0.10] |
| Partying / letting loose | -0.25 | 0.00 | -2 | -0.28 | 1.90 | 3.61 | 2.00 | 3.00 | 745.0 | 0.023 | [-0.30, -0.21] |
| High status | -0.34 | 0.00 | -2 | -0.37 | 1.76 | 3.10 | 1.00 | 3.00 | 522.3 | 0.022 | [-0.38, -0.29] |
| Spiritual / religious feelings | -0.36 | 0.00 | -3 | -0.40 | 2.04 | 4.15 | 2.00 | 3.00 | 561.6 | 0.025 | [-0.41, -0.31] |
| High intensity situations | -0.52 | -1.00 | -2 | -0.57 | 1.76 | 3.11 | 1.00 | 3.00 | 342.5 | 0.022 | [-0.56, -0.47] |
| Frightening but fun | -0.79 | -1.00 | -2 | -0.87 | 1.82 | 3.30 | 1.00 | 3.00 | 230.9 | 0.022 | [-0.83, -0.74] |
| Escaping risky situations | -0.89 | -1.00 | -2 | -0.99 | 1.81 | 3.28 | 1.00 | 3.00 | 204.2 | 0.022 | [-0.93, -0.84] |

*N/A: CV indefinido quando media ≈ 0.

### Posicao (percentis)

| Item | Min | P1 | P5 | P10 | Q1 | Q2 | Q3 | P90 | P95 | P99 | Max |
|------|-----|----|----|-----|----|----|----|----|-----|-----|-----|
| Laughing / humor | -3 | -2.00 | 0.00 | 1.00 | 2.00 | 2.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3 |
| Deep personal connection | -3 | -2.00 | 0.00 | 1.00 | 2.00 | 2.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3 |
| Exploring ideas / thinking | -3 | -2.00 | 0.00 | 1.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3 |
| Learning | -3 | -2.00 | 0.00 | 1.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3 |
| Quality time with loved ones | -3 | -2.00 | 0.00 | 1.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3 |
| Loving / being loved | -3 | -3.00 | -1.00 | 0.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3 |
| Being in nature | -3 | -3.00 | -1.00 | 0.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3 |
| Sound / music | -3 | -3.00 | -1.00 | 0.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3 |
| Using imagination | -3 | -2.00 | -1.00 | 0.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3 |
| Seeing beauty | -3 | -3.00 | -2.00 | 0.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3 |
| Helping others | -3 | -3.00 | -1.00 | 0.00 | 1.00 | 2.00 | 2.00 | 3.00 | 3.00 | 3.00 | 3 |
| Taste (food/beverages) | -3 | -3.00 | -1.00 | 0.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3 |
| Non-sexual touch | -3 | -3.00 | -2.00 | -1.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3 |
| Being liked | -3 | -3.00 | -1.00 | 0.00 | 1.00 | 2.00 | 2.00 | 3.00 | 3.00 | 3.00 | 3 |
| Relaxation | -3 | -3.00 | -2.00 | -1.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3 |
| Creativity | -3 | -3.00 | -2.00 | -1.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3 |
| Sexual arousal | -3 | -3.00 | -2.00 | -1.00 | 0.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3.00 | 3 |
| Belonging to a group | -3 | -3.00 | -2.00 | -1.00 | 0.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3.00 | 3 |
| Interacting with animals | -3 | -3.00 | -2.00 | -2.00 | 0.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3.00 | 3 |
| Social recognition | -3 | -3.00 | -2.00 | -1.00 | 0.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3.00 | 3 |
| Playing games | -3 | -3.00 | -2.00 | -2.00 | 0.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3.00 | 3 |
| Being attractive | -3 | -3.00 | -2.00 | -1.00 | 0.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3.00 | 3 |
| Charity / altruism | -3 | -3.00 | -2.00 | -2.00 | 0.00 | 1.00 | 2.00 | 2.00 | 3.00 | 3.00 | 3 |
| Taking care of others | -3 | -3.00 | -2.00 | -2.00 | 0.00 | 1.00 | 2.00 | 2.00 | 3.00 | 3.00 | 3 |
| Supporting family | -3 | -3.00 | -2.00 | -2.00 | 0.00 | 1.00 | 2.00 | 2.00 | 3.00 | 3.00 | 3 |
| Smell | -3 | -3.00 | -2.00 | -2.00 | -1.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3.00 | 3 |
| Competition / winning | -3 | -3.00 | -3.00 | -2.00 | -1.00 | 1.00 | 2.00 | 2.00 | 3.00 | 3.00 | 3 |
| Spontaneity | -3 | -3.00 | -3.00 | -2.00 | -1.00 | 0.00 | 2.00 | 2.00 | 3.00 | 3.00 | 3 |
| Supporting community | -3 | -3.00 | -3.00 | -2.00 | -1.00 | 0.00 | 1.00 | 2.00 | 2.00 | 3.00 | 3 |
| Authority / power | -3 | -3.00 | -3.00 | -2.00 | -2.00 | 0.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3 |
| High-adrenaline activities | -3 | -3.00 | -3.00 | -3.00 | -2.00 | 0.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3 |
| Partying / letting loose | -3 | -3.00 | -3.00 | -3.00 | -2.00 | 0.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3 |
| High status | -3 | -3.00 | -3.00 | -3.00 | -2.00 | 0.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3 |
| Spiritual / religious feelings | -3 | -3.00 | -3.00 | -3.00 | -2.00 | 0.00 | 1.00 | 3.00 | 3.00 | 3.00 | 3 |
| High intensity situations | -3 | -3.00 | -3.00 | -3.00 | -2.00 | -1.00 | 1.00 | 2.00 | 2.00 | 3.00 | 3 |
| Frightening but fun | -3 | -3.00 | -3.00 | -3.00 | -2.00 | -1.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3 |
| Escaping risky situations | -3 | -3.00 | -3.00 | -3.00 | -2.00 | -1.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3 |

### Forma e normalidade

**Nota:** com N = 6,587, todos os testes de normalidade rejeitam H0.
O que importa e a **magnitude** do desvio, nao o p-valor.

| Item | Skewness | Kurtosis | Shapiro-W | D'Agostino | Anderson-D | Mean-Med | DP/MAD |
|------|----------|----------|-----------|------------|------------|----------|--------|
| Laughing / humor | -1.56 | 3.75 | 0.7790 | 2017.1 | 461.5 | 0.11 | 1.01 |
| Deep personal connection | -1.57 | 3.11 | 0.7795 | 1938.8 | 470.0 | 0.05 | 1.13 |
| Exploring ideas / thinking | -1.56 | 2.91 | 0.7785 | 1896.4 | 463.3 | 0.02 | 1.16 |
| Learning | -1.51 | 2.81 | 0.7883 | 1822.3 | 440.7 | -0.00 | 1.15 |
| Quality time with loved ones | -1.52 | 2.86 | 0.7953 | 1849.3 | 429.6 | -0.04 | 1.17 |
| Loving / being loved | -1.46 | 2.23 | 0.7918 | 1676.4 | 442.1 | -0.09 | 1.28 |
| Being in nature | -1.47 | 2.43 | 0.8010 | 1721.2 | 414.8 | -0.11 | 1.26 |
| Sound / music | -1.21 | 1.48 | 0.8389 | 1244.7 | 325.1 | -0.32 | 1.32 |
| Using imagination | -1.03 | 0.71 | 0.8618 | 894.4 | 299.6 | -0.42 | 1.36 |
| Seeing beauty | -1.19 | 1.14 | 0.8373 | 1163.5 | 341.1 | -0.42 | 1.40 |
| Helping others | -1.25 | 1.96 | 0.8492 | 1380.7 | 322.8 | -0.42 | 1.24 |
| Taste (food/beverages) | -1.09 | 1.01 | 0.8587 | 1017.4 | 293.4 | -0.49 | 1.36 |
| Non-sexual touch | -1.06 | 0.61 | 0.8567 | 914.5 | 307.8 | -0.54 | 1.48 |
| Being liked | -0.99 | 0.86 | 0.8769 | 876.3 | 261.7 | -0.59 | 1.35 |
| Relaxation | -0.95 | 0.21 | 0.8664 | 732.1 | 295.9 | -0.62 | 1.52 |
| Creativity | -0.88 | 0.08 | 0.8724 | 647.5 | 273.1 | -0.63 | 1.54 |
| Sexual arousal | -0.89 | 0.10 | 0.8815 | 650.4 | 251.9 | 0.15 | 1.62 |
| Belonging to a group | -0.81 | 0.09 | 0.8955 | 567.8 | 230.0 | 0.15 | 1.51 |
| Interacting with animals | -0.78 | -0.32 | 0.8824 | 564.5 | 248.7 | 0.03 | 1.73 |
| Social recognition | -0.73 | -0.12 | 0.9065 | 475.1 | 211.4 | 0.00 | 1.55 |
| Playing games | -0.67 | -0.34 | 0.9084 | 454.1 | 206.1 | -0.08 | 1.61 |
| Being attractive | -0.61 | -0.22 | 0.9213 | 372.3 | 190.7 | -0.17 | 1.52 |
| Charity / altruism | -0.52 | -0.29 | 0.9301 | 291.8 | 167.7 | -0.35 | 1.51 |
| Taking care of others | -0.51 | -0.43 | 0.9270 | 344.1 | 174.7 | -0.36 | 1.56 |
| Supporting family | -0.48 | -0.47 | 0.9326 | 332.8 | 158.7 | -0.40 | 1.57 |
| Smell | -0.36 | -0.66 | 0.9362 | 420.9 | 145.5 | -0.53 | 1.63 |
| Competition / winning | -0.28 | -1.06 | 0.9211 | 2230.3 | 196.2 | -0.77 | 1.80 |
| Spontaneity | -0.20 | -1.04 | 0.9326 | 1934.6 | 148.9 | 0.23 | 1.78 |
| Supporting community | -0.21 | -0.72 | 0.9452 | 432.7 | 136.0 | 0.14 | 1.56 |
| Authority / power | -0.02 | -1.01 | 0.9392 | 1617.9 | 133.6 | -0.11 | 1.73 |
| High-adrenaline activities | 0.01 | -1.24 | 0.9186 | 8732.3 | 170.2 | -0.15 | 0.96 |
| Partying / letting loose | 0.12 | -1.20 | 0.9224 | 5640.0 | 163.3 | -0.25 | 0.95 |
| High status | 0.12 | -1.04 | 0.9335 | 1937.1 | 143.8 | -0.34 | 1.76 |
| Spiritual / religious feelings | 0.16 | -1.29 | 0.9021 | 19246.6 | 197.5 | -0.36 | 1.02 |
| High intensity situations | 0.26 | -1.06 | 0.9226 | 2223.3 | 179.9 | 0.48 | 1.76 |
| Frightening but fun | 0.47 | -0.92 | 0.9047 | 1202.6 | 209.1 | 0.21 | 1.82 |
| Escaping risky situations | 0.55 | -0.81 | 0.8940 | 875.3 | 225.0 | 0.11 | 1.81 |

### Frequencias de resposta (%) 

| Item | -3 | -2 | -1 | 0 | +1 | +2 | +3 | Piso% | Teto% |
|------|----|----|----|----|----|----|-----|-------|-------|
| Laughing / humor | 0.5 | 0.6 | 1.1 | 3.6 | 16.1 | 36.0 | 42.2 | 0.5 | 42.2 |
| Deep personal connection | 0.6 | 1.0 | 1.9 | 5.0 | 15.5 | 33.0 | 43.0 | 0.6 | 43.0 |
| Exploring ideas / thinking | 0.7 | 1.2 | 2.4 | 4.6 | 16.2 | 32.6 | 42.3 | 0.7 | 42.3 |
| Learning | 0.6 | 1.2 | 2.3 | 4.7 | 17.0 | 33.5 | 40.7 | 0.6 | 40.7 |
| Quality time with loved ones | 0.7 | 1.3 | 2.4 | 4.9 | 16.7 | 35.3 | 38.6 | 0.7 | 38.6 |
| Loving / being loved | 1.2 | 1.8 | 2.5 | 7.1 | 16.5 | 29.5 | 41.5 | 1.2 | 41.5 |
| Being in nature | 1.1 | 1.7 | 2.8 | 5.3 | 18.7 | 31.7 | 38.7 | 1.1 | 38.7 |
| Sound / music | 1.2 | 2.4 | 3.5 | 7.5 | 22.9 | 30.9 | 31.7 | 1.2 | 31.7 |
| Using imagination | 0.9 | 3.0 | 5.0 | 9.1 | 22.0 | 30.1 | 29.8 | 0.9 | 29.8 |
| Seeing beauty | 1.2 | 4.2 | 4.5 | 5.1 | 24.6 | 30.9 | 29.4 | 1.2 | 29.4 |
| Helping others | 1.3 | 2.0 | 3.6 | 7.2 | 25.2 | 38.4 | 22.3 | 1.3 | 22.3 |
| Taste (food/beverages) | 1.3 | 3.2 | 4.6 | 8.6 | 24.0 | 32.4 | 25.8 | 1.3 | 25.8 |
| Non-sexual touch | 1.9 | 4.1 | 5.8 | 9.0 | 20.8 | 31.1 | 27.4 | 1.9 | 27.4 |
| Being liked | 1.4 | 3.2 | 4.8 | 10.4 | 26.2 | 32.2 | 21.8 | 1.4 | 21.8 |
| Relaxation | 1.6 | 5.1 | 7.5 | 7.6 | 22.6 | 28.3 | 27.3 | 1.6 | 27.3 |
| Creativity | 1.7 | 5.0 | 6.8 | 10.3 | 22.0 | 25.4 | 28.8 | 1.7 | 28.8 |
| Sexual arousal | 3.8 | 5.7 | 6.0 | 11.8 | 23.2 | 27.3 | 22.2 | 3.8 | 22.2 |
| Belonging to a group | 2.2 | 5.5 | 6.9 | 12.6 | 24.9 | 28.8 | 19.1 | 2.2 | 19.1 |
| Interacting with animals | 4.9 | 7.5 | 7.0 | 11.1 | 21.9 | 25.0 | 22.5 | 4.9 | 22.5 |
| Social recognition | 2.8 | 6.4 | 8.2 | 13.0 | 26.3 | 26.6 | 16.7 | 2.8 | 16.7 |
| Playing games | 3.3 | 7.5 | 8.8 | 13.6 | 24.2 | 26.6 | 16.0 | 3.3 | 16.0 |
| Being attractive | 2.7 | 7.2 | 9.0 | 15.3 | 29.1 | 24.3 | 12.4 | 2.7 | 12.4 |
| Charity / altruism | 3.4 | 7.3 | 10.2 | 19.4 | 28.8 | 21.7 | 9.3 | 3.4 | 9.3 |
| Taking care of others | 3.7 | 8.0 | 11.6 | 16.0 | 28.6 | 22.1 | 9.8 | 3.7 | 9.8 |
| Supporting family | 4.1 | 8.0 | 11.4 | 18.6 | 25.9 | 22.2 | 9.9 | 4.1 | 9.9 |
| Smell | 4.7 | 10.6 | 11.2 | 18.8 | 26.1 | 18.3 | 10.4 | 4.7 | 10.4 |
| Competition / winning | 7.9 | 16.0 | 11.3 | 10.7 | 27.0 | 17.8 | 9.2 | 7.9 | 9.2 |
| Spontaneity | 7.5 | 14.1 | 14.4 | 14.1 | 21.7 | 18.4 | 9.8 | 7.5 | 9.8 |
| Supporting community | 5.3 | 12.8 | 14.4 | 23.0 | 23.8 | 15.7 | 4.9 | 5.3 | 4.9 |
| Authority / power | 9.3 | 17.2 | 15.2 | 17.4 | 21.1 | 13.4 | 6.4 | 9.3 | 6.4 |
| High-adrenaline activities | 14.5 | 17.2 | 13.3 | 11.3 | 20.2 | 14.2 | 9.2 | 14.5 | 9.2 |
| Partying / letting loose | 14.3 | 18.7 | 15.4 | 11.6 | 18.2 | 13.1 | 8.6 | 14.3 | 8.6 |
| High status | 12.5 | 19.7 | 15.3 | 16.3 | 19.5 | 11.0 | 5.7 | 12.5 | 5.7 |
| Spiritual / religious feelings | 21.2 | 16.8 | 10.3 | 14.2 | 14.3 | 12.6 | 10.6 | 21.2 | 10.6 |
| High intensity situations | 14.1 | 22.5 | 18.2 | 11.0 | 19.1 | 10.5 | 4.6 | 14.1 | 4.6 |
| Frightening but fun | 20.9 | 23.4 | 16.0 | 11.7 | 14.6 | 8.4 | 5.1 | 20.9 | 5.1 |
| Escaping risky situations | 23.0 | 23.5 | 16.1 | 11.7 | 12.8 | 7.8 | 5.1 | 23.0 | 5.1 |

### Indicadores Likert

| Item | Top-2% | Bottom-2% | Net Agr. | Entropia | Ent.Norm | BC | Outliers IQR | Outliers Z | Outliers ModZ |
|------|--------|-----------|----------|----------|----------|----|-------------|------------|---------------|
| Laughing / humor | 78.1 | 1.0 | 77.1 | 1.80 | 0.64 | 0.51 | 381 | 142 | 0 |
| Deep personal connection | 76.1 | 1.6 | 74.5 | 1.90 | 0.68 | 0.57 * | 558 | 105 | 0 |
| Exploring ideas / thinking | 74.9 | 1.9 | 73.1 | 1.94 | 0.69 | 0.58 * | 45 | 123 | 0 |
| Learning | 74.2 | 1.8 | 72.4 | 1.94 | 0.69 | 0.56 * | 40 | 119 | 0 |
| Quality time with loved ones | 73.9 | 2.0 | 71.8 | 1.97 | 0.70 | 0.57 * | 48 | 135 | 0 |
| Loving / being loved | 71.0 | 2.9 | 68.1 | 2.05 | 0.73 | 0.60 * | 76 | 192 | 0 |
| Being in nature | 70.4 | 2.8 | 67.6 | 2.05 | 0.73 | 0.58 * | 72 | 185 | 0 |
| Sound / music | 62.6 | 3.6 | 59.0 | 2.19 | 0.78 | 0.55 | 78 | 78 | 0 |
| Using imagination | 60.0 | 3.9 | 56.1 | 2.27 | 0.81 | 0.55 | 57 | 57 | 0 |
| Seeing beauty | 60.3 | 5.4 | 54.9 | 2.23 | 0.80 | 0.59 * | 79 | 79 | 0 |
| Helping others | 60.8 | 3.3 | 57.5 | 2.15 | 0.77 | 0.52 | 452 | 84 | 0 |
| Taste (food/beverages) | 58.2 | 4.5 | 53.7 | 2.28 | 0.81 | 0.55 | 85 | 85 | 0 |
| Non-sexual touch | 58.4 | 6.0 | 52.5 | 2.35 | 0.84 | 0.59 * | 122 | 122 | 0 |
| Being liked | 54.0 | 4.6 | 49.5 | 2.31 | 0.82 | 0.52 | 616 | 89 | 0 |
| Relaxation | 55.5 | 6.7 | 48.8 | 2.39 | 0.85 | 0.59 * | 107 | 0 | 0 |
| Creativity | 54.2 | 6.7 | 47.5 | 2.42 | 0.86 | 0.58 * | 109 | 0 | 0 |
| Sexual arousal | 49.5 | 9.5 | 40.0 | 2.50 | 0.89 | 0.58 * | 0 | 0 | 0 |
| Belonging to a group | 47.9 | 7.7 | 40.2 | 2.47 | 0.88 | 0.54 | 0 | 0 | 0 |
| Interacting with animals | 47.5 | 12.4 | 35.1 | 2.58 | 0.92 | 0.60 * | 0 | 0 | 0 |
| Social recognition | 43.3 | 9.2 | 34.1 | 2.52 | 0.90 | 0.53 | 0 | 0 | 0 |
| Playing games | 42.6 | 10.8 | 31.8 | 2.57 | 0.91 | 0.54 | 0 | 0 | 0 |
| Being attractive | 36.6 | 9.9 | 26.7 | 2.53 | 0.90 | 0.50 | 0 | 0 | 0 |
| Charity / altruism | 31.0 | 10.7 | 20.3 | 2.55 | 0.91 | 0.47 | 0 | 0 | 0 |
| Taking care of others | 32.0 | 11.8 | 20.2 | 2.58 | 0.92 | 0.49 | 0 | 0 | 0 |
| Supporting family | 32.1 | 12.1 | 20.0 | 2.60 | 0.93 | 0.49 | 0 | 0 | 0 |
| Smell | 28.7 | 15.3 | 13.4 | 2.65 | 0.94 | 0.48 | 0 | 0 | 0 |
| Competition / winning | 27.0 | 23.9 | 3.1 | 2.68 | 0.96 | 0.56 * | 0 | 0 | 0 |
| Spontaneity | 28.2 | 21.6 | 6.6 | 2.74 | 0.97 | 0.53 | 0 | 0 | 0 |
| Supporting community | 20.6 | 18.2 | 2.5 | 2.62 | 0.93 | 0.46 | 0 | 0 | 0 |
| Authority / power | 19.8 | 26.5 | -6.8 | 2.72 | 0.97 | 0.50 | 0 | 0 | 0 |
| High-adrenaline activities | 23.4 | 31.7 | -8.3 | 2.77 | 0.99 | 0.57 * | 0 | 0 | 0 |
| Partying / letting loose | 21.7 | 33.0 | -11.3 | 2.77 | 0.99 | 0.56 * | 0 | 0 | 0 |
| High status | 16.7 | 32.2 | -15.5 | 2.72 | 0.97 | 0.52 | 0 | 0 | 0 |
| Spiritual / religious feelings | 23.2 | 38.0 | -14.8 | 2.77 | 0.98 | 0.60 * | 0 | 0 | 0 |
| High intensity situations | 15.1 | 36.6 | -21.5 | 2.68 | 0.96 | 0.55 | 0 | 0 | 0 |
| Frightening but fun | 13.5 | 44.3 | -30.8 | 2.67 | 0.95 | 0.58 * | 0 | 0 | 0 |
| Escaping risky situations | 12.8 | 46.5 | -33.7 | 2.65 | 0.94 | 0.60 * | 0 | 0 | 0 |

\* BC > 0.555 = candidato a bimodal

---

## Tabela completa — 6 fatores

| Fator | Media | Mediana | Moda | Trim.Mean | DP | Var | MAD | IQR | Skew | Kurt | SEM | IC 95% | Outliers IQR |
|-------|-------|---------|------|-----------|-----|-----|-----|-----|------|------|-----|--------|-------------|
| Interpessoal | 1.77 | 2.00 | 2.00 | 1.84 | 0.95 | 0.90 | 0.50 | 1.25 | -1.25 | 2.50 | 0.012 | [1.74, 1.79] | 141 |
| Emocionante | -0.39 | -0.33 | -0.33 | -0.41 | 1.19 | 1.43 | 0.83 | 1.83 | 0.15 | -0.53 | 0.015 | [-0.42, -0.37] | 0 |
| Nobre | 0.54 | 0.67 | 0.67 | 0.57 | 1.09 | 1.18 | 0.67 | 1.50 | -0.46 | 0.20 | 0.013 | [0.51, 0.57] | 67 |
| Reputacional | 0.51 | 0.50 | 0.83 | 0.52 | 1.11 | 1.23 | 0.83 | 1.50 | -0.23 | -0.25 | 0.014 | [0.48, 0.53] | 33 |
| Sensorial | 1.21 | 1.25 | 1.50 | 1.25 | 1.03 | 1.07 | 0.75 | 1.50 | -0.70 | 0.53 | 0.013 | [1.18, 1.23] | 49 |
| Intelectual | 1.71 | 1.80 | 2.00 | 1.76 | 0.87 | 0.75 | 0.60 | 1.20 | -0.95 | 1.46 | 0.011 | [1.69, 1.73] | 108 |

---

## Graficos exploratórios

Todos em `outputs/figures/exploratory/`:

- `01_items_ranked_by_mean.png` — Quais fontes de prazer sao mais valorizadas?
- `02_factors_ranked_by_mean.png` — Qual categoria de prazer domina?
- `03_frequency_heatmap.png` — Como as pessoas distribuiram suas respostas?
- `04_factor_histograms.png` — Os fatores tem distribuicao normal ou enviesada?
- `05_items_ranked_by_sd.png` — Quais fontes de prazer geram mais discordancia?
- `06_net_agreement.png` — Qual o saldo liquido de concordancia de cada item?
- `07_ceiling_floor_effects.png` — Onde a escala nao captura diferencas?
- `08_skewness.png` — Quais itens tem distribuicao assimetrica e para que lado?
- `09_entropy.png` — Onde ha consenso vs. dispersao total?
- `10_bimodality.png` — Quais itens dividem as pessoas em dois grupos?

---

*Gerado a partir de `data/processed/clean.csv` — N = 6,587*
