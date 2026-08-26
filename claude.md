# CLAUDE.md — Análise Sources of Pleasure (Fase Alfa)

## O que é este projeto

Uma pipeline de análise de dados orientada a perguntas e hipóteses para a ferramenta
"Sources of Pleasure" (ClearerThinking.org, construída no GuidedTrack). A pipeline
funciona como um time virtual de analistas especializados. A especificação completa
está no `PRD.md` — leia antes de fazer qualquer coisa.

Esta é a **fase alfa**: um único dataset, construído do início ao fim junto com o
usuário. A arquitetura deve permanecer limpa o suficiente para virar um sistema
reutilizável depois (fase beta): código genérico em `src/`, configuração específica
da ferramenta em `config/`.

---

## REGRA ABSOLUTA — SOMENTE DADOS REAIS

- **Nunca** gerar, simular, inventar ou preencher dados.
- **Nunca** criar dados de exemplo, mock, dummy ou sintéticos — nem para testes.
- Trabalhar **exclusivamente** com o CSV fornecido pelo usuário (`data/raw/`).
- **Nunca** imputar valores ausentes sem autorização explícita do usuário.
- **Nunca** inventar resultados estatísticos. Todo número relatado deve vir da
  execução real de código sobre os dados reais.
- Se um dado necessário não existir: **pare e pergunte**. Não estime.
- Se uma análise não for possível com os dados reais, diga isso claramente em vez
  de produzir um resultado que apenas pareça plausível.
- **Nunca** escrever resultados fixos ("hardcoded") em relatórios. Relatórios são
  gerados a partir de saídas computadas.

## REGRA ABSOLUTA — PRIVACIDADE (PII)

O CSV bruto contém dados pessoais reais: endereços de e-mail, telefone/Skype e
anotações de disponibilidade de horário.

- A Fase 1 (limpeza) **deve** remover todas as colunas de PII antes de qualquer
  análise. Colunas de PII conhecidas (lista não exaustiva): `theirEmail`,
  `userEmail`, `theirEmailLower`, `theirEmailCleaned`, `contactInformation`,
  `convenientTimes`, e qualquer coluna cujo conteúdo seja e-mail ou contato.
  Varra o dataset em busca de outras.
- Nunca imprimir, logar ou incluir e-mail ou contato em nenhum output, relatório,
  figura, saída de terminal ou commit.
- `data/` fica no `.gitignore`. Nunca commitar arquivos de dados.

## REGRAS DE TRABALHO — como trabalhamos juntos

1. **Fase por fase, nunca tudo de uma vez.** A pipeline tem 10 fases (0–9, ver
   PRD.md). Execute exatamente uma fase (ou uma etapa dentro de uma fase) por vez.
2. **Checkpoint do usuário após cada fase.** Apresente um resumo dos resultados e
   **pare, aguardando aprovação explícita** antes de iniciar a próxima fase.
   Nunca pule etapas.
3. **Pergunte antes de começar.** Antes de iniciar qualquer fase, exponha o plano
   brevemente e pergunte se o usuário quer ajustes.
4. **Ensine enquanto executa.** O objetivo do usuário inclui aprendizado. Ao rodar
   uma análise, explique em linguagem simples o que a técnica faz, por que foi
   escolhida e como ler o resultado. Seja conciso, mas nunca pule a explicação.
5. **Idiomas.** A conversa acontece em português (pt-BR). Porém, **todos os
   entregáveis (código, relatórios, figuras, banco de insights) são em inglês** —
   decisão do usuário para esta fase.
6. **Pergunta antes da técnica.** Nunca aplique uma técnica estatística sem uma
   pergunta/hipótese nomeada que a motive (exceto Fases 0–3, que são exploratórias
   por natureza). Toda análise das Fases 5–6 deve referenciar um ID de hipótese
   (H01, H02, ...).
7. **Critique a metodologia quando necessário.** Se um passo solicitado for
   estatisticamente inadequado para este dataset, diga isso e proponha alternativa.
   Não obedeça em silêncio, nem desvie em silêncio — discuta antes.
8. **Reprodutibilidade.** Toda figura e todo número em um relatório deve ser
   regenerável rodando o script correspondente em `scripts/`. Fixe seeds
   aleatórias. Faça commit no git ao fim de cada fase aprovada.

## FATOS SOBRE OS DADOS — verificados antes do início

- Arquivo: `data/raw/sources-of-pleasure.csv`
- ~11.718 linhas × 202 colunas. Separador: **ponto e vírgula (`;`)**. Formato
  decimal **europeu/corrompido em partes** (vírgula decimal, notação científica
  quebrada como `3,89E+16` e `9.999.999.999.999.990`).
