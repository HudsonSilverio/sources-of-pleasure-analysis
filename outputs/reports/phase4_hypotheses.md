# Fase 4 — Hipoteses (Revisadas)

**Total:** 19 hipoteses (refinadas a partir de 41 originais)

**Todas viaveis** com os dados disponiveis. Nenhuma exige dados externos ou demograficos.

**Fontes:** 14 observacoes da Fase 3 + artefatos numericos das Fases 2-3 +
objetivo editorial (blog) + experiencia em ciencia de dados + **revisao de
literatura academica** (Consensus.app: psicologia hedonica, estrutura fatorial
de bem-estar, busca de sensacoes, espiritualidade e diferencas individuais,
humor e bem-estar).

---

## Resumo por tema

| Tema | Descricao | Hipoteses | Qtd |
|------|-----------|-----------|-----|
| O que mais (e menos) nos da prazer | Rankings, universalidade, polarizacao | H01-H04 | 4 |
| Como os prazeres se relacionam | Associacoes, independencia, incompatibilidades | H05-H09 | 5 |
| O instrumento mede prazer corretamente? | Estrutura fatorial, dimensoes ocultas | H10-H11 | 2 |
| Existem "tipos" de buscadores de prazer? | Perfis, clusters, subgrupos | H12-H16 | 5 |
| O que prediz o que? | Cadeias preditivas, caminhos opostos | H17-H19 | 3 |
| **Total** | | | **19** |

## Resumo por analista

| Analista | Hipoteses | Qtd |
|----------|-----------|-----|
| distribucional | H01, H02, H03, H04 | 4 |
| relacional | H05, H06, H07, H08, H09 | 5 |
| estrutural | H10, H11 | 2 |
| segmentacao | H12, H13, H14, H15, H16 | 5 |
| preditivo + comparativo | H17, H18, H19 | 3 |

---

## Tema 1 — O que mais (e menos) nos da prazer

### H01 — Rir e a fonte de prazer mais universal?

Humor teve o maior net agreement entre todos os 37 itens (77,1%), com 42%
dos respondentes no maximo da escala (+3). A diferenca para o segundo
colocado (thinking, 73%) e estatisticamente significativa, ou os itens do
topo estao empatados?

- **Manchete:** "Rir: o unico prazer com que quase todo mundo concorda"
- **Teste:** Rankear os 37 itens por net agreement; testar diferencas
  entre os 5 primeiros com intervalos de confianca bootstrap.
- **Origem:** Fase 2 stats (net_agreement, ceiling_pct)
- **Literatura:** Humor e consistentemente associado a bem-estar em
  diferentes culturas e idades. Uma meta-analise de 85 estudos
  (N=27.562) mostrou que humor afiliativo melhora o bem-estar
  subjetivo independente de cultura ou idade (Jiang et al., 2020).
  Martin et al. (2003, 1.922 citacoes) estabeleceram quatro estilos
  de humor com efeitos diferenciais no bem-estar.
- **Analista:** distribucional

### H02 — Conexao, amor e aprendizado dominam o ranking de prazer?

Conexao profunda (top-2 box 76%), aprendizado (74%), tempo de qualidade
(74%) e amar/ser amado (71%) se agrupam no topo. Eles formam um patamar
claramente acima dos demais, ou o ranking e mais gradual?

- **Manchete:** "Conexao humana e aprendizado: o que as pessoas mais valorizam"
- **Teste:** Rankear os 37 itens por top-2 box (% que marcou +2 ou +3).
  Testar se o patamar superior e estatisticamente distinto do seguinte
  usando estabilidade de rank via bootstrap.
- **Origem:** Fase 2 stats (top2_box)
- **Literatura:** Ryan e Deci (2001, 11.158 citacoes) estabeleceram que
  tanto buscas hedonicas (prazer) quanto eudaimonicas (significado/
  crescimento) contribuem para o bem-estar, com buscas eudaimonicas
  gerando significado mais duradouro. Nossos itens do topo abrangem
  ambos: aprendizado e eudaimonico, conexao e amor sao sociais/hedonicos.
- **Analista:** distribucional

