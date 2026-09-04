# VoC Análise por Vertical (Dashboard 156) — Setup Guide

Rotina independente do pipeline semanal de reports (Routine A/B, documentado no
`README.md` principal) e da rotina intraday (`README-INTRADAY.md`). Roda segunda, terça
e sexta-feira às 11h e escreve uma Análise VoC com IA direto no painel Arturito 156
("CXM — Experiência do Produto") — nunca posta no Slack.

**Responsável:** Artur Nunes (artur.nunes@recargapay.com)
**Criado em:** Setembro 2026

---

## O que essa Routine faz, em uma frase

Para cada uma das 26 verticais do dashboard 156, ela busca os dados no Databricks,
cruza com eventos/incidentes mapeados no Slack, detecta temas novos ou em crescimento, e
escreve uma Análise VoC de 5 blocos (Cenário, Principais Temas, Alerta de Novo Tema,
Destaque Positivo, Exemplos Reais) direto no card do painel — para as 9 verticais com
NPS Transacional, escreve uma segunda análise focada em NPS.

**O que ela não faz:** não substitui o report semanal nem a rotina intraday, não posta
em nenhum canal Slack, e não toca na Análise VoC de cada motivo de contato individual
(esse card continua calculado por SQL, sem IA).

---

## Por que ela é separada do pipeline semanal e da rotina intraday

Cadência, propósito e destino de saída completamente diferentes das outras duas
Routines deste repositório. Por isso:

- Usa um **arquivo de lógica próprio** (`SKILL-PRODUCT-VERTICAL.md`), não o `SKILL.md`
  do pipeline semanal nem o `SKILL-INTRADAY.md`
- Usa **arquivos de referência próprios**, com o prefixo `skill-product-vertical-`
  (mesmo padrão de `skill-databricks-mcp.md`/`skill-zendesk-cx.md` do pipeline semanal)
- **Lê** `canais.json` e `mapeamento-responsaveis.json` como referência (mesmo
  mapeamento vertical → squad → canal → responsável já usado pelas outras duas
  Routines), mas **nunca os edita** — mesmo princípio já aplicado pela rotina intraday
- **Nunca envia mensagem ao Slack** — o Slack é usado só como fonte de leitura
  (mapeamento de eventos), o destino de escrita é sempre o painel Arturito

---

## Pré-requisitos

### MCPs necessários

| MCP | Finalidade | Obrigatório |
|---|---|---|
| `MCP Data - RecargaPay` | Queries Databricks (NPS, CSAT, volume, motivos) + leitura/escrita do painel Arturito 156 | ✅ Sim |
| `Slack` | Leitura de canais para mapeamento de eventos/incidentes — nunca envia mensagem | ✅ Sim |

### Skills organizacionais (opcional, usadas quando disponíveis)

`cx-product-insights` — fonte primária para métricas oficiais (NPS/CSAT/volume/retenção
de bot via `agg_overview`). Ver `SKILL-PRODUCT-VERTICAL.md` "Arquivos a ler na Fase 0"
para a regra de precedência e o fallback quando ausente.

---

## Setup — passo a passo

### 1. Conectar os MCPs
Em `claude.ai` → Settings → Connectors:
- `MCP Data - RecargaPay` → `https://mcp-data.recargapay.com/mcp`
- Slack MCP — confirmar autenticação com conta RecargaPay

### 2. Criar a Routine

Em `claude.ai/code/routines` → New Routine:

- **Name:** `VoC Análise por Vertical — Dashboard 156`
- **Repository:** `VoC-Product-Reports` (mesmo repositório do pipeline semanal)
- **Trigger:** Schedule → Weekly → Segunda, Terça e Sexta → 14:00 UTC (= 11:00 BRT) —
  se a plataforma de Routines só permitir um dia por agendamento, criar 3 agendamentos
  separados com o mesmo prompt
- **Connectors:** `MCP Data - RecargaPay` + Slack; remover os demais

