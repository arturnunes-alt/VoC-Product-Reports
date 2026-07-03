# Orientações Editoriais e de Análise por Canal
**Repositório:** VoC-Product-Reports  
**Versão:** 2.0  
**Mantenedor:** Artur Nunes — com inputs dos DRIs de cada squad

---

## Como usar este arquivo

Este arquivo define **como** a Routine analisa e apresenta os dados — não **o quê** ela deve
encontrar. A Routine identifica automaticamente os temas mais relevantes da semana lendo os
canais Slack e os dados coletados. As orientações aqui garantem que a análise seja estruturada,
comparável entre períodos e adequada a cada público.

**Não preencha temas ou eventos antecipadamente.** A Routine descobre os temas ao executar.
Se houver contexto crítico pontual a adicionar (ex: incidente ainda não refletido nos dados),
registre em `contexto_pontual` no canal correspondente — campo opcional, limpo a cada semana.

---

## INDICADORES — REFERÊNCIA GLOBAL

Aplicar a todos os reports. A Routine usa estas definições para calcular e apresentar cada métrica.

### NPS Transacional
- **Meta:** 75 pts
- **Escala:** 0–10 · Promotores ≥9 · Detratores ≤6
- **Fonte:** `prod.cx.fat_indecx_metrics` WHERE `metric = 'nps-0-10'`
- **Quando:** Pesquisa enviada após cada transação realizada
- **Segmentação:** Por produto/vertical
- **Variações:** Correlacionar com mudanças de produto, atualizações e incidentes do período
- **Perguntas adicionais:** Extrair temas recorrentes das respostas abertas

### NPS Relacional
- **Meta:** 50 pts
- **Escala:** 0–10 · Promotores ≥9 · Detratores ≤6
- **Fonte:** `prod.cx.fat_indecx_metrics` WHERE `metric = 'nps-relacional'` (ou métrica equivalente)
- **Quando:** Pesquisa enviada para clientes ativos da base
- **Segmentação:** PF vs PJ — apresentar separadamente
- **Variações:** Fortemente impactada por incidentes, atualizações do app e mudanças de produto
- **Perguntas adicionais:** Mapear menções a produtos específicos nos feedbacks abertos

### CSAT Atendimento (Customer Service N1)
- **Meta:** 80%
- **Escala:** 1–5 · Satisfeitos ≥4 · Insatisfeitos ≤2
- **Fonte:** `prod.cx.fat_indecx_metrics` WHERE `metric = 'csat-1-5'` + `flg_human = true`
- **Quando:** Pesquisa enviada após atendimento humano (C2C, Chat, E-mail)
- **Inclui:** Pergunta de Resolutividade — apresentar % de resolução separadamente
- **Mede:** Satisfação com o atendimento recebido e solução oferecida

### CSAT RecargaBot
- **Meta:** 80%
- **Escala:** 1–5
- **Fonte:** `prod.cx.fat_indecx_metrics` WHERE `metric = 'csat-1-5'` + `flg_retention_bot = true`
- **Quando:** Pesquisa enviada para clientes retidos pelo bot sem transferência humana
- **Inclui:** Pergunta de Resolutividade — apresentar % de resolução separadamente
- **Mede:** Satisfação com o atendimento do RecargaBot

### Retenção de Bot
- **Definição:** % de contatos resolvidos pelo RecargaBot sem transbordo para humano
- **Cálculo:** Tickets com `flg_retention_bot = true` ÷ total de contatos iniciados no bot
- **Fonte:** `prod.cx.dim_zendesk_tickets_summary`
- **Apresentar:** % semanal + evolução nas últimas 5 semanas

---

## FUNIL DE SUPORTE — REFERÊNCIA GLOBAL

Apresentar em todos os reports a visão do funil completo. A Routine monta este funil
com dados do Databricks e Amplitude (ou `prod.cx.fat_help_center_events`).

