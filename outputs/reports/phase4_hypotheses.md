# Fase 4 — Hipoteses (Revisadas)

**Total:** 18 hipoteses (refinadas a partir de 41 originais)

**Todas viaveis** com os dados que temos. Nenhuma precisa de dados externos.

**Fontes:** 14 observacoes da Fase 3 + numeros das Fases 2-3 + objetivo de
blog + experiencia em ciencia de dados + **revisao de artigos academicos**
(Consensus.app: psicologia do prazer, bem-estar, busca de emocoes fortes,
espiritualidade, humor).

---

## Resumo por tema

| Tema | Descricao | Hipoteses | Qtd |
|------|-----------|-----------|-----|
| O que mais (e menos) nos da prazer | Rankings, consenso, divisoes | H01-H04 | 4 |
| Como os prazeres se relacionam | Conexoes, independencia, oposicoes | H05-H09 | 5 |
| Os itens avulsos formam um grupo? | Itens sem fator podem se conectar | H10 | 1 |
| Existem "tipos" de pessoas? | Perfis, grupos, subgrupos | H11-H15 | 5 |
| O que prediz o que? | Cadeias de associacao, caminhos opostos | H16-H18 | 3 |
| **Total** | | | **18** |

## Resumo por analista

| Analista | Hipoteses | Qtd |
|----------|-----------|-----|
| distribucional | H01, H02, H03, H04 | 4 |
| relacional | H05, H06, H07, H08, H09 | 5 |
| estrutural | H10 | 1 |
| segmentacao | H11, H12, H13, H14, H15 | 5 |
| preditivo + comparativo | H16, H17, H18 | 3 |

---

## Tema 1 — O que mais (e menos) nos da prazer

### H01 — Rir e a fonte de prazer mais universal?

Humor teve o maior nivel de concordancia entre os 37 itens (77,1%), com
42% dos respondentes no maximo da escala (+3). A diferenca para o segundo
colocado (pensar/explorar ideias, 73%) e real, ou os primeiros do ranking
estao basicamente empatados?

- **Manchete:** "Rir: o unico prazer com que quase todo mundo concorda"
- **Teste:** Rankear os 37 itens por concordancia liquida; testar se as
  diferencas entre os 5 primeiros sao reais usando intervalos de confianca
  por reamostragem (bootstrap).
- **Origem:** Fase 2 stats (net_agreement, ceiling_pct)
- **Literatura:** Humor esta ligado a bem-estar em diferentes culturas e
  idades. Uma revisao de 85 estudos (N=27.562) mostrou que humor do tipo
  social melhora o bem-estar em qualquer cultura ou idade (Jiang et al.,
  2020). Martin et al. (2003, 1.922 citacoes) identificaram quatro
  estilos de humor com efeitos diferentes no bem-estar.
- **Analista:** distribucional

### H02 — Conexao, amor e aprendizado dominam o ranking de prazer?

Conexao profunda (76% marcaram +2 ou +3), aprendizado (74%), tempo de
qualidade (74%) e amar/ser amado (71%) se agrupam no topo. Eles formam
um patamar claramente acima dos demais, ou o ranking cai de forma gradual?

- **Manchete:** "Conexao humana e aprendizado: o que as pessoas mais
  valorizam"
- **Teste:** Rankear os 37 itens pelo % que marcou +2 ou +3 (top-2 box).
  Testar se o grupo de cima e separado do resto por reamostragem.
- **Origem:** Fase 2 stats (top2_box)
- **Literatura:** Ryan e Deci (2001, 11.158 citacoes) mostraram que tanto
  a busca por prazer quanto a busca por significado/crescimento contribuem
  para o bem-estar, mas a busca por significado gera efeitos mais
  duradouros. Nossos itens do topo misturam os dois: aprendizado e
  sobre crescimento, conexao e amor sao sobre relacoes.
- **Analista:** distribucional

### H03 — Buscar emocao forte e a categoria de prazer mais rejeitada?

