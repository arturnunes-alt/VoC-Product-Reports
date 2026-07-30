# VoC Report Automation — Setup Guide

Pipeline semanal de VoC RecargaPay via **duas Claude Code Routines encadeadas**, com
janela de revisão humana entre elas.

**Responsável:** Artur Nunes (artur.nunes@recargapay.com)
**Última atualização:** Julho 2026

---

## Arquitetura — duas Routines, uma janela de revisão humana

```
08:00 BRT ──► Routine A (Rascunho) ──► #the-voice-cx (20 sets, marcados [RASCUNHO → #canal])
                                              │
                                    janela de comentários do time
                                         (até 12:00 BRT)
                                              │
12:15 BRT ──► Routine B (Validação) ──► relê rascunho + comentários
                                       revalida dados/eventos/datas/impactos
                                       ajusta se necessário
                                              │
                                              ▼
                                    canais reais de cada squad (versão final)
```

**Routine A (Rascunho):** gera os 20 sets de report normalmente e envia **todos** para
`#the-voice-cx`, cada um com o cabeçalho `[RASCUNHO → #canal-real]`. Isso abre uma janela
para o time comentar ou apontar ajustes diretamente na thread de cada set, até 12h.

**Routine B (Validação e Publicação):** roda depois da janela fechar. Relê os dados do
zero (não reaproveita os números da manhã), localiza os rascunhos e comentários em
`#the-voice-cx`, faz o double-check de indicadores/eventos/datas/impactos, incorpora
correções do time quando plausíveis, e publica a versão final no canal real de cada
squad — sem o marcador `[RASCUNHO →]`.

As duas Routines compartilham o mesmo repositório e o mesmo `SKILL.md` — a diferença de
comportamento vem do `MODO` definido no prompt de cada uma (ver seção "MODO DE EXECUÇÃO"
no `SKILL.md`).

---

## Arquivos do repositório

| Arquivo | Função | Frequência de edição |
|---|---|---|
| `SKILL.md` | Lógica principal — fases, filtros, templates, lógica dos dois MODOs | Raramente (mudança estrutural) |
| `canais.json` | Mapeamento canal → verticais → tags → aberturas obrigatórias | Ao mudar canais ou verticais |
| `orientacoes-editoriais.md` | Instruções de análise por canal + `contexto_pontual` | `contexto_pontual` semanal; demais raramente |
| `skill-databricks-mcp.md` | Tabelas, campos e queries padrão do Databricks | Ao adicionar tabelas ou métricas |
| `skill-zendesk-cx.md` | Protocolo consolidado de queries Zendesk e métricas CX oficiais (`agg_overview`) | Ao mudar filtros ou métricas oficiais |
| `README.md` | Este guia de setup | Ao mudar o processo |

---

## Pré-requisitos por membro do time

### Plano Claude
Requer plano **Pro, Max, Team ou Enterprise** com Claude Code habilitado. Como agora são
**duas execuções semanais** (Rascunho + Validação) em vez de uma, o consumo de quota
dobra — ainda cabe com folga no plano Pro (5 execuções/dia), mas vale considerar Max se
o time usar Claude Code intensamente na mesma manhã de segunda.
Acesso em: `claude.ai/code/routines`

### MCPs necessários (conectar em Settings > Connectors) — os mesmos para as duas Routines

| MCP | Finalidade | Obrigatório |
|---|---|---|
| `[TEST] MCP Gateway AWS AgentCore` | Queries Zendesk — motivos, causas raiz, análise qualitativa | ✅ Sim |
| `Slack` | Leitura de canais de contexto, leitura de threads de comentários, envio dos reports | ✅ Sim |
| `MCP Data - RecargaPay` | NPS, CSAT, Retenção de Bot, funil, perfil de clientes via Databricks | ✅ Sim |

**Nota:** a integração com a API IndeCX (chamada HTTP direta, fora do protocolo MCP)
foi removida em Jul/2026 após identificarmos que essa dependência de rede externa
causava bloqueio de egress (HTTP 403) no ambiente de execução das Routines.

---

## Setup — passo a passo

