# Governança de Dados — VoC & CXM RecargaPay

**Compilado a partir de:** pipeline semanal de reports VoC (Routine A/B) e monitoramento
intraday, ambos RecargaPay/CXM.
**Última atualização:** Agosto 2026
**Mantenedor:** Artur Nunes (artur.nunes@recargapay.com)
**Propósito deste documento:** consolidar, num único lugar organizado por domínio de
dado (não por rotina), todas as queries, mapeamentos e definições já validadas em
produção — para uso na construção de outros painéis, análises e materiais além das
automações que originaram este conteúdo.

**Como usar:** cada seção documenta a fonte de verdade, a query de referência, e — onde
relevante — armadilhas já identificadas empiricamente (nomes de coluna incorretos que
pareciam certos, tabelas bloqueadas por governança, ambiguidades resolvidas). Onde uma
informação não foi confirmada com 100% de certeza, isso está marcado explicitamente com
⚠️ — não trate como fonte de verdade sem validar antes de um uso crítico.

---

## Sumário

1. [Arquitetura de Fontes de Dados — Visão Geral](#1-arquitetura-de-fontes-de-dados--visão-geral)
2. [Mapeamento de Squads e Verticais](#2-mapeamento-de-squads-e-verticais)
3. [Métricas Oficiais — Catálogo (`agg_overview`)](#3-métricas-oficiais--catálogo-agg_overview)
4. [Distribuição de Volume — N1 / N2 / Bot / Automação](#4-distribuição-de-volume--n1--n2--bot--automação)
5. [Retenção de Bot](#5-retenção-de-bot)
6. [NPS, CSAT e Pesquisas (`fat_indecx_metrics`)](#6-nps-csat-e-pesquisas-fat_indecx_metrics)
7. [Central de Ajuda e NFHR (`fat_help_center_events`)](#7-central-de-ajuda-e-nfhr-fat_help_center_events)
8. [Tabelas Granulares de Ticket](#8-tabelas-granulares-de-ticket)
9. [Bugs](#9-bugs)
10. [Tabela de Eventos e Incidentes — Metodologia](#10-tabela-de-eventos-e-incidentes--metodologia)
11. [Amplitude — Taxonomia e Acesso a Artigos](#11-amplitude--taxonomia-e-acesso-a-artigos)
12. [Regras de Exclusão e Qualidade de Dado — Consolidado](#12-regras-de-exclusão-e-qualidade-de-dado--consolidado)
13. [Apêndice — Histórico de Correções](#13-apêndice--histórico-de-correções)

---

## 1. Arquitetura de Fontes de Dados — Visão Geral

| Fonte | Tipo | Granularidade | Defasagem | Uso principal |
|---|---|---|---|---|
| `prod.cx.agg_overview` | Databricks, agregada | Diária (exceto `source='central'`, mensal) | T-1 | Métricas oficiais: NPS Tx, CSAT, volume, retenção, HCE, NFHR, Contact Rate, Bugs, TMR/TMO |
| `prod.cx.dim_zendesk_tickets_summary` | Databricks, granular | Por ticket | T-1 | Investigação granular (motivo, causa raiz, dimensões completas) — nunca para agregado |
| `prod.cx.fat_botmaker_metrics` | Databricks, granular | Por ticket/sessão (`id_ticket`) | T-1 | Retenção de bot precisa, `flg_passive_abandonment` |
| `prod.cx.agg_botmaker_metrics` | Databricks, agregada | Diária, por `stage`/tema/fluxo | T-1 | Série histórica de bot, ranking por estágio — aproximação, não exata |
| `prod.cx.fat_help_center_events` | Databricks, granular (evento) | Por evento — permite `GROUP BY` semanal/diário | T-1 | Acessos à Central de Ajuda, NFHR |
| `prod.cx.fat_indecx_metrics` | Databricks, granular | Por resposta de pesquisa | T-1 | NPS, CSAT, NPS Relacional a nível de respondente |
| `prod.cx.fat_ticket_time` | Databricks, granular | Por evento de atendimento | T-1 | TMO/TMR granular por ticket |
| `prod.cx.amplitude_datamart` | Databricks, granular | Por usuário (mais recente) | T-1 | Dispositivo/plataforma do usuário |
| `prod.cx.fat_tickets_transcription(_summary)` | Databricks, granular | Por ticket | T-1 (raw a partir de mai/2026; summary atualiza semanalmente) | Leitura qualitativa profunda / resumo por IA |
| `prod.core.fat_order` | Databricks, governado | Por pedido | T-1 | Classificação New/NewNew/Repeat |
| `prod.credit_card.dim_card_account` | Databricks, governado | Por conta de cartão | T-1 | Tipo de cartão (substitui tabela `rwd` bloqueada) |
| Zendesk (live, via MCP) | API ao vivo | Por ticket, tempo real | Nenhuma | Dados de hoje, quando período fechado ainda não fecha o dia corrente |
| Amplitude (via `query_dataset`/`search`) | API ao vivo | Por evento | Nenhuma (mas taxonomia fragmentada — ver §11) | Acesso a artigos específicos da Central de Ajuda, em tempo real |
| Google Sheets — planilha IndeCX sincronizada | Live (sync externo, 30 min) | Por resposta | ~30 min | NPS/CSAT/NPS Relacional em cadência quase real-time, sem depender da API IndeCX direta (bloqueada por rede no ambiente de execução das Routines) |
| Slack (canais estratégicos + `#escalation_incidents`) | Live | Por mensagem | Nenhuma | Contexto de eventos/incidentes para correlação |

**Regra fundamental:** `agg_overview` é a fonte de verdade para qualquer número
agregado/oficial (volume, NPS, CSAT, etc.) — nunca reconstruir esses números a partir de
`dim_zendesk_tickets_summary` ou de contagem manual de tickets. As tabelas granulares
(`dim_zendesk_tickets_summary`, `fat_botmaker_metrics`, `fat_ticket_time`, etc.) servem
para investigação específica (ticket individual, cruzamento por dimensão que o agregado
não tem), nunca para recalcular um total que `agg_overview` já fornece.

---

## 2. Mapeamento de Squads e Verticais

### 2.1 Tabela completa — vertical, canal Slack, tags Zendesk, granularidade em `agg_overview`

| Vertical | Canal Slack | Tags Zendesk (live) | Vertical em `agg_overview` | Observação |
|---|---|---|---|---|
| Minha Conta | `#account_cx` | `minha_conta`, `minha_conta_logado` | `minha conta` | Separada — sem gap |
| Cartão de Crédito | `#cc-produto-e-cx` | `cartão_de_crédito_da_recargapay` | `cartao de credito do recargapay` | Separada — sem gap |
| Conta Desativada | `#cx_fraud` | `conta_desativada` | `conta desativada` | Separada — sem gap |
| Carteira Desativada | `#cx_fraud` | `carteira_desativada` | `carteira desativada` | Separada — sem gap |
| Chargeback Recovery | `#cx_fraud` | `chargeback_recovery_vertical` | `chargeback recovery` | Separada — sem gap |
| CDB | `#investments-e-cx` | `cdb` | `cdb` | Separada — sem gap |
| Rendimento CDI | `#investments-e-cx` | `rendimento_cdi` | ⚠️ agregada em `cashback e rendimento` | Misturada com cashback geral — usar `dim_zendesk_tickets_summary` (`vertical='rendimento cdi'`) para isolar |
| Movimentações Financeiras | `#investments-e-cx` | `movimentações_financeiras` | `movimentacoes financeiras` | Separada — sem gap |
| Transporte | `#melhoria-continua-verticais` | `transporte_vertical` | `transporte` | Separada — sem gap |
| Contas e Boletos | `#melhoria-continua-verticais` | `contas_e_boletos_` | ⚠️ agregada em `utilities` | Junto com Boleto de Cobrança — usar `dim_zendesk_tickets_summary` (`vertical='contas e boletos'`) |
| Boleto de Cobrança | `#melhoria-continua-verticais` | `boleto_de_cobrança` | ⚠️ agregada em `utilities` | Junto com Contas e Boletos — usar `dim_zendesk_tickets_summary` (`vertical='boleto de cobranca'`). Tag confirmada — vertical existe (gap anterior era erro de mapeamento, não ausência real) |
| Recarga de Celular | `#melhoria-continua-verticais` | `recarga_de_celular_vertical` | `topup` | Mapeia limpo — nome diferente do esperado, mas sem agregação |
| Pix (In/Out/Chaves) | `#pixcc-home-raf-cx` | `pix-in`, `pix-out`, `pix-chaves_pix` | ⚠️ agregada em `pix`, sem subtipo | Usar `dim_zendesk_tickets_summary` com `vertical LIKE 'pix::%'` para separar In/Out/Chaves |
| Pix CC | `#pixcc-home-raf-cx` | **sem tag própria** | ⚠️ agregada em `pix` | Identificar via busca textual por "cartão"/"cartao" em `reason_contact`/`root_cause` de tickets `pix-out` |
| RAF | `#pixcc-home-raf-cx` | `raf-indicado`, `raf-indicador` | ⚠️ agregada em `raf`, sem subtipo | Usar `dim_zendesk_tickets_summary` com `vertical LIKE 'raf::%'` |
| Empréstimo | `#squad_loan_seguimento` | `empréstimo_`, `empréstimo_crédito_consignado` | `emprestimo` | Separada — sem gap |
| Tap to Pay | `#subacquirer-cx` | `tap_to_pay` | `tap to pay` | Separada — sem gap |
| Link de Pagamento | `#subacquirer-cx` | `link_de_pagamento` | `link de pagamento` | Separada — sem gap |

**Regra geral para verticais agregadas:** NPS/CSAT desses produtos só estão disponíveis
no nível do grupo maior via `agg_overview`. Para volume e motivos/causas com precisão
no produto específico, complementar sempre com `dim_zendesk_tickets_summary` filtrando
o `vertical` exato — sinalizar essa limitação sempre que usado.

### 2.2 Responsável de CXM por vertical (para menção/atribuição)

| Vertical | Responsável | Squad de origem (planilha) |
|---|---|---|
| Minha Conta, Conta Desativada, Carteira Desativada, Chargeback Recovery | Anderson Fernandes | Account + conta desativada / COps + Carteira desativada & Chargeback |
| Cartão de Crédito, CDB, Rendimento CDI, Movimentações Financeiras, Tap to Pay, Link de Pagamento | Alexandre Luz | Credit Card / Inversiones / Sub-Acquirer |
| Pix, Pix CC | Eduardo Reis | Pix / PIX CC |
| RAF, Empréstimo | Cassio Mitherhofer | Home, RAF e Landing Pages / Lending |
| Transporte, Recarga de Celular, Contas e Boletos, Boleto de Cobrança | **On Demand** (sem responsável fixo) | Transporte e Topup / Bills |

⚠️ Fonte: planilha Google Sheets de squads (sincronizada manualmente — não há leitura
automática de Google Sheets pelas ferramentas usadas). Revalidar periodicamente contra a
planilha original.


---

## 3. Métricas Oficiais — Catálogo (`agg_overview`)

Fonte primária: skill organizacional `cx-product-insights` (`references/metrics.yml`).
Todas as 14 métricas abaixo usam **`prod.cx.agg_overview`** como única fonte —
nunca reconstruir a partir de tabelas granulares.

### CX-001 — NPS Tx (NPS Transacional)

(promotores − detratores) / total de respondentes × 100.

```sql
SELECT
  date,
  SUM(CASE WHEN metric = 'nps tx' THEN promoter_like_count END) AS promoters,
  SUM(CASE WHEN metric = 'nps tx' THEN detractor_dislike_count END) AS detractors,
  SUM(CASE WHEN metric = 'nps tx' THEN neutral_count END) AS neutrals,
  (
    SUM(CASE WHEN metric = 'nps tx' THEN promoter_like_count END)
    - SUM(CASE WHEN metric = 'nps tx' THEN detractor_dislike_count END)
  )
  /
  NULLIF(
    (
      SUM(CASE WHEN metric = 'nps tx' THEN promoter_like_count END)
      + SUM(CASE WHEN metric = 'nps tx' THEN detractor_dislike_count END)
      + SUM(CASE WHEN metric = 'nps tx' THEN neutral_count END)
    ), 0
  ) * 100 AS nps_tx
FROM prod.cx.agg_overview
WHERE metric = 'nps tx'
GROUP BY date
ORDER BY date
```

### CX-002 — CSAT

% de avaliações positivas, restrito aos canais N1 (`c2c`, `chat online`, `e-mail`) —
esse filtro de canal já faz parte da definição oficial da métrica, não é um recorte
posterior.

```sql
SELECT
  date,
  SUM(CASE WHEN metric = 'csat' AND friendly_service_channel IN ('c2c', 'chat online', 'e-mail')
      THEN promoter_like_count END) AS likes,
  SUM(CASE WHEN metric = 'csat' AND friendly_service_channel IN ('c2c', 'chat online', 'e-mail')
      THEN detractor_dislike_count END) AS dislikes,
  SUM(CASE WHEN metric = 'csat' AND friendly_service_channel IN ('c2c', 'chat online', 'e-mail')
      THEN neutral_count END) AS neutrals,
  SUM(CASE WHEN metric = 'csat' AND friendly_service_channel IN ('c2c', 'chat online', 'e-mail')
      THEN promoter_like_count END)
  /
  NULLIF(
    SUM(CASE WHEN metric = 'csat' AND friendly_service_channel IN ('c2c', 'chat online', 'e-mail')
        THEN promoter_like_count END)
    + SUM(CASE WHEN metric = 'csat' AND friendly_service_channel IN ('c2c', 'chat online', 'e-mail')
        THEN detractor_dislike_count END)
    + SUM(CASE WHEN metric = 'csat' AND friendly_service_channel IN ('c2c', 'chat online', 'e-mail')
        THEN neutral_count END)
  , 0) AS csat
FROM prod.cx.agg_overview
WHERE metric = 'csat'
  AND friendly_service_channel IN ('c2c', 'chat online', 'e-mail')
GROUP BY date
ORDER BY date
```

### CX-003 — Tickets (Contatos totais, humano + bot)

```sql
SELECT
  date,
  SUM(CASE WHEN flg_human = true OR flg_retention_bot = true
      THEN ticket_count END) AS tickets
FROM prod.cx.agg_overview
WHERE source = 'tickets'
  AND (flg_human = true OR flg_retention_bot = true)
GROUP BY date
ORDER BY date
```

### CX-004 — Tickets Bot (retidos pelo bot)

```sql
SELECT
  date,
  SUM(CASE WHEN flg_retention_bot = true
      THEN ticket_count END) AS tickets_bot
FROM prod.cx.agg_overview
WHERE source = 'tickets'
  AND flg_retention_bot = true
GROUP BY date
ORDER BY date
```

### CX-005 — Retenção Bot (% do total de contatos retido pelo bot)

```sql
SELECT
  date,
  SUM(CASE WHEN flg_retention_bot = true THEN ticket_count END) AS tickets_bot,
  SUM(CASE WHEN flg_human = true OR flg_retention_bot = true THEN ticket_count END) AS tickets_total,
  SUM(CASE WHEN flg_retention_bot = true THEN ticket_count END)
  /
  NULLIF(
    SUM(CASE WHEN flg_human = true OR flg_retention_bot = true THEN ticket_count END)
  , 0) AS bot_retention
FROM prod.cx.agg_overview
WHERE source = 'tickets'
GROUP BY date
ORDER BY date
```

> ⚠️ Esta é a retenção **no nível de canal N1/N2** (distribuição de volume). Para a taxa
> de retenção do bot em si, com precisão de sessão, ver §5 — são métricas complementares,
> não substitutas.

### CX-006 — HCE (Help Center Efficiency)

% de visitantes únicos à Central de Ajuda que **não** precisaram abrir ticket.

```sql
WITH tickets AS (
  SELECT date,
    SUM(CASE WHEN flg_human = true OR flg_retention_bot = true THEN ticket_count END) AS tickets
  FROM prod.cx.agg_overview
  WHERE source = 'tickets'
  GROUP BY date
),
visitas AS (
  SELECT date,
    SUM(CASE WHEN metric = 'vertical' AND product = 'total' AND vertical IS NOT NULL
        THEN visit_unic_count END) AS visitas_unicas_vertical
  FROM prod.cx.agg_overview
  WHERE source = 'central'
  GROUP BY date
)
SELECT
  COALESCE(t.date, v.date) AS date,
  t.tickets,
  v.visitas_unicas_vertical,
  1 - (t.tickets / NULLIF(v.visitas_unicas_vertical, 0)) AS hce
FROM tickets t
FULL OUTER JOIN visitas v ON t.date = v.date
ORDER BY date
```

### CX-007 — NFHR (Need For Help Rate)

⚠️ **O denominador é volume de transações (TX), não Active Users** — apesar do nome
sugerir o contrário.

```sql
WITH visitas AS (
  SELECT date,
    SUM(CASE WHEN metric = 'vertical' AND product = 'total' AND vertical IS NOT NULL
        THEN visit_unic_count END) AS visitas_unicas_vertical
  FROM prod.cx.agg_overview
  WHERE source = 'central'
  GROUP BY date
),
tx_prod AS (
  SELECT date,
    SUM(CASE WHEN vertical <> 'core' THEN tx END) AS tx_prod
  FROM prod.cx.agg_overview
  GROUP BY date
)
SELECT
  COALESCE(v.date, t.date) AS date,
  v.visitas_unicas_vertical,
  t.tx_prod,
  v.visitas_unicas_vertical / NULLIF(t.tx_prod, 0) AS nfhr
FROM visitas v
FULL OUTER JOIN tx_prod t ON v.date = t.date
ORDER BY date
```

> ⚠️ **Alternativa validada empiricamente para o numerador** (ver §7): quando a análise
> precisa de granularidade semanal (não diária) ou por vertical específica, usar
> `COUNT(DISTINCT CONCAT(userid, '-', session_id))` via `fat_help_center_events` em vez
> de `visit_unic_count` de `agg_overview` — mesma métrica, fonte alternativa com mais
> flexibilidade de agrupamento. Ver §7 para as queries completas e a regra crítica de
> nunca somar entre dimensões.

### CX-008 — Contact Rate (produto)

```sql
WITH tickets AS (
  SELECT date,
    SUM(CASE WHEN flg_human = true OR flg_retention_bot = true THEN ticket_count END) AS tickets
  FROM prod.cx.agg_overview
  WHERE source = 'tickets'
  GROUP BY date
),
tx_prod AS (
  SELECT date,
    SUM(CASE WHEN vertical <> 'core' THEN tx END) AS tx_prod
  FROM prod.cx.agg_overview
  GROUP BY date
)
SELECT
  COALESCE(tk.date, tx.date) AS date,
  tk.tickets,
  tx.tx_prod,
  tk.tickets / NULLIF(tx.tx_prod, 0) AS contact_rate
FROM tickets tk
FULL OUTER JOIN tx_prod tx ON tk.date = tx.date
ORDER BY date
```

### CX-009 — Visitas Únicas Vertical

```sql
SELECT
  date,
  SUM(CASE WHEN metric = 'vertical' AND product = 'total' AND vertical IS NOT NULL
      THEN visit_unic_count END) AS visitas_unicas_vertical
FROM prod.cx.agg_overview
WHERE source = 'central'
  AND metric = 'vertical'
  AND product = 'total'
  AND vertical IS NOT NULL
GROUP BY date
ORDER BY date
```

> ⚠️ Esta fonte (`agg_overview source='central'`) é **mensal**, ancorada no dia 1 do mês
> — não serve para série semanal/diária. Ver §7 para a alternativa semanal real via
> `fat_help_center_events`.

### CX-010 — Active Users (AU) ⛔ nunca reportar isoladamente

Insumo interno de outras métricas — **nunca mencionar diretamente em nenhum report**.
Agregado **mensal** (data ancorada no dia 1) — não somar com granularidade diária.

```sql
SELECT
  date,
  SUM(au) AS active_users
FROM prod.cx.agg_overview
WHERE vertical <> 'core'
  AND au IS NOT NULL
GROUP BY date
ORDER BY date
```

### CX-011 — Transactions (TX) ⛔ nunca reportar isoladamente

Insumo interno de NFHR/Contact Rate — não é métrica final de report.

```sql
SELECT
  date,
  SUM(tx) AS transactions
FROM prod.cx.agg_overview
WHERE vertical <> 'core'
  AND tx IS NOT NULL
GROUP BY date
ORDER BY date
```

### CX-013 — Bugs

```sql
SELECT
  date,
  SUM(bug_count) AS bugs
FROM prod.cx.agg_overview
WHERE source = 'bugs'
GROUP BY date
ORDER BY date
```

### CX-014 — TMR (Tempo Médio de Resolução)

Resultado em dias (segundos ÷ 86400). ⚠️ TMR costuma passar de 24h — o `hh:mm:ss` é
total acumulado, não horário do dia.

```sql
SELECT
  date,
  SUM(CASE WHEN metric = 'resolution' THEN duration_sec_sum END) AS duration_sec_sum,
  SUM(CASE WHEN metric = 'resolution' THEN duration_count END) AS duration_count,
  (
    SUM(CASE WHEN metric = 'resolution' THEN duration_sec_sum END)
    / NULLIF(SUM(CASE WHEN metric = 'resolution' THEN duration_count END), 0)
  ) / 86400 AS tmr_dias
FROM prod.cx.agg_overview
WHERE source = 'tempos'
  AND metric = 'resolution'
GROUP BY date
ORDER BY date
```

### CX-015 — TMO (Tempo Médio de Ocupação)

Mesma lógica de CX-014, com `metric = 'occupation'`.

```sql
SELECT
  date,
  SUM(CASE WHEN metric = 'occupation' THEN duration_sec_sum END) AS duration_sec_sum,
  SUM(CASE WHEN metric = 'occupation' THEN duration_count END) AS duration_count,
  (
    SUM(CASE WHEN metric = 'occupation' THEN duration_sec_sum END)
    / NULLIF(SUM(CASE WHEN metric = 'occupation' THEN duration_count END), 0)
  ) / 86400 AS tmo_dias
FROM prod.cx.agg_overview
WHERE source = 'tempos'
  AND metric = 'occupation'
GROUP BY date
ORDER BY date
```


---

## 4. Distribuição de Volume — N1 / N2 / Bot / Automação

Fonte: Dashboard Arturito #103 ("Bot & IA Agent", `optimus.recargapay.com`), query
`sss_daily` — validada com dado real de produção (identidades matemáticas confirmadas:
`bot_auto = auto + bot_maker`; `tickets = humano + bot_auto` em linhas N1).

```sql
SELECT 
  to_date(created_at_br) AS d, 
  CASE WHEN friendly_service_channel IN ('e-mail', 'chat online', 'c2c') THEN 'n1' ELSE 'n2' END AS level, 
  COUNT(DISTINCT CASE WHEN ((flg_retention_automation = True OR flg_retention_bot = True OR flg_invalid_bot = True) 
       AND friendly_service_channel IN ('e-mail', 'chat online', 'c2c')) THEN id_ticket END) AS bot_auto,
  COUNT(DISTINCT CASE WHEN (flg_retention_automation = True AND friendly_service_channel = 'e-mail') 
       THEN id_ticket END) AS auto,
  COUNT(DISTINCT CASE WHEN ((flg_retention_bot = True OR flg_invalid_bot = True) AND friendly_service_channel = 'chat online') 
       THEN id_ticket END) AS bot_maker,
  COUNT(DISTINCT CASE WHEN ((flg_retention_bot = True OR flg_invalid_bot = True) AND friendly_service_channel = 'social media') 
       THEN id_ticket END) AS bot_social,
  COUNT(DISTINCT CASE WHEN flg_human = True THEN id_ticket END) AS humano,
  COUNT(DISTINCT id_ticket) AS tickets
FROM prod.cx.dim_zendesk_tickets_summary s 
LEFT JOIN prod.cx.fat_botmaker_metrics b USING (id_ticket) 
WHERE friendly_service_channel != 'derivacao' 
  AND (b.flg_passive_abandonment = 0 OR b.flg_passive_abandonment IS NULL)
  AND created_at_br BETWEEN '{DATA_INICIO}' AND '{DATA_FIM}'
GROUP BY ALL ORDER BY d;
```

**Leitura dos campos:**
- `bot_auto` = `auto + bot_maker` — bot + automação combinados dentro de N1
- `tickets` = `humano + bot_auto` para linhas `n1` — categorias mutuamente exclusivas
  após excluir abandono passivo
- `bot_social` só aparece em linhas `n2` (porque `social media` cai no `ELSE 'n2'` do
  `CASE`) — condiz com a decisão de negócio de que redes sociais entram em N2 nesta
  organização de dados, mesmo que o `channel_class4` oficial as classifique como N1
  (ver §12)
- `auto` é restrito ao canal `e-mail` — automação em outros canais N1 entra só no
  `bot_auto` combinado, não em `auto` isolado
- `flg_invalid_bot = True` **conta como bot** aqui — diferente da regra usada em outras
  análises (onde é filtro de exclusão obrigatório, ver §12). Ticket "bot inválido" ainda
  conta como população de bot para fins de distribuição, porque não foi atendido por
  humano.

**Grupos de canal — N1 Humano vs N2 Special Cases (decisão de negócio VoC, não
`channel_class4` oficial):**

| Grupo | `friendly_service_channel` |
|---|---|
| N1 Humano | `chat online`, `c2c`, `e-mail` |
| N2 Special Cases | `special cases`, `ouvidoria`, `social media`, `stores`, `canais especiais` |
| RecargaBot | flag `flg_retention_bot = true` (independente de canal) |

⚠️ Este agrupamento (redes sociais em N2) é intencional e específico do VoC — a
organização classifica social media como N1 no `channel_class4` padrão. Não "corrigir"
para bater com a classificação oficial.

---

## 5. Retenção de Bot

Duas métricas diferentes, ambas legítimas, respondendo perguntas diferentes:

| Métrica | Pergunta que responde | Fonte |
|---|---|---|
| CX-005 / `sss_daily` (§3, §4) | Quantos tickets caem em cada canal (humano/bot/automação)? | `agg_overview` ou `dim_zendesk_tickets_summary` + `fat_botmaker_metrics` |
| Taxa de Retenção (esta seção) | Das sessões do bot, qual % foi retida? | `fat_botmaker_metrics` |

### 5.1 Taxa de Retenção — nível de sessão (fonte mais precisa)

```sql
SELECT
  SUM(CASE WHEN flg_overflow = 0 AND flg_passive_abandonment = 0 THEN 1 ELSE 0 END)
    / COUNT(*) AS taxa_retencao
FROM prod.cx.fat_botmaker_metrics
WHERE {filtros de período/vertical}
```

Retido = sessão que **não** transbordou (`flg_overflow = 0`) **e não** foi abandono
passivo (`flg_passive_abandonment = 0`). **Abandono ativo conta como retido**
(`flg_active_abandonment = 1` não entra na exclusão) — o cliente interagiu de fato, só
não teve o problema resolvido; a exclusão é só de quem nem chegou a interagir.

### 5.2 Taxa de Retenção — nível agregado (`agg_botmaker_metrics`), aproximado

```sql
SELECT
  SUM(total_sessions - overflow - passive_abandonment) / SUM(total_sessions) AS taxa_retencao
FROM prod.cx.agg_botmaker_metrics
WHERE {filtros de período/stage}
```

⚠️ **Aproximação, não fonte exata** — as categorias (`overflow`, `active_abandonment`,
`passive_abandonment`) podem se sobrepor quando somadas linha a linha em janelas
maiores nesta tabela agregada. Confirmado comparando contra `fat_botmaker_metrics`
(nível de sessão, onde as 3 flags são mutuamente exclusivas e a soma bate exatamente).
Usar `fat_botmaker_metrics` sempre que precisão importar (métrica oficial, threshold de
alerta); `agg_botmaker_metrics` serve bem para tendência agregada e ranking por estágio.

### 5.3 Tabelas de bot — schema de referência

| Tabela | Granularidade | Colunas-chave |
|---|---|---|
| `prod.cx.fat_botmaker_metrics` | Por ticket (`id_ticket`) | `flg_overflow`, `flg_passive_abandonment`, `flg_active_abandonment`, `not_understood_count`, `executing_intents_total_count`, `time_bot_seconds`, `time_user_seconds` |
| `prod.cx.agg_botmaker_metrics` | Diária, por `stage`/`entry_theme`/`conversation_theme`/fluxo | `total_sessions`, `attended_by_bot`, `retained_by_bot`, `overflow`, `passive_abandonment`, `active_abandonment`, `fcr_bot_count`, `fcr_bot_stage_count`, `csat_promoter`, `csat_answered`, `user_id`, `flg_hyperpersonalized`, `flg_generative`, `flg_static` |

### 5.4 Ranking de estágios (identificar temas de não-retenção)

```sql
SELECT
  stage,
  SUM(total_sessions) AS sess,
  SUM(retained_by_bot) AS ret,
  SUM(overflow) AS ovf,
  SUM(active_abandonment) AS aab,
  SUM(passive_abandonment) AS pab,
  SUM(fcr_bot_stage_count) AS fcr,
  SUM(csat_promoter) AS cprom,
  SUM(csat_answered) AS cans,
  ROUND(SUM(retained_by_bot) / NULLIF(SUM(total_sessions), 0) * 100, 1) AS pct_retencao
FROM prod.cx.agg_botmaker_metrics
WHERE creation_date BETWEEN '{DATA_INICIO}' AND '{DATA_FIM}' AND stage IS NOT NULL
GROUP BY stage
ORDER BY sess DESC
LIMIT 18;
```

Para "temas de não-retenção": ordenar por `pct_retencao ASC` com
`HAVING SUM(total_sessions) >= 10` — olhar `overflow` (transbordo intencional) vs
`passive_abandonment`/`active_abandonment` (desistência do cliente) para diferenciar a
causa.

### 5.5 CSAT do bot por fluxo (`action_name` confirmados)

Via `fat_indecx_metrics`, campo `metric = 'csat-1-5'` + lista de `action_name`
confirmada em produção (Dashboard #103, query `csat_auto_daily`):

```sql
SELECT DATE(answer_date) AS d,
  SUM(CASE WHEN review_class = 'promotor' THEN 1 ELSE 0 END) AS promoter_count,
  SUM(CASE WHEN review_class = 'neutro'   THEN 1 ELSE 0 END) AS neutral_count,
  SUM(CASE WHEN review_class = 'detrator' THEN 1 ELSE 0 END) AS detractor_count
FROM prod.cx.fat_indecx_metrics
WHERE answer_date BETWEEN '{DATA_INICIO}' AND '{DATA_FIM}'
  AND metric = 'csat-1-5'
  AND action_name IN (
    'bot raf: problemas na indicação','bot pix: denúncia de fraude',
    'csat bot fluxo cc rp cancelamento','bot cartão rp: ativação',
    'bot cartão rp: vencimento','bot cartão rp: cashback','bot cartão rp: fatura',
    'bot cartão rp: saldo reservado','csat bot fluxo cc rp rendimento',
    'bot cartão rp: pré-aprovado','bot cartão rp: solicitação',
    'bot cartão rp: modalidade','bot cartão rp: empréstimo','bot cartão rp: entrega',
    'csat bot saldo não utilizado','bot fraude: declined',
    'bot  benefícios: bônus carteira','bot pix: infração pix',
    'bot cartão rp: conta cartão desativada','bot unificado (eteg)',
    'bot transporte: validação recarga','csat bot timeou transporte',
    'csat bot timeou blocked','csat bot timeou wallet',
    'bot fraude: transação bloqueada','bot fraude: carteira bloqueada',
    'bot pix: pix enviado errado','bot empréstimos: pedir empréstimo',
    'bot pagamentos: cc error','bot pagamentos: validação cartão',
    'csat bot fluxo para fraude pix','bot pagamentos: adição de cartão',
    'bot empréstimos: limite','bot minha conta: validação',
    'bot cartão rp: limite garantido','bot cartão rp: resgate de saldo',
    'bot cashback: recebimento','bot pix: compensação de pix',
    'bot contas: compensação de boletos'
  )
GROUP BY ALL ORDER BY d;
```

### 5.6 Cenários de retenção via `knowledge-base-reason` (quando vertical não está no ticket)

82% dos tickets `retencao_chatbot` (tag live Zendesk) não carregam vertical de produto
(carregam `produto_não_identificado`) — são classificados por
`knowledge-base-reason`/`knowledge-base-sub-reason` (tema do artigo de Central de Ajuda
consultado), não por vertical. Tabela de correspondência tema → vertical:

| `knowledge-base-reason` | Vertical correspondente |
|---|---|
| `pix`, `pix-payment` | Pix (In/Out/Chaves) |
| `cartao-recargapay`, `recargapay-cards` | Cartão de Crédito |
| `emprestimo`, `loan-payment`, `emprestimo-consignado` | Empréstimo / Crédito Consignado |
| `investimentos`, `cashback-e-rendimento`, `cashout-collateral` | CDB / Rendimento CDI |
| `account`, `meus-dados-pessoais`, `por-selfie-reconhecimento-facial-com-atendimento` | Minha Conta |
| `tap-to-pay` | Tap to Pay |
| `link-de-pagamento` | Link de Pagamento |
| `transport`, `transport-service-card` | Transporte |
| `roubaram-meu-cartão` | Cartão de Crédito ou Conta Desativada (fraude) — confirmar caso a caso |

⚠️ Tratar como estimativa — a correspondência é por nomenclatura, não uma chave exata.
Maior cenário isolado identificado empiricamente: verificação por selfie/reconhecimento
facial (~18% do volume total de retenção numa amostra semanal) — não é um produto
financeiro específico, atravessa várias jornadas (onboarding, reativação, recuperação
de acesso).


---

## 6. NPS, CSAT e Pesquisas (`fat_indecx_metrics`)

Fonte de pesquisas de satisfação a nível de respondente individual — mais granular que
`agg_overview`.

⚠️ **Duas dimensões de classificação coexistem na tabela, confirmadas separadamente —
não usar uma achando que a outra não existe:**
- `metric` (ex: `'csat-1-5'`) — confirmado via query de produção real (Dashboard #103)
- `review_class`/`survey_type`/`quest_level`/`action_name` — confirmado via
  `support_tables.sql` oficial de `cx-product-insights`

Antes de montar uma query nova, reconciliar com:
```sql
SELECT DISTINCT metric, survey_type, quest_level FROM prod.cx.fat_indecx_metrics LIMIT 30
```

| Campo | Descrição |
|---|---|
| `user_id` | ID do usuário respondente (não `id_ticket` — tabela não tem essa coluna) |
| `review` | Nota dada pelo cliente |
| `review_class` | Classificação — **valores em português:** `promotor`, `neutro`, `detrator` |
| `metric` | Ex: `csat-1-5` — confirmado em uso real para CSAT de bot (ver §5.5) |
| `survey_type` | Ex: `transacional` |
| `quest_level` | `main` = pergunta principal; distinto de perguntas secundárias da mesma pesquisa |
| `action_name` | Nome da ação/pesquisa — **a vertical fica embutida aqui** em pesquisas transacionais gerais, não em um campo `vertical` separado |
| `answer_date` | Data da resposta |
| `deleted` | Filtrar sempre `deleted = false` |

**Confirmar `action_name` exato antes de qualquer query (NPS Transacional geral):**
```sql
SELECT DISTINCT action_name FROM prod.cx.fat_indecx_metrics
WHERE survey_type = 'transacional' AND action_name ILIKE '%{termo}%'
```

**Query padrão — NPS Transacional por produto:**
```sql
SELECT
  COUNT(CASE WHEN review_class = 'promotor' THEN 1 END) AS promotores,
  COUNT(CASE WHEN review_class = 'neutro'   THEN 1 END) AS neutros,
  COUNT(CASE WHEN review_class = 'detrator' THEN 1 END) AS detratores,
  COUNT(*) AS total_respondentes,
  ROUND(
    (COUNT(CASE WHEN review_class = 'promotor' THEN 1 END)
     - COUNT(CASE WHEN review_class = 'detrator' THEN 1 END))
    / NULLIF(COUNT(*), 0) * 100, 1
  ) AS nps_tx
FROM prod.cx.fat_indecx_metrics
WHERE survey_type = 'transacional'
  AND quest_level = 'main'
  AND action_name = '{confirmar via query acima}'
  AND answer_date BETWEEN '{inicio}' AND '{fim}'
  AND deleted = false
```

**Join com dados de ticket** — sempre por `user_id`/`userid`, nunca `id_ticket`:
```sql
LEFT JOIN prod.cx.fat_indecx_metrics m
  ON CAST(t.userid AS STRING) = CAST(m.user_id AS STRING)
```
⚠️ Um usuário pode ter vários tickets no período — join por usuário pode duplicar linha
em `LEFT JOIN` se não tratado com `ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY answer_date DESC)`
e filtro `rn = 1` para pegar só a resposta mais recente.

**Planilha IndeCX sincronizada (Google Sheets, complementar):** existe uma sincronização
externa (fora do ambiente de execução das Routines, contornando bloqueio de rede à API
IndeCX direta) que grava respostas de CSAT Atendimento N1, NPS Relacional (PF/PJ), NPS
Transacional (por produto) e CSAT Ouvidoria em Google Sheets, atualizada a cada 30 min.
Útil quando granularidade quase real-time importa mais que a defasagem T-1 do Databricks.
Ler via `Google Drive:read_file_content` (não `google_drive_fetch`, que só lê Google
Docs, não Sheets).


---

## 7. Central de Ajuda e NFHR (`fat_help_center_events`)

Tabela raw por trás de `agg_overview source='central'` — permite `GROUP BY` semanal ou
diário direto, ao contrário da tabela agregada (mensal, ancorada no dia 1 do mês).
**Preferir esta fonte sempre que granularidade semanal/diária for necessária.**

| Campo | Descrição |
|---|---|
| `userid` | ID do usuário |
| `session_id` | ID da sessão — **usar junto com `userid` para "visita única"** |
| `event_category` | Valores confirmados: `artigo`, `vertical`. `pesquisa`/`ajuda` mencionados em versões anteriores, **não confirmados** |
| `article` | Nome/identificador do artigo. **Tem valor corrompido conhecido** (`'pronto'`) — ver correção abaixo |
| `vertical` | Vertical/produto. Valores de descarte: `nao_mapeado`, `outros` — sempre excluir |
| `date_created_br` | Data do evento (BRT) |

**⚠️ Qualidade de dado conhecida:** `article = 'pronto'` é um valor truncado/corrompido.
Nome real confirmado para esse caso: "paguei meu emprestimo mas nao recebi uma nova
oferta por que". Tratar sempre com `CASE WHEN` (ver Query 7.3).

**⛔ REGRA CRÍTICA — nunca derivar o total de uma dimensão somando outra dimensão.**
`COUNT(DISTINCT CONCAT(userid, '-', session_id))` não se distribui aditivamente entre
dimensões — a soma de visitas únicas por artigo **não bate** com a soma por vertical, que
**não bate** com o total da semana (um mesmo usuário/sessão pode aparecer em mais de um
artigo/vertical na mesma semana). **Sempre rodar a query com o `GROUP BY` exato da
dimensão desejada** — nunca somar uma consulta mais granular para "chegar" no total de
uma menos granular, nem o inverso.

### Query 7.1 — Visitas únicas totais por semana

```sql
SELECT
  DATE(DATE_TRUNC('week', DATE(date_created_br))) AS semana,
  COUNT(DISTINCT CONCAT(userid, '-', session_id)) AS visitas_unicas_semana
FROM prod.cx.fat_help_center_events
WHERE event_category IN ('artigo', 'vertical')
  AND NOT vertical IN ('nao_mapeado', 'outros')
  AND DATE(date_created_br) BETWEEN '{DATA_INICIO}' AND '{DATA_FIM}'
GROUP BY DATE_TRUNC('week', DATE(date_created_br))
ORDER BY semana ASC;
```

### Query 7.2 — Visitas únicas por vertical, por semana

```sql
SELECT
  vertical,
  DATE(DATE_TRUNC('week', DATE(date_created_br))) AS start_of_week,
  COUNT(DISTINCT CONCAT(userid, '-', session_id)) AS visitas_unicas_semana
FROM prod.cx.fat_help_center_events
WHERE event_category = 'artigo'
  AND article IS NOT NULL
  AND DATE(date_created_br) BETWEEN '{DATA_INICIO}' AND '{DATA_FIM}'
GROUP BY vertical, DATE(DATE_TRUNC('week', DATE(date_created_br)))
ORDER BY visitas_unicas_semana DESC;
```

### Query 7.3 — Visitas únicas por artigo, por semana (com correção de qualidade de dado)

```sql
SELECT
  CASE
    WHEN article = 'pronto'
    THEN 'paguei meu emprestimo mas nao recebi uma nova oferta por que'
    ELSE article
  END AS article,
  vertical,
  DATE(DATE_TRUNC('week', DATE(date_created_br))) AS start_of_week,
  COUNT(DISTINCT CONCAT(userid, '-', session_id)) AS visitas_unicas_semana
FROM prod.cx.fat_help_center_events
WHERE event_category = 'artigo'
  AND article IS NOT NULL
  AND DATE(date_created_br) BETWEEN '{DATA_INICIO}' AND '{DATA_FIM}'
GROUP BY
  CASE WHEN article = 'pronto' THEN 'paguei meu emprestimo mas nao recebi uma nova oferta por que' ELSE article END,
  vertical,
  DATE(DATE_TRUNC('week', DATE(date_created_br)))
ORDER BY visitas_unicas_semana DESC;
```

### Query 7.4 — Navegação por vertical sem artigo específico (gap de conteúdo)

Alto volume aqui = cliente busca o tema mas não encontra artigo direto.

```sql
SELECT
    vertical,
    DATE(DATE_TRUNC('week', DATE(date_created_br))) AS semana,
    COUNT(DISTINCT CONCAT(userid, '-', session_id)) AS visitas_unicas_semana
FROM prod.cx.fat_help_center_events
WHERE event_category = 'vertical'
  AND NOT vertical IN ('nao_mapeado', 'outros')
  AND DATE(date_created_br) BETWEEN '{DATA_INICIO}' AND '{DATA_FIM}'
GROUP BY vertical, DATE(DATE_TRUNC('week', DATE(date_created_br)))
ORDER BY visitas_unicas_semana DESC;
```

### 7.5 — NFHR (fórmula correta e direção)

**NFHR = visitas únicas ÷ transações (TX)** — confirmar sempre essa direção, não a
inversa.

```sql
-- Numerador: Query 7.1 (visitas únicas da semana)
-- Denominador: TX da mesma semana
SELECT
  SUM(tx) AS transacoes_semana
FROM prod.cx.agg_overview
WHERE vertical <> 'core'
  AND date BETWEEN '{DATA_INICIO}' AND '{DATA_FIM}';

-- NFHR = visitas_unicas_semana (Query 7.1) / transacoes_semana
```

Calcular as duas partes separadamente (nunca um único JOIN que misture granularidade de
evento com granularidade de transação) e dividir os dois totais já agregados por semana.


---

## 8. Tabelas Granulares de Ticket

Usar apenas para investigação específica (ticket individual, cruzamento por dimensão
que `agg_overview` não tem) — nunca para recalcular um agregado que já existe em
`agg_overview`.

### 8.1 `prod.cx.dim_zendesk_tickets_summary` — dimensões completas do ticket

| Campo | Descrição |
|---|---|
| `id_ticket` | Chave primária |
| `userid` | ID do usuário |
| `vertical` | **Com acentuação** (diferente de `agg_overview`, que não tem acento) |
| `reason_contact`, `root_cause` | Motivo de contato e causa raiz |
| `friendly_service_channel` | Canal — usar este campo, não `key_channel` (descontinuado) |
| `created_at_br` | Data de criação (BRT) |
| `flg_human`, `flg_retention_bot`, `flg_retention_automation`, `flg_escalated_bot`, `flg_invalid_bot`, `flg_duplicate` | Flags de classificação |
| `user_profile` | Segmento (pf, pj ouro, pj prata, pj bronze) — já disponível aqui, não precisa de join externo |
| `entry_reason`, `entry_subreason` | Motivo de entrada |

**Filtro-base padrão (aplicar sempre, salvo instrução contrária):**
```sql
WHERE (flg_human = true OR flg_retention_bot = true)
  AND flg_invalid_bot = false
  AND friendly_service_channel != 'derivacao'
```

### 8.2 `prod.cx.fat_ticket_time` — tempos por evento de atendimento

| Campo | Descrição |
|---|---|
| `id_ticket` | Chave de join |
| `action` | `occupation`, `resolution` ou `first_reply_time` |
| `duration` | Segundos |
| `date_reference_br` | **Data do evento**, não da criação do ticket — sempre filtrar por este campo em métricas de tempo |
| `updater_email` | Quem registrou |

### 8.3 `prod.cx.amplitude_datamart` — dispositivo por usuário

Não existe em nenhuma tabela de ticket — única fonte para análise por
iOS/Android/Web app.

```sql
SELECT userid, platform
FROM (
  SELECT userid, platform,
         ROW_NUMBER() OVER (PARTITION BY userid ORDER BY event_time_br DESC) AS rn
  FROM prod.cx.amplitude_datamart
  WHERE userid IS NOT NULL
) WHERE rn = 1
```

### 8.4 `prod.cx.fat_tickets_transcription` (bruta) e `_summary` (IA)

- **Bruta:** `SELECT * FROM prod.cx.fat_tickets_transcription WHERE id_ticket = '{id}'`
  — nomes de coluna específicos não confirmados, usar `SELECT *`. Cobertura a partir de
  maio/2026.
- **Resumo IA (`_summary`):** contém `customer_issue`, `customer_complaint`,
  `support_solution`, `unresolved_reason`, `customer_sentiment`, `agent_sentiment`.
  Atualização semanal (sábados) — dado "stale" durante a semana é esperado.

### 8.5 `prod.core.fat_order` — perfil New / NewNew / Repeat

```sql
WITH user_profile AS (
    SELECT
        t.userid, u.reg_date,
        DATEDIFF('{DATA_FIM}', u.reg_date) AS dias_de_conta,
        MAX(CASE WHEN o.vertical = '{VERTICAL}' THEN 1 ELSE 0 END) AS usou_produto
    FROM prod.cx.dim_zendesk_tickets_summary t
    LEFT JOIN prod.growth.fat_user_data u ON CAST(t.userid AS STRING) = CAST(u.userid AS STRING)
    LEFT JOIN prod.core.fat_order o ON CAST(t.userid AS STRING) = CAST(o.userid AS STRING)
        AND o.vertical = '{VERTICAL}'
        AND DATE(o.order_date) < DATE(t.created_at_br)
    WHERE DATE(t.created_at_br) BETWEEN '{DATA_INICIO}' AND '{DATA_FIM}'
    GROUP BY t.userid, u.reg_date
)
SELECT
    CASE
        WHEN dias_de_conta <= 30 THEN 'New'
        WHEN dias_de_conta > 30 AND usou_produto = 0 THEN 'NewNew'
        ELSE 'Repeat'
    END AS perfil_cliente,
    COUNT(*) AS total_tickets
FROM user_profile
GROUP BY perfil_cliente;
```

⚠️ **Exceção — NewNew não é conceito válido** em Minha Conta, Conta Desativada,
Carteira Desativada e Chargeback Recovery (não têm um evento de "uso do produto"
análogo a uma transação). Usar só New vs Repeat nessas 4 verticais.

⚠️ `prod.rwd.clo_orders` está **bloqueada pela governança** — `fat_order` é o
substituto confirmado. Nomes de coluna assumidos por analogia, não formalmente
documentados — confirmar via preview antes de uso crítico.

### 8.6 `prod.credit_card.dim_card_account` — tipo de cartão

Substitui `prod.rwd.cc_recargapay_card_account` (bloqueada pela governança).

```sql
CASE
    WHEN provider_program_id = 1362 THEN 'Standard'   -- Garantido
    WHEN provider_program_id = 1271 THEN 'Gold'        -- Garantido
    WHEN provider_program_id = 1475 THEN 'PJ'          -- Garantido
    WHEN provider_program_id = 1583 THEN 'Black'       -- Concedido
    WHEN provider_program_id = 1584 THEN 'Platinum'    -- Concedido
    WHEN provider_program_id = 1705 THEN 'Titan'       -- Investment
    WHEN provider_program_id = 1769 THEN 'Platinum CDB' -- Investment
END AS tipo_cartao
```
⚠️ Nomes de coluna exatos não formalmente confirmados — validados só como funcionais.

---

## 9. Bugs

```sql
SELECT date, SUM(bug_count) AS bugs
FROM prod.cx.agg_overview
WHERE source = 'bugs'
GROUP BY date
ORDER BY date;
```
Ver CX-013 (§3) para a métrica oficial. Para live/hoje (sem defasagem T-1), usar
Zendesk MCP com `tags:bug` — ⚠️ tag não confirmada com certeza, validar antes do
primeiro uso em produção.


---

## 10. Tabela de Eventos e Incidentes — Metodologia

Construída para correlacionar eventos externos (incidentes de infra, comunicados,
features) com variações de indicador — usada tanto no report semanal quanto no
monitoramento intraday.

### 10.1 Canais lidos

| Canal | ID | Papel |
|---|---|---|
| `#escalation_incidents` | `CCP2AGBV1` | Incidentes automáticos (NewRelic) de toda a empresa — infra, PIX, Cartão, Loans, Investimentos, Antifraude |
| `#comunicados_e_atualizações_cx` | `C012NMP0UBE` | Comunicados operacionais/produto |
| `#lideres-cx-e-cxm` | `C052R2X2DEE` | Contexto executivo |
| `#the-cxm-house` | `C09DNDDFYTW` | Contexto geral do time CXM |
| Canais de squad (10, ver §2) | — | Temas ativos por vertical |
| Log de eventos — planilha IndeCX sincronizada | — | Incidentes documentados manualmente, sem alerta automático ao cliente associado |

### 10.2 Estrutura da tabela

| Data | Squad/Canal de origem | Produto(s) relacionado(s) | Tipo | Descrição | Status |
|---|---|---|---|---|---|
| DD/MM | #canal | Vertical(is) | Instabilidade / Incidente / Feature / Comunicado | resumo curto | Ativo / Resolvido |

### 10.3 Regras de construção

- **Agrupar por incidente, não por ciclo.** Alertas automáticos que abrem/fecham
  repetidamente para o mesmo problema (ex: NewRelic) são **um único incidente** — usar o
  horário do primeiro ciclo como referência.
- **`#escalation_incidents` já tem alerta automático ao cliente associado** — um
  incidente aparecer lá **não basta, isoladamente**, para justificar ação adicional de
  CXM. Só ganha peso quando corrobora um sinal reativo já existente (pico de volume,
  aumento de bug) — nesse caso, funciona como explicação do "porquê", não como gatilho
  independente.
- **O log da planilha IndeCX não tem esse alerta automático** — pode funcionar como
  gatilho preditivo independente (sem exigir corroboração de volume), mas sujeito a
  supressão se o mesmo padrão recorrer sem impacto novo em janela de 48h.
- **Correlação cruzada:** ao investigar variação em qualquer vertical, checar a tabela
  **completa** (todas as squads), não só os eventos do canal sendo analisado — um
  evento em uma squad pode explicar impacto em outra (ex: instabilidade de
  infraestrutura compartilhada afetando múltiplas verticais).
- **Evolução pós-evento:** para evento com data dentro do período analisado, buscar
  série diária ao redor do evento (alguns dias antes como base + dias depois) em vez de
  só "% vs período anterior" — isso evita mascarar a trajetória real misturando dias
  de antes e depois do evento na mesma média.
- **Instabilidades são tipicamente pontuais** — limitar a janela de "evolução
  pós-evento" ao período real de ocorrência (do início até a resolução + 1 dia de
  confirmação), não estender indefinidamente até o fim do período disponível. Só
  estender para o fim do período se o incidente ainda estiver ativo, ou se for
  feature/comunicado (efeito mais duradouro por natureza).


---

## 11. Amplitude — Taxonomia e Acesso a Artigos

**Project ID confirmado:** `332381` (app principal RecargaPay).

### 11.1 Taxonomia de evento — Central de Ajuda

Não existe evento único "acesso a artigo" com propriedade de artigo/path — cada artigo
tem seu **próprio nome de evento**, gerado a partir de título/seção/URL:

```
ViewedHelp / {Seção} - {Título do Artigo} - /help/articles/{slug}#article-container
```

Exemplo real validado: `ViewedHelp / Cartão RecargaPay - Como funciona a anuidade do
cartão? - /help/articles/Como-funciona-a-anuidade-do-cartão#article-container`.

**Descobrir o nome exato:** `Amplitude:search` (`entityTypes: ["EVENT"]`, query com
palavra-chave do tema/vertical) — mais confiável que tentar montar o nome manualmente a
partir do catálogo do Zendesk Guide (risco de erro de acentuação/encoding).

**⚠️ Eventos de nome "genérico" podem estar obsoletos** — validados dois candidatos
óbvios para "acesso geral": `Viewed /central-de-ajuda` (zero em 30 dias testados —
obsoleto) vs `Viewed /recarga:///central-de-ajuda` (vivo, mas volume muito pequeno,
provavelmente um deep link específico). Sempre confirmar `lastModified` via `search`
antes de confiar num nome óbvio.

### 11.2 Query padrão (`query_dataset`)

```json
{
  "app": "332381",
  "type": "eventsSegmentation",
  "name": "{nome descritivo}",
  "params": {
    "range": "Last 7 Days",
    "events": [{"event_type": "{NOME_COMPLETO_DO_EVENTO}", "filters": [], "group_by": []}],
    "metric": "uniques",
    "countGroup": "User",
    "groupBy": [],
    "interval": 1,
    "segments": [{"conditions": []}]
  }
}
```
Chamar com `projectId: "332381"` fora da definição também. O array `events` aceita
múltiplos objetos — validar vários artigos numa única chamada.

**Notas de schema:** `params` é campo obrigatório mesmo usando `chartId` para herdar de
um chart existente (não herda sozinho). Tipo de chart precisa bater — não sobrescrever
tipo de um chart de `funnels` com `eventsSegmentation`.

### 11.3 Fallback — quando Amplitude não responder

Ambiente de execução de Routine pode variar sessão a sessão (só `use_amplitude_metrics`
disponível, sem `query_dataset`/`search`) — testar `tool_search` de novo com termos
diferentes antes de assumir indisponível; se realmente ausente, usar
`prod.cx.fat_help_center_events` (§7) diretamente como substituto, com granularidade
real (não aproximação).

---

## 12. Regras de Exclusão e Qualidade de Dado — Consolidado

### 12.1 Exclusões obrigatórias (tickets)

```sql
WHERE (flg_human = true OR flg_retention_bot = true)
  AND flg_invalid_bot = false          -- exceto na distribuição N1/N2 (§4), onde conta como bot
  AND friendly_service_channel <> 'derivacao'
```

Lista completa de categorias de exclusão (fonte: skill organizacional
`cx-orchestrator-reference/references/exclusions.md`, mais completa que qualquer lista
embutida em documentação local): spam, teste/QA, treinamento, planning (~98 tags), MC
interno (~56 tags), duplicatas, side conversations, canais/marcas excluídos
(chargeback, pix_infraction). Sempre consultar a skill organizacional diretamente —
listas locais desatualizam.

### 12.2 "Atendimento não prestado" — entra no volume, nunca no ranking qualitativo

Motivo de contato que representa interação sem serviço real prestado (majoritariamente
fechamento por inatividade do bot). Excluir sempre de "Top motivos"/"Top causas raiz" —
nunca comentar como tema qualitativo real. **Nunca excluir do total de volume/contact
rate** — o ticket é real, só não teve serviço efetivamente prestado.

```sql
AND reason_contact <> 'Atendimento não prestado'   -- só em queries de ranking, nunca em queries de volume total
```
⚠️ Grafia exata não confirmada com acento/maiúscula — validar via `SELECT DISTINCT`.

### 12.3 Verticais agregadas em `agg_overview` (ver §2 para tabela completa)

Rendimento CDI (→ `cashback e rendimento`), Contas e Boletos + Boleto de Cobrança
(→ `utilities`), Pix In/Out/Chaves e RAF Indicado/Indicador (sem subtipo). Usar
`dim_zendesk_tickets_summary` para o corte fino nessas verticais.

### 12.4 Tabelas bloqueadas pela governança — não usar

| Tabela bloqueada | Substituto confirmado |
|---|---|
| `prod.rwd.cc_recargapay_card_account` | `prod.credit_card.dim_card_account` (§8.6) |
| `prod.rwd.clo_orders` | `prod.core.fat_order` (§8.5) |
| `prod.rwd.clo_users` | `user_profile` (já em `dim_zendesk_tickets_summary`) ou `prod.lending.fat_loan_properties_user` |

### 12.5 Qualidade de dado conhecida

- `article = 'pronto'` em `fat_help_center_events` — valor corrompido, ver §7
- Verificar sempre `SELECT MAX(date)` em `agg_overview` antes de tratar um período como
  fechado — o dia mais recente frequentemente não está consolidado ainda

---

## 13. Apêndice — Histórico de Correções

Registrado para que quem reusar este material entenda por que certas definições mudaram
— e não repita o mesmo processo de descoberta.

| Data (aprox.) | Correção | Impacto |
|---|---|---|
| Jul/2026 | `key_channel NOT LIKE '%deriva%'` → `friendly_service_channel <> 'derivacao'` | Filtro de derivação estava mesclando volume incorretamente |
| Jul/2026 | `agg_overview` confirmado como única fonte agregada oficial | Substituiu reconstrução manual via tabelas granulares |
| Jul/2026 | Boleto de Cobrança tem tag própria (`boleto_de_cobrança`) | Gap de mapeamento anterior era erro, não ausência real |
| Jul/2026 | Pix CC não tem tag própria — precisa busca textual | Confirmado, não é gap de documentação |
| Ago/2026 | Tabelas `rwd.*` bloqueadas pela governança | Substituídas por `credit_card.dim_card_account`, `core.fat_order` |
| Ago/2026 | `fat_indecx_metrics` não tem `id_ticket`, só `user_id` | Corrigia join incorreto presente em múltiplas queries legadas |
| Ago/2026 | `retencao_chatbot` (sem acento) ≠ alias de `retenção_chatbot` (com acento) | Segunda é subconjunto (~16%), propósito exato não esclarecido |
| Ago/2026 | 84% dos tickets `retencao_chatbot` são inatividade, não resolução genuína | Retenção bruta estava sistematicamente inflada |
| Ago/2026 | Retenção de bot oficial exclui `flg_passive_abandonment`, inclui `flg_invalid_bot` | Fórmula anterior (baseada em tag de inatividade) divergia da fonte oficial |
| Ago/2026 | Taxa de retenção precisa: abandono ativo conta como retido, só passivo exclui | Refinamento da fórmula acima, validado diretamente com o time |
| Ago/2026 | `agg_botmaker_metrics` tem sobreposição de categoria em janelas largas | `fat_botmaker_metrics` é a fonte exata; a agregada é só aproximação |
| Ago/2026 | `fat_indecx_metrics` tem sim coluna `metric`, contrariando correção anterior | As duas dimensões de classificação (`metric` e `survey_type`/`quest_level`) coexistem |
| Ago/2026 | `fat_help_center_events` permite série semanal real (não só mensal via `agg_overview`) | Destravou série semanal de Central de Ajuda, antes limitada a comparação mensal |
| Ago/2026 | Nunca somar acessos únicos entre dimensões (artigo/vertical/total) | `COUNT(DISTINCT)` não se distribui aditivamente — erro sutil e fácil de cometer |
| Ago/2026 | Amplitude/skills organizacionais: disponibilidade de tool varia por sessão, não é falha permanente | Retry com sessão nova resolve na maioria dos casos, antes de escalar como bug |

**Nota metodológica geral:** vários itens desta tabela só foram descobertos testando
diretamente contra dado de produção (queries reais de dashboards existentes, comparação
entre fontes) — não a partir de documentação formal, que em alguns pontos estava
incompleta ou desatualizada. Ao construir novos painéis a partir deste documento, ainda
vale validar pontualmente contra uma amostra pequena antes de confiar no número final,
especialmente nos itens marcados com ⚠️ ao longo do texto.
