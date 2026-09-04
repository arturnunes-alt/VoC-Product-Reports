---
name: voc-product-vertical-analysis
description: >
  Rotina que roda segunda, terça e sexta-feira às 11h e escreve, para cada uma das 26
  verticais do painel Arturito (dashboard 156, "CXM — Experiência do Produto"), uma
  Análise VoC com IA no card geral de Suporte e, quando a vertical tem NPS Transacional,
  também no card de Análise VoC de NPS — cobrindo evolução de indicadores, principais
  temas de reclamação/dúvida, alertas de novos temas não vistos em períodos anteriores,
  destaques positivos e exemplos reais com user_id e ticket_id. NÃO atualiza a Análise
  VoC de cada motivo de contato (o card por causa-raiz) — isso continua calculado por
  SQL, fora do escopo desta rotina.
version: "1.0"
model: "claude-sonnet-5"
trigger_segunda: "Segunda-feira às 11:00 BRT (14:00 UTC)"
trigger_terca: "Terça-feira às 11:00 BRT (14:00 UTC)"
trigger_sexta: "Sexta-feira às 11:00 BRT (14:00 UTC)"
maintainer: "Artur Nunes — artur.nunes@recargapay.com"
mcp_primary: "MCP Data - RecargaPay (Databricks + Arturito)"
mcp_secondary: "Slack MCP — leitura de canais para mapeamento de eventos (nunca posta)"
painel_destino: "Dashboard Arturito 156 (CXM — Experiência do Produto) — nunca posta no Slack"
---

# Análise VoC com IA por Vertical — Experiência do Produto (dashboard 156)

Rotina independente do pipeline semanal (`SKILL.md`, Routine A/B) e da rotina intraday
(`SKILL-INTRADAY.md`). Não compartilha execução com elas, mas reutiliza `canais.json` e
`mapeamento-responsaveis.json` como referência de leitura (mapeamento vertical → squad →
canal → responsável) — **sem editá-los**, mesmo princípio já aplicado pela rotina
intraday neste repositório. Diferente das outras duas, esta rotina nunca escreve no
Slack — o destino é sempre o painel Arturito 156.

## O que essa skill faz

Segunda, terça e sexta-feira, às 11h, esta rotina:

1. Busca os dados de cada vertical direto no Databricks — as mesmas queries já
   registradas no dashboard 156, reexecutadas via tool, mais algumas queries ad-hoc para
   os exemplos rastreáveis (ver Fase 1). **Nunca** usar `__ARTURITO_DATA__` como fonte —
   só existe dentro do navegador, não numa sessão de rotina.
2. Mapeia eventos/lançamentos/incidentes da empresa da janela de análise via Slack,
   reaproveitando o mapeamento de canais/squads/responsáveis já compartilhado neste
   repositório (`canais.json`, `mapeamento-responsaveis.json`) — ver Fase 2.
3. Detecta, por vertical, temas de contato/feedback que não apareciam (ou apareciam com
   volume muito menor) na série de 5 semanas anteriores — usando a mesma regra já
   validada em produção no pipeline semanal deste repositório (ver Fase 3).
4. Escreve, para cada uma das **26 verticais**, uma Análise VoC Geral de Suporte (card
   `pe-consolidado-voc-analise`), e para as **9 verticais com NPS Transacional** (Pix,
   Cartão de Crédito, Empréstimo, Transporte, Contas e Boletos, Link de Pagamento,
   Recarga de Celular, Tap to Pay, CDB/Investimentos), também uma Análise VoC de NPS
   (card `pe-nps-voc-analise`) — 5 blocos fixos cada, ver Fase 4/5.
5. Publica essas análises tocando **apenas** as variáveis `VOC_ANALISE_GERAL` e
   `VOC_ANALISE_NPS` já existentes no `js` do painel — nunca reescreve html, css, o resto
   do js, ou o campo `queries`.
6. Reconfere o painel publicado do zero antes de terminar. Essa etapa não é opcional —
   ver Fase 6.

