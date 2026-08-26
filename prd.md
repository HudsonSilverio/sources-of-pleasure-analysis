# PRD — Sources of Pleasure: Pipeline de Análise Orientada a Perguntas (Alfa)

## 1. Propósito

Construir, fase por fase e junto com o usuário, uma pipeline profissional de análise
para o dataset "Sources of Pleasure", funcionando como um **time virtual de analistas
especializados**. A pipeline é orientada a hipóteses: as técnicas são escolhidas
porque uma pergunta as exige, nunca o contrário.

**Objetivos (alfa):**
- G1 — Aprendizado: o usuário constrói e entende cada passo.
- G2 — Insights publicáveis: produzir descobertas interessantes, bem evidenciadas e
  visualmente polidas sobre de onde as pessoas tiram prazer (comunicação estilo
  Statista).

**Não-objetivos (alfa):**
- Avaliar ou corrigir o instrumento em si (nenhuma crítica psicométrica como
  objetivo; a análise estrutural serve ao insight, não à validação do teste).
- Afirmações causais de qualquer tipo.
- Automação. Toda fase é executada manualmente com checkpoints do usuário
  (automação é a fase beta).

**Princípio central:**
Entender → Limpar → Descrever → Explorar → Perguntar → Classificar → Testar →
Integrar → Gerar insights → Visualizar → Comunicar.

## 2. A ferramenta e o dataset

- **Ferramenta:** "Your Greatest Sources of Pleasure" (ClearerThinking.org,
  GuidedTrack). 37 afirmações, cada uma avaliada em escala Likert de 7 pontos:
  -3 Totally disagree ... +3 Totally agree. Os itens medem quanto prazer a pessoa
  tira de 37 fontes (beleza, competição, imaginação, natureza, sexo, ajudar,
  aprender, ...).
- **Fatores:** o instrumento agrega os itens em 6 fatores — interpersonal,
  thrilling, noble, reputational, sensorial, intellectual.
- **Dataset:** `data/raw/sources-of-pleasure.csv` — ~11.718 linhas × 202 colunas,
  separado por ponto e vírgula, com formatação de locale corrompida nas colunas
  derivadas.
- **Código-fonte:** `code_gt_prazer.txt` (programa GuidedTrack) — a fonte da
  verdade sobre o que cada variável significa e como os fatores são compostos.
- Ver "FATOS SOBRE OS DADOS" no CLAUDE.md para detalhes estruturais verificados
  e regras duras.

## 3. Papéis

| Papel | Responsabilidade |
|---|---|
| Usuário | Product owner e revisor. Aprova cada fase. Conversa em pt-BR. |
| Claude Code | Constrói e executa cada fase, explica didaticamente, para nos checkpoints. |
| Analistas especialistas | Personas implementadas como módulos em `src/analysts/`. Cada um recebe apenas hipóteses da sua categoria. |
| Integrador sênior | Cruza todos os relatórios dos analistas e produz insights validados. |
| Especialista em visualização | Transforma insights validados em gráficos estilo Statista. Nunca inventa insights. |

## 4. Fases

Toda fase termina com: um script em `scripts/`, um relatório em `outputs/reports/`,
um checkpoint do usuário e um commit no git. Nunca inicie a fase N+1 sem aprovação
da fase N.

---

### Fase 0 — Entendimento da ferramenta
**Objetivo:** saber exatamente o que cada variável relevante significa antes de
tocar nos dados.

Tarefas:
1. Ler `code_gt_prazer.txt` e extrair: os 37 itens (nome da variável, texto
   completo da pergunta, rótulo curto), a escala de resposta, o mapeamento
   item→fator e o fluxo do assessment (ranking do top 5, exercícios de reflexão).
2. Construir `config/instrument.yaml` contendo: lista de itens (nome, rótulo,
   texto da pergunta, fator), definição da escala (mín -3, máx +3, rótulos),
   definição dos fatores, lista de colunas PII, padrões de colunas-lixo a
   descartar e notas de locale/formato.
3. Escrever `outputs/reports/phase0_instrument.md`: o que a ferramenta mede, quem
   são os respondentes (visitantes autosselecionados do ClearerThinking — anotar
   o viés de seleção) e qualquer ambiguidade encontrada (pedir ao usuário para
   resolver).

**Pronto quando:** o usuário confirma que o yaml descreve corretamente o
instrumento.

---

### Fase 1 — Limpeza e anonimização
**Objetivo:** produzir um dataset confiável, anonimizado e pronto para análise.

Tarefas:
1. Carregar o CSV bruto (sep=';', encoding correto). Nunca modificar `data/raw/`.
2. **Remover as colunas de PII primeiro** (conforme config), depois remover as
   colunas-lixo de processo.
3. Converter os 37 itens `p_*` para numérico; validar que todo valor está em
   {-3..+3} ou ausente. Reportar qualquer anomalia em vez de coagir
   silenciosamente.
