# Handoff — Painel 141 “CXM - VoC - Experiência RecargaPay” (Arturito)

> **Para quem vai ler:** este documento resume **como o painel 141 foi construído** (layout, estrutura de dados, regras de categorização) e **o que foi alinhado com o Artur** ao longo da conversa de construção, para que um novo painel seja criado **seguindo as mesmas orientações**. Ele é autossuficiente: as expressões regulares, os trechos de SQL e as regras estão nos apêndices. Estado documentado: **07–08/10/2026, snapshot 133/134 do dashboard 141** (verificado byte a byte contra os arquivos locais após a publicação).

## Sumário
1. Contexto e objetivo
2. Arquitetura no Arturito
3. Layout e estrutura de telas
4. Filtros e comportamentos transversais
5. Modelo de dados (as 16 queries)
6. Definições de métricas e faixas de cor
7. Categorização de feedbacks (temas, tom, produtos, clusters)
8. Alinhamentos e decisões da conversa
9. Limitações conhecidas e pendências
10. Lições de processo e armadilhas técnicas
11. Como começar o novo painel (checklist e prompt sugerido)
Apêndices A–F: regex de temas · léxicos de tom · produtos · SQL-base por fonte · SQL de clusters · formato da query manual

---

## 1. Contexto e objetivo
- **Plataforma:** Arturito (dashboards em HTML/CSS/JS vanilla + queries Databricks). `connector_id = 7`. Dashboard **141**, título “CXM - VoC - Experiência RecargaPay” (antes “Hub VoC · NPS Relacional”). Agendamento atual: diário 08:38 BRT (id 286). O Databricks recomenda 14:08 BRT (driver `prod.core.fat_tpv`, última gravação 13:38) — **não alterado sem confirmação**.
- **Pergunta de negócio:** o que os clientes dizem sobre a RecargaPay (pesquisa relacional, lojas de apps, redes sociais públicas e NPS competitivo), quais temas/produtos estão subindo ou ficando críticos e como o NPS evolui frente ao mercado.
- **Princípios pedidos pelo Artur (e seguidos):** só dados ligados ao Databricks (nada de análise escrita por IA no painel); **tabelas com formatação condicional**, não gráficos de linha; granularidade dia/semana/mês; NPS colorido pelas **zonas padrão de NPS**; transparência sobre limitações dos dados; teste rigoroso antes de publicar.
- **Fontes (nenhuma certificada no DataHub na época):** `prod.cx.fat_indecx_metrics` (NPS/CSAT/CES), `prod.cx.fat_app_reviews` (lojas; coleta mudou de Sensor Tower para scraping em 31/08/2026), `prod.cx.fat_buzzmonitor_posts` (redes; DMs só desde 16/09/2026). Joins de clusters: `prod.core.fat_new_users`, `prod.credit_card.dim_card_account`, `prod.checkout.dim_investment_lifecycle`, `prod.core.fat_tpv`, `prod.cx.dim_zendesk_tickets_summary`, `prod.core.fat_active_users`.

## 2. Arquitetura no Arturito
- Um dashboard = **HTML + CSS + JS + queries + rationale (markdown)**. O JS lê **somente** `window.__ARTURITO_DATA__.queries["Nome da query"]` (array de objetos; **valores numéricos chegam como string** — converter com `Number()`).
- **Contrato de dados:** para não varrer a base 6 vezes, séries e temas de cada fonte vêm de **uma query “Agregados”** com colunas genéricas (`ds` = serie|temas, `g` = D|S|M, `periodo`, `k1..k6`, `n1..n8`); o JS devolve isso aos nomes específicos via um mapa (`AGG_MAP`). Em modo de filtro (produto/palavra-chave/segmento), o JS **recalcula tudo a partir das linhas de comentário** em memória.
- **Tamanho:** JS ≈ 137 mil caracteres (inclui gerador de PDF ≈ 12 mil); se o Arturito recusar, o primeiro corte é o PDF.
- **Atualização via MCP:** `arturito_update_dashboard` exige **payload completo** por campo: `queries` substitui **todas** as queries (omitir mantém as existentes); `html`, `css`, `js` substituem o campo inteiro. `rationale_md` é obrigatório quando html/js/queries mudam. Toda atualização preserva a versão anterior (snapshot).
- **Leitura:** `arturito_get_dashboard` devolve só **100 linhas de amostra** por query (`last_result_total_rows` mostra o total real). Os avisos “a query X não é referenciada pelo JS” são **falsos positivos** (os nomes são montados dinamicamente).
- **Teste local:** foi montado um **mock HTML** com dados reais do Databricks e testes automatizados com Playwright (reconciliação tabela × lista de comentários, regressões, PDF). Isso **não** substitui o teste no iframe real do Arturito.

## 3. Layout e estrutura de telas
**Ordem vertical (estado final):**
1. **Cabeçalho (`vh-header`)** — título “🧭 Experiência RecargaPay” + ⓘ, subtítulo e **cartões de destaque** com o resultado do **período mais recente da granularidade e do intervalo selecionados** (período em curso marcado “parcial”): 📊 NPS Relacional (cor da zona + nome da zona, n), 📱 % 4–5★ nas lojas, 💬 % positivas nas redes (público), 📣 interações públicas (+ % negativas), 🏁 NPS Competitivo (último mês comparável, “manual”). **Rola junto com a página e some ao rolar** (pedido do Artur: ocupava muito espaço).
2. **Bloco fixo (`vs-sticky-top`, sticky no topo)**:
   - **Barra de filtros:** granularidade (☀️ Diário · **📆 Semanal (padrão)** · 🗓️ Mensal) + ⓘ; chips de período: ⏪ Ontem · 7️⃣ Últimos 7 dias · 📍 Semana atual · 🗓️ Mês atual · 🗓️ 30 dias · **⭐ 90 dias (padrão)** · 📅 6 meses · 📅 12 meses · ♾️ Tudo; dois campos de data; campo **🔎 Palavras-chave (vírgula = várias)** + ⓘ; botões **🧹 Limpar filtros**, **📄 Extração geral** (PDF) e **🤖 Continue com IA** (link `claude.ai/new?q=` com contexto do painel).
   - **Abas:** 🎯 Radar de temas · 📈 Evolução por tema · 📊 NPS Relacional · 📱 Lojas de apps · 💬 Redes sociais · 🏁 NPS Competitivo.
   - **Faixa de filtros ativos** (produto / palavra-chave, com “× limpar”).
3. **Nota de rodapé de status** (granularidade, “período filtrado”, aviso de filtro ativo) e o **conteúdo da aba ativa**.

**Conteúdo por aba**
- **Radar de temas:** (a) tabela **“Evolução por tipo de voz”** (NPS Relacional + volume; Lojas % 4–5★ + volume; Redes % positivas + volume; coluna Δ vs anterior); (b) **Alertas** por regra (clicáveis → abrem o tema na Evolução); (c) **Radar** tema × fonte (comentários, % detratores, reviews, % 1–2★, interações, % negativas, Σ menções, Δ, sinal) — linhas clicáveis, colunas ordenáveis.
- **Evolução por tema:** chips de **produto** (18 + “Todos”, com contagem de comentários); fonte (Relacional/Lojas/Redes); métrica (🔢 volume · 📐 % da base · 🔴 % crítico · 😠 % comentários negativos (texto) · 😊 % positivas só em Redes); em Redes: 👥 Público / 🔒 DM / 🔀 Todos. Tabela tema × período; **clicar no tema ou numa célula (tema + período) filtra os comentários** do bloco abaixo.
- **📊 NPS Relacional:** **Segmento** (Todos · Pessoa Física · Pessoa Jurídica) que filtra a sessão inteira; **Clusters** (8 dimensões, ver §7.4) com tabela por valor e filtro por linha; tabela “NPS por período” (NPS geral, PF, PJ, % promotores, % neutros, % detratores, respostas, % com comentário); **Perguntas adicionais** (CSAT/CES; PF e PJ; % favorável · nota média · % desfavorável · respostas); **Temas** (comentários, detratores, “NPS de quem cita”, Δ); **comentários**.
- **📱 Lojas de apps:** filtro de loja (todas/Google Play/App Store); tabela por período (reviews, nota média, % 1–2★, % 4–5★, % sentimento negativo, % pendente); temas; comentários; **Benchmark por marca** (matriz marca × período em **% 4–5★**, alternativas % 1–2★ e volume; segue granularidade e datas; com filtro de produto é mensal); **marca × tema** (janela fixa de 90 dias); comentários por marca (amostra de 8 por marca e tema).
- **💬 Redes sociais:** visão geral (volume geral, público, DM, % positivas, % negativas, % com ticket); tabela por **canal** × período (métricas: interações · % negativas · % positivas · % com ticket); temas; comentários (só público).
- **🏁 NPS Competitivo:** ranking RecargaPay × PicPay × Nubank × MercadoPago (mês a mês, rank no último mês comparável, média, Δ, gap vs melhor concorrente); base de respostas da RecargaPay (respostas, % promotores/neutros/detratores com escala de calor); tabela de **temas da pesquisa** (volume · % da base · NPS de quem cita); comentários de exemplo. **Dados digitados à mão** (ver Apêndice F).

