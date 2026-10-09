# CXM - VoC - Experiência do Produto (dashboard 156, redesign by product squad)

## Request
Rebuild dashboard 156 as an experience map shared with product squads. Scope: help center, support bot, human contacts, transactions, active users, churn and a full view of transactional NPS (results and customer comments). Tables with conditional formatting and day/week/month filters (like dashboards 141/246) instead of line charts; an overview tab plus one tab per squad (Pix, Credit Card, Loans, Tap to Pay, Payment Link, Account, Insurance, CDB, Transport, Fraud, Others) with product/sub-product filters; sub-tabs Indicators, Transactional NPS, Support and Squad report; support view with pareto of contact reasons and root causes and customer examples from ticket transcription summaries; no AI-written VoC analysis in the dashboard code, but a slot per squad for the weekly squad report. The weekly squad reports are now produced by the VoC automation (Routine B, Mondays 12:15 BRT) and written to the `html` field; Slack receives only a short summary with links to these reports.

## Business Question
Where do customers need help, how well do self-service and the bot absorb it, how large is the human support load per transaction, and how satisfied are customers (NPS) — per squad and sub-product, over time?

## Main Tables
Certification status was NOT verified through datahub_get_dataset in this session.
### `prod.cx.agg_overview` (not verified)
Long-format CX hierarchy: `date`, `source`, `metric`, `vertical`, `product`, `flg_human`, `ticket_count`, `bot_retention`, `bot_total`, `visit_unic_count`, `tx`, `au` (monthly), NPS/CSAT counters, `reason_contact`, `root_cause`.
### `prod.cx.agg_botmaker_metrics` (not verified) — Pix bot split by `entry_subreason` (`entry_theme='pix'`).
### `prod.cx.dim_zendesk_tickets_summary` (not verified) — Pix human contacts and reasons by `vertical LIKE 'pix%'` + `entry_subreason`.
### `prod.cx.fat_help_center_events` (not verified) — Pix help-center sessions.
### `prod.cx.fat_indecx_metrics` (not verified) — NPS clusters, comment categories and comment list.
### `prod.cx.fat_tickets_transcription_summary` (not verified) — customer_issue, customer_complaint, customer_sentiment examples (last 28 days).
### `prod.core.fat_active_users` (not verified) — churn and AU for Pix with Card, Cashback, Cash In, Prime; uses `is_internal_active` (`internal_active` is deprecated).

## Metrics
| Metric | Type | Description | Logic |
|---|---|---|---|
| TX | Quantity | Approved transactions | SUM(tx) of transaction sources; company total = source core |
| AU | Quantity | Monthly active users | agg_overview au, product total (monthly only) |
| Churn 30d | Percent | Active in [ref-60, ref-31] and not active in [ref-30, ref] | ref = period end (min with yesterday) |
| Help center visits | Quantity | Unique sessions | SUM(visit_unic_count), source central, metric vertical |
| NFHR | Percent | Need for help rate | visits / TX |
| Bot attended / retained | Quantity | RecargaBot sessions | bot_total / bot_retention |
| Human contacts | Quantity | Human-handled tickets | SUM(ticket_count) where source tickets and flg_human |
| Contact rate | Percent | Total contacts / TX | (human + bot retained) / TX |
| CSAT N1 | Percent | Share of 4-5 ratings | channels c2c, chat online, e-mail |
| NPS tx | Score | Promoters minus detractors | (9-10 minus 0-6) / total |

## Key Notes
Each query returns three grains at once via GROUPING SETS (`grao` = dia|semana|mes), so the JS does not re-aggregate.
```sql
CASE WHEN GROUPING(dia)=0 THEN 'dia' WHEN GROUPING(semana)=0 THEN 'semana' ELSE 'mes' END AS grao
```
- agg_overview TX source `loans` stopped at 2026-09-15 when this was built; the UI flags stale TX as n/d.
- Product-level TX ("Todos"): agg_overview has sporadic `product='total'` rows (e.g. ccrp, cdb) whose sub-product is NULL and whose TX stops earlier than the sub-product rows. In the JS, rows without sub-product are ignored for TX (sum and last-date freshness) on days where sub-product rows have TX. This removes both the false n/d and a double count.
- Pix: Pix Out = Pix Wallet + Pix CC; NPS 'pix out' in agg_overview equals action 'pix out - cc' (checked against fat_indecx_metrics).
- Reasons/root causes: top-15 pairs per product/sub, rest bucketed as "Demais".
- Squad reports are JSON blocks hidden in the `html` field (`<div hidden data-px-report="squad[/sub]">`). The weekly update replaces only `html` and `rationale_md` (never `js`, `css` or `queries`). Blocks are built by `painel-156/montar_html_reports.py` from one JSON per report (contract v1, see `painel-156/contrato-report-v1.md`). A selected sub-product without its own block shows live numbers for that sub-product (KPIs, funnel and reasons from the dashboard queries, latest closed week) and keeps the squad-level text in a collapsed section.
- Direct links: Arturito runs the panel in a sandboxed iframe with an opaque origin: `window.top.location` throws SecurityError and the URL `#hash` never reaches the JS, but the parent page query string arrives through `document.referrer`. Link format: `dashboard_view.php?id=156&r=squad[/sub][/tab]` (tab = ind, nps, sup, rep), e.g. `&r=cartao/rep`, `&r=fraude/carteira%20desativada/rep`. The JS reads `r` from `document.referrer`, then `location.search`. The base URL is the constant `PANEL_URL` in the JS.
- Seguros has no Slack set: its report is built only by Routine B from the CX base and ticket transcription summaries and published in the panel only.

## Decisions & Assumptions
- One squad per product; unassigned verticals (Top Up, Utilities, Cashback, Cash In, Prime+, etc.) go to Others.
- AU only in month view; churn only week/month; Consignado has no churn.
- Dashboard 246 issues not replicated (pix::out labelled Pix CC; payment link mapped to Top Up in the human block).
- The refresh schedule (daily 10:11 BRT) was kept at the owner's request; the refresh recommendation (15:35 BRT) was not applied.
- The weekly report update runs under the owner's connection (the dashboard can only be updated by its owner).

## How to Validate
- Sep/2026 human contacts: agg_overview 33,855 vs dim_zendesk_tickets_summary 33,859; bot identical in agg_overview and agg_botmaker_metrics.
- NPS Sep/2026 identical between agg_overview and fat_indecx_metrics (e.g. Cartao RP 1529/144/339).
- Pix human Sep/2026: 543+131+539+2158 = 3,371 = Zendesk pix% total.
- Churn Jul/2026 vs dashboard 246 ref 01/08: CDB 7.1% vs 7.0%, Transporte 25.7% vs 26.4%.
- "Todos" TX: Cartao product TX for a closed week equals the sum of Garantido + Concedido + Investimento.
- Weekly update: after Routine B runs, the Report tab of each squad shows the new "Semana NN" and `&r=<chave>/rep` links open the matching report.
