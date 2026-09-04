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
version: "1.1"
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

> **v1.1 (04/09/2026)**: reformulação pós-incidente. Uma execução anterior tentou gerar
> e publicar as 26+9(+4) análises numa única resposta, estourou o limite de output
> token no meio da geração do JS, e publicou o conteúdo truncado mesmo assim — quebrando
> a sintaxe do painel em produção. Esta versão introduz publicação em lotes (Fase 6),
> consolidação de queries para reduzir chamadas ao Databricks (Fase 1), e uma regra dura
> de nunca publicar sem validação nem tentar de novo automaticamente após uma falha.

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
5. Publica essas análises **em lotes de 6-8 verticais** (nunca tudo de uma vez),
   tocando apenas as variáveis `VOC_ANALISE_GERAL` e `VOC_ANALISE_NPS` já existentes no
   `js` do painel — nunca reescreve html, css, o resto do js, ou o campo `queries`.
6. Reconfere o painel publicado do zero **depois de cada lote**, não só no final. Essa
   etapa não é opcional — ver Fase 6.

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

## Fase 1 — Coletar dados (Databricks), uma vez para todas as verticais

**Regra dura, para velocidade**: cada query é executada **uma única vez por execução
da rotina**, exatamente como está registrada no dashboard (sem adicionar `WHERE
vertical_key = X` nem qualquer filtro de vertical) — essas queries já retornam todas as
verticais de uma vez (é assim que o próprio dashboard funciona: busca tudo, filtra no
client). Rodar a mesma query 26 vezes trocando o filtro é o erro que tornou execuções
anteriores lentas e caras — **nunca fazer isso**. Buscar cada query definida via
`arturito_get_dashboard(dashboard_id=156)` (campo `queries`), reexecutar via
`databricks_run_query` sem alterações, e depois filtrar/agrupar o resultado **em
memória** por `vertical_key` (ou `subvert_key`) ao montar a análise de cada vertical.

**Determinar a janela de análise**: buscar o `js` atual do painel e ler
`VOC_ANALISE_GERAL`/`VOC_ANALISE_NPS` — para cada vertical, o `atualizado_em` da última
execução é o início da janela; agora é o fim. Se uma vertical nunca foi analisada (chave
ausente), usar como início a segunda-feira da semana corrente (ou, na primeira execução
de todas, os últimos 7 dias). Isso resulta em janelas de duração variável (tipicamente 1
dia após terça, 3-4 dias após segunda/sexta) — normal.

Rodar cada uma das queries abaixo **uma vez só**, cobrindo as 26 verticais de uma vez
(ajustando o filtro de período conforme a janela determinada acima, mas nunca o
`vertical_key`):

| Uso | Query (uma execução cobre todas as verticais) |
|---|---|
| Evolução de indicadores (Cenário) | `Consolidado Vertical Semanal`, `Churn Vertical Semanal` (o resultado desta última é ignorado nas verticais listadas em `SEM_TX_AU_CHURN` do JS, mas a query em si roda uma vez só) |
| Principais Temas / Alerta de Novo Tema | `Motivos Contato Semanal` (série de 5 semanas — ver Fase 3) |
| Causa-raiz de apoio ao Cenário/Destaque | `Causa Raiz Motivo Periodo` |

**Exemplos Reais** (`skill-product-vertical-example-queries.sql`, queries 1/2/4): estas
dependem do motivo/causa líder de cada vertical, que só é conhecido depois de processar
`Motivos Contato Semanal` acima — não dá para rodar 100% em uma única chamada. Ainda
assim, evitar uma chamada por vertical: agrupar as verticais que já têm seu motivo líder
identificado e rodar poucas chamadas cobrindo várias de uma vez (`WHERE vertical IN
(...)` com `ROW_NUMBER() OVER (PARTITION BY vertical, reason_contact ORDER BY
created_at_br DESC)` para pegar os exemplos de cada combinação em uma única query), em
vez de uma query isolada por vertical.

Para **cada uma das 9 verticais com NPS Transacional** (mais os 2 subverticais de Pix e
os 2 de Empréstimo, quando houver volume — ver Fase 5), rodar adicionalmente, também
uma vez cada, cobrindo todas de uma vez:

