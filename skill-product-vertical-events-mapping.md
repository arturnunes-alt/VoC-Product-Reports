# Mapeamento de Eventos e Squads (Fase 2 da rotina)

**Revisão:** esta versão substitui a anterior, que usava um mapeamento de canais
inventado. A partir de agora, esta referência usa o mapeamento **real** já compartilhado
neste repositório (`canais.json`, `mapeamento-responsaveis.json`, `skill-zendesk-cx.md`
§8) — os mesmos arquivos usados pelo pipeline semanal de reports
(`voc-report-automation`, em `SKILL.md`) e pela rotina intraday (`SKILL-INTRADAY.md`).

## Onde estão os dados de squad/canal (ler direto do repositório, não duplicar aqui)

- `canais.json` — canal Slack → verticais → tags Zendesk → aberturas obrigatórias →
  thresholds de alerta. Também tem `slack_channel_leitura` (a lista completa de canais a
  ler para cada produto, sempre incluindo os 2 canais transversais
  `#lideres-cx-e-cxm` e `#comunicados_e_atualizações_cx`).
- `mapeamento-responsaveis.json` — vertical → canal → responsável CXM → `user_id_slack`.
  Tem uma seção `squads_da_planilha_fora_do_escopo_desta_routine` (verticais sem CXM
  dedicado, `responsavel_cxm: "On Demand"`) e uma regra de fallback explícita
  (`fallback_sem_responsavel`): quando não há responsável mapeado, seguir sem marcar
  ninguém, só sinalizando isso no texto.
- `skill-zendesk-cx.md` §8 — tabela mais detalhada de canal → vertical → tag Zendesk →
  vertical no `agg_overview` → observação de agregação (quais verticais o
  `agg_overview` mistura no mesmo grupo, exigindo `dim_zendesk_tickets_summary` para
  isolar o corte fino).

**Ler os três antes de mapear eventos ou compor o texto de qualquer análise** — esta
rotina não mantém uma cópia própria desses dados porque eles já existem, são mantidos
pelo dono do processo, e uma cópia divergiria com o tempo.

## Tabela de correspondência — VERTICAL_KEY do dashboard 156 → vertical do repositório

O dashboard 156 usa 26 `vertical_key` (array `VERTICALS` do JS) que não são idênticas às
18 verticais monitoradas pelo pipeline semanal deste repositório — o dashboard cobre um escopo mais
amplo (inclui caudas longas sem squad dedicado). Usar esta tabela para saber qual
entrada de `canais.json`/`mapeamento-responsaveis.json` corresponde a cada
`vertical_key`:

| `vertical_key` (dashboard 156) | Vertical no repositório | Canal squad | Responsável CXM |
|---|---|---|---|
| `PIX` | Pix In / Pix Out / Chaves Pix (+ Pix CC, sem tag própria — ver flag abaixo) | `#pixcc-home-raf-cx` | Eduardo Reis |
| `CARTAO_CREDITO` | Cartão de Crédito | `#cc-produto-e-cx` | Alexandre Luz |
| `EMPRESTIMO` | Empréstimo + Crédito Consignado | `#squad_loan_seguimento` | Cassio Mitherhofer |
| `CARTEIRA_BLOQUEADA` | Carteira Desativada | `#cx_fraud` | Anderson Fernandes |
| `CONTA_DESATIVADA` | Conta Desativada | `#cx_fraud` | Anderson Fernandes |
| `MINHA_CONTA` | Minha Conta | `#account_cx` | Anderson Fernandes |
| `TRANSPORTE` | Transporte | `#melhoria-continua-verticais` | On Demand |
| `CONTAS_BOLETOS` | Contas e Boletos (+ Boleto de Cobrança, agregada junto no `agg_overview` — ver exceção) | `#melhoria-continua-verticais` | On Demand |
| `LINK_PAGAMENTO` | Link de Pagamento | `#subacquirer-cx` | Alexandre Luz |
| `RECARGA_CELULAR` | Recarga de Celular | `#melhoria-continua-verticais` | On Demand |
| `TAP_TO_PAY` | Tap to Pay | `#subacquirer-cx` | Alexandre Luz |
| `CDB_INVESTIMENTOS` | CDB + Rendimento CDI (agregada no `agg_overview`) | `#investments-e-cx` | Alexandre Luz |
| `CHARGEBACK` | Chargeback Recovery | `#cx_fraud` | Anderson Fernandes |
| `MOVIMENTACOES` | Movimentações Financeiras | `#investments-e-cx` | Alexandre Luz |
| `RAF` | RAF (Indicado + Indicador) | `#pixcc-home-raf-cx` | Cassio Mitherhofer |
| `EXCLUSIVAS`, `OPEN_FINANCE`, `SEGUROS`, `CASHBACK_RENDIMENTO`, `MAQUININHA`, `ADICIONAR_DINHEIRO`, `CONTAS_PJ`, `PARCERIA_BENEFICIOS`, `TAREFAS_APP`, `CATALOGO_PRODUTOS`, `PRIME_PLUS` | Fora do escopo monitorado hoje pelo pipeline semanal (não têm entrada em `mapeamento-responsaveis.json`) | — | On Demand (aplicar `fallback_sem_responsavel` — nunca marcar ninguém, só sinalizar no texto que a vertical não tem responsável fixo mapeado) |