**Central de Ajuda — segmentar sempre por `event_category`:**
- `artigo` → cliente abriu um artigo específico (usar para top artigos e funil artigo→bot)
- `vertical` → navegou até a categoria/vertical sem abrir artigo — sinal de gap de conteúdo
- `pesquisa` → usou a busca sem necessariamente encontrar artigo — mesmo sinal de gap
- `ajuda` → acesso genérico, usar só para o número absoluto de topo do funil

Volume alto em `vertical` ou `pesquisa` sem artigo de destaque correspondente na mesma
vertical é candidato direto à seção "Destaques e Oportunidades" do Report Geral.

```
Central de Ajuda (artigos acessados)
    ↓ [% que acessa automações ou bot]
RecargaBot (contatos iniciados)
    ↓ [% retidos pelo bot — Retenção de Bot]
Customer Service N1 (atendimento humano: C2C, Chat, E-mail)
    ↓ [% escalados]
Special Cases N2 (Ouvidoria, ReclameAqui, Regulatórios, Redes Sociais)
```

**Regras de separação obrigatórias:**
- N1 (`flg_human = true`, `flg_invalid_bot = false`, `flg_retention_bot = false`, canal não contém 'deriva')
- Bot retido (`flg_retention_bot = true`)
- Special Cases N2 (canais: ouvidoria, reclameaqui, consumidor.gov, bacen, procon, redes sociais)
- Derivações (canal contém 'deriva') — excluir de todas as contagens de volume
- Duplicados e inválidos (`flg_invalid_bot = true`) — excluir sempre

---

## PADRÃO DE APRESENTAÇÃO — SLACK

Todos os reports são lidos em janela lateral do Slack. Aplicar sempre:

- Mensagem raiz: máximo 5 linhas, nenhuma seção, texto corrido
- Thread 1 (report): seções com `*Título*` em negrito, listas com `•`, sem tabelas complexas
- Nunca usar tabelas markdown — usar listas alinhadas ou texto estruturado
- Negrito (`*texto*`) apenas em números-chave, nomes de indicadores e alertas
- Separar seções com linha em branco — sem `---` ou separadores visuais
- Máximo 2 níveis de hierarquia: seção principal → itens com `•`
- Omitir seções sem dados calculados — nunca exibir "indisponível" ou erro

**Formato padrão de evolução (usar em todas as métricas com histórico):**
```
*NPS Transacional*
Semana atual: *62 pts* (+4 vs sem. ant.) | Meta: 75
Últimas 5 semanas: 58 → 59 → 61 → 58 → 62
```

**Formato padrão de volume com variação:**
```
*Atendimento N1*
*1.243 tickets* esta semana (+8% vs sem. ant. | +12% vs média 4 sem.)
```

---

## 🏠 #the-cxm-house — REPORT GERAL

**Público:** Time CXM completo — analistas, coordenadores, gestores  
**Formato:** Report analítico completo com correlações e oportunidades

### Instruções de análise

**Antes de gerar:** Ler os últimos 7 dias de `#the-cxm-house`, `#lideres-cx-e-cxm` e
`#comunicados_e_atualizações_cx` para identificar os temas ativos da semana.
Identificar automaticamente os 3 temas mais relevantes para o time CXM com base no
volume de discussão, alertas postados e variações detectadas nos dados.

**Estrutura do report (Thread 1):**