4. Recalcular os scores de fator a partir dos itens brutos usando o mapeamento do
   yaml (ignorar todas as colunas derivadas do CSV — estão corrompidas).
5. **Critério de completude (decidido com o usuário):** manter **somente** as
   linhas em que todos os 37 itens `p_*` foram respondidos (nenhum valor
   ausente). Usuários que abandonaram a ferramenta no meio são descartados.
   Os exercícios de reflexão e o email são opcionais por design — sua ausência
   não exclui a linha. Reportar quantas linhas sobrevivem e o que se perde.
6. Deduplicar se necessário (mesmo Run/User); discutir a regra com o usuário.
7. Salvar `data/processed/clean.csv` (ou parquet) + relatório de limpeza: linhas
   que entraram, linhas que saíram, colunas removidas e por quê, decisões tomadas.

**Pronto quando:** o usuário aprova as decisões de limpeza e o N final.

---

### Fase 2 — Análise descritiva
**Objetivo:** descrever o comportamento de cada variável analítica.

Para cada um dos 37 itens e dos 6 scores de fator recalculados:
média, mediana, moda, DP, variância, quartis/IQR, mín/máx, frequências por opção
de resposta, taxa de missing, assimetria (skewness), curtose, flags de outliers,
efeitos de piso/teto.

Entregáveis: `outputs/reports/phase2_descriptive.md` com tabelas-resumo e a
leitura principal (ex.: quais prazeres ranqueiam mais alto/mais baixo no geral,
quais itens são mais polarizadores). Gráficos simples de distribuição vão para
`outputs/figures/exploratory/` (são gráficos de trabalho, não os finais estilo
Statista).

**Pronto quando:** o usuário revisou o quadro descritivo e aprovou.

---

### Fase 3 — Análise exploratória (EDA)
**Objetivo:** caçar padrões, relações, estruturas e anomalias que gerarão
hipóteses.

Tarefas: histogramas/densidade, boxplots, matriz de correlação + heatmap
(Spearman por padrão), pares de itens mais fortes/mais fracos/negativos,
redundâncias candidatas, espiada rápida em dimensionalidade (scree de PCA /
clustering de correlações) estritamente como exploração, agrupamentos naturais
candidatos, anomalias que valem investigação.

Entregável: `outputs/reports/phase3_eda.md` escrito como uma lista de
**observações**, cada uma formulada como "Observation O-nn: ... → possível
pergunta". Nenhuma conclusão nesta fase — apenas pistas.

**Pronto quando:** o usuário concorda que a lista de observações é rica o
suficiente para gerar hipóteses.

---

### Fase 4 — Registro de hipóteses
**Objetivo:** transformar observações em uma lista explícita de perguntas
testáveis.

Tarefas:
1. Junto com o usuário, escrever hipóteses derivadas das observações da Fase 3
   (mais qualquer pergunta que o usuário traga por conta própria).
2. Registrar cada uma em `outputs/reports/phase4_hypotheses.md` como:
   `ID | Pergunta | Origem (O-nn ou usuário) | Categoria | Prioridade`
3. Categorias (roteamento): RELATIONAL, COMPARATIVE, PREDICTIVE, STRUCTURAL,
   SEGMENTATION, DISTRIBUTIONAL.
4. Checar a viabilidade de cada hipótese contra os dados (é respondível com o
   que temos?). Marcar as não respondíveis como "estacionadas", com o motivo.

Notas para este dataset: COMPARATIVE não tem grupos demográficos — comparações
só podem usar grupos derivados (ex.: clusters da SEGMENTATION, coortes de
completude, períodos temporais). PREDICTIVE deve nomear um alvo com sentido
(ex.: os itens do fator X predizem a média geral de prazer, ou o pertencimento
a um cluster) — associação ≠ predição ≠ causa.

**Pronto quando:** o usuário aprova o registro e as prioridades.

---

### Fases 5–6 — Analistas especialistas executam e reportam
**Objetivo:** responder cada hipótese aprovada com a técnica certa, com rigor.

Cada módulo de analista (`src/analysts/*.py`) recebe apenas as hipóteses da sua
categoria e:
1. Escolhe a técnica e justifica.
2. Verifica premissas (normalidade, homogeneidade, KMO/Bartlett para estrutural,
   etc.); troca por alternativas robustas/não-paramétricas quando violadas.
3. Executa sobre os dados processados reais com seeds fixas.
4. Aplica correção FDR sobre a família de testes.
5. Escreve um relatório por hipótese: `outputs/reports/H{nn}_{categoria}.md`.

Técnicas típicas (escolher por pergunta, nunca aplicar em bloco):
- RELATIONAL: Pearson/Spearman, correlação parcial.
- COMPARATIVE: teste t/Mann-Whitney, ANOVA/Kruskal-Wallis + post-hoc, com
  tamanhos de efeito.