Para toda vertical da última linha: mapear eventos usando só os canais transversais
(`#lideres-cx-e-cxm`, `#comunicados_e_atualizações_cx`, `#the-cxm-house`), já que não há
canal de squad dedicado.

## Subverticais e casos especiais (usar exatamente como documentado no repositório)

- **`PIX::Pix Out - Wallet` / `PIX::Pix Out - Cartão`**: `agg_overview` não separa
  Wallet de Cartão dentro de Pix Out — usar `dim_zendesk_tickets_summary` (`vertical
  LIKE 'pix::%'`) para o corte fino. Pix CC não tem tag própria de vertical — o sinal
  primário é **qualquer menção de "cartão"/"cartao" na transcrição** do ticket
  (`fat_tickets_transcription_summary`, campos `customer_issue`/`customer_complaint`/
  `support_solution`), complementado por `reason_contact`/`root_cause` como sinal
  adicional — nunca o contrário.
- **`EMPRESTIMO::Geral` / `EMPRESTIMO::Consignado`**: mapeiam para Empréstimo Pessoal e
  Crédito Consignado, respectivamente — essas sim têm tag própria e não precisam do
  mesmo tratamento de Pix CC.
- **`CONTAS_BOLETOS`**: `agg_overview` agrega Contas e Boletos com Boleto de Cobrança no
  grupo `utilities`. Para reportar volume/motivos isolados desta vertical especificamente
  (sem Boleto de Cobrança misturado), usar `dim_zendesk_tickets_summary`
  (`vertical = 'contas e boletos'`).
- **`CDB_INVESTIMENTOS`**: mesmo caso — `agg_overview` agrega Rendimento CDI dentro de
  `cashback e rendimento`. Isolar via `dim_zendesk_tickets_summary`
  (`vertical = 'rendimento cdi'`) quando o texto precisar separar CDB de Rendimento CDI.

## Mapeamento de eventos — fontes e método

Seguir a mesma lógica de correlação cruzada já usada no pipeline semanal deste
repositório (`SKILL.md` Fase 1): ler os canais transversais
(`#the-cxm-house`, `#lideres-cx-e-cxm`, `#comunicados_e_atualizações_cx`) mais o(s)
canal(is) de squad da vertical em análise, para a janela desde a última execução desta
rotina (ver Fase 1 da `SKILL.md` principal).

**Extrair de cada canal**: incidentes/instabilidades (com data, produto(s) afetado(s),
status ativo/resolvido, e horário de resolução quando mencionado), mudanças de
produto/fluxo/regra/processo, lançamentos de feature, comunicados relevantes.

**Correlação cruzada**: um evento reportado no canal de outra squad pode explicar
variação numa vertical diferente (ex: instabilidade em Pix pode afetar volume de Pix CC,
ou uma melhoria de UX anunciada em canal geral pode reduzir contatos em qualquer
vertical específica). Ao citar uma correlação cruzada, deixar explícito que o evento
veio de outro canal — nunca apresentar como descoberto dentro do próprio canal da
vertical.

**Evolução pós-evento** (ver `skill-product-vertical-domain-knowledge.md` §"Evolução pós-evento"
para o detalhe completo e a query): quando um evento mapeado tiver data **dentro** da
janela de análise desta execução, não basta citar a variação da janela inteira — buscar
a série diária e mostrar a trajetória (crescendo/estabilizando/cedendo), limitando a
janela de "depois" ao período real de ocorrência (não estender além da resolução do
incidente, quando conhecida).

**Não mencionar quem enviou a mensagem** — apenas data, canal de origem e conteúdo.

## Cuidado crítico com datas (mesmo erro já cometido em outras automações desta linha)

Sempre confirme o ano dos timestamps retornados pelo Slack antes de usá-los — a
ferramenta pode retornar mensagens de anos anteriores mesmo com filtros calculados para
o ano-alvo. Prefira `slack_search_public_and_private` com `after:AAAA-MM-DD` e
`before:AAAA-MM-DD` explícitos, mais confiável que oldest/latest em epoch.

## Como isso alimenta a Análise VoC

Para cada vertical analisada na Fase 4/5 da `SKILL.md` principal, verificar se algum
evento mapeado aqui, dentro da janela de tempo, ajuda a explicar uma variação de
indicador ou um alerta de novo tema — citando isso de forma direta. Se nenhum evento
explicar a variação, dizer isso explicitamente em vez de inventar uma causa (ver
`skill-product-vertical-editorial-guide.md`).
