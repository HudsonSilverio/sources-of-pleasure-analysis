# Banco de Insights — Sources of Pleasure

**Data de geracao:** 2026-08-28 11:07
**Dataset:** Sources of Pleasure (ClearerThinking.org)
**Respondentes:** N = 6,587
**Insights validados:** 8

| Forca | Quantidade |
|-------|------------|
| Forte | 4 |
| Moderada | 3 |
| Sugestiva | 1 |

## Indice

| ID | Manchete | Forca | Hipoteses |
|-----|----------|-------|-----------|
| I01 | Rir e o prazer mais universal — e as pessoas concordam mais do que divergem | forte | H01, H02, H12, H11 |
| I02 | Espiritualidade e o grande divisor — nenhum outro item racha a amostra assim | forte | H04, H14 |
| I03 | Emocao forte e o prazer que a maioria rejeita — e quem busca e diferente de todos | forte | H03, H13 |
| I04 | O paradoxo do thrilling: o prazer mais rejeitado e o que mais diferencia as pessoas | forte | H03, H17, H13 |
| I05 | Quem cuida de pessoas tambem cuida de causas — existe um superfator 'cuidador' | moderada | H07, H14 |
| I06 | Gostar de pensar nao tem nada a ver com querer status — as duas dimensoes sao independentes | moderada | H06, H05 |
| I07 | Nao existem 'tipos de pessoa' no prazer — o que parecem grupos sao apenas regioes do espectro | moderada | H15, H12 |
| I08 | Generalistas reportam mais prazer — mas cuidado, parte do efeito e mecanica | sugestiva | H11 |

---

> **Como ler este banco:** cada insight foi validado pelo integrador senior (Fase 7) e rastreia de volta a pelo menos uma hipotese testada na Fase 5. A forca reflete a convergencia de evidencias e o tamanho dos efeitos. Ressalvas estao sempre presentes — nenhuma afirmacao causal e feita. Todos os numeros vem de dados reais (N = 6.587).

---

## I01 — Rir e o prazer mais universal — e as pessoas concordam mais do que divergem

- **Pergunta(s) de origem:**
  - H01 (distributional): Rir e a fonte de prazer mais universal?
  - H02 (distributional): Conexao, amor e aprendizado dominam o ranking?
  - H12 (segmentation): Perfis de prazer sao um espectro ou existem tipos reais?
  - H11 (segmentation): Somos especialistas ou generalistas do prazer?

- **Evidencias:**
  - H01 (distribucional): Laughing / humor lidera o ranking de net_agreement com 77.1% (IC 95%: 76.0–78.1), separado do segundo colocado (Deep personal connection, 74.5%) sem sobreposicao de intervalos.
  - H02 (distribucional): Mesmo resultado por top2_pct — humor lidera com 78.1% (IC 95%: 77.0–79.1). Os 5 primeiros sao iguais nas duas metricas.
  - H12 (segmentacao): Nenhum metodo de clustering (K-Means, hierarquico, GMM, k=2-8) encontrou tipos claros de prazer. Melhor silhouette = 0.228 (abaixo do limiar 0.25). Prazer e um espectro, nao categorias.
  - H11 (segmentacao): Generalistas (perfil equilibrado) reportam mais prazer geral que especialistas (d = 1.20, p < 0.001). Media generalistas = 1.21 vs especialistas = 0.58.

- **Metricas principais:**
  - Net agreement do item lider (humor): 77.1%
  - Top 5 itens universais: humor, conexao, pensar, aprender, tempo de qualidade
  - Silhouette maximo (clustering): 0.228 — sem tipos claros
  - Cohen's d generalistas vs especialistas: 1.20 (efeito grande)

- **Forca da evidencia:** forte

- **Confianca e limitacoes:**
  - H01/H02 medem o topo do ranking, nao consenso absoluto. A convergencia e sobre os prazeres mais populares, nao sobre todos os 37 itens.
  - H11 e parcialmente tautologico: quem concorda com tudo (media alta) automaticamente tem perfil equilibrado (entropia alta). Correlacao entropia × media geral: rho = 0.643. O efeito e real mas parcialmente mecanico.
  - Amostra de conveniencia (ClearerThinking) — o ranking pode nao refletir a populacao geral.