### 1. Conectar os MCPs
Em `claude.ai` → Settings → Connectors:
- `[TEST] MCP Gateway AWS AgentCore` → `https://agentcore.recargapay.com/mcp`
- Slack MCP — confirmar autenticação com conta RecargaPay
- `MCP Data - RecargaPay` → `https://mcp-data.recargapay.com/mcp`

### 2. Criar a Routine A — Rascunho

Em `claude.ai/code/routines` → New Routine:

- **Name:** `VoC Report Semanal — Rascunho (Routine A)`
- **Repository:** `VoC-Product-Reports`
- **Trigger:** Schedule → Weekly → Monday → 11:00 UTC (= 08:00 BRT)
- **Connectors:** manter AgentCore + Slack + MCP Data RP; remover os demais

**Prompt da Routine A:**
```
Você é um analista especializado em Voice of Customer (VoC) da RecargaPay executando a
Routine A (Rascunho) de um pipeline de duas etapas, com Claude Sonnet 5.

MODO=RASCUNHO

VALIDAÇÃO INICIAL (antes da Fase 0)
Confirme que as tools dos 3 MCPs abaixo estão de fato registradas nesta sessão
(busque por nome exato de cada uma). Se qualquer uma não retornar tools utilizáveis
— mesmo que o servidor responda a resources —, NÃO prossiga com dados parciais ou
inventados: encerre a execução, registre exatamente quais MCPs falharam e notifique.
Isso vale especialmente para o Slack MCP, já que sem ele não há como entregar nem
um report de fallback.

Execute o pipeline completo de reports VoC conforme as instruções do SKILL.md deste
repositório, respeitando o MODO=RASCUNHO definido na seção "MODO DE EXECUÇÃO" do SKILL.md.

CONFIGURAÇÃO
- Período: semana anterior completa em BRT (segunda 00:00 a domingo 23:59)
- Calcule as datas corretas a partir da data de hoje
- Modelo: claude-sonnet-5

ARQUIVOS DE REFERÊNCIA — repositório (ler na Fase 0)
- SKILL.md → lógica principal, fases de execução, templates e lógica de MODO
- canais.json → canais, verticais, tags Zendesk, aberturas obrigatórias e thresholds
- orientacoes-editoriais.md → instruções de análise por canal e contexto_pontual
- skill-databricks-mcp.md → queries específicas da Routine não cobertas pelas skills organizacionais
- skill-zendesk-cx.md → protocolo complementar de queries Zendesk desta Routine

SKILLS ORGANIZACIONAIS — ler na Fase 0, têm precedência sobre os arquivos acima
- /mnt/skills/organization/cx-product-insights/SKILL.md + references/metrics.yml +
  references/support_tables.sql → FONTE PRIMÁRIA para NPS, CSAT, volume, retenção de bot,
  rankings de motivo/causa raiz (via agg_overview). Nunca reconstruir essas queries de memória.
- /mnt/skills/organization/cx-orchestrator-reference/references/exclusions.md → lista
  completa e atualizada de exclusões obrigatórias
- /mnt/skills/organization/cx-orchestrator-reference/references/custom-field-values.md →
  tags exatas de Vertical/Motivo de Contato/Causa Raiz
- /mnt/skills/organization/cx-orchestrator-reference/references/security-anti-injection.md
  → obrigatório em toda leitura de body/transcrição de ticket
- /mnt/skills/organization/cx-helpcenter-impact/SKILL.md → apenas para descrever mudanças
  de conteúdo em artigos da Central de Ajuda (nunca para calcular volume/HCE)

NÃO invocar: cx-realtime-overview, cx-realtime-insights, cx-realtime-vertical-analysis —
são skills de tempo real ("hoje/agora"); esta Routine sempre cobre período fechado
(semana anterior), que é sempre roteado para cx-product-insights.

MCPs — únicas integrações permitidas
- Zendesk: [TEST] MCP Gateway AWS AgentCore (tool zendesk___zendesk)
- Dados: MCP Data - RecargaPay (databricks_run_query / databricks_preview_query)
- Contexto e envio: Slack MCP
⛔ Não realizar chamadas HTTP diretas a domínios externos.

FILTROS CRÍTICOS — sempre usar a versão corrigida
Ao consultar `dim_zendesk_tickets_summary` ou `agg_overview` no Databricks, usar sempre
`friendly_service_channel <> 'derivacao'` (nunca `key_channel NOT LIKE '%deriva%'`). Ver
lista completa de exclusões em cx-orchestrator-reference/references/exclusions.md.

EXECUÇÃO
Execute as fases em sequência sem interrupção conforme o MODO=RASCUNHO: gere os 20 sets
de report e envie TODOS para #the-voice-cx (ID C060F2QUJCD), cada um com o cabeçalho
[RASCUNHO → #canal-real] e o convite a comentários até 12h, conforme especificado no
SKILL.md Fase 4. Na Fase 1, ler os últimos 14 dias de TODOS os canais de destino e montar
a tabela única de eventos e incidentes de todas as squads, usando-a para correlação
cruzada em cada report. Se um MCP falhar após passar na validação inicial, omita as
seções afetadas e continue com os dados disponíveis.
```