### H03 — Buscar emocao forte e a categoria de prazer mais rejeitada?

O fator Thrilling (emocionante) e o unico com mediana negativa. Seus itens
(adrenalina, coisas assustadoras, risco, festas) tem as maiores taxas de
bottom-2 box. Ele e realmente um outlier entre os 6 fatores?

- **Manchete:** "A maioria das pessoas nao quer adrenalina — emocao forte
  e o prazer menos popular"
- **Teste:** Comparar mediana, net agreement e bottom-2 box entre os
  6 fatores. Testar se Thrilling e significativamente menor que o
  segundo mais baixo (Reputacional) usando Wilcoxon pareado.
- **Origem:** Observacao O-08
- **Literatura:** Busca de sensacoes e um traco de personalidade estavel
  com diferencas individuais bem caracterizadas (Zuckerman, 2010,
  3.410 citacoes). Correlaciona-se com abertura a experiencia e
  extroversao, mas esta longe de ser universal — consistente com nosso
  achado de que a maioria rejeita itens de emocao forte.
- **Analista:** distribucional

### H04 — Espiritualidade e o prazer que mais divide as pessoas?

Sentimentos espirituais tem o maior desvio-padrao de todos os 37 itens
(2,04), a moda em -3 ("discordo totalmente"), mas 10,5% em +3. Isso e
bimodalidade genuina (dois campos opostos) ou apenas alta variancia?

- **Manchete:** "Espiritualidade: o prazer que racha a sala ao meio"
- **Teste:** Calcular coeficiente de bimodalidade; ajustar uma mistura
  gaussiana de 2 componentes ao item espiritual e testar se 2
  componentes se ajustam melhor que 1 (comparacao por BIC).
  Visualizar com sobreposicao de densidades.
- **Origem:** Fase 2 stats (SD, bimodality_coeff, distribuicao de frequencia)
- **Literatura:** Villani et al. (2019, 323 citacoes) descobriram que a
  relacao da espiritualidade com bem-estar varia dramaticamente conforme
  o status religioso: positiva para religiosos, negligenciavel ou
  ausente para nao-religiosos. Vitorino et al. (2018) encontraram que
  49% de uma amostra brasileira pontuou baixo em espiritualidade e
  religiosidade, enquanto 27% pontuou alto em ambos — consistente com
  uma distribuicao polarizada.
- **Analista:** distribucional

---

## Tema 2 — Como os prazeres se relacionam

### H05 — Alguns prazeres sao genuinamente incompativeis?

Natureza e status correlacionam negativamente (rho = -0,10), assim como
competicao e criatividade (rho = -0,08). Essas correlacoes negativas fracas
sao reais (significativamente abaixo de zero) ou apenas ruido?

- **Manchete:** "Quem ama natureza nao liga pra status — alguns prazeres
  sao incompativeis"
- **Teste:** Testar todas as correlacoes inter-item negativas contra
  H0: rho >= 0 (unilateral). Aplicar correcao FDR. Reportar quais
  pares sobrevivem.
- **Origem:** Fase 3 correlacoes negativas
- **Literatura:** Pearce et al. (2020, 45 citacoes) descobriram que a
  orientacao eudaimonica (crescimento, autenticidade) mapeia para um
  escopo amplo de preocupacao (nos, futuro, causas), enquanto a
  orientacao hedonica mapeia para foco estreito (eu, agora, tangivel).
  Isso sugere uma razao estrutural para natureza (amplo) e status
  (estreito) puxarem em direcoes opostas.
- **Analista:** relacional

### H06 — Mentes curiosas sao indiferentes a status?

Os fatores Intelectual e Reputacional correlacionam em rho = 0,02 — quase
zero. O mundo intelectual e realmente ortogonal ao mundo do status?

- **Manchete:** "Mentes curiosas nao buscam status — as duas dimensoes
  sao independentes"
- **Teste:** Testar se o rho inter-fator (Intelectual-Reputacional) nao
  e significativamente diferente de zero. Complementar com a matriz de
  correlacao item-a-item entre os 5 itens intelectuais e 6 reputacionais.