```
*📊 Report VoC — Semana NN · DD/MM–DD/MM*

*Contexto da semana* 💬
• [tema 1 identificado nos canais — 1 linha]
• [tema 2 — 1 linha]
• [tema 3 — 1 linha]
Correlacionar cada tema com as variações observadas nos dados.

─────────────────────────────
*FUNIL DE SUPORTE*

*Central de Ajuda*
• [N] acessos a artigos no período 📊
• Top 3 artigos mais acessados com volume
• % que avançou para o RecargaBot

*RecargaBot*
• [N] contatos iniciados | Retenção: *[X%]* (Meta: — | sem. ant.: [X%])
• CSAT Bot: *[X pts]* | Resolutividade: *[X%]*
• Top 3 motivos de não-retenção

*Customer Service N1*
• *[N] atendimentos humanos* ([+/-X%] vs sem. ant. | [+/-X%] vs média 4 sem.)
• Canais: Chat [X%] · C2C [X%] · E-mail [X%]
• CSAT N1: *[X pts]* (Meta: 80% | Resolutividade: [X%])

*Special Cases N2*
• *[N] contatos* · Reclame Aqui: [N] · Ouvidoria: [N] · Consumidor.gov: [N]
• Sentimento predominante: [positivo/negativo/neutro]

─────────────────────────────
*INDICADORES DE SATISFAÇÃO*

*NPS Transacional* 📊
[Formato padrão de evolução — 5 semanas]
• Top 3 produtos com maior variação na semana
• Temas recorrentes nas respostas abertas dos detratores

*NPS Relacional* 📊
PF: *[X pts]* | PJ: *[X pts]* (Meta: 50)
Últimas 5 semanas: [série]
• Menções a produtos nos feedbacks abertos

*CSAT Atendimento* 📊
[Formato padrão — 5 semanas]
Satisfeitos (≥4): *[X%]* | Insatisfeitos (≤2): *[X%]*

─────────────────────────────
*TOP VERTICAIS — ATENDIMENTO N1*

Para as top 5 verticais por volume:
• [Vertical]: *[N] tickets* ([+/-X%] WoW) · Motivo principal: [motivo]

─────────────────────────────
*DESTAQUES E OPORTUNIDADES*

Listar apenas movimentos que exijam ação do time de análise:
• Crescimento fora do forecast (>20% WoW em motivo ou vertical)
• Novo cluster de contatos emergente
• Gap de automação identificado (alto volume, bot não resolve)
• Motivo recorrente sem causa raiz mapeada

─────────────────────────────
*ALERTAS* 🚨
[Apenas alertas com threshold atingido — omitir seção se não houver]
🔴 *[NOME]* | Observado: [X] | Esperado: [Y] | [contexto 1 linha]

🔗 https://sites.google.com/recargapay.com/voc/
```

**Comparação histórica:** Sempre comparar com as 5 semanas anteriores para volume,
NPS, CSAT e Retenção de Bot. Usar Databricks para puxar série histórica.

**Correlações obrigatórias:** Se houver variação >15% em qualquer indicador, identificar
o evento ou ação da semana que pode explicar — buscar em Slack e dados antes de atribuir.

```
contexto_pontual: ""
```

---

## 👔 #lideres-cx-e-cxm — REPORT EXECUTIVO

**Público:** Marco Galan, Anderson Fernandes, gestores de produto e operações  
**Formato:** Informativo e direto — correlaciona resultados com ações e eventos, sem expor oportunidades de melhoria

### Instruções de análise

**Antes de gerar:** Ler os últimos 7 dias de `#lideres-cx-e-cxm` para capturar o
contexto de gestão ativo. Identificar os 2–3 resultados mais relevantes para lideranças
(impacto em OKRs, incidentes críticos, tendências de satisfação).

**Estrutura do report (Thread 1):**

