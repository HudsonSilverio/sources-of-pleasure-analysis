# Sources of Pleasure — Memorial descritivo da análise

*Documento gerado por `scripts/build_metodologia.py` em 2026-09-08 20:32 a partir de 1 capítulo(s) em `outputs/reports/metodologia/`.*

## Sumário

- [Capítulo 0 — Como a análise foi desenhada](#capítulo-0-como-a-análise-foi-desenhada)

---

# Capítulo 0 — Como a análise foi desenhada

**Em uma frase:** limpamos as respostas, fizemos perguntas aos dados, testamos,
auditamos e transformamos o que sobreviveu em gráficos.

## O fluxo

```mermaid
flowchart TD
    A([Arquivo bruto<br/>11.718 respostas]) --> F0

    F0[Fase 0 · ENTENDER<br/>O que cada pergunta do questionário mede?] --> F1
    F1[Fase 1 · LIMPAR<br/>Tirar contatos, lixo, incompletos e duplicados] --> F2
    F2[Fase 2 · DESCREVER<br/>Como cada fonte de prazer se comporta sozinha?] --> F3
    F3[Fase 3 · EXPLORAR<br/>O que anda junto com o quê?] --> F4
    F4[Fase 4 · PERGUNTAR<br/>Transformar pistas em 17 perguntas testáveis] --> F56
    F56[Fases 5–6 · TESTAR<br/>5 analistas especialistas, um por tipo de pergunta] --> F7
    F7[Fase 7 · AUDITAR<br/>Um revisor recalcula, cruza e derruba o que é fraco] --> F8
    F8[Fase 8 · SELECIONAR<br/>Escrever as descobertas e classificar por força] --> F9
    F9[Fase 9 · MOSTRAR<br/>Um gráfico por descoberta]

    F1 -. 6.587 respostas confiáveis .-> F2
    F4 -. 17 perguntas .-> F56
    F56 -. 17 vereditos .-> F7
    F7 -. 8 descobertas .-> F8
    F9 --> Z([8 gráficos finais])
```

## Cada fase em uma linha

| Fase | Pergunta que ela responde | O que entrega |
|---|---|---|
| **0 · Entender** | O que o questionário mede? | Lista das 37 fontes de prazer e das 6 famílias |
| **1 · Limpar** | Quais respostas são confiáveis? | 6.587 respostas completas, sem dados pessoais |
| **2 · Descrever** | Como cada fonte se comporta sozinha? | Rankings, médias, o que divide as pessoas |
| **3 · Explorar** | O que anda junto com o quê? | Pistas para gerar perguntas |
| **4 · Perguntar** | O que vale a pena testar? | 17 perguntas numeradas (H01–H17) |
| **5–6 · Testar** | Cada pergunta se confirma? | 17 vereditos com tamanho do efeito |
| **7 · Auditar** | Quais resultados se sustentam? | 8 candidatos a descoberta |
| **8 · Selecionar** | O que dizer e com que confiança? | 8 fichas de descoberta (forte / moderada / sugestiva) |
| **9 · Mostrar** | Como comunicar? | 8 gráficos, um por descoberta |

## Três regras que valem em todas as fases

1. **Só dado real** — nada simulado, estimado ou preenchido.
2. **Pergunta antes da técnica** — nenhum teste roda sem uma pergunta numerada.
3. **Quem testa não é quem julga** — a auditoria é separada dos testes.

Cada fase é detalhada em seu próprio capítulo, nesta mesma ordem.