- **Origem:** Observacao O-01
- **Literatura:** Pearce et al. (2020) encontraram que a orientacao
  eudaimonica se relaciona com escopo amplo de preocupacao, enquanto
  a orientacao hedonica se relaciona com valores egoistas (poder/
  riqueza). Porem, a orientacao eudaimonica tambem mostrou alguma
  ligacao com ambicao — sugerindo que a ortogonalidade pode nao ser
  absoluta.
- **Analista:** relacional

### H07 — Existe um superfator prossocial?

Interpessoal e Noble correlacionam em rho = 0,46 — a correlacao inter-fator
mais forte. Eles formam um fator de segunda ordem: uma orientacao unica de
"cuidado" que abrange tanto pessoas quanto causas?

- **Manchete:** "Quem cuida de pessoas tambem cuida de causas"
- **Teste:** Rodar analise fatorial de segunda ordem: Interpessoal e Noble
  carregam em um fator de ordem superior comum? Comparar ajuste do modelo
  (CFA) com e sem o fator prossocial de segunda ordem.
- **Origem:** Observacao O-01
- **Literatura:** Huta e Ryan (2010, 1.221 citacoes) mostraram que buscas
  eudaimonicas se relacionam com significado, admiracao e senso de conexao
  com algo maior. Chen et al. (2023) descobriram que a orientacao
  eudaimonica promove tanto comportamentos de maestria quanto altruistas
  — consistente com uma dimensao prossocial unificada.
- **Analista:** relacional

### H08 — Prazer sexual tem mais a ver com emocao e status do que com sensacao?

Sexo (item avulso) correlaciona mais com Thrilling (rho = 0,25) e
Reputacional (rho = 0,21) do que com Sensorial (rho = 0,17) — o oposto
da intuicao ingenue. Esse padrao e robusto?

- **Manchete:** "Prazer sexual: mais emocao e ego do que pura sensacao?"
- **Teste:** Comparar as correlacoes de p_sex com cada um dos 6 scores
  de fator. Testar se rho(sexo, thrilling) > rho(sexo, sensorial) usando
  o teste de Steiger para comparacao de correlacoes dependentes.
- **Origem:** Observacao O-14
- **Analista:** relacional

### H09 — Amor prediz valorizar conexao e tempo de qualidade?

Amar/ser amado, conexao profunda e tempo de qualidade formam um triangulo
apertado (rho = 0,43-0,44). Saber o score de alguem em "amar" realmente
prediz seu score em "conexao" e "tempo de qualidade" fora da amostra?

- **Manchete:** "Amor gera conexao: quem ama tambem valoriza tempo
  de qualidade"
- **Teste:** Regressao com split treino/teste: p_connection ~ p_loving +
  p_qualityTime. Reportar R-quadrado fora da amostra. Complementar com
  correlacoes parciais controlando tendencia geral de resposta.
- **Origem:** Fase 3 correlacoes
- **Analista:** relacional

---

## Tema 3 — O instrumento mede prazer corretamente?

### H10 — Os dados sugerem 8 dimensoes em vez de 6?

A analise paralela da Fase 3 sugeriu 8 componentes, nao 6. Uma EFA com
rotacao obliqua nos 37 itens pode revelar uma estrutura que se ajusta
melhor aos dados do que os 6 fatores pre-definidos do instrumento.

- **Manchete:** "O mapa do prazer tem 8 continentes, nao 6"
- **Teste:** Rodar EFA (rotacao oblimin) para 6, 7 e 8 fatores nos
  37 itens. Comparar: variancia explicada, RMSEA, TLI, BIC e
  interpretabilidade de cada solucao. Usar ESEM se restricoes de
  cross-loading do tipo CFA distorcerem o resultado.
- **Origem:** Observacao O-04
- **Literatura:** Joshanloo (2016, 201 citacoes) mostrou que ESEM produz
  correlacoes inter-fator mais precisas (menores) que CFA ao permitir
  cross-loadings — sugerindo que estruturas fatoriais baseadas em CFA
  podem superestimar a unidade. Bjorndal et al. (2023) encontraram 6
  fatores de bem-estar carregando em um unico fator de ordem superior
  ("fator de felicidade").