- **Não confie em nenhuma coluna derivada/calculada** (`sop_*`, `*Mean0to10`,
  `*Percentile`, `*StdDev`, `factor*`, `zscore`, etc.). Elas foram corrompidas
  pela conversão de locale. **Recalcule tudo a partir dos 37 itens brutos.**
- Os 37 itens analíticos são as colunas `p_*` (`p_seeingBeauty` ...
  `p_supportFamily`), escala Likert de 7 pontos: **-3 (Totally disagree) a
  +3 (Totally agree)**.
- A ferramenta agrupa os itens em 6 fatores: interpersonal, thrilling, noble,
  reputational, sensorial, intellectual. O mapeamento item→fator deve ser extraído
  do código-fonte GuidedTrack (`code_gt_prazer.txt`) na Fase 0 e armazenado em
  `config/instrument.yaml`. Se o mapeamento for ambíguo, pergunte ao usuário.
- A maioria das 202 colunas é lixo de processo (internals da barra de progresso,
  MailChimp, parâmetros UTM, variáveis temporárias). Apenas ~40 colunas importam.
- **Não há variáveis demográficas** (idade, sexo, país). Comparações entre grupos
  ficam limitadas a grupos derivados (ex.: clusters, status de conclusão, período
  temporal). Limitação conhecida — registre, não contorne inventando grupos.
- Muitas linhas são execuções incompletas (usuários que abandonaram no meio).
  **Critério de completude (decidido com o usuário):** manter **somente** linhas
  com todos os 37 itens `p_*` respondidos. Quem não completou todas as 37
  perguntas é descartado. Exercícios de reflexão e email são opcionais por
  design e sua ausência não exclui a linha.

## GUARDRAILS ESTATÍSTICOS

- Com N ≈ 11 mil, quase tudo dá "estatisticamente significativo". P-valores
  sozinhos não significam nada aqui. **Sempre reporte tamanhos de efeito**
  (r, d de Cohen, η², R², silhouette, etc.) e julgue a relevância substantiva,
  não apenas a significância.
- Quando muitas hipóteses forem testadas (Fases 5–6), aplique controle de
  comparações múltiplas (FDR de Benjamini-Hochberg por padrão) e declare isso
  nos relatórios.
- Verifique premissas antes de testes paramétricos; use alternativas
  robustas/não-paramétricas quando violadas, e documente a decisão.
- Itens Likert são ordinais. Tratá-los como intervalares é aceitável e
  convencional para escalas de 7 pontos, mas declare essa premissa uma vez na
  Fase 2 e prefira Spearman onde as distribuições forem muito assimétricas.
- Soluções de cluster devem ser validadas (estabilidade, silhouette e um teste
  de sanidade de interpretabilidade) antes de qualquer cluster ser reportado
  como um "tipo de pessoa".
- Correlação ≠ predição ≠ causalidade. Estes são dados transversais de
  autorrelato: **nenhuma afirmação causal, nunca**. Use linguagem como
  "está associado a".

## ARQUITETURA

```
data/raw/        CSV original — SOMENTE LEITURA, nunca modificado, no .gitignore
data/processed/  dados limpos e anonimizados, gerados pela Fase 1
config/          instrument.yaml — tudo que é específico desta ferramenta
src/             funções genéricas e reutilizáveis (cleaning, descriptive, eda,
                 analysts/{relational,comparative,predictive,structural,
                 segmentation,distributional}.py, integrator, viz)
scripts/         um runner por fase (phase1_cleaning.py, ...)
outputs/reports/ relatório Markdown por fase e por hipótese
outputs/figures/ PNGs finais
outputs/insights/insight_bank.md  ← produto final
```

- Lógica genérica vai em `src/` e lê tudo que é específico da ferramenta de
  `config/instrument.yaml`. Nunca fixe nomes de itens, limites de escala ou
  mapeamentos de fatores dentro de `src/`.
- `src/viz.py` centraliza o estilo de gráfico inspirado na Statista (fonte única
  de verdade para tipografia, cores, títulos-como-descoberta e linha de fonte).
- Python + pandas/numpy/scipy/statsmodels/scikit-learn/matplotlib. Use ambiente
  virtual; fixe dependências em `requirements.txt`.

## DEFINIÇÃO DE PRONTO (por fase)

Uma fase só está completa quando:
1. Seu script roda do início ao fim sem erros sobre os dados reais.
2. Seu relatório Markdown existe em `outputs/reports/`.
3. O usuário revisou o resumo e aprovou explicitamente.
4. O trabalho foi commitado no git.