O fator Emocionante (Thrilling) e o unico com mediana negativa. Seus itens
(adrenalina, coisas assustadoras, risco, festas) tem as maiores taxas de
rejeicao. Ele e realmente um caso a parte entre os 6 fatores?

- **Manchete:** "A maioria das pessoas nao quer adrenalina — emocao forte
  e o prazer menos popular"
- **Teste:** Comparar mediana, concordancia e rejeicao entre os 6 fatores.
  Testar se Emocionante e significativamente menor que o segundo mais
  baixo (Reputacional).
- **Origem:** Observacao O-08
- **Literatura:** Busca de sensacoes fortes e um traco de personalidade
  estavel, com grandes diferencas entre pessoas (Zuckerman, 2010,
  3.410 citacoes). Ele aparece junto com abertura a novas experiencias
  e extroversao, mas esta longe de ser universal — combina com nosso
  achado de que a maioria rejeita esses itens.
- **Analista:** distribucional

### H04 — Espiritualidade e o prazer que mais divide as pessoas?

Sentimentos espirituais tem a maior variacao de todos os 37 itens
(desvio-padrao = 2,04). A resposta mais frequente e -3 ("discordo
totalmente"), mas 10,5% marcaram +3 ("concordo totalmente"). Sera que
existem mesmo dois grupos opostos, ou e apenas muita variacao sem um
padrao claro?

- **Manchete:** "Espiritualidade: o prazer que racha a sala ao meio"
- **Teste:** Verificar se a distribuicao tem dois picos (ajustar um
  modelo de mistura com 2 curvas e comparar se funciona melhor que 1
  curva so). Visualizar a distribuicao com grafico de densidade.
- **Origem:** Fase 2 stats (SD, distribuicao de frequencia)
- **Literatura:** Villani et al. (2019, 323 citacoes) descobriram que a
  relacao entre espiritualidade e bem-estar muda muito conforme a pessoa:
  positiva para religiosos, quase nula para nao-religiosos. Vitorino et
  al. (2018) acharam que 49% de uma amostra brasileira pontuou baixo em
  espiritualidade e religiosidade, enquanto 27% pontuou alto nas duas
  — combina com uma distribuicao dividida em dois grupos.
- **Analista:** distribucional

---

## Tema 2 — Como os prazeres se relacionam

### H05 — Alguns prazeres sao realmente incompativeis?

Natureza e status tem uma correlacao negativa (rho = -0,10), assim como
competicao e criatividade (rho = -0,08). Esses numeros negativos sao
reais, ou e apenas variacao aleatoria?

- **Manchete:** "Quem ama natureza nao liga pra status — alguns prazeres
  sao incompativeis"
- **Teste:** Testar se as correlacoes negativas entre itens sao realmente
  menores que zero (teste de um lado). Corrigir para multiplas comparacoes
  (FDR). Ver quais pares sobrevivem.
- **Origem:** Fase 3 correlacoes negativas
- **Literatura:** Pearce et al. (2020, 45 citacoes) descobriram que quem
  busca crescimento pessoal tende a se preocupar com coisas amplas (os
  outros, o futuro, causas), enquanto quem busca prazer imediato foca em
  coisas imediatas (eu, agora, o que posso tocar). Isso pode explicar
  por que natureza (preocupacao ampla) e status (foco em si) puxam em
  direcoes opostas.
- **Analista:** relacional

### H06 — Mentes curiosas sao indiferentes a status?

Os fatores Intelectual e Reputacional tem correlacao quase zero
(rho = 0,02). O mundo da curiosidade e o mundo do status sao mesmo
mundos separados, sem relacao entre si?

- **Manchete:** "Mentes curiosas nao buscam status — as duas dimensoes
  sao independentes"
- **Teste:** Testar se a correlacao entre os fatores Intelectual e
  Reputacional nao e diferente de zero. Complementar olhando as
  correlacoes entre cada item intelectual e cada item reputacional.
- **Origem:** Observacao O-01
- **Literatura:** Pearce et al. (2020) encontraram que quem busca
  crescimento se preocupa com coisas amplas, enquanto quem busca prazer
  valoriza poder e riqueza. Porem, quem busca crescimento tambem
  mostrou alguma ligacao com ambicao — entao a separacao pode nao ser
  total.
- **Analista:** relacional

### H07 — Existe um superfator "quem cuida"?

Os fatores Interpessoal e Nobre tem a correlacao mais forte entre todos
os pares de fatores (rho = 0,46). Sera que quem se importa com pessoas
(interpessoal) tambem se importa com causas (nobre), formando uma unica
dimensao de "cuidado"?

- **Manchete:** "Quem cuida de pessoas tambem cuida de causas"
- **Teste:** Verificar se Interpessoal e Nobre formam uma dimensao de
  nivel superior (analise fatorial de segunda ordem). Comparar modelos
  com e sem esse agrupamento.
- **Origem:** Observacao O-01
- **Literatura:** Huta e Ryan (2010, 1.221 citacoes) mostraram que
  quem busca significado na vida tende a sentir admiracao e conexao
  com algo maior. Chen et al. (2023) descobriram que esse tipo de
  orientacao promove tanto desenvolvimento pessoal quanto ajuda ao
  proximo — combina com uma dimensao unificada de cuidado.
- **Analista:** relacional

### H08 — Prazer sexual tem mais a ver com emocao e ego do que com sensacao fisica?

Sexo (item avulso) correlaciona mais com o fator Emocionante (rho = 0,25)
e com o fator Reputacional (rho = 0,21) do que com o fator Sensorial
(rho = 0,17) — o oposto do que a maioria esperaria. Esse padrao se
confirma?

- **Manchete:** "Prazer sexual: mais emocao e ego do que pura sensacao?"
- **Teste:** Comparar as correlacoes do item sexo com cada um dos 6
  fatores. Testar se a correlacao com Emocionante e maior que com
  Sensorial (teste de Steiger para correlacoes que compartilham dados).
- **Origem:** Observacao O-14
- **Analista:** relacional

### H09 — Amor prediz valorizar conexao e tempo de qualidade?

Amar/ser amado, conexao profunda e tempo de qualidade formam um
triangulo apertado (correlacoes de 0,43-0,44). Se eu souber quanto
alguem pontua em "amar", consigo adivinhar quanto vai pontuar em
"conexao" e "tempo de qualidade"?

- **Manchete:** "Amor gera conexao: quem ama tambem valoriza tempo
  de qualidade"
- **Teste:** Dividir os dados em treino e teste. Usar o item "amar" e
  "tempo de qualidade" para prever "conexao". Ver se a previsao funciona
  fora da amostra de treino.
- **Origem:** Fase 3 correlacoes
- **Analista:** relacional

---

## Tema 3 — Os itens avulsos formam um grupo?

### H10 — Os 6 itens "sem casa" se conectam entre si?

Humor, som/musica, natureza, animais, jogos e sexo nao pertencem a nenhum
dos 6 fatores do instrumento. Mas humor e musica correlacionam em 0,36,
e natureza e animais em 0,25. Sera que alguns desses itens avulsos formam
duplas ou trios com conexoes fortes, ou cada um e realmente independente?

**Nota importante:** esta hipotese NAO tenta corrigir os 6 fatores do
instrumento. Aceitamos os fatores como sao. O objetivo e apenas explorar
se os itens avulsos tem conexoes interessantes entre si que valham
comentar.

- **Manchete:** "Humor e musica, natureza e animais: pares naturais entre
  os itens avulsos"
- **Teste:** Examinar a matriz de correlacao entre os 6 itens avulsos.
  Verificar se algum par ou trio tem correlacao forte (rho > 0,30).
  Se sim, descrever o padrao. Se nao, confirmar que sao independentes.
  So considerar criar um "novo grupo" se as correlacoes forem
  surpreendentemente altas (rho > 0,50).
- **Origem:** Observacao O-14
- **Literatura:** Gallagher et al. (2009, 556 citacoes) mostraram que
  modelos de bem-estar podem ser organizados em estruturas com varios
  niveis (grupos dentro de grupos). Mesmo sem criar um novo fator,
  encontrar pares fortes entre os itens avulsos e uma descoberta
  interessante.
- **Analista:** estrutural

---

## Tema 4 — Existem "tipos" de pessoas?

### H11 — Somos especialistas ou generalistas do prazer?

A maioria das pessoas concentra seu prazer em 2-3 fatores dominantes
(especialistas) ou distribui de forma equilibrada entre todos os 6
(generalistas)? E quem gosta de tudo reporta mais prazer no geral do
que quem foca em poucos?

- **Manchete:** "Especialistas vs. generalistas: como as pessoas organizam
  seu prazer"
- **Teste:** Calcular um indice de diversidade (entropia de Shannon — mede
  o quanto o perfil e equilibrado vs concentrado) dos 6 scores de fator
  de cada pessoa. Dividir em generalistas e especialistas pela mediana.
  Comparar o prazer medio geral entre os dois grupos.
- **Origem:** H06-antigo + H25 + H40 (fundidos)
- **Literatura:** Avsec et al. (2016) encontraram quatro perfis de
  felicidade em 7 paises: Vida Plena (alto em tudo), Vida Vazia (baixo
  em tudo), Vida Prazerosa e Vida com Significado. Quem tinha o perfil
  "Vida Plena" (parecido com nossos generalistas) tinha o maior
  bem-estar. Huta e Ryan (2010) tambem acharam que quem combina prazer
  com significado vive melhor.
- **Analista:** segmentacao

### H12 — Perfis de prazer sao um espectro, ou existem "tipos" reais?

A melhor tentativa de agrupar os respondentes (k=2) deu um indice de
separacao (silhouette) de apenas 0,114 — muito fraco. Isso significa que
nao existem grupos naturais, e cada pessoa tem um perfil unico dentro de
um espectro continuo?

- **Manchete:** "Nao existem tipos claros — prazer e um espectro"
- **Teste:** Rodar varios metodos de agrupamento (K-Means, hierarquico,
  mistura gaussiana) com 2 a 8 grupos. Se todos derem separacao fraca
  (silhouette < 0,25), a hipotese do espectro se confirma. Validar
  repetindo em 100 sub-amostras aleatorias.
- **Origem:** Observacoes O-09, O-10
- **Literatura:** Pancheva et al. (2020, 44 citacoes) acharam que ~70%
  das pessoas convergem (alto em tudo ou baixo em tudo), enquanto ~30%
  divergem. Isso sugere um espectro parcial em vez de tipos separados
  — combina com nosso silhouette baixo.
- **Analista:** segmentacao

### H13 — Quem busca emocao forte tem um perfil de prazer completamente diferente?

Respondentes no quartil superior (top 25%) do fator Emocionante podem
diferir dos do quartil inferior nao so em emocao forte, mas em *todos*
os outros tipos de prazer.

- **Manchete:** "Quem busca adrenalina: um perfil de prazer completamente
  diferente"
- **Teste:** Dividir a amostra em top 25% e bottom 25% no fator
  Emocionante. Comparar todos os outros 5 fatores entre os dois grupos.
  Medir o tamanho da diferenca (d de Cohen — quanto maior, mais
  diferente). Corrigir para multiplas comparacoes.
- **Origem:** Observacoes O-08 (fusao de H27 + H37 antigos)
- **Literatura:** Busca de sensacoes e um traco de personalidade ligado a
  abertura, extroversao e baixa disciplina (Zuckerman, 2010; de Vries
  et al., 2009, 139 citacoes). Nossos dados podem mostrar se esse traco
  muda o perfil de prazer inteiro da pessoa.
- **Analista:** segmentacao + comparativo

### H14 — Quem gosta de espiritualidade e uma tribo a parte?

Como a espiritualidade divide as pessoas em dois campos, quem pontua
alto (>= +1) pode ter um perfil de prazer bem diferente — talvez mais
voltado para cuidar de pessoas e causas (Noble, Interpessoal), e menos
para emocao forte e status.

- **Manchete:** "A minoria espiritual: um perfil de prazer distinto"
- **Teste:** Dividir: espiritual >= +1 vs espiritual <= -1. Comparar
  todos os 6 fatores entre os grupos, medindo o tamanho da diferenca.
- **Origem:** Fase 2 stats (distribuicao dividida da espiritualidade)
- **Literatura:** Villani et al. (2019) acharam que espiritualidade esta
  ligada a bem-estar pela via do "proposito de vida". Saroglou et al.
  (2020, 104 citacoes) mostraram que a dimensao de "vinculo" da
  religiosidade esta ligada a satisfacao com a vida — sugerindo que
  pessoas espirituais podem ter uma orientacao diferente, mais voltada
  para relacionamentos e causas.
- **Analista:** segmentacao + comparativo

### H15 — Existe um grupo "puramente intelectual"?

Entre todos os perfis possiveis, da pra identificar um grupo de pessoas
que pontua alto em prazeres intelectuais (aprender, pensar, criar) mas
baixo em quase todo o resto?

- **Manchete:** "A vida da mente: existem pessoas que so sentem prazer
  em pensar?"
- **Teste:** Nas solucoes de agrupamento com 3 a 6 grupos, procurar
  um grupo com Intelectual acima da media e todos os outros fatores
  abaixo. Descrever o perfil se encontrado.
- **Origem:** Experiencia em ciencia de dados
- **Literatura:** van Halem et al. (2024) descobriram que tracos de
  personalidade (Big Five) nao mudam o impacto de motivos de prazer vs
  significado no bem-estar — sugerindo que perfis "so intelectuais"
  podem ser raros em vez de um tipo fundamental de pessoa.
- **Analista:** segmentacao

---

## Tema 5 — O que prediz o que?

### H16 — Adrenalina e serenidade sao caminhos opostos?

Situacoes emocionantes e relaxamento tem correlacao negativa (rho = -0,08).
Gostar de atividades de alto risco (adrenalina, coisas assustadoras)
realmente prediz *nao gostar* de relaxamento e natureza?

- **Manchete:** "Adrenalina vs. serenidade: dois caminhos opostos para
  o prazer"
- **Teste:** Regressao: usar adrenalina, assustador e risco para prever
  relaxamento (e vice-versa). Ver se o efeito se confirma fora da
  amostra de treino.
- **Origem:** Fase 3 correlacoes negativas
- **Literatura:** Giuntoli et al. (2020, 87 citacoes) mostraram que
  "buscar excitacao" e "buscar relaxamento" sao componentes separados
  do prazer — nao a mesma coisa. Chen et al. (2023) propuseram que
  buscar emocao forte e buscar conforto sao psicologicamente distintos.
  Nossos dados podem mostrar se isso aparece como itens de emocao vs
  itens sensoriais.
- **Analista:** preditivo

### H17 — Qual fator mais contribui para o prazer geral?

Se usarmos os 6 fatores para prever o prazer medio geral (media dos 37
itens), qual fator pesa mais? Sera o Interpessoal (que tem a maior media)
ou algum outro menos obvio?

- **Manchete:** "O maior motor do prazer geral pode te surpreender"
- **Teste:** Regressao multipla: prazer medio ~ 6 fatores. Ver qual
  fator tem o maior peso. Nota: como os fatores fazem parte dos 37
  itens, essa analise mostra pesos relativos, nao uma descoberta
  independente.
- **Origem:** Experiencia em ciencia de dados
- **Analista:** preditivo

### H18 — Menos de 10 perguntas conseguem capturar seu perfil completo?

37 itens e muito. Uma versao curta com menos de 10 perguntas bem
escolhidas conseguiria prever o perfil completo de 6 fatores com boa
precisao?

- **Manchete:** "Um atalho de 10 perguntas para seu DNA de prazer"
- **Teste:** Usar selecao automatica de variaveis (Lasso — tecnica que
  escolhe os itens mais importantes e descarta o resto) em dados de
  treino/teste. Ver quantos itens sao necessarios para prever os 6
  fatores com pelo menos 70% de acerto.
- **Origem:** Experiencia em ciencia de dados
- **Analista:** preditivo

---

## Hipoteses eliminadas — justificativa

As 41 hipoteses originais foram reduzidas para 19. Abaixo esta o registro
do que foi removido e por que.

### Eliminadas por tentar corrigir o instrumento (1)

| ID antigo | Titulo | Motivo |
|-----------|--------|--------|
| H10 (rev.) | 8 dimensoes vs 6 | O objetivo nao e corrigir o instrumento — aceitamos os 6 fatores como sao. Tentar propor 8 fatores seria criticar a ferramenta, nao analisar os dados. |

### Eliminadas por serem obvias (7)

| ID antigo | Titulo | Motivo |
|-----------|--------|--------|
| H07 | Efeito teto reduz variacao do item | Verdade por definicao — nao precisa testar |
| H15 | Itens do mesmo fator se predizem | Isso e a propria definicao de fator |
| H31 | Fatores predizem a media geral | Obvio — fatores sao pedacos da media |
| H32 | Interpessoal e o que mais pesa na media | Obvio — e o fator com a media mais alta |
| H38 | Intelectuais pontuam baixo em reputacional | Repete H06 de outro angulo |
| H41 | Tirar respondentes suspeitos nao muda nada | Checagem de qualidade, nao hipotese |
| H05 | Coeficiente de bimodalidade > 0,555 | Muito tecnico; o interessante ficou em H04 |

### Eliminadas por serem so sobre metodo (5)

| ID antigo | Titulo | Motivo |
|-----------|--------|--------|
| H22 | Tirar itens ambiguos melhora a EFA | Um procedimento, nao uma pergunta |
| H29 | GMM e melhor que K-Means | Comparacao de ferramenta, sem valor editorial |
| H30 | Estabilidade dos clusters e baixa | Agora faz parte de H13 |
| H33 | Modelo enxuto com < 10 itens | Agora faz parte de H19 |
| H35 | Top 5 itens extremos predizem perfil | Variante tecnica de H19 |

### Eliminadas por serem detalhes muito especificos (6)

| ID antigo | Titulo | Motivo |
|-----------|--------|--------|
| H08 | Comunidade e Caridade medem a mesma coisa | Detalhe de par de itens; aparece na EFA |
| H09 | Cuidar e Familia medem a mesma coisa | Idem |
| H10 | "Ser gostado" pertence ao fator errado | Detalhe tecnico de classificacao |
| H18 | Fator Intelectual e o menos coeso | Detalhe que aparece na EFA |
| H19-antigo | "Ser gostado" e "Pertencer" no fator errado | Mesmo que H10 |
| H39 | Outliers tem perfil diferente | Grupo muito pequeno (66 pessoas) |

### Fundidas em novas hipoteses (4)

| IDs antigos | Virou | Por que |
|-------------|-------|--------|
| H06 + H25 + H40 | H11 (especialistas vs generalistas) | Faziam a mesma pergunta de angulos diferentes |
| H17 + H20 + H23 | ~~H10~~ (eliminada na fase 4c) | Todas sobre a estrutura dos 37 itens — eliminada por tentar corrigir o instrumento |
| H27 + H37 | H13 (perfil de quem busca emocao) | Ambas comparavam quartis de Emocionante |
| H12-antigo + H21 | H10 (itens avulsos se conectam?) | Ambas sobre itens avulsos formando conexoes |

---

## Metodologia

### Como as hipoteses foram refinadas

1. **Geracao original (Fase 4a):** 41 hipoteses a partir de 14 observacoes
   da analise exploratoria, numeros das Fases 2-3, objetivos de blog e
   experiencia em ciencia de dados.
2. **Revisao de artigos (Fase 4b):** Busca de literatura academica via
   Consensus.app. Temas: psicologia do prazer, estrutura do bem-estar,
   busca de sensacoes, espiritualidade, humor. Referencias-chave: Ryan e
   Deci (2001), Huta e Ryan (2010), Avsec et al. (2016), Villani et al.
   (2019), Zuckerman (2010), Joshanloo (2016), Pearce et al. (2020),
   Pancheva et al. (2020).
3. **Filtragem (Fase 4b):** Tres filtros aplicados:
   - **Obvio:** removido se a resposta ja e conhecida antes de testar
   - **So metodo:** removido se testa uma ferramenta em vez de gerar
     uma descoberta
   - **Muito especifico:** removido se e um detalhe tecnico que aparece
     naturalmente durante a analise
4. **Fusao:** Hipoteses que faziam a mesma pergunta de angulos diferentes
   foram combinadas em uma so, mais forte.

### Prioridade

Todas as 19 hipoteses restantes sao de alta prioridade — as de media e
baixa foram eliminadas ou absorvidas durante o refinamento.

### Quem executa cada uma

Cada hipotese esta marcada com o analista especialista que vai executa-la
nas Fases 5-6:

- **distribucional** — como as respostas se distribuem
- **relacional** — correlacoes e associacoes entre itens/fatores
- **estrutural** — como os itens se organizam em fatores (EFA/PCA)
- **segmentacao** — agrupamento de pessoas por perfil
- **preditivo** — o que prediz o que
- **comparativo** — diferencas entre grupos

### Viabilidade

Todas as 19 hipoteses funcionam com os dados que temos. Nenhuma precisa de
dados demograficos ou externos. As comparacoes entre grupos usam grupos
criados a partir dos proprios dados (quartis, clusters, divisoes por
diversidade).

---

## De-para: IDs antigos e novos

| ID novo | ID(s) antigo(s) | Titulo curto |
|---------|-----------------|--------------|
| H01 | H01 | Rir e o mais universal |
| H02 | H02 | Conexao + aprendizado no topo |
| H03 | H03 | Emocionante e o mais rejeitado |
| H04 | H04 + H05 | Espiritualidade divide |
| H05 | H11 | Prazeres incompativeis |
| H06 | H13 | Intelectual e reputacional sao independentes |
| H07 | H14 | Superfator "quem cuida" |
| H08 | H16 | Sexo: mais emocao que sensacao |
| H09 | H34 | Amor prediz conexao |
| ~~H10~~ | ~~H17 + H20 + H23~~ | ~~8 dimensoes vs 6~~ (eliminada — nao corrigir instrumento) |
| H10 | H21 + H12-antigo | Itens avulsos se conectam? |
| H11 | H06-antigo + H25 + H40 | Especialistas vs generalistas |
| H12 | H24 + H30 | Perfis sao um espectro |
| H13 | H27 + H37 | Perfil de quem busca emocao |
| H14 | H28 | Grupo espiritual |
| H15 | H26 | Perfil puramente intelectual |
| H16 | H36 | Adrenalina vs serenidade |
| H17 | H31 + H32 | Maior motor do prazer geral |
| H18 | H33 + H35 | Versao curta do instrumento |

---

*Revisado de 41 para 18 hipoteses apos revisao de literatura e refinamento.*
*Fase 4b — revisao informada por artigos academicos.*
*Fase 4c — H10-antigo (8 dimensoes vs 6) eliminada por tentar corrigir o instrumento;
H11-antigo reformulada como H10 (explorar itens avulsos de forma conservadora).*