## 4. Filtros e comportamentos transversais
- **Períodos:** *Ontem, 7 dias, Semana atual e Mês atual* trocam a granularidade para **Diário**. *6 meses* = desde o dia 1º do mês de 5 meses atrás (coincide com a base de comentários). O padrão ao abrir é **90 dias, semanal**.
- **Linha de referência acima das datas** em todas as tabelas de evolução: **W##** (semana ISO do ano; ex.: W40 = 28/09 a 04/10) em diário/semanal (dias da mesma semana agrupados); **Q#** (trimestre) em mensal e nas tabelas mensais do benchmark e do competitivo.
- **Palavras-chave (global e por bloco de comentários):** substring, **sem diferenciar acentos/maiúsculas**; **vírgula = “ou”** entre termos; **espaço dentro do termo = “e”**. Filtra o painel inteiro pelos comentários que contêm o termo; destaca as palavras nos comentários.
- **Produto (18):** recalcula o painel a partir dos comentários que citam o produto (classificação por texto). **Segmento PF/PJ** e **Cluster:** filtram a sessão NPS Relacional. Todos combinam entre si (E). **Não filtráveis:** ranking e temas do NPS Competitivo (a pesquisa não identifica produto); % por marca do benchmark não filtra por palavra-chave.
- **Tom dos comentários:** chips ⚪ Todos · 🟠 Negativos · 🔴 Críticos (com contagem) em todo bloco de comentários; métrica “% comentários negativos (texto)” na Evolução.
- **Comentários:** base = **todos os comentários dos últimos 6 meses, sem LIMIT**; 200 por vez (“Mostrar mais 200”/“Mostrar todos”); **CSV baixa todos os filtrados** (mascara e-mail/CPF/telefone); botão Copiar como alternativa.
- **Aviso de 3 segundos** ao clicar numa linha/célula/cabeçalho que filtra comentários (“Comentários abaixo filtrados por Tema: … · Período: …”).
- **ⓘ** (≈36 pontos): tooltip ao passar o mouse/focar/tocar, explicando filtros, cartões, títulos e cabeçalhos; não aparece no PDF.
- **🧹 Limpar filtros:** volta a 90 dias/semanal e zera produto, palavra-chave, segmento, cluster, loja, tipo de redes, métrica da evolução e filtros de comentários.
- **📄 Extração geral (PDF):** PDF A4 paisagem gerado no navegador (sem bibliotecas; Helvetica; emojis removidos e símbolos substituídos), com **todas as tabelas conforme os filtros**, a linha W/Q e **sem comentários de clientes**; cobre as 3 fontes na Evolução por tema, PF/PJ nas perguntas adicionais e os 8 clusters. O download por Blob **não foi testado dentro do iframe do Arturito** (há alerta se bloquear).
- **Estilo:** emojis em abas, filtros, temas, produtos, clusters e zonas; **dados centralizados** nas tabelas (coluna de rótulos à esquerda); períodos em curso em *itálico* com selo “parcial” e fora das médias/alertas.

## 5. Modelo de dados (as 16 queries, `connector_id = 7`)
| # | Nome | Grão / janela | Conteúdo |
|---|---|---|---|
| 1 | Rel Agregados | D 89 dias · S ≈25 semanas (`date_sub(date_trunc('week',hoje),175)`) · M 12 meses | `serie` (k1=ut pf/pj; n1 total, n2 promotores, n3 neutros, n4 detratores, n5 com texto) e `temas` (k1=tema; n1..n4 idem; n5 negativos; n6 críticos) |
| 2 | Apps Agregados | idem | `serie` (k1=loja; n1 reviews, n2 soma da nota, n3 1–2★, n4 4–5★, n5 sent. negativo, n6 positivo, n7 neutro, n8 pendente) e `temas` (n1 reviews, n2 1–2★, n3 sent. neg., n4 pendente, n5 tom neg., n6 tom crítico) — marca RecargaPay |
| 3 | Social Agregados | idem | `serie` (k1=canal, k2=tp publico/dm; n1 interações, n2 neg., n3 pos., n4 neutras, n5 com ticket) e `temas` (k1=tema, k2=tp; n1, n2 neg., n3 tom neg., n4 crítico) |
| 4–6 | Rel Perguntas Diário / Semanal / Mensal | D 89 dias · S · M 12 meses | periodo, ut, metric, quest, total, favoraveis, neutros, desfavoraveis, soma_nota (quest_level='add'; metric ces/csat) |
| 7 | Apps Marcas Diário | **dia × marca × loja**, 12 meses (~6 mil linhas) | reviews, soma_nota, notas_1_2, **notas_4_5**, sent_neg, sent_class (agregado no navegador pela granularidade/datas) |
| 8 | Apps Marcas Temas | marca × tema, 89 dias | reviews, notas_1_2 |
| 9 | Apps Marcas Reviews Recentes | amostra: até 8 mais recentes por marca × tema, 89 dias | marca, data, loja, nota, temas, texto |
| 10 | Rel Feedbacks Recentes | **todos os comentários de 6 meses** (~10 mil) | data, classe, user_type, k (cluster), p (produtos ativos), a (notas adicionais), temas, texto, tom |
| 11 | Apps Reviews Recentes | idem (~11 mil) | data, loja, nota, sentimento, temas, texto, tom |
| 12 | Social Interações Recentes | idem, só públicas (~7 mil) | data, canal, tipo, sentimento, temas, texto, tom |
| 13 | Apps Marcas Produtos Mensal | produto × marca × loja × mês, 12 meses | idem #7 em granularidade mensal (usado com filtro de produto) |
| 14 | Apps Marcas Produtos Temas | produto × marca × tema, 89 dias | reviews, notas_1_2 |
| 15 | Rel Respostas Clusters | **1 linha por resposta**, 6 meses (~14 mil) | d, u (pf/pj), r (nota 0–10), k (cluster, §7.4), p, m (bitmask de temas; −1 sem texto), a (9 notas adicionais) |
| 16 | NPS Competitivo Manual | `SELECT … FROM VALUES` (221 linhas) | ver Apêndice F (editar o SQL todo mês) |

Volumes de referência (07/10/2026): Rel Agregados 1.912 · Apps 1.953 · Social 2.545 · Rel Feedbacks 9.964 · Apps Reviews 10.936 · Social 6.846 · Clusters 13.754. **Total ≈ 27,7 mil comentários na página (~11 MB).**
**Convenções de SQL:** texto normalizado `lower(translate(texto,'áàâãäéèêëíìîïóòôõöúùûüç','aaaaaeeeeiiiiooooouuuuc'))`; texto exibido = 300 primeiros caracteres sem quebras de linha; janelas de 6 meses = `add_months(date_trunc('month', current_date()), -5)`; apps: marca `RecargaPay`, `length(content) > 1`; relacional: `feedback` com mais de 5 caracteres; redes: `only_emojis` falso e tipos de voz de cliente (comentário, resposta, menção, review de terceiros; **exclui posts da marca e RTs**).

