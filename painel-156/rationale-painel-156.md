# CXM - VoC - Experiência do Produto (dashboard 156, redesign by product squad)

## Request
Rebuild dashboard 156 as an experience map shared with product squads. Scope: help center, support bot, human contacts, transactions, active users, churn and a full view of transactional NPS (results, additional survey questions and customer comments). Tables with conditional formatting and day/week/month filters (like dashboards 141/246) instead of line charts; an overview tab plus one tab per squad (Pix, Credit Card, Loans, Tap to Pay, Payment Link, Account, Insurance, CDB, Transport, Fraud, Others) with product/sub-product filters; sub-tabs Indicators, Transactional NPS, Support, What customers ask for and Squad report; support view with pareto of contact reasons and root causes and customer examples from ticket transcription summaries; no AI-written VoC analysis in the dashboard code, but a slot per squad for the weekly squad report. The weekly squad reports are now produced by the VoC automation (Routine B, Mondays 12:15 BRT) and written to the `html` field; Slack receives a short message (root: brief summary with links to the panels; thread: highlights and alerts) pointing to these reports. The navigation bars (filters, squad tabs, sub-products and the sub-tabs) stay visible while scrolling, and switching sub-tab scrolls back to the top of the page.

Sub-tab "O que os clientes pedem" (14/10/2026): per squad and sub-product, the main customer requests (themes), how often they appear, their impact and recent examples with the customer id, from four sources: transactional NPS comments, CSAT feedback of human support (N1), app store reviews and social media. The sources can be combined (16/10/2026): several can be ticked at once, requests are summed, each theme shows the impact per source and the examples alternate between sources. On 14/10/2026 the "Atendimento" source was changed from official contact reasons to the free-text feedback of the support CSAT survey, at the owner's request. Themes are defined by AI (initial configuration) and counted by the queries.

Sub-tab "NPS Transacional" (16/10/2026): new section with the evolution of the additional survey questions (scores 1-5, effort and yes/no) per product and sub-product.

## Business Question
Where do customers need help, how well do self-service and the bot absorb it, how large is the human support load per transaction, and how satisfied are customers (NPS and the extra survey questions) — per squad and sub-product, over time? And what are customers asking for, how often, and how much does each request hurt?

