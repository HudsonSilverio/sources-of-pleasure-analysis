"""
phase8_insight_bank.py — Generate the Insight Bank (Phase 8).

Reads the Phase 7 audit results and Phase 5/6 analyst results,
then compiles the final insight bank in outputs/insights/insight_bank.md.

Usage:
    python scripts/phase8_insight_bank.py
"""

import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import yaml
import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
DATA_DIR = PROJECT_ROOT / "data" / "processed"
CONFIG_DIR = PROJECT_ROOT / "config"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "insights"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
print("Carregando dados...")

audit_df = pd.read_csv(DATA_DIR / "phase7_audit.csv")
results_df = pd.read_csv(DATA_DIR / "phase56_results.csv")

with open(CONFIG_DIR / "hypotheses.yaml", "r", encoding="utf-8") as f:
    hypotheses_raw = yaml.safe_load(f)["hypotheses"]

hypotheses = {}
for hid, hdata in hypotheses_raw.items():
    hdata["id"] = hid
    hypotheses[hid] = hdata

with open(CONFIG_DIR / "instrument.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Count respondents from results interpretation
N_RESPONDENTS = 6587  # from clean.csv, verified in all phases

print(f"  {len(hypotheses)} hipoteses")
print(f"  {len(audit_df)} linhas no audit CSV")
print(f"  {len(results_df)} resultados de analistas")

# ---------------------------------------------------------------------------
# Extract candidates and audit notes
# ---------------------------------------------------------------------------
candidates = audit_df[audit_df["category"] == "candidato"].copy()
audit_notes = audit_df[audit_df["category"] == "auditoria"].copy()

print(f"  {len(candidates)} candidatos a insight")

# Build lookup: hypothesis_id -> result row
result_lookup = {}
for _, row in results_df.iterrows():
    result_lookup[row["hypothesis_id"]] = row

# Build lookup: hypothesis_id -> audit notes
audit_lookup = {}
for _, row in audit_notes.iterrows():
    hid = row["hypothesis"]
    if hid not in audit_lookup:
        audit_lookup[hid] = []
    audit_lookup[hid].append(row)

# ---------------------------------------------------------------------------
# Insight definitions (enriched from Phase 7 + analyst reports)
# ---------------------------------------------------------------------------

INSIGHTS = [
    {
        "id": "I01",
        "headline": "Rir e o prazer mais universal — e as pessoas concordam mais do que divergem",
        "hypotheses": ["H01", "H02", "H12", "H11"],
        "strength": "forte",
        "type": "convergencia",
        "evidence_detail": (
            "- H01 (distribucional): Laughing / humor lidera o ranking de "
            "net_agreement com 77.1% (IC 95%: 76.0–78.1), separado do "
            "segundo colocado (Deep personal connection, 74.5%) sem "
            "sobreposicao de intervalos.\n"
            "- H02 (distribucional): Mesmo resultado por top2_pct — "
            "humor lidera com 78.1% (IC 95%: 77.0–79.1). Os 5 primeiros "
            "sao iguais nas duas metricas.\n"
            "- H12 (segmentacao): Nenhum metodo de clustering (K-Means, "
            "hierarquico, GMM, k=2-8) encontrou tipos claros de prazer. "
            "Melhor silhouette = 0.228 (abaixo do limiar 0.25). Prazer "
            "e um espectro, nao categorias.\n"
            "- H11 (segmentacao): Generalistas (perfil equilibrado) "
            "reportam mais prazer geral que especialistas (d = 1.20, "
            "p < 0.001). Media generalistas = 1.21 vs especialistas = 0.58."
        ),
        "key_metrics": (
            "- Net agreement do item lider (humor): 77.1%\n"
            "- Top 5 itens universais: humor, conexao, pensar, aprender, tempo de qualidade\n"
            "- Silhouette maximo (clustering): 0.228 — sem tipos claros\n"
            "- Cohen's d generalistas vs especialistas: 1.20 (efeito grande)"
        ),
        "caveats": (
            "- H01/H02 medem o topo do ranking, nao consenso absoluto. "
            "A convergencia e sobre os prazeres mais populares, nao sobre "
            "todos os 37 itens.\n"
            "- H11 e parcialmente tautologico: quem concorda com tudo "
            "(media alta) automaticamente tem perfil equilibrado (entropia "
            "alta). Correlacao entropia × media geral: rho = 0.643. "
            "O efeito e real mas parcialmente mecanico.\n"
            "- Amostra de conveniencia (ClearerThinking) — o ranking pode "
            "nao refletir a populacao geral."
        ),
        "context": (
            "As pessoas convergem sobre as fontes de prazer mais "
            "valorizadas: rir, conectar-se, pensar e aprender aparecem "
            "no topo por qualquer metrica. Nao existem 'tipos de pessoa' "
            "com preferencias radicalmente diferentes — o prazer e mais "
            "um espectro continuo do que categorias separadas. Quem "
            "distribui seu prazer entre mais fontes reporta mais "
            "satisfacao geral, embora parte desse efeito seja mecanica."
        ),
    },
    {
        "id": "I02",
        "headline": "Espiritualidade e o grande divisor — nenhum outro item racha a amostra assim",
        "hypotheses": ["H04", "H14"],
        "strength": "forte",
        "type": "convergencia",
        "evidence_detail": (
            "- H04 (distribucional): Modelo de mistura gaussiana (GMM) "
            "confirma bimodalidade no item p_spiritual. BIC com 2 curvas "
            "(25.973) muito melhor que 1 curva (28.087), diferenca = 2.114 "
            "(> 10 = evidencia forte). Dois grupos: um centrado em -2.6 "
            "(64.4%, rejeitam) e outro em +0.9 (35.6%, concordam). "
            "Separacao = 3.4 pontos na escala.\n"
            "- H14 (segmentacao): Quem pontua alto em espiritualidade "
            "(>= 1, N = 2.469) difere em TODOS os 6 fatores comparado "
            "com quem pontua baixo (<= -1, N = 3.180). Maior efeito: "
            "noble (d = 1.31). Todos os p_corrigidos < 0.001.\n"
            "- Cruzamento CROSS-16 (fase 7): 100% dos que pontuam >= 1 "
            "no corte fixo tambem estao no grupo alto do GMM. Os dois "
            "metodos convergem."
        ),
        "key_metrics": (
            "- BIC diff (1 vs 2 componentes): 2.114 (evidencia forte de bimodalidade)\n"
            "- Grupo espiritual: 35.6% da amostra (centrado em +0.9)\n"
            "- Grupo nao-espiritual: 64.4% (centrado em -2.6)\n"
            "- Separacao entre grupos: 3.4 pontos\n"
            "- Maior Cohen's d entre grupos: 1.31 (noble)"
        ),
        "caveats": (
            "- Amostra viesada: ClearerThinking atrai perfil "
            "secular/analitico. A proporcao 65/35 pode nao refletir a "
            "populacao geral.\n"
            "- Item discreto (7 valores), nao continuo — GMM e uma "
            "aproximacao.\n"
            "- Pontos de corte do H14 (>= 1 e <= -1) sao arbitrarios."
        ),
        "context": (
            "Espiritualidade e o unico item que divide a amostra em dois "
            "grupos nitidos: a maioria rejeita fortemente e uma minoria "
            "significativa abraca. Quem valoriza espiritualidade tem um "
            "perfil de prazer completamente diferente — pontua mais alto "
            "em todas as dimensoes, especialmente no cuidado com causas "
            "e pessoas (noble). Nenhum outro item ou fator produz uma "
            "divisao tao limpa."
        ),
    },
    {
        "id": "I03",
        "headline": "Emocao forte e o prazer que a maioria rejeita — e quem busca e diferente de todos",
        "hypotheses": ["H03", "H13"],
        "strength": "forte",
        "type": "convergencia",
        "evidence_detail": (
            "- H03 (distribucional): O fator thrilling e o unico com "
            "mediana negativa (-0.33). O segundo mais baixo (reputational) "
            "tem mediana = 0.50. Teste Wilcoxon: W = 3.101.829, p < 0.001, "
            "efeito grande (r reportado como inf devido a precisao do "
            "float — ver BUG-01).\n"
            "- H13 (segmentacao): Top 25% vs Bottom 25% do fator "
            "thrilling diferem em 5 de 5 outros fatores. Maior efeito: "
            "reputacional (d = 0.887). O perfil de prazer dos "
            "thrill-seekers e realmente distinto.\n"
            "- Ranking dos 6 fatores por mediana: thrilling (-0.33) < "
            "reputational (0.50) < noble (0.67) < sensorial (1.25) < "
            "intellectual (1.80) < interpersonal (2.00)."
        ),
        "key_metrics": (
            "- Mediana do fator thrilling: -0.33 (unico negativo)\n"
            "- Gap para o segundo mais baixo: 0.83 pontos\n"
            "- Cohen's d entre Q1 e Q4 do thrilling: ate 0.887 (reputacional)\n"
            "- Fatores onde thrill-seekers diferem: 5 de 5"
        ),
        "caveats": (
            "- BUG-01: tamanho de efeito reportado como r = inf no H03 "
            "(o efeito e grande, mas o numero exato nao e interpretavel).\n"
            "- O efeito pode ser amplificado pela amostra (publico "
            "analitico/intelectual tende a rejeitar risco).\n"
            "- Quartis sao uma divisao arbitraria (H13)."
        ),
        "context": (
            "A maioria das pessoas neste dataset nao gosta de emocao forte "
            "— adrenalina, risco, sustos sao os unicos prazeres com "
            "discordancia liquida. E quem busca essas sensacoes tem um "
            "perfil completamente diferente: tende a valorizar mais "
            "status, competicao e festas. Os thrill-seekers sao uma "
            "minoria com um 'paladar' de prazer diferente da maioria."
        ),
    },
    {
        "id": "I04",
        "headline": "O paradoxo do thrilling: o prazer mais rejeitado e o que mais diferencia as pessoas",
        "hypotheses": ["H03", "H17", "H13"],
        "strength": "forte",
        "type": "emergente",
        "evidence_detail": (
            "- H03: Thrilling e o fator mais rejeitado (mediana = -0.33).\n"
            "- H17 (preditivo): Na regressao dos 6 fatores sobre o prazer "
            "geral, thrilling tem o MAIOR beta padronizado (0.354), "
            "seguido de noble (0.301) e reputational (0.287). R² total = "
            "0.974 (mas com circularidade parcial — ver AUD-09).\n"
            "- H13: Thrill-seekers diferem em todos os outros fatores "
            "(d ate 0.887).\n"
            "- A explicacao: thrilling tem a MAIOR VARIANCIA entre os 6 "
            "fatores. As pessoas divergem muito sobre ele. Por ter muita "
            "variacao, ele 'puxa' mais a media geral — tanto pra cima "
            "(thrill-seekers) quanto pra baixo (a maioria). E o fator "
            "mais polarizador."
        ),
        "key_metrics": (
            "- Beta padronizado do thrilling: 0.354 (maior dos 6 fatores)\n"
            "- Mediana do thrilling: -0.33 (unico fator negativo)\n"
            "- R² total da regressao: 0.974 (circularidade parcial)\n"
            "- Cohen's d thrill-seekers vs demais: ate 0.887"
        ),
        "caveats": (
            "- AUD-09: R² = 0.974 e inflado por circularidade (fatores "
            "sao subconjuntos dos itens que compoem a media geral). O "
            "numero absoluto nao e uma descoberta, mas os pesos relativos "
            "(betas) sao informativos.\n"
            "- O beta alto nao significa que thrilling 'gera mais prazer'. "
            "Significa que, por ter mais variancia, ele diferencia mais "
            "quem tem prazer geral alto vs baixo.\n"
            "- Este insight so aparece quando se combinam 3 analises — "
            "nenhuma delas sozinha revela o paradoxo."
        ),
        "context": (
            "O fator mais rejeitado e, ao mesmo tempo, o que mais "
            "'puxa' o prazer geral pra cima ou pra baixo. Isso parece "
            "paradoxo, mas a explicacao e simples: thrilling e o assunto "
            "sobre o qual as pessoas mais divergem. Quem busca adrenalina "
            "tende a gostar de tudo mais tambem; quem rejeita tende a "
            "ser mais seletivo. Thrilling nao e o 'motor' do prazer — "
            "e o termometro que mais varia."
        ),
    },
    {
        "id": "I05",
        "headline": "Quem cuida de pessoas tambem cuida de causas — existe um superfator 'cuidador'",
        "hypotheses": ["H07", "H14"],
        "strength": "moderada",
        "type": "convergencia",
        "evidence_detail": (
            "- H07 (relacional): Os fatores interpersonal e noble tem "
            "correlacao forte (Spearman rho = 0.460, p < 0.001). Alpha "
            "de Cronbach como dimensao unica: 0.67 (aceitavel, acima de "
            "0.60, mas abaixo de 0.70 = bom).\n"
            "- H14 (segmentacao): Quem pontua alto em espiritualidade "
            "pontua alto em ambos: noble (d = 1.31) e interpersonal "
            "(d = 0.47). Os dois fatores caminham juntos."
        ),
        "key_metrics": (
            "- Spearman rho (interpersonal × noble): 0.460\n"
            "- Cronbach alpha (2 fatores como dimensao unica): 0.67\n"
            "- Cohen's d noble (espirituais vs nao): 1.31\n"
            "- Cohen's d interpersonal (espirituais vs nao): 0.47"
        ),
        "caveats": (
            "- AUD-05: Cronbach alpha = 0.67 com apenas 2 itens (fatores) "
            "e uma estimativa instavel. O limiar 'bom' e 0.70.\n"
            "- O superfator 'quem cuida' e uma hipotese exploratoria, nao "
            "um fato confirmado. Precisaria de analise fatorial "
            "confirmatoria com todos os itens dos dois fatores.\n"
            "- A correlacao 0.46 e forte mas nao fortissima — os dois "
            "fatores ainda tem variancia propria."
        ),
        "context": (
            "Pessoas que se importam com seus entes queridos "
            "(interpersonal: tempo de qualidade, pertencer, amar) tambem "
            "tendem a se importar com causas maiores (noble: caridade, "
            "comunidade, ajudar). Isso sugere uma dimensao latente de "
            "'cuidado' que unifica os dois fatores. O grupo espiritual "
            "pontua alto em ambos, reforcando a conexao."
        ),
    },
    {
        "id": "I06",
        "headline": "Gostar de pensar nao tem nada a ver com querer status — as duas dimensoes sao independentes",
        "hypotheses": ["H06", "H05"],
        "strength": "moderada",
        "type": "convergencia",
        "evidence_detail": (
            "- H06 (relacional): Teste TOST confirma que a correlacao "
            "entre intellectual e reputational e equivalente a zero "
            "(rho = 0.023, p_TOST < 0.001, faixa de equivalencia: "
            "|rho| < 0.1). Sao estatisticamente independentes.\n"
            "- H05 (relacional): No nivel dos itens, pares como "
            "criatividade × competicao (rho = -0.083) e natureza × "
            "status (rho = -0.098) sao negativos e significativos "
            "apos correcao FDR. 26 de 55 pares negativos sobreviveram."
        ),
        "key_metrics": (
            "- Spearman rho (intellectual × reputational): 0.023 (praticamente zero)\n"
            "- TOST p-valor: < 0.001 (confirmada equivalencia a zero)\n"
            "- Pares negativos significativos entre itens: 26 de 55\n"
            "- Correlacao negativa mais forte: natureza × status (rho = -0.098)"
        ),
        "caveats": (
            "- AUD-04: Mesmo os pares 'incompativeis' do H05 tem "
            "|rho| < 0.1 — efeito negligivel na pratica. A "
            "incompatibilidade entre itens existe mas e muito sutil.\n"
            "- Independencia nao significa incompatibilidade. Pessoas "
            "podem pontuar alto em ambos — sao dimensoes que variam "
            "separadamente."
        ),
        "context": (
            "Quem busca prazer intelectual (pensar, criar, aprender) "
            "nao busca nem evita prazer reputacional (status, "
            "reconhecimento, poder). As duas coisas simplesmente nao "
            "tem relacao. Isso desafia a intuicao de que 'intelectuais "
            "desprezam status' — na verdade, sao dimensoes ortogonais "
            "(independentes, sem relacao uma com a outra)."
        ),
    },
    {
        "id": "I07",
        "headline": "Nao existem 'tipos de pessoa' no prazer — o que parecem grupos sao apenas regioes do espectro",
        "hypotheses": ["H15", "H12"],
        "strength": "moderada",
        "type": "emergente",
        "evidence_detail": (
            "- H12 (segmentacao): Tres metodos de clustering (K-Means, "
            "hierarquico, GMM) com k de 2 a 8. Nenhum encontrou grupos "
            "claros. Melhor silhouette: 0.228 (hierarquico, k=2) — "
            "abaixo do limiar 0.25. Estabilidade bootstrap: 0.183 ± 0.039.\n"
            "- H15 (segmentacao): K-Means k=3 encontrou um cluster com "
            "N = 1.712 onde intellectual e dominante. Mas sem silhouette "
            "reportado para esse cluster.\n"
            "- Recalculo do integrador (EMER-27): silhouette do k=3 = "
            "0.152 — pior que o melhor de H12. O 'grupo intelectual' e "
            "uma regiao do espectro recortada pelo algoritmo."
        ),
        "key_metrics": (
            "- Melhor silhouette geral: 0.228 (hierarquico k=2)\n"
            "- Silhouette do k=3 usado em H15: 0.152 (recalculado)\n"
            "- Estabilidade bootstrap: 0.183 +/- 0.039\n"
            "- Tamanho do 'cluster intelectual': 1.712 pessoas"
        ),
        "caveats": (
            "- AUD-07: O limiar 0.25 e arbitrario — silhouette < 0.25 "
            "nao prova que grupos nao existem, apenas que estes metodos "
            "nao os encontram nestes dados.\n"
            "- AUD-08: H15 tem vies de busca — procurar um perfil "
            "especifico quase sempre encontra algo. K-Means particiona "
            "o espaco de qualquer jeito.\n"
            "- BUG-02: H15 nao reportou silhouette do cluster."
        ),
        "context": (
            "E tentador pensar que existem 'tipos de pessoa' — "
            "o intelectual, o aventureiro, o cuidador. Mas os dados "
            "nao sustentam isso. Quando algoritmos encontram 'grupos', "
            "as fronteiras sao difusas e os perfis instáveis. O prazer "
            "e um espectro continuo: as pessoas se distribuem "
            "gradualmente, sem saltos nem clusters naturais."
        ),
    },
    {
        "id": "I08",
        "headline": "Generalistas reportam mais prazer — mas cuidado, parte do efeito e mecanica",
        "hypotheses": ["H11"],
        "strength": "sugestiva",
        "type": "emergente",
        "evidence_detail": (
            "- H11 (segmentacao): Divisao pela mediana da entropia de "
            "Shannon dos 6 fatores. Generalistas (N = 3.294, perfil "
            "equilibrado) tem media de prazer geral = 1.21. Especialistas "
            "(N = 3.293, perfil concentrado) = 0.58. Mann-Whitney U = "
            "8.802.914, p < 0.001, Cohen's d = 1.20 (efeito grande).\n"
            "- Recalculo do integrador (EMER-28): correlacao entre "
            "entropia e media geral = rho = 0.643. Isso sugere "
            "tautologia parcial: quem diz 'concordo' pra tudo "
            "(media alta) automaticamente tem perfil uniforme "
            "(entropia alta)."
        ),
        "key_metrics": (
            "- Cohen's d generalistas vs especialistas: 1.20 (efeito grande)\n"
            "- Media generalistas: 1.21 vs especialistas: 0.58\n"
            "- Correlacao entropia × media geral: rho = 0.643\n"
            "- Proporcao: ~50/50 (divisao pela mediana)"
        ),
        "caveats": (
            "- Tautologia parcial: entropia alta e media alta estao "
            "mecanicamente correlacionadas (rho = 0.643). Parte do "
            "efeito grande (d = 1.20) e artefato dessa relacao.\n"
            "- Divisao pela mediana e arbitraria.\n"
            "- A interpretacao 'diversificar fontes de prazer gera mais "
            "satisfacao' e mais forte do que os dados suportam. O que "
            "podemos dizer: quem concorda mais com os itens de prazer "
            "tende a ter perfil mais equilibrado.\n"
            "- Dados transversais: nao sabemos se diversificar CAUSA "
            "mais prazer ou se quem ja e mais satisfeito simplesmente "
            "concorda mais com tudo."
        ),
        "context": (
            "Pessoas com perfil de prazer mais equilibrado (generalistas) "
            "reportam mais satisfacao geral do que as mais concentradas "
            "em poucas fontes (especialistas). E uma diferenca grande "
            "(d = 1.20), mas parte dela e mecanica: quem concorda mais "
            "com tudo naturalmente fica com perfil mais uniforme. "
            "O achado e real mas a interpretacao causal ('diversifique "
            "suas fontes de prazer') vai alem do que os dados permitem."
        ),
    },
]


# ---------------------------------------------------------------------------
# Build the insight bank markdown
# ---------------------------------------------------------------------------
def build_insight_bank():
    """Generate the complete insight bank markdown."""
    lines = []

    # Header
    lines.append("# Banco de Insights — Sources of Pleasure")
    lines.append("")
    lines.append(f"**Data de geracao:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Dataset:** Sources of Pleasure (ClearerThinking.org)")
    lines.append(f"**Respondentes:** N = {N_RESPONDENTS:,}")
    lines.append(f"**Insights validados:** {len(INSIGHTS)}")
    lines.append("")

    # Summary by strength
    n_forte = sum(1 for i in INSIGHTS if i["strength"] == "forte")
    n_mod = sum(1 for i in INSIGHTS if i["strength"] == "moderada")
    n_sug = sum(1 for i in INSIGHTS if i["strength"] == "sugestiva")
    lines.append(f"| Forca | Quantidade |")
    lines.append(f"|-------|------------|")
    lines.append(f"| Forte | {n_forte} |")
    lines.append(f"| Moderada | {n_mod} |")
    lines.append(f"| Sugestiva | {n_sug} |")
    lines.append("")

    # Summary table
    lines.append("## Indice")
    lines.append("")
    lines.append("| ID | Manchete | Forca | Hipoteses |")
    lines.append("|-----|----------|-------|-----------|")
    for ins in INSIGHTS:
        hyps = ", ".join(ins["hypotheses"])
        lines.append(
            f"| {ins['id']} | {ins['headline']} | "
            f"{ins['strength']} | {hyps} |"
        )
    lines.append("")

    # Pipeline note
    lines.append("---")
    lines.append("")
    lines.append(
        "> **Como ler este banco:** cada insight foi validado pelo integrador "
        "senior (Fase 7) e rastreia de volta a pelo menos uma hipotese testada "
        "na Fase 5. A forca reflete a convergencia de evidencias e o tamanho "
        "dos efeitos. Ressalvas estao sempre presentes — nenhuma afirmacao "
        "causal e feita. Todos os numeros vem de dados reais (N = 6.587)."
    )
    lines.append("")

    # Individual insight cards
    for ins in INSIGHTS:
        lines.append("---")
        lines.append("")
        lines.append(f"## {ins['id']} — {ins['headline']}")
        lines.append("")

        # Hypotheses of origin
        hyp_list = []
        for hid in ins["hypotheses"]:
            h = hypotheses.get(hid, {})
            title = h.get("title", hid)
            analyst = h.get("analyst", "?")
            hyp_list.append(f"{hid} ({analyst}): {title}")
        lines.append("- **Pergunta(s) de origem:**")
        for h_str in hyp_list:
            lines.append(f"  - {h_str}")
        lines.append("")

        # Evidence
        lines.append("- **Evidencias:**")
        for evid_line in ins["evidence_detail"].strip().split("\n"):
            lines.append(f"  {evid_line}")
        lines.append("")

        # Key metrics
        lines.append("- **Metricas principais:**")
        for metric_line in ins["key_metrics"].strip().split("\n"):
            lines.append(f"  {metric_line}")
        lines.append("")

        # Strength
        lines.append(f"- **Forca da evidencia:** {ins['strength']}")
        lines.append("")

        # Confidence and limitations
        lines.append("- **Confianca e limitacoes:**")
        for caveat_line in ins["caveats"].strip().split("\n"):
            lines.append(f"  {caveat_line}")
        lines.append("")

        # Context and interpretation
        lines.append(f"- **Contexto e interpretacao:**")
        lines.append(f"  {ins['context']}")
        lines.append("")

    # Footer: general limitations
    lines.append("---")
    lines.append("")
    lines.append("## Limitacoes gerais do dataset")
    lines.append("")
    lines.append(
        "Estas limitacoes se aplicam a **todos** os insights acima e devem "
        "ser consideradas ao interpretar qualquer achado:"
    )
    lines.append("")
    lines.append(
        "1. **Amostra de conveniencia.** Os respondentes sao visitantes do "
        "ClearerThinking.org — provavelmente mais analiticos, mais "
        "escolarizados e menos religiosos que a populacao geral. Rankings "
        "e proporcoes podem mudar com outra amostra."
    )
    lines.append(
        "2. **Sem dados demograficos.** Nao ha idade, genero, pais ou "
        "renda. Nao e possivel controlar por essas variaveis nem "
        "generalizar para subgrupos."
    )
    lines.append(
        "3. **Dados transversais de autorrelato.** Um unico momento, "
        "uma unica resposta por pessoa. Nenhuma afirmacao causal e "
        "possivel. 'Associado a' nao significa 'causa'."
    )
    lines.append(
        "4. **Itens Likert de 7 pontos.** Tratados como intervalares "
        "(convencional para escalas de 7+), mas sao tecnicamente ordinais. "
        "Preferimos Spearman quando as distribuicoes sao assimetricas."
    )
    lines.append(
        "5. **N grande inflaciona significancia.** Com N ~ 6.500, quase "
        "qualquer correlacao e 'significativa'. Todos os insights acima "
        "usam tamanhos de efeito (d de Cohen, rho, R²) como criterio "
        "primario, nao p-valores."
    )
    lines.append(
        "6. **Hipoteses pos-exploracao.** As 17 hipoteses foram formuladas "
        "apos analise exploratoria dos dados (Fases 2-4), o que favorece "
        "confirmacao. A taxa de 88% de confirmacao reflete isso."
    )
    lines.append("")

    # Final footer
    lines.append("---")
    lines.append("")
    lines.append(
        "*Banco gerado automaticamente por `scripts/phase8_insight_bank.py`*"
    )
    lines.append(
        f"*Pipeline: Fases 0-8 | Dados: Sources of Pleasure "
        f"(ClearerThinking.org) — N = {N_RESPONDENTS:,}*"
    )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
print("\nGerando banco de insights...")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
content = build_insight_bank()
output_path = OUTPUT_DIR / "insight_bank.md"
output_path.write_text(content, encoding="utf-8")

print(f"\n{'='*60}")
print(f"  FASE 8 COMPLETA")
print(f"{'='*60}")
print(f"\n  Banco de insights: {output_path}")
print(f"  Insights gerados: {len(INSIGHTS)}")

n_forte = sum(1 for i in INSIGHTS if i["strength"] == "forte")
n_mod = sum(1 for i in INSIGHTS if i["strength"] == "moderada")
n_sug = sum(1 for i in INSIGHTS if i["strength"] == "sugestiva")
print(f"    Fortes: {n_forte}")
print(f"    Moderados: {n_mod}")
print(f"    Sugestivos: {n_sug}")

print(f"\n  Insights:")
for ins in INSIGHTS:
    print(f"    {ins['id']}: {ins['headline']} [{ins['strength']}]")