```
*📊 Report Executivo VoC — Semana NN · DD/MM–DD/MM*

*Resultado da semana em 3 linhas*
[Síntese dos movimentos mais relevantes para decisão executiva — sem detalhes técnicos]

─────────────────────────────
*SATISFAÇÃO DO CLIENTE*

*NPS Transacional:* *[X pts]* ([+/-X] vs sem. ant.) | Meta: 75
Últimas 5 semanas: [série compacta]
• [produto com maior alta] ↑ e [produto com maior queda] ↓
• Correlação com [evento/ação da semana se houver]

*NPS Relacional:* PF *[X pts]* · PJ *[X pts]* | Meta: 50
• [variação relevante e correlação com ação/incidente]

*CSAT Atendimento:* *[X%]* satisfeitos | Meta: 80%
*CSAT RecargaBot:* *[X%]* satisfeitos | Meta: 80%

─────────────────────────────
*VOLUME DE SUPORTE*

*[N] atendimentos totais* ([+/-X%] vs sem. ant.)
• RecargaBot resolveu *[X%]* dos contatos (Retenção)
• N1 humano: *[N]* atendimentos · N2 Special Cases: *[N]*
• Vertical de maior volume: [vertical] — [motivo principal]

─────────────────────────────
*EVENTOS E IMPACTOS DA SEMANA* 💬
• [evento 1] → impacto em [indicador/volume] [+/-X%]
• [evento 2] → [impacto]
[Omitir se não houver eventos relevantes com impacto mensurável]

─────────────────────────────
*PONTOS DE ATENÇÃO*
[Apenas situações que exijam decisão ou acompanhamento executivo]
🔴 [alerta crítico se houver]
🟡 [situação a monitorar se houver]

🔗 https://sites.google.com/recargapay.com/voc/
```

**Regras editoriais:**
- Não expor oportunidades de melhoria operacional — foco em resultados e correlações
- Não usar jargões técnicos de dados (tags, IDs de campo, nomes de tabelas)
- Cada dado deve ter uma correlação com ação, evento ou incidente quando disponível
- Máximo 1 scroll de leitura na janela lateral do Slack

```
contexto_pontual: ""
```

---

## 👤 #account_cx — MINHA CONTA

**Público:** Squad Account e CX  
**Formato:** Report de produto com abertura por perfil de cliente

### Instruções de análise

Identificar automaticamente os temas ativos lendo o canal `#account_cx` dos últimos 7 dias.
Priorizar na análise os motivos com maior variação WoW e os temas com mais discussão no canal.

**Aberturas obrigatórias por perfil:**
- **New** (conta criada há ≤30 dias): via `fat_user_data.reg_date`
- **NewNew** (conta >30 dias, nunca usou o produto): via `clo_orders` sem pedidos em Minha Conta
- **Repeat** (já utilizou o produto anteriormente)

**Estrutura do report (Thread 1):**

```
*📊 Report VoC — Minha Conta · Semana NN*

─────────────────────────────
*FUNIL DE SUPORTE — MINHA CONTA*
[Funil completo: Central de Ajuda → Bot → N1 → N2]

*ATENDIMENTO N1*
*[N] tickets* ([+/-X%] WoW | [+/-X%] vs média 4 sem.)
CSAT: *[X pts]* | Resolutividade: *[X%]*
Últimas 5 semanas: [série]

Top motivos de contato:
• *[motivo 1]:* [N] tickets ([X%]) — [variação WoW]
• *[motivo 2]:* [N] tickets ([X%])
• *[motivo 3]:* [N] tickets ([X%])

Top causas raiz (análise qualitativa via Zendesk MCP):
• *[causa 1]:* [problema do cliente em 1 linha] | Bot resolve? [Sim/Não]
• *[causa 2]:* [problema] | Bot: [Sim/Não]

─────────────────────────────
*PERFIL DOS CLIENTES*

• *New* (≤30 dias): [N] tickets ([X%]) — motivo principal: [motivo]
• *NewNew* (>30d sem uso): [N] tickets ([X%]) — motivo principal: [motivo]
• *Repeat*: [N] tickets ([X%]) — motivo principal: [motivo]
PF: [X%] · PJ: [X%]

─────────────────────────────
*NPS TRANSACIONAL — MINHA CONTA* 📊
*[X pts]* ([+/-X] vs sem. ant.) | Meta: 75
Últimas 5 semanas: [série]
• Temas dos detratores: [temas das respostas abertas]

─────────────────────────────
*SPECIAL CASES N2*
• [N] contatos · Sentimento: [predominante]
• Temas principais: [temas]

─────────────────────────────
*DESTAQUES DA SEMANA* 💬
• [tema identificado no canal com correlação nos dados]
• [variação relevante com explicação]

🔗 https://sites.google.com/recargapay.com/voc/
```