| Uso | Query |
|---|---|
| Evolução do NPS (Cenário) | `NPS Transacional Semanal`, `NPS Transacional Subvertical Semanal` |
| Principais Temas | `NPS Categoria Feedback Semanal`, `NPS Frases Chave Periodo` |
| Alerta de Novo Tema | mesma lógica de `skill-product-vertical-new-topic-detection.md`, aplicada a `NPS Categoria Feedback Semanal` |
| Exemplos Reais | query ad-hoc de `skill-product-vertical-example-queries.sql` (3) — mesma otimização de agrupar verticais numa query quando possível |

**Contagem esperada de chamadas ao Databricks nesta fase**: por volta de 10-14
chamadas no total (uma por query template + algumas poucas queries agrupadas de
exemplos), não 60+ como em execuções anteriores.

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

## Fase 6 — Publicar em lotes, com segurança (o passo mais importante)

**Mudança de arquitetura, pós-incidente de 04/09/2026**: uma execução anterior tentou
gerar e publicar as 26+9(+4) análises numa única resposta gigante, estourou o limite de
output token no meio da geração do JS, e o conteúdo truncado foi publicado mesmo assim
— quebrando a sintaxe do painel em produção (`Unexpected end of input`, faltando o
fechamento `})();` do arquivo). A partir de agora, a publicação é sempre **em lotes**,
nunca tudo de uma vez.

### Divisão em lotes

Depois de escrever o texto das análises (Fase 4/5, que pode ser feito em memória para
todas as verticais de uma vez — é só texto, não é a etapa arriscada), publicar em grupos
de **6 a 8 verticais por lote** (contando a Análise Geral e, quando aplicável, a de NPS
da mesma vertical como parte do mesmo lote). Cada lote roda o ciclo completo abaixo,
independente dos outros — se um lote falhar, os lotes já publicados com sucesso
continuam valendo, e só o lote problemático precisa ser investigado.

### Ciclo de publicação de um lote

1. `arturito_get_dashboard(156)` — buscar o `js` **na hora**, nunca reaproveitar uma
   cópia de uma sessão anterior nem de um lote anterior já publicado nesta mesma
   execução (o conteúdo pode ter mudado a cada publicação).
2. Validar esse `js` recém-buscado **antes de mexer**: `node --check` (sintaxe). Se o
   painel já estiver quebrado (por exemplo, por um lote anterior desta mesma execução
   que falhou silenciosamente), **parar tudo e avisar** — nunca publicar um novo lote em
   cima de uma base já quebrada.
3. Localizar `var VOC_ANALISE_GERAL = {...};` e `var VOC_ANALISE_NPS = {...};` nesse
   `js`. **Fazer merge**, não substituir: adicionar/sobrescrever só as chaves das
   verticais deste lote — nunca remover ou reescrever chaves de outras verticais
   (deste ou de execuções anteriores).
   - **Formato da chave**: `VERTICAL_KEY` (ex: `PIX`, `CARTAO_CREDITO`), ou
     `VERTICAL_KEY::SubvertLabel` quando houver subvertical (ex:
     `PIX::Pix Out - Wallet`, `EMPRESTIMO::Consignado`) — usar exatamente os
     `vertical_key` do array `VERTICALS` do próprio JS, e os rótulos de subvert exatos
     do objeto `SUBVERTS` (`Pix Out - Wallet`, `Pix Out - Cartão`, `Geral`,
     `Consignado`).
   - **Formato de cada valor**: `{texto: '<html>', atualizado_em: 'DD/MM/AAAA'}` — o
     `texto` é o HTML dos 5 blocos (Fase 4/5); `atualizado_em` é a data de hoje.
4. Validar o `js` resultante **antes de publicar**: `node --check` (sintaxe) e conferir
   que o arquivo termina com `})();` (o fechamento do IIFE) — essa checagem específica
   existe por causa do incidente citado acima e nunca deve ser pulada. Como o texto tem
   aspas e acentos, prestar atenção redobrada ao escapamento.