- **Analista:** estrutural

### H11 — Os itens "sem teto" formam um fator oculto?

Humor, som/musica, natureza, animais, jogos e sexo nao pertencem a nenhum
fator. Mas humor e som correlacionam em rho = 0,36, e natureza e animais
em rho = 0,25. Alguns desses itens avulsos se agrupam em uma ou mais novas
dimensoes quando incluidos na EFA?

- **Manchete:** "Uma dimensao escondida: humor, musica, natureza e animais
  podem pertencer juntos"
- **Teste:** Comparar resultados da EFA com 31 itens (apenas atribuidos)
  vs todos os 37 itens. Os avulsos formam um novo fator coerente?
  Examinar loadings e interpretar.
- **Origem:** Observacao O-14
- **Literatura:** Gallagher et al. (2009, 556 citacoes) demonstraram que
  modelos de bem-estar podem ser integrados em estruturas hierarquicas.
  Encontrar um novo fator entre itens avulsos seria analogo a descobertas
  de dimensoes adicionais de bem-estar alem da divisao hedonica/eudaimonica.
- **Analista:** estrutural

---

## Tema 4 — Existem "tipos" de buscadores de prazer?

### H12 — Somos especialistas ou generalistas do prazer?

A maioria das pessoas concentra seu prazer em 2-3 fatores dominantes
(especialistas) ou distribui igualmente entre todos os 6 (generalistas)?
E os generalistas reportam mais prazer geral que os especialistas?

- **Manchete:** "Especialistas vs. generalistas: como as pessoas organizam
  seu prazer"
- **Teste:** Calcular entropia de Shannon dos 6 scores de fator de cada
  respondente (normalizados para proporcoes). Classificar: entropia >
  mediana = generalista, abaixo = especialista. Comparar prazer medio
  geral (media dos 37 itens) entre grupos (Mann-Whitney + d de Cohen).
- **Origem:** H06-antigo + H25 + H40 (fundidos)
- **Literatura:** Avsec et al. (2016) encontraram quatro perfis de
  felicidade replicados em 7 paises: Vida Plena (alto em tudo), Vida
  Vazia (baixo em tudo), Vida Prazerosa e Vida Significativa. Pessoas
  com perfil "Vida Plena" (nossos generalistas) reportaram o maior
  bem-estar. Huta e Ryan (2010) encontraram igualmente que pessoas
  altas em hedonia e eudaimonia tinham o maior bem-estar.
- **Analista:** segmentacao

### H13 — Perfis de prazer sao continuos, ou existem "tipos" reais?

A melhor tentativa de clustering (k=2) produziu um silhouette de apenas
0,114 — separacao muito fraca. Isso significa que nao existem agrupamentos
naturais, e perfis de prazer sao essencialmente um espectro?

- **Manchete:** "Nao existem tipos claros — prazer e um espectro"
- **Teste:** Rodar K-Means (k=2 a 8), clustering hierarquico e GMM.
  Se todos produzirem silhouette < 0,25, a hipotese do espectro e
  sustentada. Validar com estabilidade bootstrap (100 reamostras,
  medir ARI).
- **Origem:** Observacoes O-09, O-10
- **Literatura:** Pancheva et al. (2020, 44 citacoes) encontraram que
  ~70% das pessoas convergem em bem-estar hedonico e eudaimonico (ambos
  altos ou ambos baixos), enquanto ~30% divergem. Isso sugere um
  espectro parcial em vez de tipos limpos — consistente com nosso
  silhouette baixo.
- **Analista:** segmentacao

### H14 — Quem busca emocao forte tem um perfil de prazer fundamentalmente diferente?

Respondentes no quartil superior de Thrilling podem diferir sistematicamente
do quartil inferior em todos os outros fatores — nao apenas em emocao, mas
em todo o seu mapa de prazer.

- **Manchete:** "Quem busca adrenalina: uma raca diferente de buscador de prazer"
- **Teste:** Dividir a amostra em Q4 (top 25%) e Q1 (bottom 25%) no score
  do fator Thrilling. Comparar todos os outros 5 scores de fator entre
  os grupos (Mann-Whitney por fator + d de Cohen). Aplicar correcao FDR.