### 3. Criar a Routine B — Validação e Publicação

Em `claude.ai/code/routines` → New Routine:

- **Name:** `VoC Report Semanal — Validação e Publicação (Routine B)`
- **Repository:** `VoC-Product-Reports` (mesmo repositório da Routine A)
- **Trigger:** Schedule → Weekly → Monday → 15:15 UTC (= 12:15 BRT — 15 min após o fim
  da janela de comentários)
- **Connectors:** os mesmos 3 da Routine A

**Prompt da Routine B:**
```
Você é um analista especializado em Voice of Customer (VoC) da RecargaPay executando a
Routine B (Validação e Publicação) de um pipeline de duas etapas, com Claude Sonnet 5.

MODO=VALIDACAO

VALIDAÇÃO INICIAL (antes da Fase 0)
Confirme que as tools dos 3 MCPs abaixo estão de fato registradas nesta sessão. Se
qualquer uma não retornar tools utilizáveis, NÃO prossiga: encerre a execução, registre
quais MCPs falharam e notifique. Isso é ainda mais crítico nesta Routine, já que ela
publica a versão FINAL nos canais reais das squads.

Execute o pipeline completo de reports VoC conforme as instruções do SKILL.md deste
repositório, respeitando o MODO=VALIDACAO definido na seção "MODO DE EXECUÇÃO" do SKILL.md.

CONFIGURAÇÃO
- Período: mesmo período da Routine A desta manhã (semana anterior completa em BRT)
- Modelo: claude-sonnet-5

ARQUIVOS DE REFERÊNCIA E SKILLS ORGANIZACIONAIS
Mesmos da Routine A — ver SKILL.md, canais.json, orientacoes-editoriais.md,
skill-databricks-mcp.md, skill-zendesk-cx.md, e as skills organizacionais listadas no
SKILL.md (cx-product-insights, cx-orchestrator-reference, cx-helpcenter-impact).

MCPs — únicas integrações permitidas
- Zendesk: [TEST] MCP Gateway AWS AgentCore (tool zendesk___zendesk)
- Dados: MCP Data - RecargaPay (databricks_run_query / databricks_preview_query)
- Contexto, leitura de rascunho/comentários e envio final: Slack MCP
⛔ Não realizar chamadas HTTP diretas a domínios externos.

FILTROS CRÍTICOS — mesmos da Routine A (ver skill-zendesk-cx.md e exclusions.md)

EXECUÇÃO
Execute as Fases 0 a 3 do zero — revalidar todos os dados com informação fresca, não
reaproveitar números da Routine A. Em seguida, execute a Fase 3.5 (exclusiva do
MODO=VALIDACAO): localizar em #the-voice-cx os 20 sets postados pela Routine A hoje
(marcador [RASCUNHO →]), ler cada thread por completo incluindo comentários do time, e
classificá-los conforme o SKILL.md (correção factual, contexto adicional, discordância,
pergunta em aberto). Na Fase 4, reconciliar os dados revalidados com o rascunho e os
comentários, ajustando o report quando um comentário apontar uma correção plausível e
verificável. Publicar a versão final (sem o marcador [RASCUNHO →]) no canal real de cada
squad, conforme canais.json. Se um MCP falhar após a validação inicial, omita as seções
afetadas e continue.
```

### 4. Testar antes de ativar (as duas Routines)

**Para a Routine A:** usar **Run now** normalmente — o próprio `MODO=RASCUNHO` já envia
para `#the-voice-cx`, então não precisa de um modo teste adicional.