- PREDICTIVE: regressão linear/múltipla, modelos regularizados, split honesto de
  treino/teste, reportar R²/RMSE — e distinguir explicitamente associação de
  capacidade preditiva.
- STRUCTURAL: KMO, Bartlett, EFA (com rotação) / PCA quando apropriado; comparar
  a estrutura empírica com os 6 fatores do instrumento como *insight*, não como
  veredito.
- SEGMENTATION: K-Means / hierárquico / GMM; escolher k via cotovelo+silhouette;
  validar estabilidade (bootstrap/subamostra); perfilar os clusters.
- DISTRIBUTIONAL: análises de forma, testes de normalidade (com a ressalva de que
  neste N eles sempre rejeitam — enfatizar a magnitude do desvio), checagens de
  polarização/bimodalidade.

**Template de relatório do analista (obrigatório):**
```
# H{nn} — {pergunta}
- Categoria / Analista:
- Técnica + justificativa:
- Premissas verificadas (e resultados):
- Resultado (estatísticas, tamanho de efeito, IC, p corrigido):
- Veredito: sustentada / não sustentada / inconclusiva
- Interpretação em linguagem simples:
- Relevância substantiva (o efeito é grande o suficiente para importar?):
- Limitações e ressalvas:
```

**Pronto quando:** toda hipótese priorizada tem um relatório aprovado. Executar
em lotes por categoria, com checkpoint após cada lote.

---

### Fase 7 — Integrador sênior
**Objetivo:** cruzar todos os relatórios e separar descobertas reais de ruído.

Tarefas: comparar resultados entre analistas; encontrar convergências (múltiplos
métodos apontando na mesma direção), contradições (investigar e resolver ou
sinalizar), resultados fortes vs. fracos; eliminar conclusões mal sustentadas;
revelar descobertas que só aparecem quando as análises são combinadas (ex.:
correlação + EFA + clustering contando uma história coerente).

Entregável: `outputs/reports/phase7_integration.md` — lista de insights
candidatos com a trilha de evidências (IDs de hipóteses) e um grau de força por
candidato.

**Pronto quando:** o usuário aprova os insights candidatos.

---

### Fase 8 — Banco de Insights
**Objetivo:** o produto final de conhecimento, com evidência graduada.

`outputs/insights/insight_bank.md`, uma entrada por insight validado:
```
## I{nn} — {descoberta em uma frase, escrita como manchete}
- Pergunta(s) de origem: H..
- Evidências: (relatórios, estatísticas, tamanhos de efeito)
- Métricas principais:
- Força da evidência: forte / moderada / sugestiva
- Confiança e limitações:
- Contexto / interpretação:
```
Só entram insights aprovados pelo integrador. Toda afirmação rastreia de volta a
um relatório.

**Pronto quando:** o usuário aprova o banco.

---

### Fase 9 — Data storytelling e visualização
**Objetivo:** comunicar os insights visualmente, no estilo Statista.

Regras:
- O especialista em visualização recebe os insights do banco e **nunca inventa
  descobertas**.
- Um gráfico = uma mensagem. Títulos são descobertas ("Loving and being loved is
  the #1 source of pleasure"), não descrições ("Mean scores by item").
- Escolher o tipo de gráfico por insight (barras ranqueadas, barras divergentes
  de Likert, heatmap, perfis de cluster, dumbbell/slope quando couber).
  Hierarquia clara, rótulos diretos em vez de legendas quando possível, linha de
  fonte ("Source: Sources of Pleasure assessment, ClearerThinking.org — N = ...").
- Estilo centralizado em `src/viz.py`; exportar PNGs em alta resolução para
  `outputs/figures/final/`.
- Opcionalmente, montar um documento narrativo curto ordenando os gráficos como
  uma história.

**Pronto quando:** o usuário aprova as figuras finais e a narrativa.

## 5. Limitações conhecidas (declarar honestamente nos outputs)

- Amostra online autosselecionada (audiência do ClearerThinking) — não
  representativa da população.
- Autorrelato, transversal — apenas associações, nenhuma linguagem causal.
- Sem demográficos — comparações de grupo limitadas a grupos derivados.
- Colunas derivadas do export bruto estão corrompidas — tudo recalculado a partir
  dos itens.
- Premissa Likert-como-intervalar, declarada uma vez na Fase 2.

## 6. Sementes da beta (não construir agora, não quebrar)

- Tudo que é específico do instrumento vive em `config/instrument.yaml`.
- `src/` permanece genérico e orientado por configuração.
- Os runners de fase compartilham um padrão comum para poderem ser orquestrados
  depois.

## 7. Nota de idioma

A conversa entre usuário e Claude Code acontece em português (pt-BR). Este PRD e o
CLAUDE.md estão em português. Porém, **todos os entregáveis do projeto — código,
comentários, relatórios, figuras e o banco de insights — são escritos em inglês**,
por decisão do usuário para a fase alfa.