- **Origem:** Observacoes O-08 (fusao de H27 + H37 antigos)
- **Literatura:** Busca de sensacoes e um traco de personalidade associado
  a abertura, extroversao e baixa conscienciosidade (Zuckerman, 2010;
  de Vries et al., 2009, 139 citacoes). Nossos dados podem testar se
  esse traco remodela todo o perfil de prazer.
- **Analista:** segmentacao + comparativo

### H15 — Entusiastas espirituais sao uma tribo a parte?

Com a espiritualidade sendo bimodal, respondentes com score alto (>= +1)
podem formar um subgrupo com perfil de prazer distintamente diferente —
talvez maior em Noble e Interpessoal, menor em Thrilling e Reputacional?

- **Manchete:** "A minoria espiritual: um perfil de prazer distinto"
- **Teste:** Dividir: espiritual >= +1 vs espiritual <= -1. Comparar
  todos os 6 scores de fator entre os grupos (Mann-Whitney + d de Cohen).
- **Origem:** Fase 2 stats (bimodalidade espiritual)
- **Literatura:** Villani et al. (2019) encontraram que espiritualidade
  prediz positivamente o bem-estar independente do status religioso,
  pela dimensao de "proposito". Saroglou et al. (2020, 104 citacoes)
  encontraram que a dimensao "bonding" da religiosidade prediz
  satisfacao com a vida de forma unica — sugerindo que pessoas
  espirituais podem ter uma orientacao distinta para prazeres
  interpessoais e nobres.
- **Analista:** segmentacao + comparativo

### H16 — Existe um subgrupo "puramente intelectual"?

Entre todos os perfis possiveis, existe um cluster identificavel de pessoas
que pontuam alto em prazeres intelectuais (aprender, pensar, criar) mas
relativamente baixo em todo o resto?

- **Manchete:** "A vida da mente: buscadores de prazer puramente
  intelectuais existem?"
- **Teste:** Nas solucoes de clustering k=3 a k=6, procurar um cluster
  com z-score Intelectual > 0,5 e todos os outros fatores abaixo da
  media geral. Perfilar e caracterizar se encontrado.
- **Origem:** Experiencia em ciencia de dados
- **Literatura:** van Halem et al. (2024) descobriram que diferentes
  tracos de personalidade (Big Five) nao moderaram o impacto de motivos
  hedonicos vs eudaimonicos no bem-estar — sugerindo que perfis
  "somente intelectuais" podem ser raros em vez de um tipo fundamental
  de personalidade.
- **Analista:** segmentacao

---

## Tema 5 — O que prediz o que?

### H17 — Adrenalina e serenidade sao caminhos opostos para o prazer?

Situacoes excitantes e relaxamento correlacionam negativamente (rho = -0,08).
Gostar de atividades de alto risco (adrenalina, assustador, risco) realmente
prediz *nao gostar* de relaxamento e natureza?

- **Manchete:** "Adrenalina vs. serenidade: dois caminhos opostos para o prazer"
- **Teste:** Regressao multipla: p_relax ~ p_adrenaline + p_scary + p_risk
  (e vice-versa). Reportar betas padronizados e R-quadrado. Testar em split
  treino/teste para confirmar fora da amostra.
- **Origem:** Fase 3 correlacoes negativas
- **Literatura:** Giuntoli et al. (2020, 87 citacoes) distinguiram
  orientacao hedonica de prazer da orientacao hedonica de relaxamento —
  sao sub-componentes separados da hedonia. Chen et al. (2023) propuseram
  que abordagem hedonica (buscar excitacao) e evitacao hedonica (buscar
  conforto) sao psicologicamente distintas. Nossos dados podem testar se
  essas mapeiam para itens thrilling vs sensoriais.
- **Analista:** preditivo

### H18 — Qual fator mais contribui para o prazer geral?

Se regredirmos a media geral de prazer (media dos 37 itens) nos 6 scores
de fator, qual fator tem o maior coeficiente padronizado? E o Interpessoal
(o fator com maior score) ou algo menos obvio?