- **Contexto e interpretacao:**
  As pessoas convergem sobre as fontes de prazer mais valorizadas: rir, conectar-se, pensar e aprender aparecem no topo por qualquer metrica. Nao existem 'tipos de pessoa' com preferencias radicalmente diferentes — o prazer e mais um espectro continuo do que categorias separadas. Quem distribui seu prazer entre mais fontes reporta mais satisfacao geral, embora parte desse efeito seja mecanica.

---

## I02 — Espiritualidade e o grande divisor — nenhum outro item racha a amostra assim

- **Pergunta(s) de origem:**
  - H04 (distributional): Espiritualidade divide as pessoas em dois grupos?
  - H14 (segmentation): Quem gosta de espiritualidade e uma tribo a parte?

- **Evidencias:**
  - H04 (distribucional): Modelo de mistura gaussiana (GMM) confirma bimodalidade no item p_spiritual. BIC com 2 curvas (25.973) muito melhor que 1 curva (28.087), diferenca = 2.114 (> 10 = evidencia forte). Dois grupos: um centrado em -2.6 (64.4%, rejeitam) e outro em +0.9 (35.6%, concordam). Separacao = 3.4 pontos na escala.
  - H14 (segmentacao): Quem pontua alto em espiritualidade (>= 1, N = 2.469) difere em TODOS os 6 fatores comparado com quem pontua baixo (<= -1, N = 3.180). Maior efeito: noble (d = 1.31). Todos os p_corrigidos < 0.001.
  - Cruzamento CROSS-16 (fase 7): 100% dos que pontuam >= 1 no corte fixo tambem estao no grupo alto do GMM. Os dois metodos convergem.

- **Metricas principais:**
  - BIC diff (1 vs 2 componentes): 2.114 (evidencia forte de bimodalidade)
  - Grupo espiritual: 35.6% da amostra (centrado em +0.9)
  - Grupo nao-espiritual: 64.4% (centrado em -2.6)
  - Separacao entre grupos: 3.4 pontos
  - Maior Cohen's d entre grupos: 1.31 (noble)

- **Forca da evidencia:** forte

- **Confianca e limitacoes:**
  - Amostra viesada: ClearerThinking atrai perfil secular/analitico. A proporcao 65/35 pode nao refletir a populacao geral.
  - Item discreto (7 valores), nao continuo — GMM e uma aproximacao.
  - Pontos de corte do H14 (>= 1 e <= -1) sao arbitrarios.

- **Contexto e interpretacao:**
  Espiritualidade e o unico item que divide a amostra em dois grupos nitidos: a maioria rejeita fortemente e uma minoria significativa abraca. Quem valoriza espiritualidade tem um perfil de prazer completamente diferente — pontua mais alto em todas as dimensoes, especialmente no cuidado com causas e pessoas (noble). Nenhum outro item ou fator produz uma divisao tao limpa.

---

## I03 — Emocao forte e o prazer que a maioria rejeita — e quem busca e diferente de todos

- **Pergunta(s) de origem:**
  - H03 (distributional): Buscar emocao forte e a categoria mais rejeitada?
  - H13 (segmentation): Quem busca emocao forte tem perfil completamente diferente?

- **Evidencias:**
  - H03 (distribucional): O fator thrilling e o unico com mediana negativa (-0.33). O segundo mais baixo (reputational) tem mediana = 0.50. Teste Wilcoxon: W = 3.101.829, p < 0.001, efeito grande (r reportado como inf devido a precisao do float — ver BUG-01).
  - H13 (segmentacao): Top 25% vs Bottom 25% do fator thrilling diferem em 5 de 5 outros fatores. Maior efeito: reputacional (d = 0.887). O perfil de prazer dos thrill-seekers e realmente distinto.
  - Ranking dos 6 fatores por mediana: thrilling (-0.33) < reputational (0.50) < noble (0.67) < sensorial (1.25) < intellectual (1.80) < interpersonal (2.00).

- **Metricas principais:**
  - Mediana do fator thrilling: -0.33 (unico negativo)
  - Gap para o segundo mais baixo: 0.83 pontos
  - Cohen's d entre Q1 e Q4 do thrilling: ate 0.887 (reputacional)
  - Fatores onde thrill-seekers diferem: 5 de 5

- **Forca da evidencia:** forte

- **Confianca e limitacoes:**
  - BUG-01: tamanho de efeito reportado como r = inf no H03 (o efeito e grande, mas o numero exato nao e interpretavel).
  - O efeito pode ser amplificado pela amostra (publico analitico/intelectual tende a rejeitar risco).
  - Quartis sao uma divisao arbitraria (H13).