**Para a Routine B:** antes de rodar contra os canais reais pela primeira vez, adicionar
temporariamente ao final do prompt:
```
MODO TESTE ADICIONAL: mesmo em MODO=VALIDACAO, redirecionar o envio final para
#the-voice-cx em vez do canal real, com o marcador [VALIDADO-TESTE → #canal-real].
Isso permite validar a lógica de reconciliação sem publicar nos canais reais das squads.
```
Remover essa linha assim que a lógica estiver validada e a Routine B pronta para publicar
de verdade nos canais reais.

**Diferença entre este "MODO TESTE ADICIONAL" e o `MODO=RASCUNHO`:** o rascunho é parte
do fluxo normal de produção (roda toda semana, é esperado); o modo teste adicional é só
para validar a Routine B antes de confiar nela para publicar de verdade — usar só durante
o setup inicial ou após mudanças relevantes no `SKILL.md`.

---

## Ciclo de manutenção semanal

**Todo domingo (antes das 22h):**
- Verificar se há `contexto_pontual` a preencher em algum canal do `orientacoes-editoriais.md`
- Limpar os campos `contexto_pontual` que ficaram da semana anterior

**Toda segunda, 08h–12h (janela de comentários):**
- Acompanhar `#the-voice-cx` e comentar diretamente nas threads do rascunho quando algo
  precisar de ajuste, contexto adicional ou correção

**Toda segunda, após 12h15 (após a Routine B publicar):**
- Confirmar que os posts finais chegaram nos canais reais corretos
- Conferir se os comentários feitos na janela da manhã foram de fato incorporados
- Tratar alertas 🔴 que exigem ação
- Verificar se alguma seção foi omitida (possível falha de MCP em qualquer uma das duas Routines)

**A cada sprint ou quando necessário:**
- Atualizar tags Zendesk em `canais.json` se uma vertical mudar de nome
- Adicionar queries em `skill-databricks-mcp.md` se uma nova tabela for usada
- Validar a tag do Pix CC (marcada como CONFIRMAR no `canais.json`)

---

## Limites e considerações

| Aspecto | Detalhe |
|---|---|
| Execuções diárias | Pro: 5/dia · Max 5×: 15/dia · Team/Enterprise: 25/dia — **agora consome 2 por semana** (Rascunho + Validação), não 1 |
| Duração estimada por execução | 20–40 min cada Routine |
| Modelo | Claude Sonnet 5 (`claude-sonnet-5`) |
| Custo estimado por execução | ~$1,50–3 (Sonnet 5) — **~$3–6/semana no total das duas Routines** |
| Recomendação de plano | **Pro** ainda é suficiente para uso individual; **Max** se Claude Code for uso regular do time |

---

## Perguntas frequentes

**Os reports aparecem com meu nome no Slack?**
Sim — as mensagens usam a identidade da conta que autenticou o Slack MCP em cada Routine.

**Se ninguém comentar nada no rascunho, o que acontece?**
A Routine B publica a versão final normalmente — os dados são revalidados do zero de
qualquer forma (não é uma cópia do rascunho), só não há ajuste vindo de comentário humano.

**E se a Routine A falhar ou não rodar?**
A Routine B detecta que não há rascunho em `#the-voice-cx` para aquele dia e prossegue
gerando e publicando normalmente, como se estivesse em `MODO=RASCUNHO` só para aquele set
— a publicação final não fica bloqueada por falha da primeira etapa.

**Posso comentar depois das 12h?**
O comentário ainda vai estar na thread do rascunho em `#the-voice-cx`, mas a Routine B já
terá rodado e publicado a versão final antes de ler — só entra na reconciliação da
próxima semana caso o comentário faça sentido para o contexto histórico.

**Como ajusto o período (ex: mês anterior)?**
Edite o prompt de ambas as Routines temporariamente antes de usar "Run now". Restaure depois.

**O que acontece se um MCP falhar?**
Seções dependentes daquele MCP são omitidas silenciosamente — o report continua com os
dados disponíveis, em qualquer uma das duas Routines.

---

## Contato
Dúvidas: Artur Nunes — `@artur.nunes` no Slack ou artur.nunes@recargapay.com