- **Manchete:** "O maior motor do prazer geral pode te surpreender"
- **Teste:** Regressao multipla: media_37 ~ 6 scores de fator. Reportar
  betas padronizados, R-quadrado e checar multicolinearidade (VIF).
  Nota: parcialmente tautologico ja que fatores sao subconjuntos dos
  itens, entao interpretar pesos relativos, nao ajuste absoluto.
- **Origem:** Experiencia em ciencia de dados
- **Analista:** preditivo

### H19 — Menos de 10 itens conseguem capturar seu perfil completo de prazer?

37 itens e muito. Uma versao curta com menos de 10 itens cuidadosamente
selecionados poderia prever o perfil completo de 6 fatores com acuracia
razoavel (R-quadrado > 0,70)?

- **Manchete:** "Um atalho de 10 perguntas para seu DNA de prazer"
- **Teste:** Regressao Lasso em split treino/teste: para cada score de
  fator, selecionar os itens mais preditivos dos itens dos *outros*
  fatores mais avulsos. Reportar quantos itens sao necessarios para
  alcancar R2 > 0,70 para os 6 fatores simultaneamente.
- **Origem:** Experiencia em ciencia de dados
- **Analista:** preditivo

---

## Hipoteses eliminadas — justificativa

As 41 hipoteses originais foram reduzidas para 19. Abaixo esta o registro
do que foi removido e por que, para transparencia.

### Eliminadas como obvias ou tautologicas (7)

| ID antigo | Titulo | Motivo |
|-----------|--------|--------|
| H07 | Efeito teto reduz discriminacao do item | Truismo psicometrico — verdadeiro por definicao |
| H15 | Itens intra-fator predizem uns aos outros | Isso e literalmente a definicao de um fator |
| H31 | Scores de fator predizem media geral | Tautologico — fatores sao subconjuntos dos 37 itens |
| H32 | Interpessoal e o preditor mais forte do prazer geral | Consequencia obvia de ter a media mais alta |
| H38 | Quartil superior intelectual tem baixo reputacional | Repete H06 (ortogonalidade) em forma de grupo |
| H41 | Remover respondentes suspeitos nao muda resultados | Etapa de controle de qualidade, nao hipotese |
| H05 | Coeficiente de bimodalidade > 0,555 | Tecnico demais; a parte interessante foi absorvida por H04 |

### Eliminadas como puramente metodologicas (5)

| ID antigo | Titulo | Motivo |
|-----------|--------|--------|
| H22 | Remover itens com cross-loading melhora EFA | Um procedimento, nao um insight testavel |
| H29 | GMM melhor que K-Means | Comparacao de metodo sem valor editorial |
| H30 | Estabilidade de cluster por bootstrap e baixa | Etapa de validacao agora embutida em H13 |
| H33 | Modelo parcimonioso com < 10 itens | Absorvido por H19 (versao curta) |
| H35 | Top 5 itens extremos predizem perfil | Variante tecnica; menos interessante que H19 |

### Eliminadas como granulares demais (6)

| ID antigo | Titulo | Motivo |
|-----------|--------|--------|
| H08 | Redundancia Community ~ Charity | Par de itens granular; emerge naturalmente na EFA |
| H09 | Redundancia Caring ~ Family | Idem |
| H10 | Being liked tem cross-loading em Reputacional | Detalhe tecnico de cross-loading |
| H18 | Fator Intelectual e o menos coeso | Detalhe que emerge da EFA, sem valor para blog |
| H19-antigo | Being liked / Belonging cross-loading | Mesmo que H10 |
| H39 | Perfis de outliers diferem | Nicho demais para blog; N pequeno (66 outliers) |

### Fundidas em novas hipoteses (4)

| IDs antigos | Fundidos em | Justificativa |
|-------------|-------------|---------------|
| H06 + H25 + H40 | H12 (especialistas vs generalistas) | Todos fazem a mesma pergunta de angulos diferentes |
| H17 + H20 + H23 | H10 (8 dimensoes vs 6) | Todos sobre estrutura fatorial dos 37 itens |
| H27 + H37 | H14 (perfil de quem busca emocao) | Ambos comparam quartis de Thrilling entre fatores |
| H12-antigo + H21 | H11 (fator oculto) | Ambos sobre itens avulsos formando novos agrupamentos |

