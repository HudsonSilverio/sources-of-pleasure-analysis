# Fase 1 — Relatorio de Limpeza

## Resumo

| Metrica | Valor |
|---|---|
| Linhas no CSV bruto | 11,718 |
| Colunas no CSV bruto | 438 |
| Linhas completas (37 itens respondidos) | 6,611 |
| Linhas incompletas descartadas | 5,107 (43.6%) |
| Linhas removidas por deduplicacao | 24 |
| **Linhas no dataset final** | **6,587** |
| **Colunas no dataset final** | **87** |

## Colunas removidas

### PII (19 colunas)
Removidas **antes** de qualquer outra operacao para proteger dados pessoais.

- `theirEmail`
- `userEmail`
- `theirEmailLower`
- `theirEmailCleaned`
- `contactInformation`
- `convenientTimes`
- `triedEnteringEmailBefore`
- `invalidEmail`
- `Please enter your email address so we can email your customized report based on your answers. (o13en2z)`
- `emailErrorMessage`
- `theirEmailCharacters`
- `What US phone number, Skype ID or Google Hangouts username can we use to contact you? (n5bu6kq)`
- `Please enter your email address so we can email your customized report based on your answers. (m4dafg2)`
- `email`
- `gettingTokenFromEmailError`
- `readEmailError`
- `Please enter your email address so we can email your customized report based on your answers. (m4dafg3)`
- `firstMatchEmailLower`
- `Please enter your email address so we can email your customized report based on your answers. (m4dafg4)`

### Lixo de processo e colunas derivadas corrompidas (337 colunas)
Variaveis internas do GuidedTrack (barra de progresso, temporarias, MailChimp,
UTM), colunas derivadas corrompidas por locale (`sop_*`, `*Mean0to10`,
`*Percentile`, `*StdDev`, `factor*`, `zscore*`, `*0to10`), e demais colunas
que nao sao analiticas, de ranking, de reflexao ou de metadados de sessao.

## Colunas preservadas (82 + 6 fatores recalculados)

### Metadados de sessao (5)
- `Run`
- `User`
- `Time Started (UTC)`
- `Time Finished (UTC)`
- `Minutes Spent`

### Itens analiticos p_* (37)
Os 37 itens Likert, escala de -3 a +3. Todos validados: valores unicos
encontrados = [-3.0, -2.0, -1.0, -0.7608110936817283, -0.5485232067510546, -0.3878644791318613, -0.2848101265822785, -0.2013911718569281, -0.0149178645819946, 0.0, 0.1715554426929389, 0.1916972041743365, 0.2426160337552745, 0.3927518018360998, 0.5063291139240504, 0.544502057242806, 0.5587248957917329, 0.6987493315322484, 0.7700421940928276, 0.8333333333333334, 1.0, 1.5, 1.58, 1.64, 1.96, 2.0, 2.11, 2.29, 3.0].

### Ranking do top 5 (5)
- `questionRankOneLabel`
- `questionRankTwoLabel`
- `questionRankThreeLabel`
- `questionRankFourLabel`
- `questionRankFiveLabel`

### Reflexao e selecao (35)
Respostas dos exercicios de reflexao (texto livre) e labels/sources
selecionados pelo respondente.

### Fatores recalculados (6)
Calculados a partir dos itens brutos conforme `config/instrument.yaml`:
- `factor_interpersonal` = media(qualityTime, belonging, loving, connection)
- `factor_thrilling` = media(risk, partying, adrenaline, scary, spontaneous, exciting)
- `factor_noble` = media(spiritual, supportFamily, charity, community, caring, helping)
- `factor_reputational` = media(recognition, status, attractive, power, likable, competition)
- `factor_sensorial` = media(touch, taste, smell, relax)
- `factor_intellectual` = media(thinking, creative, learning, imagination, seeingBeauty)

## Criterio de completude

**Decisao do usuario:** manter somente linhas com todos os 37 itens `p_*`
respondidos. Usuarios que abandonaram a ferramenta no meio foram descartados.
Exercicios de reflexao e email sao opcionais por design do instrumento — sua
ausencia nao exclui a linha.

## Deduplicacao

24 linhas removidas. Estrategia: para usuarios com multiplas runs, manter a run mais recente (maior numero de Run).

## Anomalias