- **Contexto e interpretacao:**
  A maioria das pessoas neste dataset nao gosta de emocao forte — adrenalina, risco, sustos sao os unicos prazeres com discordancia liquida. E quem busca essas sensacoes tem um perfil completamente diferente: tende a valorizar mais status, competicao e festas. Os thrill-seekers sao uma minoria com um 'paladar' de prazer diferente da maioria.

---

## I04 — O paradoxo do thrilling: o prazer mais rejeitado e o que mais diferencia as pessoas

- **Pergunta(s) de origem:**
  - H03 (distributional): Buscar emocao forte e a categoria mais rejeitada?
  - H17 (predictive): Qual fator mais contribui pro prazer geral?
  - H13 (segmentation): Quem busca emocao forte tem perfil completamente diferente?

- **Evidencias:**
  - H03: Thrilling e o fator mais rejeitado (mediana = -0.33).
  - H17 (preditivo): Na regressao dos 6 fatores sobre o prazer geral, thrilling tem o MAIOR beta padronizado (0.354), seguido de noble (0.301) e reputational (0.287). R² total = 0.974 (mas com circularidade parcial — ver AUD-09).
  - H13: Thrill-seekers diferem em todos os outros fatores (d ate 0.887).
  - A explicacao: thrilling tem a MAIOR VARIANCIA entre os 6 fatores. As pessoas divergem muito sobre ele. Por ter muita variacao, ele 'puxa' mais a media geral — tanto pra cima (thrill-seekers) quanto pra baixo (a maioria). E o fator mais polarizador.

- **Metricas principais:**
  - Beta padronizado do thrilling: 0.354 (maior dos 6 fatores)
  - Mediana do thrilling: -0.33 (unico fator negativo)
  - R² total da regressao: 0.974 (circularidade parcial)
  - Cohen's d thrill-seekers vs demais: ate 0.887

- **Forca da evidencia:** forte

- **Confianca e limitacoes:**
  - AUD-09: R² = 0.974 e inflado por circularidade (fatores sao subconjuntos dos itens que compoem a media geral). O numero absoluto nao e uma descoberta, mas os pesos relativos (betas) sao informativos.
  - O beta alto nao significa que thrilling 'gera mais prazer'. Significa que, por ter mais variancia, ele diferencia mais quem tem prazer geral alto vs baixo.
  - Este insight so aparece quando se combinam 3 analises — nenhuma delas sozinha revela o paradoxo.

- **Contexto e interpretacao:**
  O fator mais rejeitado e, ao mesmo tempo, o que mais 'puxa' o prazer geral pra cima ou pra baixo. Isso parece paradoxo, mas a explicacao e simples: thrilling e o assunto sobre o qual as pessoas mais divergem. Quem busca adrenalina tende a gostar de tudo mais tambem; quem rejeita tende a ser mais seletivo. Thrilling nao e o 'motor' do prazer — e o termometro que mais varia.

---

## I05 — Quem cuida de pessoas tambem cuida de causas — existe um superfator 'cuidador'

- **Pergunta(s) de origem:**
  - H07 (relational): Existe um superfator 'quem cuida'?
  - H14 (segmentation): Quem gosta de espiritualidade e uma tribo a parte?

- **Evidencias:**
  - H07 (relacional): Os fatores interpersonal e noble tem correlacao forte (Spearman rho = 0.460, p < 0.001). Alpha de Cronbach como dimensao unica: 0.67 (aceitavel, acima de 0.60, mas abaixo de 0.70 = bom).
  - H14 (segmentacao): Quem pontua alto em espiritualidade pontua alto em ambos: noble (d = 1.31) e interpersonal (d = 0.47). Os dois fatores caminham juntos.

- **Metricas principais:**
  - Spearman rho (interpersonal × noble): 0.460
  - Cronbach alpha (2 fatores como dimensao unica): 0.67
  - Cohen's d noble (espirituais vs nao): 1.31
  - Cohen's d interpersonal (espirituais vs nao): 0.47

- **Forca da evidencia:** moderada

