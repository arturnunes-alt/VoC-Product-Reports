# VoC Monitoramento Intraday — Setup Guide

Rotina independente do pipeline semanal (Routine A/B). Roda 3x ao dia para identificar
anomalias de alta criticidade que ainda não estão mapeadas, e alerta o time de CXM em
tempo quase real — sem esperar o report da próxima segunda-feira.

**Responsável:** Artur Nunes (artur.nunes@recargapay.com)
**Criado em:** Julho 2026

---

## O que essa Routine faz, em uma frase

A cada 3 horas (10h, 13h, 16h), ela olha o que aconteceu desde a última checagem, compara
com o que é normal para aquele mesmo horário do dia, confere se algo assim já foi
sinalizado em algum canal relevante, e — só se for realmente crítico e realmente novo —
avisa a pessoa certa do time de CXM, marcando-a diretamente em `#the-voice-cx`.

**O que ela não faz:** não substitui o report semanal, não posta no canal da squad, e não
avisa sobre coisa que já está sendo tratada.

---

## Por que ela é separada do pipeline semanal

Esta Routine roda em cadência e propósito completamente diferentes do pipeline de
report semanal (Routine A/B, documentado no `README.md` principal). Por isso:

- Usa um **arquivo de lógica próprio** (`SKILL-INTRADAY.md`), não o `SKILL.md` do
  pipeline semanal
- Usa um **arquivo de mapeamento próprio** (`mapeamento-responsaveis.json`)
- **Lê** `canais.json` como referência (mesmo mapeamento vertical → squad → canal já
  usado no pipeline semanal), mas **nunca o edita** — isso evita que uma mudança nesta
  Routine afete acidentalmente o report de segunda-feira

---

## Pré-requisitos

### MCPs necessários — diferente do pipeline semanal
| MCP | Finalidade | Obrigatório |
|---|---|---|
| `[TEST] MCP Gateway AWS AgentCore` | Contatos humanos/bot **ao vivo** (hoje) | ✅ Sim |
| `Amplitude` | Acessos à Central de Ajuda **ao vivo** (hoje) | ✅ Sim |
| `Slack` | Checagem de mapeamento prévio + envio de alerta | ✅ Sim |
| `MCP Data - RecargaPay` | Apenas contexto histórico amplo — não usado para detectar anomalia | ⚠️ Recomendado |

**Diferença crítica do pipeline semanal:** o Databricks (`MCP Data - RecargaPay`) tem
defasagem de 1 dia — por isso esta Routine usa Zendesk MCP e Amplitude **ao vivo** como
fonte primária dos dados de hoje, e reserva o Databricks só para contexto histórico mais
amplo (ver `SKILL-INTRADAY.md` Fase 1C).

### Mapeamento de responsáveis — já preenchido (31/07/2026)

O arquivo `mapeamento-responsaveis.json` já está populado com os dados reais da planilha:
https://docs.google.com/spreadsheets/d/1ENUwksFJbaU3tfq_yz62KM6-4Ud-W9trrQ0X3t1Ejs0

**Sempre que a planilha mudar**, atualizar o arquivo manualmente — não há leitura
automática (Google Sheets não é legível pelas ferramentas desta Routine, só Google Docs).

**Pontos de atenção no mapeamento atual:**
- Verticais marcadas `"On Demand"` não têm responsável fixo — a Routine envia o alerta
  normalmente, sem marcar ninguém (Transporte, Recarga de Celular, Contas e Boletos,
  Boleto de Cobrança)
- `Contas e Boletos` e `Boleto de Cobrança` foram confirmadas como correspondendo a
  "Bills" na planilha
- Squads da planilha sem vertical correspondente hoje (Checkout, Campanhas e Parcerias,
  Merchants, Seguros, Open Finance, Fraud Prevention, Payments, Acquirer) ficaram
  registradas em `squads_da_planilha_fora_do_escopo_desta_routine`, para o caso da Routine
  expandir cobertura no futuro

---

## Setup — passo a passo

### 1. Conectar o Amplitude (adicional em relação ao pipeline semanal)
Em `claude.ai` → Settings → Connectors → adicionar Amplitude, se ainda não estiver
conectado. Os outros 3 MCPs (AgentCore, Slack, MCP Data RP) já devem estar conectados
pelo setup do pipeline semanal.