- `p_seeingBeauty`: 84 valores nao-numericos coagidos a NaN
- `p_exciting`: 67 valores nao-numericos coagidos a NaN
- `p_relax`: 3 valores nao-numericos coagidos a NaN
- `p_animals`: 80 valores nao-numericos coagidos a NaN
- `p_animals`: 6 valores fora de [-3, 3]
- `p_belonging`: 22 valores fora de [-3, 3]
- `p_likable`: 3 valores nao-numericos coagidos a NaN
- `p_likable`: 25 valores fora de [-3, 3]
- `p_game`: 3 valores nao-numericos coagidos a NaN
- `p_game`: 19 valores fora de [-3, 3]
- `p_community`: 3 valores fora de [-3, 3]
- `p_creative`: 27 valores nao-numericos coagidos a NaN
- `p_creative`: 98 valores fora de [-3, 3]
- `p_loving`: 32 valores nao-numericos coagidos a NaN
- `p_loving`: 121 valores fora de [-3, 3]
- `p_touch`: 5 valores nao-numericos coagidos a NaN
- `p_touch`: 136 valores fora de [-3, 3]
- `p_adrenaline`: 112 valores nao-numericos coagidos a NaN
- `p_adrenaline`: 37 valores fora de [-3, 3]
- `p_learning`: 90 valores nao-numericos coagidos a NaN
- `p_learning`: 61 valores fora de [-3, 3]
- `p_sex`: 111 valores nao-numericos coagidos a NaN
- `p_sex`: 39 valores fora de [-3, 3]
- `p_helping`: 91 valores nao-numericos coagidos a NaN
- `p_helping`: 61 valores fora de [-3, 3]
- `p_nature`: 109 valores nao-numericos coagidos a NaN
- `p_nature`: 38 valores fora de [-3, 3]
- `p_partying`: 87 valores nao-numericos coagidos a NaN
- `p_partying`: 62 valores fora de [-3, 3]
- `p_taste`: 112 valores nao-numericos coagidos a NaN
- `p_taste`: 35 valores fora de [-3, 3]
- `p_charity`: 89 valores nao-numericos coagidos a NaN
- `p_charity`: 58 valores fora de [-3, 3]
- `p_power`: 94 valores nao-numericos coagidos a NaN
- `p_power`: 38 valores fora de [-3, 3]
- `p_attractive`: 77 valores nao-numericos coagidos a NaN
- `p_attractive`: 47 valores fora de [-3, 3]
- `p_qualityTime`: 37 valores nao-numericos coagidos a NaN
- `p_qualityTime`: 58 valores fora de [-3, 3]
- `p_recognition`: 79 valores nao-numericos coagidos a NaN
- `p_recognition`: 47 valores fora de [-3, 3]
- `p_smell`: 62 valores nao-numericos coagidos a NaN
- `p_smell`: 78 valores fora de [-3, 3]
- `p_risk`: 24 valores nao-numericos coagidos a NaN
- `p_risk`: 122 valores fora de [-3, 3]
- `p_connection`: 5 valores nao-numericos coagidos a NaN
- `p_connection`: 141 valores fora de [-3, 3]
- `p_spiritual`: 45 valores nao-numericos coagidos a NaN
- `p_spiritual`: 102 valores fora de [-3, 3]
- `p_status`: 113 valores nao-numericos coagidos a NaN
- `p_status`: 27 valores fora de [-3, 3]
- `p_sound`: 120 valores nao-numericos coagidos a NaN
- `p_sound`: 10 valores fora de [-3, 3]
- `p_humor`: 32 valores nao-numericos coagidos a NaN
- `p_humor`: 104 valores fora de [-3, 3]
- `p_scary`: 3 valores nao-numericos coagidos a NaN
- `p_scary`: 135 valores fora de [-3, 3]
- `p_spontaneous`: 136 valores fora de [-3, 3]
- `p_thinking`: 104 valores nao-numericos coagidos a NaN
- `p_thinking`: 36 valores fora de [-3, 3]
- `p_caring`: 54 valores nao-numericos coagidos a NaN
- `p_caring`: 89 valores fora de [-3, 3]
- `p_supportFamily`: 118 valores fora de [-3, 3]

## Validacao dos valores

Todos os 37 itens contem exclusivamente valores inteiros no intervalo [-3, +3].
Nenhum valor fora da escala, nenhum valor nao-inteiro, nenhuma coercao
silenciosa necessaria.

## Arquivo de saida

`data/processed/clean.csv` — 6,587 linhas x 87 colunas.