## 6. Definições de métricas e faixas de cor
- **NPS Relacional** = % promotores (nota ≥ 9) − % detratores (≤ 6), sobre respostas do tipo `relacional`, `action_name != 'relacional de cc titan'`, `quest_level='main'`, `lower(metric) LIKE 'nps%'`, `deleted IS NOT TRUE`.
- **Zonas de NPS (arredondando a 1 casa):** 🏆 Excelência 75 a 100 · 👍 Qualidade 50 a 74 · 🛠️ Aperfeiçoamento 0 a 49 · 🚨 Crítica −100 a −1.
- **Lojas:** métrica principal = **% de notas 4–5★**; faixas `pos45` = verde ≥ 80, verde claro ≥ 75, laranja ≥ 65, abaixo vermelho. “% 1–2★” é a referência robusta porque o **sentimento tem backlog desde 31/08** (coleta nova).
- **Redes:** **% positivas = 100% − % negativas** (neutras contam como positivas — definição do painel). Faixas `posSocial` = 55 / 40 / 25. “% com ticket” alto é esperado (as interações entram pela fila de atendimento); o sentimento do BuzzMonitor é **enviesado para negativo** → ler como demanda.
- **Perguntas adicionais:** escala 1–5; favorável = 4–5, neutro = 3, desfavorável = 1–2. Faixas: % favorável 85/78/70; nota média 4,4/4,2/4,0; % desfavorável vermelho ≥ 15, laranja ≥ 10.
- **“NPS de quem cita”** (por tema) = (promotores − detratores) ÷ comentários que citam o tema; **não é o NPS oficial**; células com < 10 comentários ficam sem cor.
- **% crítico:** detratores (NPS) · notas 1–2★ (lojas) · sentimento negativo (redes) — medidas diferentes, comparar dentro da mesma fonte.
- **Faixas de “% comentários negativos (texto)”** (quartis da base): rel 64/51, apps 84/72, social 86/69; **% crítico:** rel 35/25, apps 70/55, social 80/65.
- **Picos de volume:** valor ≥ 1,5× a média do próprio tema (laranja) e ≥ 2× (vermelho); ≤ 0,5× (azul claro). Períodos em curso ficam fora da média.
- **Volume mínimo para colorir célula:** temas/alertas — diário 5, semanal 15, mensal 40; perguntas adicionais 5/10/30; clusters 8/20/40; benchmark 5/15/30 reviews; % crítico/negativo só com ≥ 5 menções.
- **Alertas (regras):** pico de volume de tema (≥ 1,5× a média dos 4 períodos anteriores); alta de ≥ 10 pp na taxa crítica; queda de NPS ≥ 3 pts ou mudança de zona; queda de ≥ 3 pp em % 4–5★ nas lojas; queda de ≥ 2 pts no NPS competitivo; backlog de sentimento ≥ 20% nas lojas.

## 7. Categorização de feedbacks
### 7.1 Os 15 temas (taxonomia definida pelo Artur; multi-rótulo; sem match = “sem tema identificado”)
Classificação por **regex sobre o texto normalizado** (Apêndice A), idêntica em SQL (Databricks `RLIKE`) e no JS. Um comentário pode citar vários temas (por isso “Σ menções” soma citações, não pessoas). Ordem/bit do bitmask (`m`): cartao 1 · credito 2 · bloqueio 4 · app 8 · ux 16 · fraude 32 · seguranca 64 · suporte 128 · concorrencia 256 · pix 512 · taxas 1024 · cashback 2048 · recargas 4096 · cadastro 8192 · invest 16384.

| id | Rótulo exibido |
|---|---|
| cartao | 💳 Cartão · anuidade, fatura, cobrança |
| credito | 💰 Empréstimo / limite |
| bloqueio | 🔒 Bloqueio de conta / carteira / saldo |
| app | 📲 App · instabilidade, login, acesso |
| ux | 🎨 UX · usabilidade e funcionalidades |
| fraude | 🚨 Fraude e golpes |
| seguranca | 🛡️ Segurança e verificação |
| suporte | 🎧 Suporte · bot, atendimento, Central de ajuda |
| concorrencia | ⚔️ Concorrência |
| pix | ⚡ Pix e transferências |
| taxas | 💸 Taxas, tarifas e juros |
| cashback | 🎁 Cashback e benefícios |
| recargas | 🚌 Recargas, transporte e contas |
| cadastro | 📝 Cadastro e abertura de conta |
| invest | 📈 Investimentos e rendimento |

### 7.2 Tom do comentário (negativo / crítico) — **heurística, não validada por leitura amostral**
Campo `tom` ∈ {0, 1, 2} calculado em SQL. Sinais por fonte:
| Fonte | sinal negativo (`sn`) | sinal positivo (`po`) | extremo (`ex`) |
|---|---|---|---|
| Relacional | nota ≤ 6 **ou** `gcp_score` ≤ −0,25 | nota ≥ 9 | nota ≤ 2 **ou** `gcp_score` ≤ −0,5 |
| Lojas | sentimento = negative **ou** nota ≤ 2 | nota ≥ 4 e sentimento ≠ negative | nota = 1 |
| Redes | sentimento = negative | sentimento = positive | — (falso) |

- `st` = vocabulário **forte** de reclamação; `ml` = vocabulário **brando** (Apêndice B).
- **tom 1 (Negativo)** = `sn` **OU** (`ml` **E NÃO** `po`).
- **tom 2 (Crítico)** = (`sn` OU (`ml` E NÃO `po`)) **E** (`st` OU `ex`).
- Léxicos compartilhados entre as queries; revisar com leitura amostral antes de tratar como verdade.

### 7.3 Os 18 produtos (filtro global; multi-rótulo por regex — Apêndice C)
Cartão de Crédito · Empréstimo · Empréstimo Consignado · Pix · Pix com Cartão · Criação de Conta · Carteira Bloqueada · Conta Desativada · Chargeback · Transporte · Tap to Pay · CDB/Investimentos · Seguros · Contas e Boletos · Link de Pagamento · **RAF (indique um amigo — significado assumido, a confirmar)** · Recarga de Celular · Open Finance. O benchmark por produto nas lojas vem das queries 13–14 (mesmas regex em SQL).

### 7.4 Clusters (NPS Relacional) — string `k` de 7 posições + extras
| Pos | Cluster | Valores |
|---|---|---|
| 0 | 🆕 New vs Repeat | N = novo no mês (`fat_new_users`), R = repeat |
| 1 | 💳 Tipo de cartão | C = Garantido (COLLATERAL), G = Concedido (GRANTED), I = Investment, `-` = sem cartão (`dim_card_account`, status NORMAL) |
| 2 | 📈 Investimentos | 1 = investimento ativo (`dim_investment_lifecycle`, ACTIVE), 0 = não |
| 3 | 💵 Faixa de TPV (mês) | 0 sem TPV · 1 até R$200 · 2 R$200 a R$1.000 · 3 R$1.000 a R$4.000 · 4 acima de R$4.000 (`fat_tpv.tpv_monetizable`) |
| 4 | 🔢 Ordens no mês | 0 nenhuma · 1 = 1–5 · 2 = 6–20 · 3 = 21–60 · 4 = 61+ |
| 5 | 🎧 Passou por suporte | 1/0 (`dim_zendesk_tickets_summary` no mês) |
| 6 | 🔁 Retenção (semana de atividade) | N = novo (1ª semana ativa) · R = retained (ativo na semana) · S = resurrected (ativo só na anterior) · C = churned |
| — | 🧩 Produtos ativos | campo `p` (lista separada por `;`), **multi-rótulo**; só últimos 30 dias; mostra os 10 mais frequentes |
Correções em relação ao painel antigo: rótulos de TPV (“R$1.000 a R$4.000”) e ordens (“6 a 20”, “61+”) acertados; “Sem cartão” agora é um valor de Tipo de Cartão. SQL completo no Apêndice E.
**Perguntas adicionais (campo `a`, 9 posições; 0 = não respondeu):** 0 Facilidade de uso (CSAT) · 1 Aparência do app (CSAT) · 2 Utilidade da comunicação (CSAT) · 3 Praticidade do suporte (CES) · 4 Confiança em cuidar do dinheiro (CES) · 5 Estabilidade do app (CSAT) · 6 Facilidade de conciliação (CSAT) · 7 Rapidez para vender (CSAT) · 8 Segurança em recebimentos/prazos (CES). **PF vê [0,1,2,3,4]; PJ vê [5,6,7,3,8]** (a 3 é comum).