---

## Metodologia

### Processo de refinamento das hipoteses

1. **Geracao original (Fase 4a):** 41 hipoteses a partir de 14 observacoes
   da EDA, artefatos numericos das Fases 2-3, objetivos editoriais e
   experiencia em ciencia de dados.
2. **Revisao de literatura (Fase 4b):** Busca de literatura academica via
   Consensus.app cobrindo psicologia hedonica, estrutura fatorial de
   bem-estar, busca de sensacoes, espiritualidade e diferencas individuais,
   e humor e bem-estar. Referencias-chave: Ryan e Deci (2001), Huta e
   Ryan (2010), Avsec et al. (2016), Villani et al. (2019), Zuckerman
   (2010), Joshanloo (2016), Pearce et al. (2020), Pancheva et al. (2020).
3. **Refinamento (Fase 4b):** Aplicados tres filtros:
   - **Obvio/tautologico:** removido se a resposta e conhecida antes de
     testar (ex: "itens dentro de um fator correlacionam entre si")
   - **Puramente metodologico:** removido se a hipotese testa um metodo
     em vez de gerar um insight (ex: "GMM vs K-Means")
   - **Granular demais:** removido se o achado e um detalhe tecnico que
     emerge naturalmente durante a analise (ex: cross-loadings especificos)
4. **Fusao:** Hipoteses que fazem a mesma pergunta de angulos diferentes
   foram combinadas em uma unica hipotese mais forte.

### Criterios de prioridade

Todas as 19 hipoteses restantes sao de alta prioridade — as de media/baixa
foram eliminadas ou absorvidas durante o refinamento.

### Roteamento por analista

Cada hipotese esta marcada com o(s) analista(s) especialista(s) que a
executara nas Fases 5-6, seguindo as categorias do PRD:

- **distribucional** — formas de distribuicao, padroes de resposta
- **relacional** — correlacoes, associacoes entre variaveis
- **estrutural** — estrutura fatorial, dimensionalidade, EFA/PCA
- **segmentacao** — clustering, perfis, tipologias
- **preditivo** — modelos preditivos, feature selection
- **comparativo** — comparacoes entre grupos derivados

### Viabilidade

Todas as 19 hipoteses sao viaveis com os dados disponiveis. Nenhuma requer
dados demograficos ou externos. Comparacoes de grupo usam grupos derivados
(quartis, clusters, divisoes por entropia, flags de anomalia).

---

## Mapeamento de IDs: antigo para novo

| ID novo | ID(s) antigo(s) | Titulo curto |
|---------|-----------------|--------------|
| H01 | H01 | Rir e o mais universal |
| H02 | H02 | Conexao + aprendizado no topo |
| H03 | H03 | Thrilling mais rejeitado |
| H04 | H04 + H05 | Espiritualidade polariza |
| H05 | H11 | Prazeres incompativeis |
| H06 | H13 | Intelectual ortogonal a reputacional |
| H07 | H14 | Superfator prossocial |
| H08 | H16 | Sexo: emocao > sensacao |
| H09 | H34 | Amor prediz conexao |
| H10 | H17 + H20 + H23 | 8 dimensoes vs 6 |
| H11 | H21 + H12-antigo | Fator oculto (avulsos) |
| H12 | H06-antigo + H25 + H40 | Especialistas vs generalistas |
| H13 | H24 + H30 | Perfis sao continuos |
| H14 | H27 + H37 | Perfil de quem busca emocao |
| H15 | H28 | Subgrupo espiritual |
| H16 | H26 | Perfil puramente intelectual |
| H17 | H36 | Adrenalina vs serenidade |
| H18 | H31 + H32 | Maior motor do prazer geral |
| H19 | H33 + H35 | Versao curta do instrumento |

---

*Revisado de 41 para 19 hipoteses apos revisao de literatura e refinamento.*
*Fase 4b — revisao informada por literatura.*