```
contexto_pontual: ""
```

---

## 💳 #cc-produto-e-cx — CARTÃO DE CRÉDITO

**Público:** Squad Cartão de Crédito e CX  
**Formato:** Report de produto com abertura por tipo de cartão e perfil de cliente

### Instruções de análise

Identificar automaticamente os temas ativos lendo `#cc-produto-e-cx` dos últimos 7 dias.

**Aberturas obrigatórias:**

Por tipo de cartão (via `cc_recargapay_card_account`):
- **Garantido** (Standard, Gold, PJ)
- **Concedido** (Platinum, Black)
- **Investment** (Titan, Platinum CDB)

Por perfil de cliente: New · NewNew · Repeat

Por tipo de transação Pix (quando relevante):
- Pix com Wallet vs Pix com Cartão de Crédito (via `flag_pix_cartao`)

**Estrutura do report (Thread 1):**

```
*📊 Report VoC — Cartão de Crédito · Semana NN*

─────────────────────────────
*FUNIL DE SUPORTE — CARTÃO DE CRÉDITO*
[Funil completo]

*ATENDIMENTO N1*
*[N] tickets* ([+/-X%] WoW)
CSAT: *[X pts]* | Resolutividade: *[X%]*
Últimas 5 semanas: [série]

Top motivos:
• *[motivo 1]:* [N] ([X%]) — [variação WoW + contexto se houver]
• *[motivo 2]:* [N] ([X%])
• *[motivo 3]:* [N] ([X%])

Top causas raiz (qualitativo):
• *[causa 1]:* [problema] | Bot: [Sim/Não]
• *[causa 2]:* [problema] | Bot: [Sim/Não]

─────────────────────────────
*ABERTURA POR TIPO DE CARTÃO*

• *Garantido* (Standard/Gold/PJ): [N] tickets ([X%]) | CSAT: [X] | Motivo principal: [motivo]
• *Concedido* (Platinum/Black): [N] tickets ([X%]) | CSAT: [X] | Motivo principal: [motivo]
• *Investment* (Titan/Platinum CDB): [N] tickets ([X%]) | CSAT: [X] | Motivo principal: [motivo]

─────────────────────────────
*PERFIL DOS CLIENTES*
• New: [N] ([X%]) · NewNew: [N] ([X%]) · Repeat: [N] ([X%])

*PIX — ABERTURA POR ORIGEM* (quando volume relevante)
• Pix com Wallet: [N] tickets
• Pix com Cartão: [N] tickets | Motivo principal: [motivo]

─────────────────────────────
*NPS TRANSACIONAL — CARTÃO* 📊
*[X pts]* ([+/-X] vs sem. ant.) | Meta: 75
Últimas 5 semanas: [série]
• Temas dos detratores por tipo de cartão

─────────────────────────────
*SPECIAL CASES N2*
• [N] contatos · Reclame Aqui: [N] · Ouvidoria: [N]
• Tema predominante: [tema]

─────────────────────────────
*DESTAQUES DA SEMANA* 💬
• [temas do canal correlacionados com variações nos dados]

🔗 https://sites.google.com/recargapay.com/voc/
```

```
contexto_pontual: ""
```

---

## 🔒 #cx_fraud — CONTA DESATIVADA · CARTEIRA DESATIVADA · CHARGEBACK

**Público:** Squad Fraud Operations, Fabio Serra de Abreu e CX  
**Formato:** Um report por produto — 3 sets separados no mesmo canal

### Instruções de análise

Ler `#cx_fraud` dos últimos 7 dias para identificar temas ativos.
Para Conta Desativada e Carteira Desativada, separar por tipo de bloqueio (AUTO vs MANUAL).

**Estrutura padrão por produto:**