## 8. Alinhamentos e decisões da conversa (em ordem de importância)
1. **Sem análise por IA no painel** (cartões “Análise VoC”, aba Eventos e gráficos de linha foram removidos; texto manual “Análise do analista” também foi removido depois). Rotina semanal `voc-weekly-analysis` ficou **sem destino** no JS → desativar ou reescrever.
2. **Tabelas com formatação condicional + granularidade D/S/M**, NPS pelas zonas padrão, períodos em curso sinalizados.
3. **Taxonomia de 15 temas** e **18 produtos** definidas pelo Artur; cliques em tema filtram comentários, com busca por palavra-chave e CSV.
4. **Clusters do painel antigo viram sub-abas** do NPS Relacional; **perguntas adicionais** (CSAT/CES) por PF/PJ; **segmento PF/PJ** filtra a sessão toda.
5. **Janela de comentários = 6 meses, sem LIMIT**, com paginação e CSV completo; **período padrão 90 dias**; chip “6 meses” alinhado à base.
6. **Filtro de produto global** e **filtro de palavra-chave global** (vírgula = “ou”), combináveis; **filtro de tom** (negativo/crítico) nos comentários e métrica de % negativos.
7. **Header some ao rolar**; filtros, abas e faixa de filtros ficam fixos. Abas logo abaixo dos filtros de data.
8. **“Evolução por tipo de voz” fica dentro do Radar de temas** (não fixa em todas as abas).
9. **Benchmark nas lojas em % 4–5★**, por marca, **seguindo granularidade e datas** (query diária); marca × tema permanece 90 dias.
10. **Linha W/Q** acima das datas em todas as tabelas de evolução (também benchmark e competitivo); **ⓘ** com explicação em tudo que precisa; **aviso de 3 s** ao filtrar comentários por clique; **🧹 Limpar filtros**; **📄 Extração geral** em PDF sem comentários; **🗓️ Mês atual**.
11. **NPS Competitivo:** dados **manuais** em `SELECT … FROM VALUES` (atualizar o SQL todo mês); formatação condicional (“% da base” em escala de calor azul; base RecargaPay com escalas verde/laranja/vermelho); **não filtrável por produto**.
12. **Redes sociais:** só interações **públicas** têm texto; DMs só agregadas e só desde 16/09/2026; “% positivas = 100% − % negativas”.
13. **Preferências de trabalho do Artur (valem para o novo painel):** precisão acima de velocidade; transparência sobre limitações dos dados; teste rigoroso antes de publicar; para análises por vertical, tratar subverticais separadamente e incluir perfil/cluster do cliente.

## 9. Limitações conhecidas e pendências
**Pendências abertas (precisam do Artur):** (a) confirmar o significado de **RAF** (“indique um amigo”); (b) mudar o agendamento para **14:08 BRT**?; (c) **desativar/reescrever `voc-weekly-analysis`**; (d) validar léxicos de **tom** e de **produto** por leitura amostral; (e) as queries do 141 ainda precisavam rodar após a última publicação para o painel mostrar dados (checar `last_run_at`).
**Limitações:** download de CSV/PDF por Blob **não testado no iframe**; desempenho com ~27 mil comentários (~11 MB) **não medido no Arturito real**; o painel real **não foi aberto** pela conversa de construção (só código/dados e mock); sentimento de lojas com backlog pós-31/08 e volume de reviews ~3× maior pela mudança de coleta (comparar com cautela, preferir % da base/% 1–2★); “Satisf.” (67,4%) citado no benchmark antigo **não foi localizado**; marca × tema do benchmark e comentários-amostra por marca ficam em **90 dias**; benchmark com filtro de produto é **mensal**; classificações por regex são heurísticas.

## 10. Lições de processo e armadilhas técnicas
- **Fluxo seguro:** `get_dashboard` antes de editar e **depois de publicar, comparando byte a byte** (ou hash) com os arquivos locais. Foi o que pegou erros reais.
- **Não redigitar queries grandes “de memória”:** ao reenviar as 16 queries, a `NPS Competitivo Manual` (20 mil caracteres) saiu com valores trocados (ex.: MercadoPago jul/26 52,4 em vez de 53,1) e só a leitura de volta revelou. Sempre gerar o payload a partir do arquivo e conferir diferenças.
- **Substituição ampla de janelas** em gerador de SQL pode atingir queries que não deveriam mudar (a janela diária das agregadas quase foi para 6 meses) → revisar o diff de cada query antes de publicar.
- **`arturito_get_dashboard` falha às vezes** logo após publicar (cron reexecutando as queries pesadas): esperar e repetir.
- **Databricks via MCP:** apenas leitura (SELECT/WITH); **`UNION` no topo não é permitido** (envolver em `SELECT * FROM (...)`); `max_rows` ≤ 10.000; resultados grandes são salvos em arquivo (usar para extrair dados do mock); `ai_query()` não funciona no warehouse do Arturito.
- **Arquivos locais de apoio** (anexe na nova conversa): `js.js`, `html.html`, `css.css`, `queries.json`, `ESPECIFICACAO.md` (histórico v8–v14) e o mock `painel_experiencia_recargapay_mock.html`.

## 11. Como começar o novo painel
**Perguntas para fazer ao Artur antes de construir:** (1) objetivo/pergunta de negócio e público do novo painel; (2) quais fontes (mesmas 3? outras tabelas?) e janela de histórico; (3) o que muda na **taxonomia** (temas/produtos/clusters) ou se reaproveita a do 141; (4) quais abas/seções do 141 manter, cortar ou trocar; (5) se há dados manuais; (6) agendamento desejado.
**O que reaproveitar do 141:** contrato de dados e query “Agregados” genérica; funções de período/granularidade (D/S/M, parcial, linha W/Q); tabelas com formatação condicional e faixas (§6); filtros globais (palavra-chave, produto, segmento) recalculando a partir de linhas de comentário; bloco de comentários (paginação, tom, CSV, destaque); ⓘ, avisos de 3 s, Limpar filtros, PDF.
**Processo:** extrair dados reais → montar **mock** com testes (reconciliação tabela × lista) → publicar → ler de volta e comparar → documentar no `ESPECIFICACAO.md`.

**Prompt sugerido para abrir a nova conversa:**
> “Quero criar um novo painel no Arturito seguindo as orientações do painel 141 (documento anexo: layout, estrutura de dados, categorização e alinhamentos). O novo painel é sobre ______ , para ______ , com as fontes ______ . Reaproveite a taxonomia de 15 temas / 18 produtos [ou: adapte assim: ______]. Antes de construir, me faça as perguntas que faltam e proponha o layout. Siga as regras: só dados do Databricks, tabelas com formatação condicional, teste com mock, publique só com minha confirmação e confira byte a byte depois de publicar.”

---
## Apêndice A — Regex dos 15 temas (SQL `RLIKE`, sobre texto normalizado `t`)
Cada regex vale em SQL e em JS (`new RegExp`). Em SQL entram dentro de `filter(array(CASE WHEN t RLIKE '…' THEN 'id' END, …), x -> x IS NOT NULL)`.

- **cartao** (💳 Cartão · anuidade, fatura, cobrança):
  `cartao|fatura|anuidade|cobranc|mensalidade`
- **credito** (💰 Empréstimo / limite):
  `emprestimo|limite|consignado|renegoc|financiamento|(?<!cartao de )(?<!cartao )credito`
- **bloqueio** (🔒 Bloqueio de conta / carteira / saldo):
  `bloque|congel|suspen|encerr|desativ|banid|retid|saldo.{0,40}(sumiu|zerad|preso|nao (liber|receb|apar))|(sumiu|zerou|preso).{0,30}saldo|dinheiro (preso|sumiu)`
- **app** (📲 App · instabilidade, login, acesso):
  `travand|trava(?!r)|lent[oa]|lentidao|(^|[^a-z])bug|erro|fora do ar|instabil|nao (abre|carrega|funciona|entra|loga)|login|logar|sem acesso|nao consigo (entrar|acessar)|crash|fechando|caiu|offline`
- **ux** (🎨 UX · usabilidade e funcionalidades):
  `interface|usabilidade|layout|design|intuitiv|complicad|confus|dificil|funcionalidad|navega|(^|[^a-z])tela|botao|menu|sugest|falta (de )?(opcao|funcao|recurso)|poderia ter`
- **fraude** (🚨 Fraude e golpes):
  `fraud|golp|clonad|clonag|invad|hack|roubad|roubo|furt|estelion|phishing|laranja|nao reconheco|compra (indevida|nao reconhec)|transacao (indevida|desconhecida)`
