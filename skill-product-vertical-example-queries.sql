-- Queries de referência para os "exemplos reais" da Análise VoC (user_id + ticket_id)
-- Nenhuma delas está registrada no dashboard 156 hoje — o painel usa fat_tickets_transcription_summary
-- sem selecionar identificadores. Estas são queries ad-hoc que a própria rotina roda via
-- databricks_run_query, direto nesta sessão, apenas para extrair os identificadores dos
-- exemplos já citados no texto (nunca usar para nada além disso — ver Fase 4/5 e
-- "O que NÃO fazer" na SKILL.md sobre não expor dados pessoais fora do necessário).

-- ═══ 1) Exemplo de ticket de suporte (Análise Geral), por motivo de contato ═══
-- Ajustar :vertical_raw (valor bruto de `vertical`, o mesmo usado no mapeamento CASE WHEN
-- das queries do painel — não a vertical_key), :motivo (reason_contact exato do pareto) e
-- a janela de datas.
SELECT
  id_ticket,
  userid AS user_id,
  created_at_br,
  reason_contact,
  root_cause
FROM prod.cx.dim_zendesk_tickets_summary
WHERE flg_human = true AND flg_invalid_bot = false AND flg_retention_bot = false
  AND friendly_service_channel <> 'derivacao'
  AND vertical = :vertical_raw
  AND reason_contact = :motivo
  AND created_at_br >= :inicio_janela_atual AND created_at_br < :fim_janela_atual
ORDER BY created_at_br DESC
LIMIT 8;

-- ═══ 2) Exemplo com contexto qualitativo (resumo do problema/solução), por motivo ═══
-- Mesma vertical/motivo, mas puxando de fat_tickets_transcription_summary para ter o
-- resumo em linguagem natural (customer_issue/support_solution) junto com o identificador.
SELECT
  id_ticket,
  id_user AS user_id,
  date_created_at,
  customer_issue,
  support_solution,
  unresolved_reason
FROM prod.cx.fat_tickets_transcription_summary
WHERE vertical = :vertical_raw
  AND reason_contact = :motivo
  AND date_created_at >= :inicio_janela_atual AND date_created_at < :fim_janela_atual
ORDER BY date_created_at DESC
LIMIT 8;

-- ═══ 3) Exemplo de feedback de NPS Transacional (Análise de NPS), por classe ═══
-- Ajustar :action_name_pattern (o valor bruto de action_name da vertical/subvertical —
-- ver o CASE WHEN da query "NPS Transacional Semanal" já registrada no painel para o
-- mapeamento exato) e :review_class ('promotor' ou 'detrator').
SELECT
  id_ticket,
  user_id,
  answer_date,
  review,
  feedback,
  gcp_key_phrases
FROM prod.cx.fat_indecx_metrics
WHERE survey_type = 'transacional' AND quest_level = 'main'
  AND (deleted = false OR deleted IS NULL)
  AND action_name = :action_name_pattern
  AND review_class = :review_class
  AND feedback IS NOT NULL AND feedback <> ''
  AND answer_date >= :inicio_janela_atual AND answer_date < :fim_janela_atual
ORDER BY answer_date DESC
LIMIT 8;

-- Em todas as três: pegar sempre os exemplos mais recentes dentro da janela (ORDER BY DESC),
-- e escolher manualmente, entre os 8 retornados, os 4-5 mais representativos do que está
-- sendo dito no texto da análise (não necessariamente o primeiro da lista) — ver Fase 4/5
-- da SKILL.md para o número de exemplos esperado por análise.

-- ═══ 4) Exemplo de ticket de Pix CC (subvertical PIX::Pix Out - Cartão) ═══
-- Pix CC não tem tag própria — o sinal primário é a menção de "cartão"/"cartao" na
-- transcrição (ver skill-product-vertical-domain-knowledge.md §7), não reason_contact/root_cause
-- isolados. Usar esta query em vez da query 1/2 quando o exemplo for especificamente de
-- PIX::Pix Out - Cartão.
SELECT
  t.id_ticket,
  t.userid AS user_id,
  t.created_at_br,
  t.reason_contact,
  t.root_cause,
  s.customer_issue,
  s.support_solution
FROM prod.cx.dim_zendesk_tickets_summary t
LEFT JOIN prod.cx.fat_tickets_transcription_summary s
  ON CAST(t.id_ticket AS STRING) = s.id_ticket
WHERE t.flg_human = true AND t.flg_invalid_bot = false AND t.flg_retention_bot = false
  AND t.friendly_service_channel <> 'derivacao'
  AND LOWER(t.vertical) = 'pix::out'
  AND REGEXP_LIKE(LOWER(CONCAT_WS(' ', t.reason_contact, t.root_cause,
      COALESCE(s.customer_issue,''), COALESCE(s.support_solution,''))), 'cartao|cartão')
  AND t.created_at_br >= :inicio_janela_atual AND t.created_at_br < :fim_janela_atual
ORDER BY t.created_at_br DESC
LIMIT 8;