```
*📊 Report VoC — [Conta Desativada / Carteira Desativada / Chargeback] · Semana NN*

*FUNIL DE SUPORTE*
[Funil completo para o produto]

*ATENDIMENTO N1*
*[N] tickets* ([+/-X%] WoW)
CSAT: *[X pts]* | Resolutividade: *[X%]*
Últimas 5 semanas: [série]

[Para Conta/Carteira Desativada]
*Abertura por tipo de bloqueio:*
• *AUTO:* [N] tickets ([X%]) | CSAT: [X] | Motivo: [motivo]
• *MANUAL:* [N] tickets ([X%]) | CSAT: [X] | Motivo: [motivo]

Top motivos e causas raiz:
• [top 3 com volume, variação WoW e análise qualitativa]

*PERFIL:* New [X%] · NewNew [X%] · Repeat [X%] | PF [X%] · PJ [X%]

*NPS TRANSACIONAL* 📊
[Formato padrão com série de 5 semanas]

*SPECIAL CASES N2*
• [N] contatos · [canais] · Sentimento: [predominante]

*DESTAQUES DA SEMANA* 💬
• [temas do canal + variações nos dados]

🔗 https://sites.google.com/recargapay.com/voc/
```

```
contexto_pontual: ""
```

---

## 📈 #investments-e-cx — CDB · RENDIMENTO CDI · MOVIMENTAÇÕES FINANCEIRAS

**Público:** Squad Investments e CX  
**Formato:** Um report por produto — 3 sets separados

### Instruções de análise

Ler `#investments-e-cx` dos últimos 7 dias.

**Aberturas obrigatórias para CDB:**
- Por tipo de investimento (se disponível via `dim_investment_lifecycle`)
- Por faixa de valor investido: até R$1K · R$1K–R$10K · R$10K–R$50K · acima de R$50K
- Perfil: New · NewNew · Repeat

**Estrutura padrão por produto:**

```
*📊 Report VoC — [CDB / Rendimento CDI / Movimentações] · Semana NN*

*FUNIL DE SUPORTE*
[Funil completo]

*ATENDIMENTO N1*
*[N] tickets* ([+/-X%] WoW)
CSAT: *[X pts]* | Resolutividade: *[X%]*
Últimas 5 semanas: [série]

Top motivos e causas raiz:
• [top 3 com análise qualitativa]

[Para CDB — adicionar]
*Abertura por faixa de investimento:*
• Até R$1K: [N] tickets ([X%])
• R$1K–R$10K: [N] tickets ([X%])
• R$10K–R$50K: [N] tickets ([X%])
• Acima de R$50K: [N] tickets ([X%])
Motivo predominante por faixa quando relevante.

*PERFIL:* New [X%] · NewNew [X%] · Repeat [X%]

*NPS TRANSACIONAL* 📊
[Formato padrão — 5 semanas]
Temas dos detratores nas respostas abertas.

*SPECIAL CASES N2*
• [N] contatos · Sentimento: [predominante]

*DESTAQUES DA SEMANA* 💬
• [temas do canal + variações]

🔗 https://sites.google.com/recargapay.com/voc/
```

```
contexto_pontual: ""
```

---

## 🚌 #melhoria-continua-verticais — TRANSPORTE · CONTAS E BOLETOS · BOLETO DE COBRANÇA · RECARGA DE CELULAR

**Público:** Squad de verticais de utilidades e CX  
**Formato:** Um report por produto — 4 sets separados

### Instruções de análise

Ler `#melhoria-continua-verticais` dos últimos 7 dias.

**Aberturas obrigatórias para Transporte:**
- Por cidade/consórcio (Bilhete Único SP, VEM Recife, Bilhete Único São Luís etc.)
- Por tipo de problema: validação · recarga · outros
- Perfil: New · NewNew · Repeat

**Estrutura do report de Transporte:**