- **seguranca** (🛡️ Segurança e verificação):
  `segur|biometri|facial|reconhecimento|selfie|autentic|token|senha|dois fatores|verifica(cao|r)|validacao|privacidade|lgpd|dados pessoais|desconfi`
- **suporte** (🎧 Suporte · bot, atendimento, Central de ajuda):
  `atendiment|suporte|atendente|(^|[^a-z])chat([^a-z]|$)|(^|[^a-z])sac([^a-z]|$)|central de ajuda|robo|(^|[^a-z])bot([^a-z]|$)|chatbot|ouvidoria|reclame aqui|protocolo|ninguem (responde|atende)|sem (resposta|retorno)|falar com`
- **concorrencia** (⚔️ Concorrência):
  `nubank|nu bank|picpay|pic pay|mercado ?pago|banco inter|(^|[^a-z])inter([^a-z]|$)|c6 ?bank|(^|[^a-z])c6([^a-z]|$)|itau|bradesco|santander|pagbank|pagseguro|infinitepay|99pay|meutudo|(^|[^a-z])neon([^a-z]|$)|concorr|outros? (banco|bancos|app|apps)|melhor que|pior que|migr(ei|ar)|troq(uei|uar) (de )?(banco|app)`
- **pix** (⚡ Pix e transferências):
  `(^|[^a-z])pix([^a-z]|$)|transferenc|(^|[^a-z])ted([^a-z]|$)|chave|qr ?code|copia e cola|saque|sacar`
- **taxas** (💸 Taxas, tarifas e juros):
  `taxa|tarifa|juros|(^|[^a-z])caro|abusiv|custo|preco|iof|multa|encargo|spread`
- **cashback** (🎁 Cashback e benefícios):
  `cashback|cash back|beneficio|promocao|cupom|desconto|bonus|pontos|recompensa|premio|sorteio`
- **recargas** (🚌 Recargas, transporte e contas):
  `recarga|recarreg|bilhete|transporte|onibus|passagem|boleto|operadora|conta de (luz|agua)|pagar conta|giftcard|gift card|loteria`
- **cadastro** (📝 Cadastro e abertura de conta):
  `cadastr|abrir (a |minha )?conta|abertura de conta|criar (a |minha )?conta|kyc|comprovante|conta (nao )?(aprovada|negada|recusada)|reprovad|negou|negaram`
- **invest** (📈 Investimentos e rendimento):
  `investi|cdb|cofrinho|rendiment|rende|poupanca|renda fixa|cdi|(^|[^a-z])aplicar`

## Apêndice B — Léxicos de tom
**Forte (`st`)**
```
pessim|horrivel|lixo|vergonha|absurd|golpe|golpista|roubo|roubaram|enganacao|enganad|estelion|fraude|palhacada|descaso|desrespeit|inaceitavel|safad|ladr|nunca mais|pior (app|banco|empresa|atendimento)|processar|justica|procon|reclame aqui|banco central|bacen|denunci|calote|bandid|mentira|mentiroso|incompetent|ridicul|revolt|indignad|detest|lamentavel|inutil|nao recomendo
```
**Brando (`ml`)**
```
ruim|problema|erro|nao (consigo|funciona|resolve|resolveram|responde|libera|aprova|recebo|cai|chegou|abre|carrega)|demora|demorando|travand|bloquearam|bloqueou|bloqueio|cobranca indevida|cobraram|indevid|prejuizo|sem resposta|insatisf|decepc|reclam|dificuldade|complicad|lent[oa]|falha|(^|[^a-z])bug|instavel|piorou|burocra|ninguem (responde|resolve|atende)|dinheiro (preso|sumiu)|perdi|sumiu|abusiv|(^|[^a-z])caro
```
## Apêndice C — Regex dos 18 produtos (texto normalizado; ordem = bit do bitmask de produto)

- **cc** 💳 Cartão de Crédito  _(bit 1)_
  `(?<!pix com )(?<!pix no )(?<!pix pelo )cartao(?! de (transporte|bilhete|vale))|fatura|anuidade|mastercard|rotativo|limite do cartao`
- **emp** 💰 Empréstimo  _(bit 2)_
  `emprestimo(?! consignado)|financiamento|renegoc|credito pessoal|saque aniversario|pagar depois`
- **cons** 🏛️ Empréstimo Consignado  _(bit 4)_
  `consignado|inss|aposentad|margem consignavel|desconto em folha`
- **pix** ⚡ Pix  _(bit 8)_
  `(^|[^a-z])pix([^a-z]|$)|chave pix|qr ?code|copia e cola`
- **pixcc** 💳⚡ Pix com Cartão  _(bit 16)_
  `pix (com|no|pelo|via|parcelado|no credito)|pix parcelado|pix.{0,12}cartao|cartao.{0,12}pix`
- **conta** 🆕 Criação de Conta  _(bit 32)_
  `cadastr|abrir (a |minha )?conta|abertura de conta|criar (a |minha )?conta|criacao de conta|kyc|validacao (de )?(documento|identidade)|selfie|conta (nao )?(aprovada|negada|recusada)`
- **cartb** 🔒 Carteira Bloqueada  _(bit 64)_
  `carteira.{0,30}bloque|bloque.{0,30}carteira|saldo.{0,30}bloque|bloque.{0,30}saldo|bloquearam (minha |a )?(conta|carteira)|bloqueou (minha |a )?(conta|carteira)|conta bloquead|bloqueio (da|na|de) (conta|carteira)`
- **contad** 🚫 Conta Desativada  _(bit 128)_
  `desativad|desativou|desativaram|encerrad|encerrou|encerramento|conta (foi )?(cancelad|fechad|excluid)|banid|baniram|conta suspens|suspenderam`
- **chb** ↩️ Chargeback  _(bit 256)_
  `chargeback|contestac|contestei|contestar|estorno|estornaram|disputa|nao reconheco (a )?compra|compra (indevida|nao reconhec)|cobranca indevida`
- **transp** 🚌 Transporte  _(bit 512)_
  `transporte|bilhete|onibus|metro|passagem|sptrans|urbs|cptm|(^|[^a-z])brt([^a-z]|$)`
- **tap** 📲 Tap to Pay  _(bit 1024)_
  `tap ?to ?pay|tap ?on ?phone|tap2pay|maquinin|maquina de cartao|mpos|receber por aproximacao`
- **inv** 📈 CDB/Investimentos  _(bit 2048)_
  `investi|cdb|cofrinho|rendiment|rende|poupanca|renda fixa|cdi|(^|[^a-z])aplicar`
- **seg** 🛡️ Seguros  _(bit 4096)_
  `seguro (de |do |para |)?(vida|celular|residencial|auto|carro|viagem|prestamista|saude|desemprego)|(contratei|contratar|cancelar|cancelei|cobranca d?o?|desconto d?o?) seguro|apolice|sinistro|seguradora|prestamista`
- **bol** 🧾 Contas e Boletos  _(bit 8192)_
  `boleto|conta de (luz|agua|gas|telefone|internet)|pagar conta|pagamento de conta|codigo de barras|darf|iptu|ipva|debito automatico`
- **link** 🔗 Link de Pagamento  _(bit 16384)_
  `link de pagamento|link pay|payment link|link de cobranca|cobrar por link|link para cobrar`
- **raf** 🤝 RAF (indique um amigo)  _(bit 32768)_
  `indique e ganhe|indique um amigo|indicacao de amigo|codigo de (indicacao|convite)|convite de amigo|refer a friend|(^|[^a-z])raf([^a-z]|$)|bonus (por|de) indicacao|ganhar por indicar|programa de indicacao`
- **rec** 📞 Recarga de Celular  _(bit 65536)_
  `recarga.{0,15}(celular|vivo|claro|tim|oi)|(vivo|claro|tim|oi) recarga|operadora|recarregar (o )?celular|credito (no|do|de) celular|creditos? celular`
- **of** 🔄 Open Finance  _(bit 131072)_
  `open ?finance|open ?banking|compartilhamento de dados|conectar (outro |meu )?banco|vincular (outro |meu )?banco|agregar conta`

## Apêndice D — SQL-base por fonte (seleção bruta que alimenta as queries Agregados e Recentes)
Cada query faz `base` (seleção abaixo + tom) → `th` (array de temas) → agregação/lista. Janela de leitura: 12 meses; filtros finais por query.