### 2. Criar a Routine — 3 triggers, mesma lógica

Em `claude.ai/code/routines` → New Routine:

- **Name:** `VoC Monitoramento Intraday`
- **Repository:** `VoC-Product-Reports` (mesmo repositório)
- **Trigger:** Schedule → Daily (dias úteis) → três horários: 13:00 UTC (10h BRT),
  16:00 UTC (13h BRT), 19:00 UTC (16h BRT). Se a plataforma só permitir um horário por
  Routine, criar 3 Routines idênticas, uma por horário.
- **Connectors:** AgentCore + Amplitude + Slack + MCP Data RP

**Prompt da Routine:**
```
Você é um analista de CXM da RecargaPay executando a Routine de Monitoramento Intraday,
com Claude Sonnet 5. Esta Routine é independente do pipeline semanal de reports.

VALIDAÇÃO INICIAL (antes de qualquer coisa)
Confirme que as tools do Zendesk (AgentCore), Amplitude e Slack estão de fato registradas
nesta sessão. Se qualquer uma não retornar tools utilizáveis, encerre sem alertar — esta
Routine depende de dados ao vivo, não há fallback seguro via Databricks.

Execute conforme as instruções de SKILL-INTRADAY.md deste repositório.

ARQUIVOS DE REFERÊNCIA
- SKILL-INTRADAY.md → lógica completa desta Routine (fases, critérios, templates)
- mapeamento-responsaveis.json → responsável de CXM por squad/vertical, para o @ no alerta
- canais.json (do pipeline semanal) → ler apenas como referência de vertical→squad→canal,
  nunca editar

REGRA FUNDAMENTAL
Dados de HOJE vêm sempre de Zendesk MCP (ao vivo) e Amplitude — nunca do Databricks, que
tem defasagem de 1 dia. O Databricks só é usado para contexto histórico mais amplo.

DESTINO
O único canal de saída é #the-voice-cx (ID C060F2QUJCD). Nunca postar no canal de
nenhuma squad. Marcar o responsável mapeado com @ quando existir; se a vertical estiver
marcada como On Demand ou não estiver no arquivo de mapeamento, enviar o alerta mesmo
assim, sem marcar ninguém.

CRITÉRIO DE ALERTA
Só alertar se passar os dois portões do SKILL-INTRADAY.md: (1) criticidade alta conforme
os thresholds da Fase 3, e (2) o tema ainda não estar mapeado em nenhum dos canais
estratégicos checados na Fase 2. Na grande maioria das execuções, o resultado esperado é
nenhum alerta — isso é o comportamento correto, não uma falha.

JANELA
Calcule a janela desde a última execução conforme a Fase 0 — considerando que a execução
das 10h de segunda cobre desde sexta às 16h.
```

### 3. Testar antes de ativar

Rodar **"Run now"** manualmente em um horário fora do agendamento, e conferir:
- Se ela identificou corretamente a janela de análise
- Se os thresholds de criticidade (Fase 3) não estão disparando alerta para variação
  normal do dia a dia — calibrar se necessário
- Se a checagem de mapeamento prévio está de fato suprimindo temas já conhecidos

Recomenda-se rodar por 2–3 semanas observando os "quase alertas" (perto do threshold,
mas não dispararam) antes de considerar os números da Fase 3 definitivos.

---

## Manutenção

**Sempre que a planilha de responsáveis mudar:** atualizar `mapeamento-responsaveis.json`
manualmente (ver seção acima).

**Após 2–3 semanas de operação:** revisar os thresholds da Fase 3 do
`SKILL-INTRADAY.md` com base no volume real de alertas gerados — ajustar se estiver
alertando demais (ruído) ou de menos (passando coisa real).

**Se o Amplitude MCP mudar de estrutura de eventos:** revalidar os nomes de evento
usados na Fase 1B antes que a Routine passe a reportar zero acessos silenciosamente.

---

## Contato
Dúvidas: Artur Nunes — `@artur.nunes` no Slack ou artur.nunes@recargapay.com