5. **Regra dura, sem exceção: nunca chamar `arturito_update_dashboard` com um `js` que
   falhou em qualquer verificação do passo 4.** Se a validação falhar — incluindo o
   caso em que a própria geração do texto foi cortada pelo limite de output no meio do
   processo — **parar este lote, registrar o que aconteceu, e não tentar de novo
   automaticamente**. Uma nova tentativa só acontece depois de entender por que a
   anterior falhou (ex: reduzir ainda mais o tamanho do lote), nunca como reflexo
   imediato ao erro.
6. Só então chamar `arturito_update_dashboard`, com o campo `js` (nunca `html`, `css`,
   ou `queries`, que não mudam) + `rationale_md` citando quais verticais este lote
   cobre.
7. **Nunca confiar só na resposta "success" da tool.** Buscar o painel de novo
   (`arturito_get_dashboard`) e:
   - Confirmar que as chaves deste lote estão presentes com o `atualizado_em` correto,
     e que as chaves de outros lotes/execuções anteriores continuam intactas.
   - Rodar `node --check` no arquivo **inteiro** recém-buscado.
   - Montar a página no Chromium (Playwright) e conferir, para pelo menos uma vertical
     deste lote, que os cards de Análise VoC Geral (e de NPS, quando aplicável)
     renderizam o texto novo sem erro de console.
8. Só depois de passar em todas as checagens do passo 7, seguir para o próximo lote,
   repetindo o ciclo do passo 1.

### Se um lote falhar

Parar a execução inteira, registrar quantos e quais lotes já foram publicados com
sucesso, e não tentar "completar" os lotes restantes na mesma sessão sem antes entender
a causa. Uma próxima execução (a próxima ocorrência do agendamento seg/ter/sex, ou uma
execução manual depois do diagnóstico) cobre as verticais que ficaram de fora — elas
simplesmente mantêm o `atualizado_em` de sua última análise bem-sucedida até lá.

## O que NÃO fazer

- Não tocar na Análise VoC de motivo de contato (`gerarVocCausa`, card por causa-raiz) —
  fora do escopo desta rotina.
- Não reescrever html, css, `queries`, ou qualquer parte do js além das declarações
  `VOC_ANALISE_GERAL` / `VOC_ANALISE_NPS`.
- Não sobrescrever ou remover chaves de verticais/subverticais não analisadas neste
  lote/execução — sempre merge, nunca replace do objeto inteiro.
- Não usar `__ARTURITO_DATA__` como fonte de dados.
- Não rodar a mesma query uma vez por vertical — cada query roda uma vez por execução,
  cobrindo todas as verticais; filtrar em memória (ver Fase 1).
- Não tentar publicar as 26+9(+4) verticais em uma única chamada de
  `arturito_update_dashboard` — sempre em lotes de 6-8 (Fase 6).
- Não chamar `arturito_update_dashboard` com um `js` que falhou em qualquer validação
  (sintaxe, fechamento `})();`, teste no Chromium) — parar e diagnosticar, nunca
  publicar mesmo assim torcendo para dar certo.
- Não tentar republicar automaticamente depois de uma falha — cada nova tentativa exige
  entender a causa da anterior primeiro.
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
- Não pular a reconferência pós-publicação de cada lote, mesmo se a resposta disser
  "success".
- Não usar a palavra "chatbot" — usar "RecargaBot".

## Referências

- `skill-product-vertical-events-mapping.md` — mapeamento real de canais/squads/responsáveis (aponta para `canais.json`/`mapeamento-responsaveis.json`, compartilhados neste repositório), tabela de correspondência de verticais (Fase 2)
- `skill-product-vertical-new-topic-detection.md` — regra validada em produção para detecção de temas novos (Fase 3)
- `skill-product-vertical-domain-knowledge.md` — exceções de domínio e técnicas confirmadas (fórmulas, agregações, flag Pix CC, evolução pós-evento) — usar em todas as fases
- `skill-product-vertical-example-queries.sql` — queries ad-hoc para exemplos com user_id/ticket_id (Fases 1, 4, 5)
- `skill-product-vertical-editorial-guide.md` — tom, estrutura de 5 blocos e regras editoriais (Fases 4 e 5)