```
*📊 Report VoC — Transporte · Semana NN*

*FUNIL DE SUPORTE — TRANSPORTE*
[Funil completo]

*ATENDIMENTO N1*
*[N] tickets* ([+/-X%] WoW | [+/-X%] vs média 4 sem.)
CSAT: *[X pts]* | Resolutividade: *[X%]*
Últimas 5 semanas: [série]

*Abertura por tipo de problema:*
• Problemas de validação: *[N]* ([X%]) — [consórcio principal]
• Problemas de recarga: *[N]* ([X%])
• Outros: *[N]* ([X%])

*Abertura por cidade/consórcio (top 5):*
• [Consórcio 1]: [N] tickets — Motivo: [motivo]
• [Consórcio 2]: [N] tickets — Motivo: [motivo]
[...]

Top causas raiz (qualitativo):
• *[causa 1]:* [problema] | SLA parceiro: [X dias] | Bot resolve? [Sim/Não]
• *[causa 2]:* [problema]

*PERFIL:* New [X%] · NewNew [X%] · Repeat [X%]

*NPS TRANSACIONAL* 📊
[Formato padrão — 5 semanas]

*SPECIAL CASES N2*
• [N] contatos · Sentimento: [predominante]

*DESTAQUES DA SEMANA* 💬
• [temas do canal + variações]

🔗 https://sites.google.com/recargapay.com/voc/
```

**Para Contas e Boletos, Boleto de Cobrança e Recarga de Celular:** usar estrutura padrão
de produto sem as aberturas específicas de Transporte.

```
contexto_pontual: ""
```

---

## ⚡ #pixcc-home-raf-cx — PIX · PIX CC · RAF

**Público:** Squad Pix, Pix CC, RAF e CX  
**Formato:** Um report por produto — 3 sets separados

### Instruções de análise

Ler `#pixcc-home-raf-cx` dos últimos 7 dias.

**Aberturas obrigatórias para Pix:**
- Pix com Wallet vs Pix com Cartão de Crédito (via `flag_pix_cartao`)
- Por subtipo: Pix In · Pix Out · Chaves Pix
- Perfil: New · NewNew · Repeat

**Estrutura do report de Pix:**

```
*📊 Report VoC — Pix · Semana NN*

*FUNIL DE SUPORTE — PIX*
[Funil completo]

*ATENDIMENTO N1*
*[N] tickets* ([+/-X%] WoW)
CSAT: *[X pts]* | Resolutividade: *[X%]*
Últimas 5 semanas: [série]

*Abertura por subtipo:*
• Pix Out: [N] ([X%]) | Pix In: [N] ([X%]) | Chaves: [N] ([X%])

*Abertura por origem do Pix:*
• Pix com Wallet: [N] tickets
• Pix com Cartão (CC): [N] tickets

Top motivos e causas raiz:
• [top 3 com análise qualitativa e flag Bot/Humano]

*PERFIL:* New [X%] · NewNew [X%] · Repeat [X%]

*NPS TRANSACIONAL — PIX* 📊
[Formato padrão — 5 semanas]
Temas dos detratores.

*SPECIAL CASES N2*
• [N] contatos · Sentimento: [predominante]

*DESTAQUES DA SEMANA* 💬
• [temas do canal + variações]

🔗 https://sites.google.com/recargapay.com/voc/
```

**Para Pix CC e RAF:** usar estrutura padrão de produto sem a abertura de subtipo de Pix.

```
contexto_pontual: ""
```

---

## 💰 #squad_loan_seguimento — EMPRÉSTIMO · CRÉDITO CONSIGNADO

**Público:** Squad Lending e CX  
**Formato:** Report de produto com abertura por perfil e comportamento de inadimplência

### Instruções de análise

Ler `#squad_loan_seguimento` dos últimos 7 dias.

**Aberturas obrigatórias:**
- Perfil: New · NewNew · Repeat
- Por tipo de produto: Empréstimo Pessoal vs Crédito Consignado
- Collateral Wallet: separar contatos relacionados a débito automático quando relevante

**Estrutura do report (Thread 1):**