## Main Tables
Certification status was NOT verified through datahub_get_dataset in this session.
### `prod.cx.agg_overview` (not verified)
Long-format CX hierarchy: `date`, `source`, `metric`, `vertical`, `product`, `flg_human`, `ticket_count`, `bot_retention`, `bot_total`, `visit_unic_count`, `tx`, `au` (monthly), NPS/CSAT counters, `reason_contact`, `root_cause`.
### `prod.cx.agg_botmaker_metrics` (not verified) — Pix bot split by `entry_subreason` (`entry_theme='pix'`).
### `prod.cx.dim_zendesk_tickets_summary` (not verified) — Pix human contacts and reasons by `vertical LIKE 'pix%'` + `entry_subreason`; also gives the product (`vertical`) of the ticket behind each CSAT response (join by `id_ticket`).
### `prod.cx.fat_help_center_events` (not verified) — Pix help-center sessions.
### `prod.cx.fat_indecx_metrics` (not verified) — NPS clusters, comment categories and comment list; NPS comments (`feedback`) and CSAT N1 comments (`action_name = 'csat atendimento n1 v3 push'`, `metric = 'csat-1-5'`, key `id_ticket`) classified into request themes; additional questions of the transactional NPS surveys (`quest_level = 'add'`, `metric` in csat-1-5, ces, like/dislike; the main NPS question has `quest_level = 'main'`).
### `prod.cx.fat_tickets_transcription_summary` (not verified) — customer_issue, customer_complaint, customer_sentiment examples.
### `prod.core.fat_active_users` (not verified) — churn and AU for Pix with Card, Cashback, Cash In, Prime; uses `is_internal_active` (`internal_active` is deprecated).
### `prod.cx.fat_app_reviews` (not verified) — Google Play / App Store reviews of brand RecargaPay (`rating`, `content`, `product` tag, masked `username`).
### `prod.cx.fat_buzzmonitor_posts` (not verified) — public social media interactions (comments, replies, mentions; direct messages excluded), masked `author_login`.
### `prod.credit_card.dim_card_account` (not verified) — `credit_type` (COLLATERAL / GRANTED / INVESTMENT) used to split card NPS comments, card NPS additional questions and card CSAT responses into Garantido / Concedido / Investimento.

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
| Additional question score | Score | Average answer of an extra survey question | SUM(review)/COUNT per question and period; "% 4-5" = share of answers >= 4; yes/no = share of yes; periods with fewer than 5 answers are hidden |
| Request (pedido) | Quantity | Comment that asks for something or criticizes | text has a request marker (queria, poderia, falta, precisa...) OR author is unhappy (NPS 0-6, store rating 1-3, CSAT 1-3, negative social sentiment); min. 12 characters |
| Request theme mentions | Quantity | Requests per theme | 25 themes, a comment can have several; keyword lexicon inside the query |
| NPS / average rating of who asks | Score | Impact of each request | NPS of the theme's comments; average stars for stores and CSAT |

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
- Scenario chart (`cenario`, 12/10/2026 fix): `cenario.base` may be a number (drawn as a dashed reference line) or free text (shown as "Referência: ..." under the chart); before the fix a text `base` made the bar scale NaN and every bar and value disappeared. The `marc` annotations are no longer drawn as long SVG text (they overlapped and were clipped): each one is a ▼ marker above its bar plus a legend line under the chart (`.marc`). Non-numeric values in `serie` are drawn as 0 instead of breaking the chart.
- Navigation: the controls bar, the squad rail, the sub-product rail and the sub-tabs are sticky and stacked by `pxStick()` (offsets measured at runtime, recomputed after every render and on resize). The extra CSS for these changes is injected by the JS (`<style id="px-extra-css">`), so the CSS field was not changed. Clicking a sub-tab runs `scrollTopSec()` (window.scrollTo(0,0) and scrollIntoView on the root, so the parent page also goes to the top).
- Direct links: Arturito runs the panel in a sandboxed iframe with an opaque origin: `window.top.location` throws SecurityError and the URL `#hash` never reaches the JS, but the parent page query string arrives through `document.referrer`. Link format: `dashboard_view.php?id=156&r=squad[/sub][/tab]` (tab = ind, nps, sup, ped, rep), e.g. `&r=cartao/ped`, `&r=fraude/carteira%20desativada/rep`. The JS reads `r` from `document.referrer`, then `location.search`. The base URL is the constant `PANEL_URL` in the JS.
- UX section of the squad report (19/10/2026, owner request): `renderReportData()` draws a new section "🎨 UX" from the optional top-level `ux` block of each report JSON (`temas[{t,n,f,tom,pede,trechos[]}]`, `isoladas[]`, `vazio`, `resumo`, `fonte`), placed after "Menções" and also shown inside the collapsed squad analysis of a sub-product. It states what customers ask for or comment about design, layout, information and screens, from NPS Relacional comments, store reviews and social posts; themes need 3+ mentions, smaller ones appear as isolated mentions. This one-off change edited `js` (a single insertion plus the `ux` key in the list copied by `renderLive()`); the weekly update still replaces only `html` and `rationale_md`.
- Seguros has no Slack set: its report is built only by Routine B from the CX base and ticket transcription summaries and published in the panel only.
- Additional questions (query `NPS Perguntas Adicionais`): one row per grain/period/product/sub-product/question/type with n, sum and favourable answers (4-5, or yes). Product and sub-product come from the survey `action_name` (Pix Out = wallet + cc, Others = topup + utilities, card sub-products by `dim_card_account.credit_type` of the respondent); the same question text is never shared by two surveys, so parents can add their children. Windows: 70 days, 30 weeks, 12 months. Only numeric answers are kept: multiple-choice questions and open comments do not store the chosen option in the table, so they are not shown. Questions whose wording changed appear as separate rows (the older wording fades out of the selected window).
- Requests tab (2 queries: `Pedidos Temas` and `Pedidos Exemplos`). Window: last 6 months, weeks (Monday) and months in the same result (`g` = w|m, `per`). Both queries union four sources in one long table (`src` = nps|csat|loja|rede; `tp` b = base per product/sub/period, t = theme; generic counters c1..c10), so the theme lexicon exists once per query. Products map to squads: NPS by `action_name`; CSAT by the `vertical` of the Zendesk ticket (join by `id_ticket`, same vertical mapping as the support tab, plus "geral" for all responses, including tickets without a mapped vertical); reviews and social by the same product regexes as dashboard 141 plus the store's own `product` tag. A text can belong to several products and always belongs to "geral". Card sub-products come from `dim_card_account.credit_type` of the author. CSAT base counts all N1 responses (`metric = 'csat-1-5'`, avoids the duplicated like/dislike metric), only texts with 12+ characters enter the themes, and the CSAT of the Ouvidoria is not included. Examples are the 15 most recent per source/product/sub/theme (min. 10 mentions), one per author, with e-mail, CPF and long numbers masked; store usernames and social handles are masked at the source; CSAT examples show the customer id and the contact channel. The JS (module `PD`) follows the panel filters: granularity (day falls back to week), number of periods and "hide period in progress"; the weekly window start is dropped when it begins before the data window. With several sources ticked, `renderMulti()` sums mentions by theme, shows a per-source impact table (NPS of who asks, average stars or % negative vs the product) and interleaves the examples of the sources (each tagged with its source).
- Cost note: the two theme queries evaluate ~25 regexes over ~120 k NPS comments + ~16 k CSAT + ~13 k reviews/posts; each ran in the preview warehouse (2X-Small) in well under the tool timeout when separated; do not merge the two queries into one (three references to the same classified set timed out in preview).