**Relacional (`fat_indecx_metrics`)**
```sql
(SELECT b.*, (b.t RLIKE 'pessim|horrivel|lixo|vergonha|absurd|golpe|golpista|roubo|roubaram|enganacao|enganad|estelion|fraude|palhacada|descaso|desrespeit|inaceitavel|safad|ladr|nunca mais|pior (app|banco|empresa|atendimento)|processar|justica|procon|reclame aqui|banco central|bacen|denunci|calote|bandid|mentira|mentiroso|incompetent|ridicul|revolt|indignad|detest|lamentavel|inutil|nao recomendo') AS st, (b.t RLIKE 'ruim|problema|erro|nao (consigo|funciona|resolve|resolveram|responde|libera|aprova|recebo|cai|chegou|abre|carrega)|demora|demorando|travand|bloquearam|bloqueou|bloqueio|cobranca indevida|cobraram|indevid|prejuizo|sem resposta|insatisf|decepc|reclam|dificuldade|complicad|lent[oa]|falha|(^|[^a-z])bug|instavel|piorou|burocra|ninguem (responde|resolve|atende)|dinheiro (preso|sumiu)|perdi|sumiu|abusiv|(^|[^a-z])caro') AS ml, (b.r <= 6 OR coalesce(b.gs, 0) <= -0.25) AS sn, (b.r >= 9) AS po, (b.r <= 2 OR coalesce(b.gs, 0) <= -0.5) AS ex FROM (SELECT answer_date AS d, lower(user_type) AS ut, review AS r, CASE WHEN review >= 9 THEN 'p' WHEN review >= 7 THEN 'n' ELSE 'd' END AS c, gcp_score AS gs, (feedback IS NOT NULL AND length(trim(feedback)) > 5) AS tx, lower(translate(coalesce(feedback,''), 'áàâãäéèêëíìîïóòôõöúùûüç', 'aaaaaeeeeiiiiooooouuuuc')) AS t, substr(translate(coalesce(feedback,''), chr(10) || chr(13), '  '), 1, 300) AS txt FROM prod.cx.fat_indecx_metrics WHERE survey_type = 'relacional' AND action_name != 'relacional de cc titan' AND quest_level = 'main' AND lower(metric) LIKE 'nps%' AND deleted IS NOT TRUE AND answer_date >= add_months(date_trunc('month', current_date()), -11)
```
**Lojas (`fat_app_reviews`)**
```sql
(SELECT b.*, (b.t RLIKE 'pessim|horrivel|lixo|vergonha|absurd|golpe|golpista|roubo|roubaram|enganacao|enganad|estelion|fraude|palhacada|descaso|desrespeit|inaceitavel|safad|ladr|nunca mais|pior (app|banco|empresa|atendimento)|processar|justica|procon|reclame aqui|banco central|bacen|denunci|calote|bandid|mentira|mentiroso|incompetent|ridicul|revolt|indignad|detest|lamentavel|inutil|nao recomendo') AS st, (b.t RLIKE 'ruim|problema|erro|nao (consigo|funciona|resolve|resolveram|responde|libera|aprova|recebo|cai|chegou|abre|carrega)|demora|demorando|travand|bloquearam|bloqueou|bloqueio|cobranca indevida|cobraram|indevid|prejuizo|sem resposta|insatisf|decepc|reclam|dificuldade|complicad|lent[oa]|falha|(^|[^a-z])bug|instavel|piorou|burocra|ninguem (responde|resolve|atende)|dinheiro (preso|sumiu)|perdi|sumiu|abusiv|(^|[^a-z])caro') AS ml, (b.s = 'negative' OR b.r <= 2) AS sn, (b.r >= 4 AND b.s != 'negative') AS po, (b.r = 1) AS ex FROM (SELECT review_date AS d, source AS loja, rating AS r, coalesce(sentiment,'') AS s, lower(translate(concat_ws(' ', title, content), 'áàâãäéèêëíìîïóòôõöúùûüç', 'aaaaaeeeeiiiiooooouuuuc')) AS t, (length(content) > 1) AS tx, substr(translate(concat_ws(' ', content), chr(10) || chr(13), '  '), 1, 300) AS txt FROM prod.cx.fat_app_reviews WHERE brand = 'RecargaPay' AND review_date >= add_months(date_trunc('month', current_date()), -11)
```
**Redes (`fat_buzzmonitor_posts`)**
```sql
(SELECT b.*, (b.t RLIKE 'pessim|horrivel|lixo|vergonha|absurd|golpe|golpista|roubo|roubaram|enganacao|enganad|estelion|fraude|palhacada|descaso|desrespeit|inaceitavel|safad|ladr|nunca mais|pior (app|banco|empresa|atendimento)|processar|justica|procon|reclame aqui|banco central|bacen|denunci|calote|bandid|mentira|mentiroso|incompetent|ridicul|revolt|indignad|detest|lamentavel|inutil|nao recomendo') AS st, (b.t RLIKE 'ruim|problema|erro|nao (consigo|funciona|resolve|resolveram|responde|libera|aprova|recebo|cai|chegou|abre|carrega)|demora|demorando|travand|bloquearam|bloqueou|bloqueio|cobranca indevida|cobraram|indevid|prejuizo|sem resposta|insatisf|decepc|reclam|dificuldade|complicad|lent[oa]|falha|(^|[^a-z])bug|instavel|piorou|burocra|ninguem (responde|resolve|atende)|dinheiro (preso|sumiu)|perdi|sumiu|abusiv|(^|[^a-z])caro') AS ml, (b.s = 'negative') AS sn, (b.s = 'positive') AS po, false AS ex FROM (SELECT CAST(created_at AS DATE) AS d, lower(service) AS canal, CASE WHEN type IN ('direct_message','message') THEN 'dm' ELSE 'publico' END AS tp, coalesce(sentiment,'') AS s, (post_related_ticket IS NOT NULL) AS tk, (content IS NOT NULL AND length(trim(content)) > 1 AND coalesce(only_emojis,false) = false) AS tx, lower(translate(coalesce(content,''), 'áàâãäéèêëíìîïóòôõöúùûüç', 'aaaaaeeeeiiiiooooouuuuc')) AS t, substr(translate(coalesce(content,''), chr(10) || chr(13), '  '), 1, 300) AS txt FROM prod.cx.fat_buzzmonitor_posts WHERE type IN ('comment','comment_reply','mention','comment_from_mention','review','COMMENT','REPLY','reply','direct_message','message') AND CAST(created_at AS DATE) >= add_months(date_trunc('month', current_date()), -11)
```
**Estrutura de agregação (exemplo: Rel Agregados — `gr` repete a base nas 3 janelas D/S/M; `se` = série; `te` = temas com `explode`)**
```sql
gr AS (SELECT 'D' AS g, date_format(d,'yyyy-MM-dd') AS p, th.* FROM th WHERE d >= date_sub(current_date(), 89) UNION ALL SELECT 'S', date_format(date_trunc('week', d),'yyyy-MM-dd'), th.* FROM th WHERE d >= date_sub(date_trunc('week', current_date()), 175) UNION ALL SELECT 'M', date_format(date_trunc('month', d),'yyyy-MM-dd'), th.* FROM th WHERE d >= add_months(date_trunc('month', current_date()), -11)), ex AS (SELECT *, explode(CASE WHEN size(arr) = 0 THEN array('sem_tema') ELSE arr END) AS tema FROM gr WHERE tx), se AS (SELECT 'serie' AS ds, g, p AS periodo, ut AS k1, '' AS k2, '' AS k3, '' AS k4, '' AS k5, '' AS k6, count(*) AS n1, sum(CASE WHEN c = 'p' THEN 1 ELSE 0 END) AS n2, sum(CASE WHEN c = 'n' THEN 1 ELSE 0 END) AS n3, sum(CASE WHEN c = 'd' THEN 1 ELSE 0 END) AS n4, sum(CASE WHEN tx THEN 1 ELSE 0 END) AS n5, CAST(NULL AS BIGINT) AS n6, CAST(NULL AS BIGINT) AS n7, CAST(NULL AS BIGINT) AS n8 FROM gr GROUP BY g, p, ut), te AS (SELECT 'temas' AS ds, g, p AS periodo, tema AS k1, '' AS k2, '' AS k3, '' AS k4, '' AS k5, '' AS k6, count(*) AS n1, sum(CASE WHEN c = 'p' THEN 1 ELSE 0 END) AS n2, sum(CASE WHEN c = 'n' THEN 1 ELSE 0 END) AS n3, sum(CASE WHEN c = 'd' THEN 1 ELSE 0 END) AS n4, sum(CASE WHEN tom >= 1 THEN 1 ELSE 0 END) AS n5, sum(CASE WHEN tom = 2 THEN 1 ELSE 0 END) AS n6, CAST(NULL AS BIGINT) AS n7, CAST(NULL AS BIGINT) AS n8 FROM ex GROUP BY g, p, tema) SELECT * FROM (SELECT * FROM se UNION ALL SELECT * FROM te) u
```
## Apêndice E — SQL completo de “Rel Respostas Clusters” (1 linha por resposta, 6 meses)
Contém a derivação dos 8 clusters, das 9 notas adicionais, do bitmask de temas e do tom (`tom` é calculado, mas esta query devolve d, u, r, k, p, m, a).
```sql
WITH r AS (SELECT i.control_id AS cid, i.answer_date AS d, lower(i.user_type) AS u, i.review AS rv, i.review_class AS cls, i.gcp_score AS gs, i.user_id AS uid, (i.feedback IS NOT NULL AND length(trim(i.feedback)) > 5) AS tx, lower(translate(coalesce(i.feedback,''), 'áàâãäéèêëíìîïóòôõöúùûüç', 'aaaaaeeeeiiiiooooouuuuc')) AS t, substr(translate(coalesce(i.feedback,''), chr(10) || chr(13), '  '), 1, 300) AS txt FROM prod.cx.fat_indecx_metrics i WHERE i.survey_type = 'relacional' AND i.action_name != 'relacional de cc titan' AND i.quest_level = 'main' AND lower(i.metric) LIKE 'nps%' AND i.deleted IS NOT TRUE AND i.answer_date >= add_months(date_trunc('month', current_date()), -5)), ru AS (SELECT DISTINCT uid FROM r), ad AS (SELECT control_id AS cid, max(CASE WHEN lower(quest) LIKE 'facilidade de uso%' THEN review END) AS q1, max(CASE WHEN lower(quest) LIKE 'aparência%' THEN review END) AS q2, max(CASE WHEN lower(quest) LIKE 'utilidade da comunicação%' THEN review END) AS q3, max(CASE WHEN lower(quest) LIKE '%praticidade de esclarecer%' THEN review END) AS q4, max(CASE WHEN lower(quest) LIKE '%confia no recargapay%' THEN review END) AS q5, max(CASE WHEN lower(quest) LIKE 'estabilidade%' THEN review END) AS q6, max(CASE WHEN lower(quest) LIKE 'facilidade de conciliação%' THEN review END) AS q7, max(CASE WHEN lower(quest) LIKE 'rapidez para vender%' THEN review END) AS q8, max(CASE WHEN lower(quest) LIKE '%seguro em relação%' THEN review END) AS q9 FROM prod.cx.fat_indecx_metrics WHERE survey_type = 'relacional' AND quest_level = 'add' AND (lower(metric) = 'ces' OR lower(metric) LIKE 'csat%') AND deleted IS NOT TRUE AND answer_date >= add_months(date_trunc('month', current_date()), -5) GROUP BY 1), nr AS (SELECT r.cid, min(CASE WHEN n.event_timestamp IS NOT NULL AND date_trunc('month', n.event_timestamp) = date_trunc('month', r.d) THEN 'N' ELSE 'R' END) AS c FROM r LEFT JOIN prod.core.fat_new_users n ON r.uid = CAST(n.user_id AS STRING) GROUP BY r.cid), tc AS (SELECT r.cid, min(CASE c.credit_type WHEN 'COLLATERAL' THEN 'C' WHEN 'GRANTED' THEN 'G' WHEN 'INVESTMENT' THEN 'I' END) AS c FROM r JOIN prod.credit_card.dim_card_account c ON r.uid = CAST(c.rp_user_id AS STRING) WHERE c.account_status = 'NORMAL' AND c.credit_type IS NOT NULL GROUP BY r.cid), inv AS (SELECT DISTINCT CAST(userid AS STRING) AS uid FROM prod.checkout.dim_investment_lifecycle WHERE lifecycle_status = 'ACTIVE'), tp AS (SELECT user_id AS uid, date_trunc('month', fat_date) AS mes, sum(tpv_monetizable) AS tpv, count(*) AS n FROM prod.core.fat_tpv WHERE fat_date >= add_months(date_trunc('month', current_date()), -5) AND user_id IN (SELECT uid FROM ru) GROUP BY 1, 2), sp AS (SELECT DISTINCT userid AS uid, date_trunc('month', created_at_br) AS mes FROM prod.cx.dim_zendesk_tickets_summary WHERE created_at_br >= add_months(date_trunc('month', current_date()), -5)), act AS (SELECT DISTINCT user_id AS uid, date_trunc('week', event_date) AS wk FROM prod.core.fat_active_users WHERE event_date >= date_sub(add_months(date_trunc('month', current_date()), -5), 14) AND user_id IN (SELECT uid FROM ru)), pa AS (SELECT user_id AS uid, min(date_trunc('week', event_date)) AS fw FROM prod.core.fat_active_users WHERE user_id IN (SELECT uid FROM ru) GROUP BY 1), rt AS (SELECT r.cid, min(CASE WHEN pa.fw = date_trunc('week', r.d) THEN 'N' WHEN a1.uid IS NOT NULL THEN 'R' WHEN a0.uid IS NOT NULL THEN 'S' ELSE 'C' END) AS c FROM r LEFT JOIN pa ON r.uid = pa.uid LEFT JOIN act a1 ON r.uid = a1.uid AND a1.wk = date_trunc('week', r.d) LEFT JOIN act a0 ON r.uid = a0.uid AND a0.wk = date_trunc('week', r.d) - INTERVAL 7 DAYS GROUP BY r.cid), pr AS (SELECT r.cid, concat_ws(';', collect_set(f.product_name)) AS p FROM r JOIN (SELECT DISTINCT user_id AS uid, date_trunc('week', event_date) AS wk, product_name FROM prod.core.fat_active_users WHERE event_date >= date_sub(current_date(), 30) AND user_id IN (SELECT uid FROM ru)) f ON r.uid = f.uid AND f.wk = date_trunc('week', r.d) GROUP BY r.cid), fx0 AS (SELECT r.cid, r.d, r.u, r.rv, r.cls, r.gs, r.tx, r.t, r.txt, (r.t RLIKE 'pessim|horrivel|lixo|vergonha|absurd|golpe|golpista|roubo|roubaram|enganacao|enganad|estelion|fraude|palhacada|descaso|desrespeit|inaceitavel|safad|ladr|nunca mais|pior (app|banco|empresa|atendimento)|processar|justica|procon|reclame aqui|banco central|bacen|denunci|calote|bandid|mentira|mentiroso|incompetent|ridicul|revolt|indignad|detest|lamentavel|inutil|nao recomendo') AS st, (r.t RLIKE 'ruim|problema|erro|nao (consigo|funciona|resolve|resolveram|responde|libera|aprova|recebo|cai|chegou|abre|carrega)|demora|demorando|travand|bloquearam|bloqueou|bloqueio|cobranca indevida|cobraram|indevid|prejuizo|sem resposta|insatisf|decepc|reclam|dificuldade|complicad|lent[oa]|falha|(^|[^a-z])bug|instavel|piorou|burocra|ninguem (responde|resolve|atende)|dinheiro (preso|sumiu)|perdi|sumiu|abusiv|(^|[^a-z])caro') AS ml, concat(coalesce(nr.c, 'R'), coalesce(tc.c, '-'), CASE WHEN inv.uid IS NOT NULL THEN '1' ELSE '0' END, CASE WHEN tp.tpv IS NULL OR tp.tpv = 0 THEN '0' WHEN tp.tpv < 200 THEN '1' WHEN tp.tpv < 1000 THEN '2' WHEN tp.tpv < 4000 THEN '3' ELSE '4' END, CASE WHEN tp.n IS NULL OR tp.n = 0 THEN '0' WHEN tp.n <= 5 THEN '1' WHEN tp.n <= 20 THEN '2' WHEN tp.n <= 60 THEN '3' ELSE '4' END, CASE WHEN sp.uid IS NOT NULL THEN '1' ELSE '0' END, coalesce(rt.c, 'C')) AS k, coalesce(pr.p, '') AS p, filter(array(CASE WHEN t RLIKE 'cartao|fatura|anuidade|cobranc|mensalidade' THEN 'cartao' END, CASE WHEN t RLIKE 'emprestimo|limite|consignado|renegoc|financiamento|(?<!cartao de )(?<!cartao )credito' THEN 'credito' END, CASE WHEN t RLIKE 'bloque|congel|suspen|encerr|desativ|banid|retid|saldo.{0,40}(sumiu|zerad|preso|nao (liber|receb|apar))|(sumiu|zerou|preso).{0,30}saldo|dinheiro (preso|sumiu)' THEN 'bloqueio' END, CASE WHEN t RLIKE 'travand|trava(?!r)|lent[oa]|lentidao|(^|[^a-z])bug|erro|fora do ar|instabil|nao (abre|carrega|funciona|entra|loga)|login|logar|sem acesso|nao consigo (entrar|acessar)|crash|fechando|caiu|offline' THEN 'app' END, CASE WHEN t RLIKE 'interface|usabilidade|layout|design|intuitiv|complicad|confus|dificil|funcionalidad|navega|(^|[^a-z])tela|botao|menu|sugest|falta (de )?(opcao|funcao|recurso)|poderia ter' THEN 'ux' END, CASE WHEN t RLIKE 'fraud|golp|clonad|clonag|invad|hack|roubad|roubo|furt|estelion|phishing|laranja|nao reconheco|compra (indevida|nao reconhec)|transacao (indevida|desconhecida)' THEN 'fraude' END, CASE WHEN t RLIKE 'segur|biometri|facial|reconhecimento|selfie|autentic|token|senha|dois fatores|verifica(cao|r)|validacao|privacidade|lgpd|dados pessoais|desconfi' THEN 'seguranca' END, CASE WHEN t RLIKE 'atendiment|suporte|atendente|(^|[^a-z])chat([^a-z]|$)|(^|[^a-z])sac([^a-z]|$)|central de ajuda|robo|(^|[^a-z])bot([^a-z]|$)|chatbot|ouvidoria|reclame aqui|protocolo|ninguem (responde|atende)|sem (resposta|retorno)|falar com' THEN 'suporte' END, CASE WHEN t RLIKE 'nubank|nu bank|picpay|pic pay|mercado ?pago|banco inter|(^|[^a-z])inter([^a-z]|$)|c6 ?bank|(^|[^a-z])c6([^a-z]|$)|itau|bradesco|santander|pagbank|pagseguro|infinitepay|99pay|meutudo|(^|[^a-z])neon([^a-z]|$)|concorr|outros? (banco|bancos|app|apps)|melhor que|pior que|migr(ei|ar)|troq(uei|uar) (de )?(banco|app)' THEN 'concorrencia' END, CASE WHEN t RLIKE '(^|[^a-z])pix([^a-z]|$)|transferenc|(^|[^a-z])ted([^a-z]|$)|chave|qr ?code|copia e cola|saque|sacar' THEN 'pix' END, CASE WHEN t RLIKE 'taxa|tarifa|juros|(^|[^a-z])caro|abusiv|custo|preco|iof|multa|encargo|spread' THEN 'taxas' END, CASE WHEN t RLIKE 'cashback|cash back|beneficio|promocao|cupom|desconto|bonus|pontos|recompensa|premio|sorteio' THEN 'cashback' END, CASE WHEN t RLIKE 'recarga|recarreg|bilhete|transporte|onibus|passagem|boleto|operadora|conta de (luz|agua)|pagar conta|giftcard|gift card|loteria' THEN 'recargas' END, CASE WHEN t RLIKE 'cadastr|abrir (a |minha )?conta|abertura de conta|criar (a |minha )?conta|kyc|comprovante|conta (nao )?(aprovada|negada|recusada)|reprovad|negou|negaram' THEN 'cadastro' END, CASE WHEN t RLIKE 'investi|cdb|cofrinho|rendiment|rende|poupanca|renda fixa|cdi|(^|[^a-z])aplicar' THEN 'invest' END), x -> x IS NOT NULL) AS arr, concat(coalesce(CAST(ad.q1 AS STRING), '0'), coalesce(CAST(ad.q2 AS STRING), '0'), coalesce(CAST(ad.q3 AS STRING), '0'), coalesce(CAST(ad.q4 AS STRING), '0'), coalesce(CAST(ad.q5 AS STRING), '0'), coalesce(CAST(ad.q6 AS STRING), '0'), coalesce(CAST(ad.q7 AS STRING), '0'), coalesce(CAST(ad.q8 AS STRING), '0'), coalesce(CAST(ad.q9 AS STRING), '0')) AS a FROM r LEFT JOIN nr ON r.cid = nr.cid LEFT JOIN tc ON r.cid = tc.cid LEFT JOIN inv ON r.uid = inv.uid LEFT JOIN tp ON r.uid = tp.uid AND date_trunc('month', r.d) = tp.mes LEFT JOIN sp ON r.uid = sp.uid AND date_trunc('month', r.d) = sp.mes LEFT JOIN rt ON r.cid = rt.cid LEFT JOIN pr ON r.cid = pr.cid LEFT JOIN ad ON r.cid = ad.cid), fx AS (SELECT *, CASE WHEN tx THEN aggregate(transform(arr, x -> CASE x WHEN 'cartao' THEN 1 WHEN 'credito' THEN 2 WHEN 'bloqueio' THEN 4 WHEN 'app' THEN 8 WHEN 'ux' THEN 16 WHEN 'fraude' THEN 32 WHEN 'seguranca' THEN 64 WHEN 'suporte' THEN 128 WHEN 'concorrencia' THEN 256 WHEN 'pix' THEN 512 WHEN 'taxas' THEN 1024 WHEN 'cashback' THEN 2048 WHEN 'recargas' THEN 4096 WHEN 'cadastro' THEN 8192 WHEN 'invest' THEN 16384 END), 0, (acc, v) -> acc + v) ELSE -1 END AS m, CASE WHEN ((rv <= 6 OR coalesce(gs, 0) <= -0.25) OR (ml AND NOT (rv >= 9))) AND (st OR (rv <= 2 OR coalesce(gs, 0) <= -0.5)) THEN 2 WHEN ((rv <= 6 OR coalesce(gs, 0) <= -0.25) OR (ml AND NOT (rv >= 9))) THEN 1 ELSE 0 END AS tom FROM fx0) SELECT date_format(d, 'yyyy-MM-dd') AS d, u, CAST(rv AS STRING) AS r, k, p, m, a FROM fx ORDER BY d
```
## Apêndice F — Formato da query manual “NPS Competitivo Manual”
`SELECT tp, a, b, c, d, e, f, g, h, i, j FROM VALUES (...) AS v(tp, a, b, c, d, e, f, g, h, i, j)` — tudo texto; célula vazia = dado ausente (aparece hachurado).
| tp | a | b | c | d | e | f | g | h | i | j |
|---|---|---|---|---|---|---|---|---|---|---|
| `nps` | id (rp, pp, nu, mp) | nome | cor hex | fonte (“Benchmark (digitado)”) | mês `YYYY-MM` | NPS do benchmark | NPS recalculado das planilhas* | n respostas* | promotores* | detratores* |
| `base` | mês | nº de comentários com > 5 caracteres | | | | | | | | |
| `tema` | id do tema | mês | volume | promotores | detratores | | | | | |
| `coment` | mês | classe (p/n/d) | temas (csv) | texto (≈150 caracteres) | | | | | | |
\* só para a linha da RecargaPay. Jan–set/26 digitados: RecargaPay 59,9 · 60,5 · 61,2 · 62,9 · 63,1 · 63,5 · 63,9 · 62,5 · 60,5; PicPay 56,9 · 57,3 · 58,0 · 58,8 · 59,0 · 59,6 · 57,9 · 58,4 · 57,6; Nubank 58,3 · 57,3 · 56,6 · 55,3 · 57,1 · 57,8 · 54,9 · 53,9 · 53,3; MercadoPago 50,8 · 52,6 · 52,2 · 51,0 · 50,2 · 51,6 · 53,1 · 53,6 · 52,4. O ranking usa só meses em que os 4 players têm dado.