- **Confianca e limitacoes:**
  - AUD-05: Cronbach alpha = 0.67 com apenas 2 itens (fatores) e uma estimativa instavel. O limiar 'bom' e 0.70.
  - O superfator 'quem cuida' e uma hipotese exploratoria, nao um fato confirmado. Precisaria de analise fatorial confirmatoria com todos os itens dos dois fatores.
  - A correlacao 0.46 e forte mas nao fortissima — os dois fatores ainda tem variancia propria.

- **Contexto e interpretacao:**
  Pessoas que se importam com seus entes queridos (interpersonal: tempo de qualidade, pertencer, amar) tambem tendem a se importar com causas maiores (noble: caridade, comunidade, ajudar). Isso sugere uma dimensao latente de 'cuidado' que unifica os dois fatores. O grupo espiritual pontua alto em ambos, reforcando a conexao.

---

## I06 — Gostar de pensar nao tem nada a ver com querer status — as duas dimensoes sao independentes

- **Pergunta(s) de origem:**
  - H06 (relational): Mentes curiosas sao indiferentes a status?
  - H05 (relational): Alguns prazeres sao realmente incompativeis?

- **Evidencias:**
  - H06 (relacional): Teste TOST confirma que a correlacao entre intellectual e reputational e equivalente a zero (rho = 0.023, p_TOST < 0.001, faixa de equivalencia: |rho| < 0.1). Sao estatisticamente independentes.
  - H05 (relacional): No nivel dos itens, pares como criatividade × competicao (rho = -0.083) e natureza × status (rho = -0.098) sao negativos e significativos apos correcao FDR. 26 de 55 pares negativos sobreviveram.

- **Metricas principais:**
  - Spearman rho (intellectual × reputational): 0.023 (praticamente zero)
  - TOST p-valor: < 0.001 (confirmada equivalencia a zero)
  - Pares negativos significativos entre itens: 26 de 55
  - Correlacao negativa mais forte: natureza × status (rho = -0.098)

- **Forca da evidencia:** moderada

- **Confianca e limitacoes:**
  - AUD-04: Mesmo os pares 'incompativeis' do H05 tem |rho| < 0.1 — efeito negligivel na pratica. A incompatibilidade entre itens existe mas e muito sutil.
  - Independencia nao significa incompatibilidade. Pessoas podem pontuar alto em ambos — sao dimensoes que variam separadamente.

- **Contexto e interpretacao:**
  Quem busca prazer intelectual (pensar, criar, aprender) nao busca nem evita prazer reputacional (status, reconhecimento, poder). As duas coisas simplesmente nao tem relacao. Isso desafia a intuicao de que 'intelectuais desprezam status' — na verdade, sao dimensoes ortogonais (independentes, sem relacao uma com a outra).

---

## I07 — Nao existem 'tipos de pessoa' no prazer — o que parecem grupos sao apenas regioes do espectro

- **Pergunta(s) de origem:**
  - H15 (segmentation): Existe um grupo puramente intelectual?
  - H12 (segmentation): Perfis de prazer sao um espectro ou existem tipos reais?

- **Evidencias:**
  - H12 (segmentacao): Tres metodos de clustering (K-Means, hierarquico, GMM) com k de 2 a 8. Nenhum encontrou grupos claros. Melhor silhouette: 0.228 (hierarquico, k=2) — abaixo do limiar 0.25. Estabilidade bootstrap: 0.183 ± 0.039.
  - H15 (segmentacao): K-Means k=3 encontrou um cluster com N = 1.712 onde intellectual e dominante. Mas sem silhouette reportado para esse cluster.
  - Recalculo do integrador (EMER-27): silhouette do k=3 = 0.152 — pior que o melhor de H12. O 'grupo intelectual' e uma regiao do espectro recortada pelo algoritmo.

- **Metricas principais:**
  - Melhor silhouette geral: 0.228 (hierarquico k=2)
  - Silhouette do k=3 usado em H15: 0.152 (recalculado)
  - Estabilidade bootstrap: 0.183 +/- 0.039
  - Tamanho do 'cluster intelectual': 1.712 pessoas

- **Forca da evidencia:** moderada

- **Confianca e limitacoes:**
  - AUD-07: O limiar 0.25 e arbitrario — silhouette < 0.25 nao prova que grupos nao existem, apenas que estes metodos nao os encontram nestes dados.
  - AUD-08: H15 tem vies de busca — procurar um perfil especifico quase sempre encontra algo. K-Means particiona o espaco de qualquer jeito.
  - BUG-02: H15 nao reportou silhouette do cluster.