**Fora do escopo desta rotina**: a Análise VoC de cada motivo de contato individual (o
card que aparece ao clicar em um motivo específico dentro de "Motivos de Contato",
função `gerarVocCausa` no JS) continua 100% calculada por SQL determinístico, como já
era — esta rotina nunca toca nela.

O painel já vem pronto para receber isso: os dois cards mostram "Aguardando a próxima
execução da rotina de Análise VoC com IA (seg/ter/sex, 11h)" até essa skill rodar pela
primeira vez para uma dada vertical.

Tools necessárias nesta sessão: acesso a Databricks (`databricks_run_query` /
`databricks_validate_query`), `MCP Data - RecargaPay:arturito_get_dashboard`,
`MCP Data - RecargaPay:arturito_update_dashboard`, ferramentas de Slack
(`slack_search_public_and_private`, `slack_read_channel`, `slack_search_channels`), e
bash/node com Playwright disponível para validação.

## Arquivos a ler na Fase 0 (nesta ordem de precedência)

1. **Skills organizacionais**, quando disponíveis — mesma regra de precedência já usada
   no pipeline semanal deste repositório (`SKILL.md`, seção "Skills
   organizacionais"): tentar `/mnt/skills/organization/{nome}/` e, se ausente,
   `/root/.claude/skills/{nome}/`. Em especial `cx-product-insights` (fonte primária de
   NPS/CSAT/volume/retenção de bot oficiais via `agg_overview` — nunca reconstruir essas
   métricas de memória quando esta skill estiver disponível). Se ausente nos dois
   caminhos: seguir com as queries já registradas no dashboard 156 e as referências
   deste repositório, sem bloquear a execução.
2. **Arquivos desta rotina** (raiz do repositório, mesmo padrão de
   `skill-databricks-mcp.md`/`skill-zendesk-cx.md` do pipeline semanal):
   `skill-product-vertical-events-mapping.md`,
   `skill-product-vertical-new-topic-detection.md`,
   `skill-product-vertical-domain-knowledge.md`,
   `skill-product-vertical-example-queries.sql`,
   `skill-product-vertical-editorial-guide.md`.
3. **Arquivos compartilhados do repositório** (mantidos pelo pipeline semanal
   `SKILL.md`/`voc-report-automation` — esta rotina só lê, nunca edita):
   `canais.json` (mapeamento canal → vertical → tags → thresholds),
   `mapeamento-responsaveis.json` (vertical → squad → responsável CXM),
   `skill-zendesk-cx.md` §7-9 (campos de classificação, agregações do `agg_overview`,
   hierarquia de flags bot/humano), `skill-databricks-mcp.md` (tabelas e queries de
   referência), `orientacoes-editoriais.md` (tom e regras editoriais complementares).
   Em caso de conflito entre esses arquivos compartilhados e os arquivos específicos
   desta rotina (item 2) sobre o mesmo dado (ex: mapeamento de canal, regra de
   exceção), **os arquivos compartilhados vencem** — são a fonte de verdade mantida
   pelo dono do processo, e mudam com mais frequência que os arquivos desta rotina.

## Fase 1 — Coletar dados (Databricks)

Buscar a definição de cada query já registrada no dashboard via
`arturito_get_dashboard(dashboard_id=156)` (campo `queries`), e reexecutar cada uma
diretamente via `databricks_run_query`.

**Determinar a janela de análise**: buscar o `js` atual do painel e ler
`VOC_ANALISE_GERAL`/`VOC_ANALISE_NPS` — para cada vertical, o `atualizado_em` da última
execução é o início da janela; agora é o fim. Se uma vertical nunca foi analisada (chave
ausente), usar como início a segunda-feira da semana corrente (ou, na primeira execução
de todas, os últimos 7 dias). Isso resulta em janelas de duração variável (tipicamente 1
dia após terça, 3-4 dias após segunda/sexta) — normal.

Para **cada uma das 26 verticais**, reexecutar (ajustando o filtro `vertical_key` /
`vertical` conforme o mapeamento CASE WHEN de cada query, e consultando a tabela de
correspondência em `skill-product-vertical-events-mapping.md` para saber a vertical equivalente no
`agg_overview`/`dim_zendesk_tickets_summary`):

| Uso | Queries |
|---|---|
| Evolução de indicadores (Cenário) | `Consolidado Vertical Semanal`, `Churn Vertical Semanal` (quando a vertical não estiver na lista `SEM_TX_AU_CHURN` do JS) |
| Principais Temas / Alerta de Novo Tema | `Motivos Contato Semanal` (série de 5 semanas — ver Fase 3) |
| Causa-raiz de apoio ao Cenário/Destaque | `Causa Raiz Motivo Periodo` |
| Exemplos Reais | queries ad-hoc de `skill-product-vertical-example-queries.sql` (1, 2 e, para Pix CC, 4) — **não** a query do painel, que não seleciona `userid`/`id_ticket` |

Para **cada uma das 9 verticais com NPS Transacional** (mais os 2 subverticais de Pix e
os 2 de Empréstimo, quando houver volume — ver Fase 5), reexecutar adicionalmente:

| Uso | Queries |
|---|---|
| Evolução do NPS (Cenário) | `NPS Transacional Semanal`, `NPS Transacional Subvertical Semanal` |
| Principais Temas | `NPS Categoria Feedback Semanal`, `NPS Frases Chave Periodo` |
| Alerta de Novo Tema | mesma lógica de `skill-product-vertical-new-topic-detection.md`, aplicada a `NPS Categoria Feedback Semanal` |
| Exemplos Reais | query ad-hoc de `skill-product-vertical-example-queries.sql` (3) |

**Antes de tratar qualquer período como fechado**: `agg_overview` frequentemente não tem
o dia mais recente consolidado — checar `SELECT MAX(date) FROM prod.cx.agg_overview
WHERE source='tickets'` e, se o resultado for anterior ao fim da janela de análise,
sinalizar o período como parcial no bloco de Cenário em vez de apresentá-lo como
fechado.

**Validar cada número antes de escrever**: variações percentuais e contagens devem bater
exatamente com o que a query retornou.

## Fase 2 — Mapear eventos e squads

Seguir `skill-product-vertical-events-mapping.md`, que aponta para o mapeamento real de
canais/squads/responsáveis já compartilhado neste repositório (`canais.json`,
`mapeamento-responsaveis.json`) — não usar um mapeamento inventado. Rodar o
mapeamento de eventos **uma vez por execução** (não por vertical) e reaproveitar,
filtrando os canais relevantes por vertical na hora de escrever cada análise.

Aplicar a técnica de "Evolução pós-evento" (`skill-product-vertical-domain-knowledge.md` §8) para
todo evento mapeado com data dentro da janela de análise.

## Fase 3 — Detectar temas novos ou não mapeados

Seguir `skill-product-vertical-new-topic-detection.md` (regra validada em produção, não a
inventada de uma versão anterior deste repositório) para cada vertical (Motivos de
Contato, para a Análise Geral) e para cada vertical com NPS (Categorias/Frases de
Feedback, para a Análise de NPS). Excluir sempre "Atendimento não prestado" dessa
checagem (`skill-product-vertical-domain-knowledge.md` §1). É esperado e correto que a maioria das execuções
não encontre nenhum alerta em várias verticais.

## Fase 4 — Escrever a Análise VoC Geral (26 verticais)

Ver `skill-product-vertical-editorial-guide.md` para tom, estrutura de 5 blocos, regras
de uso de identificadores, e `skill-product-vertical-domain-knowledge.md` para as exceções de
domínio a respeitar (perfil New/Repeat em 4 verticais específicas, Central de Ajuda
mensal, 3 categorias de bloqueio em Conta/Carteira Desativada, retenção de bot líquida
de abandono, verticais agregadas em `agg_overview`).

Para cada vertical, escrever os 5 blocos (Cenário, Principais Temas, Alerta de Novo
Tema, Destaque Positivo, Exemplos Reais) cobrindo:

- **Cenário**: evolução de Acessos Central / Bot Retido / Humano / TX / AU / Churn (os
  que existirem para a vertical) no período vs. o período imediatamente anterior de
  mesma duração, cruzando com eventos da Fase 2 quando a janela bater.
- **Principais Temas**: os 2-3 motivos de contato de maior volume no período (excluindo
  "Atendimento não prestado").
- **Alerta de Novo Tema**: resultado da Fase 3.
- **Destaque Positivo**: algo favorável no período (queda de um motivo problemático,
  melhoria de causa-raiz, evento com impacto positivo mapeado, etc.) — se genuinamente
  não houver nada digno de nota, dizer isso em vez de forçar um destaque artificial.
- **Exemplos Reais**: 2-3 casos com `id_ticket` e `user_id`, tirados das queries ad-hoc
  da Fase 1, relacionados aos temas citados nos blocos acima.

**Verticais de baixo volume**: se uma vertical não tiver dado suficiente no período para
uma leitura confiável em algum bloco, dizer isso diretamente nesse bloco (não pular a
vertical inteira — cada uma das 26 recebe uma entrada nesta execução).

**Verticais sem responsável CXM mapeado** (ver tabela de correspondência em
`skill-product-vertical-events-mapping.md`): não afeta a redação do texto em si — a rotina escreve a
análise normalmente para as 26 verticais, o mapeamento de responsável só importa se, em
algum momento futuro, esta rotina passar a notificar alguém (hoje ela só escreve no
painel, não notifica).

## Fase 5 — Escrever a Análise VoC de NPS Transacional (9 verticais)

Mesma estrutura de 5 blocos, mesma referência editorial, mas com o foco do NPS:

- **Cenário**: evolução do NPS Transacional no período vs. o anterior.
- **Principais Temas**: temas mais mencionados entre promotores e entre detratores
  (`NPS Categoria Feedback Semanal` + `NPS Frases Chave Periodo`).
- **Alerta de Novo Tema** / **Destaque Positivo** / **Exemplos Reais**: mesma lógica da
  Fase 4, adaptada à fonte de NPS.

**Subverticais (Pix, Empréstimo)**: cobertura opcional nesta execução — só escrever a
entrada com chave composta (`PIX::Pix Out - Wallet`, `PIX::Pix Out - Cartão`,
`EMPRESTIMO::Geral`, `EMPRESTIMO::Consignado`) quando houver volume de respostas
suficiente no período para uma leitura própria (sugestão: ao menos ~15-20 respostas com
feedback no período). A chave sem subvertical (`PIX`, `EMPRESTIMO`) é sempre
obrigatória. Para `PIX::Pix Out - Cartão`: usar a `flag_pix_cartao`
(`skill-product-vertical-domain-knowledge.md` §7), não `reason_contact`/`root_cause` isolados.

## Fase 6 — Publicar com segurança (o passo mais importante)

Seguir este protocolo à risca — é o mesmo já usado nos dashboards 141 e 295, adaptado
para o fato de que esta rotina atualiza várias verticais de uma vez, numa única
publicação.

1. `arturito_get_dashboard(156)` — buscar o `js` **na hora**, nunca reaproveitar uma
   cópia de uma sessão anterior.
2. Validar esse `js` recém-buscado **antes de mexer**: `node --check` (sintaxe). Montar a
   página completa (`html`+`css`+`js`, com `window.__ARTURITO_DATA__ = {queries:{}}`) e
   carregar num Chromium headless via Playwright, conferindo que não há erros de página
   nem de console. Se o painel atual já estiver quebrado, **parar e avisar antes de
   publicar em cima de uma base quebrada**.
3. Localizar `var VOC_ANALISE_GERAL = {...};` e `var VOC_ANALISE_NPS = {...};` nesse `js`.
   **Fazer merge**, não substituir: para cada vertical/subvertical analisada nesta
   execução, adicionar ou sobrescrever apenas a chave correspondente — nunca remover ou
   reescrever chaves de verticais não tocadas nesta execução.
   - **Formato da chave**: `VERTICAL_KEY` (ex: `PIX`, `CARTAO_CREDITO`), ou
     `VERTICAL_KEY::SubvertLabel` quando houver subvertical (ex:
     `PIX::Pix Out - Wallet`, `EMPRESTIMO::Consignado`) — usar exatamente os
     `vertical_key` do array `VERTICALS` do próprio JS, e os rótulos de subvert exatos
     do objeto `SUBVERTS` (`Pix Out - Wallet`, `Pix Out - Cartão`, `Geral`,
     `Consignado`).
   - **Formato de cada valor**: `{texto: '<html>', atualizado_em: 'DD/MM/AAAA'}` — o
     `texto` é o HTML dos 5 blocos (Fase 4/5); `atualizado_em` é a data de hoje.
4. Validar o `js` resultante de novo: sintaxe (`node --check`). Como o texto tem aspas e
   acentos, prestar atenção redobrada ao escapamento.
5. Chamar `arturito_update_dashboard` só com o campo `js` (nunca `html`, `css`, ou
   `queries`, que não mudam) + `rationale_md` (obrigatório sempre que `js` muda).
6. **Nunca confiar só na resposta "success" da tool.** Buscar o painel de novo
   (`arturito_get_dashboard`) e:
   - Confirmar que as chaves desta execução estão presentes com o `atualizado_em`
     correto, e que as chaves de execuções anteriores continuam intactas.
   - Rodar `node --check` no arquivo **inteiro**.
   - Montar a página de novo no Chromium e conferir, para uma amostra de verticais
     (pelo menos uma com NPS e uma sem), que os cards de Análise VoC Geral e de NPS
     renderizam o texto novo sem erro de console.
7. Se qualquer verificação falhar: **não tentar de novo automaticamente**. Parar,
   registrar o que falhou, e deixar o painel como estava.

## O que NÃO fazer

- Não tocar na Análise VoC de motivo de contato (`gerarVocCausa`, card por causa-raiz) —
  fora do escopo desta rotina.
- Não reescrever html, css, `queries`, ou qualquer parte do js além das declarações
  `VOC_ANALISE_GERAL` / `VOC_ANALISE_NPS`.
- Não sobrescrever ou remover chaves de verticais/subverticais não analisadas nesta
  execução — sempre merge, nunca replace do objeto inteiro.
- Não usar `__ARTURITO_DATA__` como fonte de dados.
- Não inventar `user_id`/`id_ticket` — todo identificador citado vem de uma query real
  (`skill-product-vertical-example-queries.sql`).
- Não inventar correlação com eventos que não apareceram no mapeamento da Fase 2, ou cuja
  janela de tempo não bate.
- Não usar um mapeamento de canal/squad/responsável inventado — sempre ler
  `canais.json`/`mapeamento-responsaveis.json`, compartilhados neste repositório.
- Não incluir "Atendimento não prestado" em Principais Temas ou Alerta de Novo Tema.
- Não misturar New/NewNew/Repeat nas 4 verticais que só usam New/Repeat.
- Não reportar retenção de bot bruta (sem excluir abandono passivo).
- Não pedir ou apresentar série semanal de Central de Ajuda (é mensal).
- Não forçar um Alerta de Novo Tema ou um Destaque Positivo quando genuinamente não há
  um — dizer isso explicitamente no bloco.
- Não pular a reconferência pós-publicação, mesmo se a resposta disser "success".
- Não usar a palavra "chatbot" — usar "RecargaBot".

## Referências

- `skill-product-vertical-events-mapping.md` — mapeamento real de canais/squads/responsáveis (aponta para `canais.json`/`mapeamento-responsaveis.json`, compartilhados neste repositório), tabela de correspondência de verticais (Fase 2)
- `skill-product-vertical-new-topic-detection.md` — regra validada em produção para detecção de temas novos (Fase 3)
- `skill-product-vertical-domain-knowledge.md` — exceções de domínio e técnicas confirmadas (fórmulas, agregações, flag Pix CC, evolução pós-evento) — usar em todas as fases
- `skill-product-vertical-example-queries.sql` — queries ad-hoc para exemplos com user_id/ticket_id (Fases 1, 4, 5)
- `skill-product-vertical-editorial-guide.md` — tom, estrutura de 5 blocos e regras editoriais (Fases 4 e 5)