```
*📊 Report VoC — Empréstimo · Semana NN*

*FUNIL DE SUPORTE — EMPRÉSTIMO*
[Funil completo]

*ATENDIMENTO N1*
*[N] tickets* ([+/-X%] WoW)
CSAT: *[X pts]* | Resolutividade: *[X%]*
Últimas 5 semanas: [série]

*Abertura por produto:*
• Empréstimo Pessoal: [N] ([X%]) | Motivo principal: [motivo]
• Crédito Consignado: [N] ([X%]) | Motivo principal: [motivo]

Top motivos e causas raiz:
• [top 3 com análise qualitativa]

*PERFIL:* New [X%] · NewNew [X%] · Repeat [X%]

*NPS TRANSACIONAL* 📊
[Formato padrão — 5 semanas]
Temas dos detratores nas respostas abertas.

*SPECIAL CASES N2*
• [N] contatos · Canais regulatórios: [N] · Sentimento: [predominante]

*DESTAQUES DA SEMANA* 💬
• [temas do canal + variações]

🔗 https://sites.google.com/recargapay.com/voc/
```

```
contexto_pontual: ""
```

---

## 🏪 #subacquirer-cx — TAP TO PAY · LINK DE PAGAMENTO

**Público:** Squad Subadquirente e CX  
**Formato:** Um report por produto — 2 sets separados

### Instruções de análise

Ler `#subacquirer-cx` dos últimos 7 dias.
Atenção ao perfil PJ — lojistas têm padrão de contato distinto de clientes PF.

**Estrutura padrão por produto:**

```
*📊 Report VoC — [Tap to Pay / Link de Pagamento] · Semana NN*

*FUNIL DE SUPORTE*
[Funil completo]

*ATENDIMENTO N1*
*[N] tickets* ([+/-X%] WoW)
CSAT: *[X pts]* | Resolutividade: *[X%]*
Últimas 5 semanas: [série]

Top motivos e causas raiz:
• [top 3 com análise qualitativa]

*PERFIL:* PF [X%] · PJ [X%] (PJ Ouro [X%] · PJ Prata [X%])
New [X%] · NewNew [X%] · Repeat [X%]

*NPS TRANSACIONAL* 📊
[Formato padrão — 5 semanas]

*SPECIAL CASES N2*
• [N] contatos · Sentimento: [predominante]

*DESTAQUES DA SEMANA* 💬
• [temas do canal + variações]

🔗 https://sites.google.com/recargapay.com/voc/
```

```
contexto_pontual: ""
```

---

## REGRAS GLOBAIS DE ANÁLISE

### O que sempre fazer
- Identificar temas automaticamente pelos dados e pelo Slack — nunca inventar
- Comparar com 5 semanas anteriores em todos os indicadores (NPS, CSAT, volume, retenção)
- Correlacionar variações com eventos, ações e incidentes identificados no Slack
- Negritir números-chave, nomes de indicadores e alertas
- Omitir seções sem dados calculados — sem mensagem de erro ou indisponibilidade
- Separar rigorosamente N1, Bot retido, N2 e derivações em todas as contagens

### O que nunca fazer
- Mostrar tabelas markdown (quebram na janela lateral do Slack)
- Expor tags, IDs de campo ou nomes de tabelas nos reports enviados
- Exibir "⚠️ indisponível" — simplesmente omitir a seção
- Inventar correlações sem base nos dados ou no Slack
- Misturar volumes de N1, Bot e N2 sem separação explícita

### Thresholds de alerta (disparar 🔴)
- Volume N1 fora do padrão: >30% vs média 4 semanas
- Pico em vertical ou motivo: >20% WoW (report geral) ou >30% WoW (report de produto)
- Novo cluster emergente: motivo não estava no top 10, chegou ao top 3
- CSAT Atendimento abaixo de 75% de satisfeitos
- NPS Transacional abaixo de 55 pts em qualquer produto
- Retenção de Bot abaixo de 45%
- Canal regulatório (Ouvidoria, Consumidor.gov, BACEN) acima da média histórica