- **Contexto e interpretacao:**
  E tentador pensar que existem 'tipos de pessoa' — o intelectual, o aventureiro, o cuidador. Mas os dados nao sustentam isso. Quando algoritmos encontram 'grupos', as fronteiras sao difusas e os perfis instáveis. O prazer e um espectro continuo: as pessoas se distribuem gradualmente, sem saltos nem clusters naturais.

---

## I08 — Generalistas reportam mais prazer — mas cuidado, parte do efeito e mecanica

- **Pergunta(s) de origem:**
  - H11 (segmentation): Somos especialistas ou generalistas do prazer?

- **Evidencias:**
  - H11 (segmentacao): Divisao pela mediana da entropia de Shannon dos 6 fatores. Generalistas (N = 3.294, perfil equilibrado) tem media de prazer geral = 1.21. Especialistas (N = 3.293, perfil concentrado) = 0.58. Mann-Whitney U = 8.802.914, p < 0.001, Cohen's d = 1.20 (efeito grande).
  - Recalculo do integrador (EMER-28): correlacao entre entropia e media geral = rho = 0.643. Isso sugere tautologia parcial: quem diz 'concordo' pra tudo (media alta) automaticamente tem perfil uniforme (entropia alta).

- **Metricas principais:**
  - Cohen's d generalistas vs especialistas: 1.20 (efeito grande)
  - Media generalistas: 1.21 vs especialistas: 0.58
  - Correlacao entropia × media geral: rho = 0.643
  - Proporcao: ~50/50 (divisao pela mediana)

- **Forca da evidencia:** sugestiva

- **Confianca e limitacoes:**
  - Tautologia parcial: entropia alta e media alta estao mecanicamente correlacionadas (rho = 0.643). Parte do efeito grande (d = 1.20) e artefato dessa relacao.
  - Divisao pela mediana e arbitraria.
  - A interpretacao 'diversificar fontes de prazer gera mais satisfacao' e mais forte do que os dados suportam. O que podemos dizer: quem concorda mais com os itens de prazer tende a ter perfil mais equilibrado.
  - Dados transversais: nao sabemos se diversificar CAUSA mais prazer ou se quem ja e mais satisfeito simplesmente concorda mais com tudo.

- **Contexto e interpretacao:**
  Pessoas com perfil de prazer mais equilibrado (generalistas) reportam mais satisfacao geral do que as mais concentradas em poucas fontes (especialistas). E uma diferenca grande (d = 1.20), mas parte dela e mecanica: quem concorda mais com tudo naturalmente fica com perfil mais uniforme. O achado e real mas a interpretacao causal ('diversifique suas fontes de prazer') vai alem do que os dados permitem.

---

## Limitacoes gerais do dataset

Estas limitacoes se aplicam a **todos** os insights acima e devem ser consideradas ao interpretar qualquer achado:

1. **Amostra de conveniencia.** Os respondentes sao visitantes do ClearerThinking.org — provavelmente mais analiticos, mais escolarizados e menos religiosos que a populacao geral. Rankings e proporcoes podem mudar com outra amostra.
2. **Sem dados demograficos.** Nao ha idade, genero, pais ou renda. Nao e possivel controlar por essas variaveis nem generalizar para subgrupos.
3. **Dados transversais de autorrelato.** Um unico momento, uma unica resposta por pessoa. Nenhuma afirmacao causal e possivel. 'Associado a' nao significa 'causa'.
4. **Itens Likert de 7 pontos.** Tratados como intervalares (convencional para escalas de 7+), mas sao tecnicamente ordinais. Preferimos Spearman quando as distribuicoes sao assimetricas.
5. **N grande inflaciona significancia.** Com N ~ 6.500, quase qualquer correlacao e 'significativa'. Todos os insights acima usam tamanhos de efeito (d de Cohen, rho, R²) como criterio primario, nao p-valores.
6. **Hipoteses pos-exploracao.** As 17 hipoteses foram formuladas apos analise exploratoria dos dados (Fases 2-4), o que favorece confirmacao. A taxa de 88% de confirmacao reflete isso.

---

*Banco gerado automaticamente por `scripts/phase8_insight_bank.py`*
*Pipeline: Fases 0-8 | Dados: Sources of Pleasure (ClearerThinking.org) — N = 6,587*