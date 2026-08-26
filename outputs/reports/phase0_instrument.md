# Fase 0 — Entendimento do Instrumento

## O que a ferramenta mede

**"Your Greatest Sources of Pleasure"** é um assessment online criado pela
ClearerThinking.org (plataforma GuidedTrack), concebido por Spencer Greenberg
e desenvolvido por Belén Cobeta, com base em dois estudos realizados com 600
pessoas nos EUA.

O instrumento mede **quanto prazer uma pessoa obtém de 37 fontes diferentes**
— desde beleza e competição até espiritualidade e humor. Cada fonte é avaliada
numa escala Likert de 7 pontos:

| Valor | Rótulo                       |
|-------|------------------------------|
| +3    | Totally agree                |
| +2    | Agree                        |
| +1    | Somewhat agree               |
|  0    | Neither agree nor disagree   |
| -1    | Somewhat disagree            |
| -2    | Disagree                     |
| -3    | Totally disagree             |

Todas as perguntas seguem o mesmo enunciado-tronco: *"One of the things I find
most pleasurable in life is..."*, completado pela fonte de prazer específica.

---

## Estrutura: fatores e itens avulsos

O instrumento agrupa **31 dos 37 itens** em **6 fatores**, calculados como
média simples dos itens componentes. Os **6 itens restantes** não pertencem a
nenhum fator e são reportados individualmente.

### Fator 1 — Interpersonal (4 itens)
| Variável        | Rótulo curto                  |
|-----------------|-------------------------------|
| p_qualityTime   | Quality time with loved ones  |
| p_belonging     | Belonging to a group          |
| p_loving        | Loving / being loved          |
| p_connection    | Deep personal connection      |

### Fator 2 — Thrilling (6 itens)
| Variável        | Rótulo curto                         |
|-----------------|--------------------------------------|
| p_risk          | Escaping risky situations            |
| p_partying      | Partying / letting loose             |
| p_adrenaline    | High-adrenaline activities           |
| p_scary         | Frightening but fun                  |
| p_spontaneous   | Spontaneity                          |
| p_exciting      | High intensity situations            |

### Fator 3 — Noble (6 itens)
| Variável         | Rótulo curto              |
|------------------|---------------------------|
| p_spiritual      | Spiritual / religious     |
| p_supportFamily  | Supporting family         |
| p_charity        | Charity / altruism        |
| p_community      | Supporting community      |
| p_caring         | Taking care of others     |
| p_helping        | Helping others            |

### Fator 4 — Reputational (6 itens)
| Variável        | Rótulo curto              |
|-----------------|---------------------------|
| p_recognition   | Social recognition        |
| p_status        | High status               |
| p_attractive    | Being attractive          |
| p_power         | Authority / power         |
| p_likable       | Being liked               |
| p_competition   | Competition / winning     |

### Fator 5 — Sensorial (4 itens)
| Variável   | Rótulo curto              |
|------------|---------------------------|
| p_touch    | Non-sexual touch          |
| p_taste    | Taste (food/beverages)    |
| p_smell    | Smell                     |
| p_relax    | Relaxation                |

### Fator 6 — Intellectual (5 itens)
| Variável        | Rótulo curto              |
|-----------------|---------------------------|
| p_thinking      | Exploring ideas / thinking|
| p_creative      | Creativity                |
| p_learning      | Learning                  |
| p_imagination   | Using imagination         |
| p_seeingBeauty  | Seeing beauty             |

### Itens sem fator (6 itens)
| Variável   | Rótulo curto              |
|------------|---------------------------|
| p_humor    | Laughing / humor          |
| p_nature   | Being in nature           |
| p_sound    | Sound / music             |
| p_animals  | Interacting with animals  |
| p_game     | Playing games             |
| p_sex      | Sexual arousal            |

Esses 6 itens são convertidos individualmente para escala 0-10 no relatório do
assessment, mas nunca são combinados em nenhum fator. A fórmula de conversão
(igual para fatores e itens avulsos) é: `(score + 3) * (10/6)`.

---

## Fluxo do assessment

1. **37 perguntas Likert** — apresentadas uma por vez, cada uma com uma imagem
   ilustrativa. Ordem fixa (não randomizada).
2. **Ranking automático** — o sistema ordena os 37 itens por score e seleciona
   os 5 mais altos. Se houver empate na fronteira (posições 5 e 6 com mesmo
   score), o respondente é solicitado a desempatar manualmente.
3. **Exercícios de reflexão** — para cada um dos top 5, o respondente pode
   fazer um exercício com 3 perguntas abertas (texto livre):
   - Como aumentar a frequência dessa experiência?
   - Como extrair mais prazer dela?
   - Como usar esse prazer para melhorar sua vida?
   O respondente pode fazer de 1 a 5 rodadas (pode parar após cada uma).
4. **Coleta de email** — integração com MailChimp para envio do relatório
   personalizado.
5. **Relatório** — gerado como uma página web com os scores dos 6 fatores,
   os 6 itens avulsos e os textos dos exercícios de reflexão.

---

## Quem são os respondentes

Os dados vêm de **visitantes autosselecionados do site ClearerThinking.org**
que decidiram fazer o assessment voluntariamente.

### Viés de seleção (importante)
Esta é uma **amostra de conveniência online**, não uma amostra representativa
de nenhuma população. Os respondentes provavelmente:
- Têm interesse em auto-conhecimento e desenvolvimento pessoal
- São falantes de inglês com acesso à internet
- Tendem a ser mais analíticos/intelectualmente curiosos que a média (perfil
  típico do público do ClearerThinking)
- Podem ter sido direcionados por redes sociais, newsletters ou podcasts
  específicos

**Consequência:** os resultados descrevem *esta amostra*, não "as pessoas em
geral". Toda generalização deve ser feita com extrema cautela e sempre com
esta ressalva declarada.

### Sem dados demográficos
O instrumento **não coleta** idade, sexo, país, etnia, renda ou qualquer outra
variável demográfica. Comparações entre grupos só poderão ser feitas com
**grupos derivados** (ex.: clusters, coortes de completude, períodos temporais).

---

## Ambiguidades e decisões

Nenhuma ambiguidade foi encontrada na extração do código-fonte. O mapeamento
item → fator é explícito e inequívoco (linhas 384-389 de `code_gt_prazer.txt`).

### Decisão registrada
Os 6 itens sem fator (humor, nature, sound, animals, game, sex) **serão
incluídos em todas as análises de nível de item** (descritivas, correlações,
EDA, etc.), mas obviamente não participam dos scores de fator. Eles são fontes
de prazer legítimas que simplesmente não se encaixaram na estrutura fatorial
dos autores.

---

## Fonte da extração
- Arquivo: `code_gt_prazer.txt` (código-fonte GuidedTrack do assessment)
- Configuração estruturada: `config/instrument.yaml`
- Data da extração: 2026-08-26
