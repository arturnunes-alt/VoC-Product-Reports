# VoC Report Automation — Setup Guide

Report semanal autônomo de VoC RecargaPay via Claude Code Routine.

**Responsável:** Artur Nunes (artur.nunes@recargapay.com)  
**Última atualização:** Junho 2026

---

## O que essa Routine faz

Toda segunda-feira às 08:00 BRT, o Claude executa automaticamente:

1. Lê eventos e incidentes recentes nos canais `#lideres-cx-e-cxm` e `#comunicados_e_atualizações_cx`
2. Coleta NPS da semana via Databricks (IndeCX)
3. Consulta o Zendesk (via AgentCore MCP) para cada vertical mapeada
4. Gera e envia reports para 10 canais Slack (2 gerais + 8 de produto)
5. Cada report tem: mensagem raiz no canal + report completo em thread + alertas em thread

---

## Pré-requisitos por membro do time

### Plano Claude
- Requer plano **Pro, Max, Team ou Enterprise** com Claude Code habilitado.
- Acesso em: `claude.ai/code/routines`

### MCPs necessários (conectar em Settings > Connectors)
| MCP | Finalidade | Obrigatório |
|---|---|---|
| `[TEST] MCP Gateway AWS AgentCore` | Consultas Zendesk | ✅ Sim |
| `Slack` | Leitura de canais + envio de reports | ✅ Sim |
| `MCP Data - RecargaPay` | NPS IndeCX via Databricks | ⚠️ Recomendado |

Se o `MCP Data - RecargaPay` não estiver disponível, a seção NPS é omitida com ⚠️ e o restante funciona normalmente.

---

## Setup — passo a passo

### 1. Conectar os MCPs
Em `claude.ai` → Settings → Connectors:
- Adicionar `[TEST] MCP Gateway AWS AgentCore` (`https://agentcore.recargapay.com/mcp`)
- Confirmar que o Slack MCP está conectado e autenticado com sua conta RP
- Adicionar `MCP Data - RecargaPay` se tiver acesso

### 2. Criar a Routine
Em `claude.ai/code/routines` → New Routine:

- **Name:** `VoC Report Semanal — RecargaPay`
- **Repository:** este repositório (`voc-automation`)
- **Prompt inicial:** colar o conteúdo abaixo
- **Trigger:** Schedule → Weekly → Monday → 11:00 UTC (= 08:00 BRT)
- **Connectors:** manter AgentCore + Slack + MCP Data RP; remover os demais

**Prompt a colar na Routine:**
```
Execute o pipeline completo de reports VoC conforme o SKILL.md deste repositório.

Período: semana anterior completa em BRT (segunda 00:00 a domingo 23:59).
Calcule as datas corretas a partir da data de hoje.
Use o arquivo canais.json para o mapeamento de canais e verticais.

Prioridade de MCP para Zendesk: [TEST] MCP Gateway AWS AgentCore (tool zendesk___zendesk).

Siga todas as fases em sequência: Slack contexto → NPS → Zendesk por vertical → geração e envio.
Em caso de falha em um MCP, registre ⚠️ e continue as demais fases.
```

### 3. Testar antes de ativar
Na página da Routine, usar **Run now** para testar.

**Recomendado:** antes do primeiro envio real, ativar o "modo teste" alterando
o prompt para redirecionar todos os reports para um canal de teste específico.
Adicionar no final do prompt:
```
MODO TESTE: redirecionar todos os reports para o canal #artur-teste (ou similar).
Identificar cada bloco com o canal de destino original.
```

---

## Arquivos do repositório

```
voc-automation/
├── SKILL.md          ← lógica principal da Routine (este é o "cérebro")
├── canais.json       ← mapeamento canal Slack → verticais → tags Zendesk
└── README.md         ← este arquivo
```

### Editar o mapeamento de verticais
Para adicionar/remover verticais de um canal: editar `canais.json`.
Para mudar a lógica de geração dos reports: editar `SKILL.md`.
Mudanças no repositório são aplicadas na próxima execução da Routine.

---

## Limites e considerações

| Aspecto | Detalhe |
|---|---|
| Execuções diárias | Pro: 5/dia · Max: 15/dia · Team/Enterprise: 25/dia |
| A Routine consome | Mesmo limite das sessões interativas do Claude Code |
| Duração estimada | 30–60 min por execução (muitas queries Zendesk + envios Slack) |
| Recomendação | Usar plano **Max** para garantir quota suficiente |
| Se a Routine for pulada | Executa automaticamente na próxima abertura do app (Cowork) ou no próximo trigger (cloud) |

---

## Perguntas frequentes

**O report vai com o meu nome no Slack?**
Sim. As mensagens enviadas via Slack MCP aparecem com a identidade da conta que autenticou o connector. Cada membro do time envia com o seu próprio nome/conta.

**Posso rodar on-demand fora do agendamento?**
Sim. Use "Run now" na página da Routine, ou adicione um trigger de API à Routine para acionar via HTTP POST.

**Como ajustar o período (ex: rodar para o mês anterior)?**
Edite o prompt da Routine temporariamente antes de usar "Run now". Restaure depois.

**O que acontece se o Zendesk AgentCore estiver fora?**
A seção de dados fica marcada com ⚠️. O report ainda é enviado com os dados disponíveis de outras fontes (Slack contexto, NPS).

---

## Contato
Dúvidas: Artur Nunes — `@artur.nunes` no Slack ou artur.nunes@recargapay.com
