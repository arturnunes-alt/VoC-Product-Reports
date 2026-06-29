# VoC Report Automation — Setup Guide

Report semanal autônomo de VoC RecargaPay via Claude Code Routine.

**Responsável:** Artur Nunes (artur.nunes@recargapay.com)  
**Última atualização:** Julho 2026

---

## O que essa Routine faz

Toda segunda-feira às 08:00 BRT, o Claude executa automaticamente:

1. Lê o `orientacoes-editoriais.md` para carregar as instruções de análise por canal
2. Lê os canais Slack relevantes para identificar eventos e temas da semana
3. Coleta dados do Databricks: NPS, CSAT N1, CSAT Bot, Retenção de Bot, funil de Central de Ajuda, perfil de clientes
4. Consulta o Zendesk (AgentCore MCP) para motivos, causas raiz e análise qualitativa por vertical
5. Gera e envia reports para 10 canais Slack (2 gerais + 8 de produto)
6. Cada report: mensagem raiz no canal + report completo em thread + alertas em thread

---

## Arquivos do repositório

| Arquivo | Função | Frequência de edição |
|---|---|---|
| `SKILL.md` | Lógica principal da Routine — fases, filtros, templates | Raramente (mudança estrutural) |
| `canais.json` | Mapeamento canal → verticais → tags → aberturas obrigatórias | Ao mudar canais ou verticais |
| `orientacoes-editoriais.md` | Instruções de análise por canal + `contexto_pontual` | `contexto_pontual` semanal; demais raramente |
| `skill-databricks-mcp.md` | Tabelas, campos e queries padrão do Databricks | Ao adicionar tabelas ou métricas |
| `README.md` | Este guia de setup | Ao mudar o processo |

---

## Pré-requisitos por membro do time

### Plano Claude
Requer plano **Max 5× ou superior** com Claude Code habilitado — o Opus 4.8 consome quota significativamente mais alta do que o Sonnet. O plano Pro pode atingir o limite em semanas com uso interativo intenso no mesmo dia da Routine.
Acesso em: `claude.ai/code/routines`

### MCPs necessários (conectar em Settings > Connectors)

| MCP | Finalidade | Obrigatório |
|---|---|---|
| `[TEST] MCP Gateway AWS AgentCore` | Queries Zendesk — motivos, causas raiz, análise qualitativa | ✅ Sim |
| `Slack` | Leitura de canais de contexto + envio dos reports | ✅ Sim |
| `MCP Data - RecargaPay` | NPS, CSAT, Retenção de Bot, funil, perfil de clientes via Databricks | ✅ Sim |

---

## Setup — passo a passo

### 1. Conectar os MCPs
Em `claude.ai` → Settings → Connectors:
- `[TEST] MCP Gateway AWS AgentCore` → `https://agentcore.recargapay.com/mcp`
- Slack MCP — confirmar autenticação com conta RecargaPay
- `MCP Data - RecargaPay` → `https://mcp-data.recargapay.com/mcp`

### 2. Criar a Routine
Em `claude.ai/code/routines` → New Routine:

- **Name:** `VoC Report Semanal — RecargaPay`
- **Repository:** `VoC-Product-Reports`
- **Trigger:** Schedule → Weekly → Monday → 11:00 UTC (= 08:00 BRT)
- **Connectors:** manter AgentCore + Slack + MCP Data RP; remover os demais

**Prompt da Routine:**
```
Execute o pipeline completo de reports VoC conforme o SKILL.md deste repositório.

Período: semana anterior completa em BRT (segunda 00:00 a domingo 23:59).
Calcule as datas corretas a partir da data de hoje.

Use canais.json para o mapeamento de canais, verticais, aberturas obrigatórias e thresholds.
Use orientacoes-editoriais.md para as instruções de análise de cada canal.
Use skill-databricks-mcp.md para todas as queries Databricks.

MCP Zendesk: [TEST] MCP Gateway AWS AgentCore (tool zendesk___zendesk).
MCP Dados: MCP Data - RecargaPay (databricks_run_query / databricks_preview_query).

Execute as fases em sequência. Se um MCP falhar, omita as seções afetadas e continue.
```

### 3. Testar antes de ativar
Na página da Routine, usar **Run now** com o modo teste:

Adicionar ao final do prompt antes de testar:
```
MODO TESTE: enviar todos os reports para #the-voice-cx (ID: C060F2QUJCD).
Identificar cada bloco com o canal original: [TESTE → #nome-do-canal]
```

---

## Ciclo de manutenção semanal

**Todo domingo (antes das 22h):**
- Verificar se há `contexto_pontual` a preencher em algum canal do `orientacoes-editoriais.md`
- Limpar os campos `contexto_pontual` que ficaram da semana anterior

**Toda segunda (após o envio):**
- Confirmar que os posts chegaram nos canais corretos
- Tratar alertas 🔴 que exigem ação
- Verificar se alguma seção foi omitida (possível falha de MCP)

**A cada sprint ou quando necessário:**
- Atualizar tags Zendesk em `canais.json` se uma vertical mudar de nome
- Adicionar queries em `skill-databricks-mcp.md` se uma nova tabela for usada
- Validar a tag do Pix CC (marcada como CONFIRMAR no `canais.json`)

---

## Limites e considerações

| Aspecto | Detalhe |
|---|---|
| Execuções diárias | Pro: 5/dia · Max 5×: 15/dia · Team/Enterprise: 25/dia |
| Duração estimada por execução | 30–60 min |
| Modelo | Claude Opus 4.8 (`claude-opus-4-8`) |
| Custo estimado por execução | ~$8–12 (Opus 4.8) |
| Recomendação de plano | **Max 5×** se Claude Code for uso regular do time |

---

## Perguntas frequentes

**Os reports aparecem com meu nome no Slack?**
Sim — as mensagens usam a identidade da conta que autenticou o Slack MCP.

**Posso rodar on-demand?**
Sim — use "Run now" na página da Routine, ou adicione um trigger de API.

**Como ajusto o período (ex: mês anterior)?**
Edite o prompt temporariamente antes do "Run now". Restaure depois.

**O que acontece se um MCP falhar?**
Seções dependentes daquele MCP são omitidas silenciosamente — o report continua com os dados disponíveis.

---

## Contato
Dúvidas: Artur Nunes — `@artur.nunes` no Slack ou artur.nunes@recargapay.com