**Prompt da Routine:**
```
Você é um analista especializado em Voice of Customer (VoC) da RecargaPay, escrevendo
Análises VoC com IA direto no painel Arturito 156, com Claude Sonnet 5.

Execute o pipeline completo conforme as instruções do SKILL-PRODUCT-VERTICAL.md deste
repositório.

CONFIGURAÇÃO
- Determine a janela de análise conforme a Fase 1 do SKILL-PRODUCT-VERTICAL.md (desde a
  última execução registrada em VOC_ANALISE_GERAL/VOC_ANALISE_NPS até agora)
- Modelo: claude-sonnet-5

ARQUIVOS DE REFERÊNCIA — ler na ordem descrita em "Arquivos a ler na Fase 0"
- SKILL-PRODUCT-VERTICAL.md → lógica principal, fases de execução
- skill-product-vertical-events-mapping.md → mapeamento de eventos e squads (aponta
  para canais.json / mapeamento-responsaveis.json deste repositório)
- skill-product-vertical-new-topic-detection.md → regra de detecção de temas novos
- skill-product-vertical-domain-knowledge.md → exceções de domínio e técnicas confirmadas
- skill-product-vertical-example-queries.sql → queries para exemplos com user_id/ticket_id
- skill-product-vertical-editorial-guide.md → tom, estrutura de 5 blocos, regras editoriais

SKILLS ORGANIZACIONAIS — ler na Fase 0, ANTES dos arquivos acima
Tentar /mnt/skills/organization/{nome}/ primeiro, depois /root/.claude/skills/{nome}/
se o primeiro não existir. cx-product-insights é fonte primária para métricas oficiais
via agg_overview; se ausente nos dois caminhos, seguir com as queries já registradas no
dashboard 156, sem bloquear a execução.

MCPs — únicas integrações permitidas
- Dados e painel: MCP Data - RecargaPay (databricks_run_query, arturito_get_dashboard,
  arturito_update_dashboard)
- Contexto de eventos: Slack MCP (somente leitura — esta Routine nunca envia mensagem)
⛔ Não realizar chamadas HTTP diretas a domínios externos.

EXECUÇÃO
Execute as Fases 1 a 6 do SKILL-PRODUCT-VERTICAL.md em sequência, cobrindo as 26
verticais na Análise Geral e as 9 verticais com NPS Transacional na Análise de NPS.
Colete os dados da Fase 1 consolidando queries (uma execução por template, cobrindo
todas as verticais — nunca uma query por vertical). Publique em lotes de 6-8 verticais
por vez (Fase 6) — nunca tudo em uma única chamada de arturito_update_dashboard. Para
cada lote: merge de chaves (nunca substituir o objeto inteiro), validação de sintaxe
completa antes de publicar, e reconferência pós-publicação obrigatória antes de seguir
para o próximo lote. Se qualquer lote falhar em uma validação, pare e reporte — nunca
tente republicar automaticamente sem antes diagnosticar a causa.
```

### 3. Testar antes de ativar

Rodar **Run now** manualmente e conferir, antes de deixar agendado:
- Se a janela de análise foi calculada corretamente (primeira execução: últimos 7 dias)
- Se as 26 verticais receberam entrada em `VOC_ANALISE_GERAL` e as 9 com NPS receberam
  entrada em `VOC_ANALISE_NPS`
- Se a publicação de fato ocorreu em lotes (não numa única chamada gigante) e se cada
  lote passou pela reconferência pós-publicação (Fase 6) antes do próximo começar
- Se nenhuma vertical de execuções anteriores foi perdida (merge, não replace)
- Se o número de chamadas ao Databricks ficou na faixa esperada (~10-14, não 60+)

---

## Ciclo de manutenção

**Sempre que `canais.json` ou `mapeamento-responsaveis.json` mudar** (mantidos pelo
pipeline semanal): nada a fazer nesta rotina — ela lê os arquivos atualizados na
próxima execução automaticamente.

**Se uma nova vertical for adicionada ao dashboard 156** (array `VERTICALS` do JS):
atualizar a tabela de correspondência em `skill-product-vertical-events-mapping.md`.

**A cada sprint ou quando necessário:**
- Revisar se a regra de detecção de temas novos (`skill-product-vertical-new-topic-detection.md`)
  está gerando alertas úteis ou ruído, ajustando os thresholds se necessário
- Confirmar que o merge de chaves na Fase 6 não está, em algum caso, sobrescrevendo
  verticais de execuções anteriores por engano

---

## Limites e considerações

| Aspecto | Detalhe |
|---|---|
| Execuções semanais | 3 (segunda, terça, sexta) |
| Duração estimada por execução | 20–40 min (26 verticais na Análise Geral + 9 na de NPS) |
| Modelo | Claude Sonnet 5 (`claude-sonnet-5`) |
| Destino | Painel Arturito 156 — nunca Slack |

---

## Perguntas frequentes

**Por que a janela de análise varia de tamanho?**
A rotina roda 3x por semana; a janela é sempre "desde a última execução até agora" —
tipicamente 1 dia após terça, 3-4 dias após segunda/sexta. Isso é esperado.

**O que acontece se uma vertical não tiver dado suficiente na janela?**
A rotina ainda escreve uma entrada para ela, dizendo isso explicitamente em cada bloco
afetado — nunca pula a vertical inteira.

**Por que os subverticais de Pix e Empréstimo às vezes não são atualizados?**
Cobertura opcional — só são escritos quando há volume suficiente na janela para uma
leitura própria (ver `SKILL-PRODUCT-VERTICAL.md` Fase 5).

**O que acontece se o Slack MCP falhar?**
A rotina segue sem a tabela de eventos — a análise é escrita mesmo assim, só sem
correlação com eventos/incidentes daquela janela.

---

## Contato
Dúvidas: Artur Nunes — `@artur.nunes` no Slack ou artur.nunes@recargapay.com