## Decisions & Assumptions
- One squad per product; unassigned verticals (Top Up, Utilities, Cashback, Cash In, Prime+, etc.) go to Others.
- AU only in month view; churn only week/month; Consignado has no churn.
- Dashboard 246 issues not replicated (pix::out labelled Pix CC; payment link mapped to Top Up in the human block).
- The refresh schedule (daily 10:11 BRT) was kept at the owner's request; the refresh recommendation (15:35 BRT) was not applied.
- The weekly report update runs under the owner's connection (the dashboard can only be updated by its owner).
- The sticky stack takes about 160 px of the viewport (controls 49 + squad rail 37 + sub-product rail 34 + sub-tabs 43); if it is too tall the controls bar can be allowed to scroll away.
- Requests tab: themes are a keyword taxonomy proposed by AI and tuned over three test rounds; about 70% of NPS request comments, 69% of store requests and 50% of social requests fall in some theme (the tab shows the share, including for CSAT). "Request" includes critical comments from unhappy customers; the title keeps "o que os clientes pedem". The old contact-reason view of the Atendimento source (queries `Pedidos Atendimento` and `Pedidos Atendimento Exemplos`) was removed on 14/10/2026; contact reasons remain in the Support tab. Account, Seguros and Fraude have no transactional NPS, so they show CSAT, stores and social only. Social direct messages are excluded. Sub-products without data in a source show that source disabled. Sources are combined by summing mentions; impact metrics are never mixed across sources.

## How to Validate
- Sep/2026 human contacts: agg_overview 33,855 vs dim_zendesk_tickets_summary 33,859; bot identical in agg_overview and agg_botmaker_metrics.
- NPS Sep/2026 identical between agg_overview and fat_indecx_metrics (e.g. Cartao RP 1529/144/339).
- Pix human Sep/2026: 543+131+539+2158 = 3,371 = Zendesk pix% total.
- Churn Jul/2026 vs dashboard 246 ref 01/08: CDB 7.1% vs 7.0%, Transporte 25.7% vs 26.4%.
- "Todos" TX: Cartao product TX for a closed week equals the sum of Garantido + Concedido + Investimento.
- Weekly update: after Routine B runs, the Report tab of each squad shows the new "Semana NN" and `&r=<chave>/rep` links open the matching report.
- Scenario charts (Semana 41): the 7 reports with a `cenario` block (account, cartao, transporte, pix, pix/cartao, emprestimo/pessoal, t2p) draw bars, values and a marker legend; no `NaN` in the SVG.
- Scrolling any squad: the controls, squad rail, sub-product rail and the sub-tabs stay pinned in this order and do not overlap; clicking another sub-tab returns to the top.
- Requests tab: `Pedidos Temas` NPS base for "geral" in the last 6 months matches `fat_indecx_metrics` responses (119,024 on 14/10/2026 for abr-out); CSAT "geral" on 14/10/2026 = 15,537 responses (7,893 with text, average 4.01) = `fat_indecx_metrics` where `action_name = 'csat atendimento n1 v3 push'` and `metric = 'csat-1-5'`; examples are dated up to the previous day.
- Additional questions: on 16/10/2026 the query returned 71 distinct questions (6,439 daily, 3,024 weekly and 1,059 monthly rows); e.g. Cartão RP "o limite disponível atendeu sua necessidade?" averages about 3.2 against about 4.4 for the other card questions, matching `fat_indecx_metrics` (Aug-Oct/2026).
