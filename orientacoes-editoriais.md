# Orientações Editoriais por Canal
**Repositório:** voc-automation  
**Arquivo:** orientacoes-editoriais.md  
**Como usar:** Edite este arquivo antes de cada ciclo de reports para ajustar
o foco analítico de cada canal à estratégia do período. A Routine lê este
arquivo e aplica as orientações ao gerar cada report.

---

## Como funciona

Cada canal tem três campos editáveis:

| Campo | O que controla |
|---|---|
| `foco_periodo` | O tema ou métrica que deve receber ênfase especial neste ciclo |
| `contexto_estrategico` | Informação de negócio que o Claude deve usar para contextualizar variações |
| `perguntas_prioritarias` | As 2–3 perguntas que o report deve responder obrigatoriamente para aquele canal |

Campos em branco fazem a Routine usar o template padrão sem personalização.
Mantenha os textos curtos — o Claude interpreta, não executa literalmente.

---

## 🏠 #the-cxm-house — Report Geral

**Público:** Time CXM completo (analistas, coordenadores, gestores de CX)  
**Cadência:** Semanal · toda segunda-feira

```
foco_periodo: >
  Acompanhar o impacto do rollout de cashback (chegada a 100% da base em 29/06)
  no volume e CSAT do Cartão de Crédito. Monitorar também a curva de Carteira
  Bloqueada — verificar se o volume de contatos está cedendo após os ajustes
  de comunicação do Projeto Carteira Bloqueada.

contexto_estrategico: >
  Semana 27 marca o encerramento do ciclo de junho. A principal variável de
  volume é o rollout de cashback (100% da base a partir de 29/06) e seus
  reflexos em cancelamentos e contatos de Cartão. O Dreno Automático (Collateral
  Wallet) deve estar estabilizando — comparar com o pico da semana 25.

perguntas_prioritarias:
  - O volume total da semana está dentro da tendência pós-pico de junho?
  - Cartão de Crédito mantém queda WoW ou voltou a crescer com o rollout?
  - Carteira Bloqueada: o contato por Fraud Strategy MANUAL cedeu ou manteve?
```

---

## 👔 #lideres-cx-e-cxm — Report Executivo

**Público:** Marco Galan, Anderson Fernandes, líderes de produto e operações  
**Cadência:** Semanal · toda segunda-feira  
**Formato:** Condensado — máximo 5 seções, foco em impacto e tendência

```
foco_periodo: >
  Destacar os três movimentos mais relevantes para decisão executiva:
  (1) impacto do cashback no NPS e intenção de saída do Cartão,
  (2) evolução do Projeto Carteira Bloqueada — redução de impacto ao cliente,
  (3) curva de Empréstimo — estabilização pós-Collateral Wallet e novos clusters
  de dívida cedida.

contexto_estrategico: >
  Lideranças estão acompanhando três OKRs simultaneamente: redução de contato
  em Wallet Bloqueada, NPS Cartão acima de 55 pts, e taxa de automação do bot
  acima de 50%. Cada seção do report deve conectar os dados a pelo menos um desses
  objetivos quando possível.

perguntas_prioritarias:
  - NPS Transacional da semana — subiu, caiu ou estabilizou vs semana anterior?
  - Qual vertical representa o maior risco operacional desta semana?
  - Há algum alerta que exige decisão executiva antes da próxima semana?
```

---

## 👤 #account_cx — Minha Conta

**Público:** Squad de Account e CX responsável pela vertical  
**Cadência:** Semanal

```
foco_periodo: >
  Monitorar impacto do upgrade Spring 3 (SMS em Account — bug resolvido em jun/26)
  verificando se há reincidência de falhas no envio de SMS de autenticação.
  Atenção também para contatos de clientes que não conseguem acessar o app —
  possível reflexo do anti-spam VIVO no C2C de recuperação de conta.

contexto_estrategico: >
  O bug de SMS por efeito colateral do upgrade Spring 3 foi corrigido, mas o time
  está substituindo mandatories por feature flags — período de risco de regressão.
  O bloqueio anti-spam da VIVO (57,5% das ligações não entregues) afeta o C2C
  de recuperação de acesso — clientes que não recebem ligação voltam ao chat.

perguntas_prioritarias:
  - Há crescimento em motivos de contato relacionados a SMS ou autenticação?
  - Contatos de dificuldade de acesso ao app aumentaram vs semana anterior?
  - Qual o perfil PF/PJ dos tickets — há concentração incomum?
```

---

## 💳 #cc-produto-e-cx — Cartão de Crédito

**Público:** Squad Cartão de Crédito e CX  
**Cadência:** Semanal

```
foco_periodo: >
  Esta é a vertical de maior risco no período. O rollout de cashback chega a
  100% da base em 29/06 — monitorar volume, intenção de cancelamento e NPS
  com atenção máxima. Os dois bugs de Loans no CC (INC-15244 e INC-15246)
  ainda estão abertos — verificar se geraram aumento de tickets de "cobrança
  incorreta" ou "cancelamento sem efeito".

contexto_estrategico: >
  NPS do Cartão estava em 53 pts na semana 25 — menor do portfólio. Novas regras
  de cashback impactaram -14% no spending dos clientes repeat com 62% da base.
  O parcelamento da fatura foi desligado como medida paliativa em ~06/06 — verificar
  se voltou ou se ainda gera contatos. Bug de Loans no CC: cancelamento sem baixa
  de saldo garantido (INC-15244) e falha pós-resgate (INC-15246) — ambos com
  poucos casos mas sem fix confirmado.

perguntas_prioritarias:
  - Volume de intenção de cancelamento/saída cresceu vs semana 25?
  - Bugs INC-15244 e INC-15246 aparecem nos motivos de contato da semana?
  - NPS Cartão da semana — abaixo, igual ou acima de 53 pts?
```

---

## 🔒 #cx_fraud — Conta Desativada · Carteira Desativada · Chargeback

**Público:** Squad Fraud Operations, Fabio Serra de Abreu e CX  
**Cadência:** Semanal

```
foco_periodo: >
  Acompanhar evolução do Projeto Carteira Bloqueada — especialmente o tipo
  Fraud Strategy MANUAL, que concentra o maior CSAT negativo (20% promotores,
  87% sem desbloqueio previsto na semana 25). Verificar se as ações de comunicação
  e treinamento (carrossel de 6 slides publicado em jun/26) reduziram derivações
  incorretas e tempo de resolução. Para Chargeback Recovery, monitorar reflexo
  do incidente Pix/Elo (180 clientes, R$200K) que está sendo tratado via chargeback.

contexto_estrategico: >
  O Fraud Strategy MANUAL é o tipo de bloqueio de maior fricção: clientes sem
  previsão de desbloqueio e CSAT crítico. O reforço de prazos de tratativa foi
  publicado pelo Leonardo de Castro em jun/26 — a Routine deve verificar se o
  volume de contatos por "sem previsão" reduziu. Para Chargeback, o incidente
  Pix/Elo gerou 180 casos ativos sendo tratados via chargeback bancário —
  possível entrada de novos tickets se clientes não receberem resolução.

perguntas_prioritarias:
  - Conta Desativada / Carteira Bloqueada: o CSAT do tipo MANUAL melhorou?
  - Há redução no motivo "sem previsão de desbloqueio" após o treinamento?
  - Chargeback Recovery: novos tickets relacionados ao incidente Pix/Elo?
```

---

## 📈 #investments-e-cx — CDB · Rendimento CDI · Movimentações

**Público:** Squad Investments e CX  
**Cadência:** Semanal

```
foco_periodo: >
  Monitorar o impacto da mudança de elegibilidade do Rendimento CDI (saldo
  garantido não utilizado do Cartão não gera mais rendimento a partir de 11/06).
  Verificar se há aumento de contatos de clientes questionando a mudança ou
  solicitando resgate de saldo garantido.

contexto_estrategico: >
  A mudança foi comunicada internamente pela Ingrid Mamolli em 10/06 com pedido
  de reforço para a operação. Clientes que mantinham saldo garantido parado
  como "investimento informal" podem perceber a mudança somente ao verificar
  o extrato — o contato tende a ser defasado (2–4 semanas após a mudança).

perguntas_prioritarias:
  - Há crescimento em contatos relacionados a Rendimento CDI ou saldo garantido?
  - Qual o sentimento predominante nos tickets de Movimentações Financeiras?
  - CDB: volume estável ou com variação relevante?
```

---

## 🚌 #melhoria-continua-verticais — Transporte · Boletos · Recarga Celular

**Público:** Squad responsável pelas verticais de utilidades e CX  
**Cadência:** Semanal

```
foco_periodo: >
  Transporte está com crescimento MoM (+19,9% em junho vs maio) e 65% de
  sentimento negativo — a principal alavanca de melhoria identificada é a
  automação de "falta de validação no terminal" (37 casos/mês) via bot.
  Para Recarga de Celular, verificar estabilidade após a instabilidade de
  integração com o provedor (01/06). Para Contas e Boletos, monitorar
  sazonalidade de vencimentos quinzenais.

contexto_estrategico: >
  Em Transporte, o problema central (crédito não disponibilizado após validação)
  depende do SLA dos consórcios parceiros — a alavanca real de CX é reduzir o
  prazo de retorno do consórcio ou criar notificação proativa ao cliente quando
  o caso é enviado. O Bilhete Único SP concentra 53% dos casos com entry_reason
  identificado. Recarga de Celular: integração normalizada desde ~02/06, mas
  monitorar reincidência.

perguntas_prioritarias:
  - Transporte: o volume da semana mantém tendência de alta ou cedeu?
  - O motivo "falta de validação no terminal" está reduzindo (candidato a bot)?
  - Recarga de Celular: algum sinal de nova instabilidade com o provedor?
```

---

## ⚡ #pixcc-home-raf-cx — Pix · Pix CC · RAF

**Público:** Squad Pix, Pix CC, RAF e CX  
**Cadência:** Semanal

```
foco_periodo: >
  Pix está em estabilização pós-BTG (semana 24 foi o pico). Verificar se o
  volume voltou à média pré-incidente. Para Pix CC, monitorar reflexo da
  Collateral Wallet — clientes com empréstimo debitado da carteira que tentam
  fazer Pix e encontram saldo insuficiente. Para RAF, acompanhar impacto da
  mudança de 08/06 (indicado não recebe mais o bônus de R$20 — apenas o
  indicador ganha o prêmio).

contexto_estrategico: >
  O incidente BTG (3 episódios entre 08–12/06) causou o pico de atendimento
  da semana 24. A estabilização está confirmada, mas verificar se há tickets
  residuais de clientes que não receberam restituição de transações falhas.
  RAF: a mudança de 08/06 foi comunicada pela Mirela Dantas com materiais
  atualizados — possível aumento de contatos de indicados que esperavam o
  bônus de R$20 e não receberam.

perguntas_prioritarias:
  - Pix: volume voltou à média pré-BTG (antes de 08/06)?
  - Há tickets residuais do incidente BTG (transações não entregues/restituídas)?
  - RAF: crescimento de contatos após a mudança do bônus do indicado?
```

---

## 💰 #squad_loan_seguimento — Empréstimo · Crédito Consignado

**Público:** Squad Lending e CX  
**Cadência:** Semanal

```
foco_periodo: >
  Dois clusters emergentes que precisam de acompanhamento semanal:
  (1) dívidas vendidas para cessão — clientes questionando Registrato/BACEN
  após quitação com cessionário (11 casos na semana 26, não estava no top 20
  anterior); (2) bugs em Loans no CC (INC-15244 e INC-15246 — sem fix confirmado).
  Para Consignado, monitorar volume de dúvidas após a expansão da política
  RNN Simplificada para todos os segmentos em 03/06.

contexto_estrategico: >
  A Collateral Wallet (Dreno Automático) foi ativada em 17/06 para inadimplentes
  de Empréstimo — o pico de contatos da semana 25 está cedendo, mas verificar
  se a curva segue descendente. O cluster de dívida cedida/Registrato é novo
  e regulatório — clientes com intenção de ação judicial e prazo de remoção
  de 20–40 dias (ciclo BACEN). Comunicação proativa inexistente — oportunidade
  de melhoria de jornada.

perguntas_prioritarias:
  - Collateral Wallet: o volume de "empréstimo debitado da carteira" está caindo?
  - Cluster de dívida cedida/Registrato cresceu ou estabilizou vs semana 26?
  - Bugs INC-15244 e INC-15246 aparecem nos motivos de contato?
```

---

## 🏪 #subacquirer-cx — Tap to Pay · Link de Pagamento

**Público:** Squad Subadquirente e CX  
**Cadência:** Semanal

```
foco_periodo: >
  Monitorar impacto do bloqueio anti-spam da VIVO no C2C de suporte ao lojista
  (Tap to Pay e Link de Pagamento têm perfil PJ mais elevado — ligações de
  suporte ao estabelecimento são críticas). Verificar se há crescimento em
  contatos de lojistas que não receberam ligação de retorno.

contexto_estrategico: >
  O anti-spam da VIVO impacta 57,5% das ligações para clientes da operadora —
  lojistas PJ Ouro e Prata usam linhas corporativas que frequentemente são da
  VIVO ou de operadoras com políticas similares. O canal de e-mail pode estar
  absorvendo os contatos que antes eram resolvidos por C2C. Para Link de
  Pagamento, monitorar sazonalidade de fim de mês (cobranças e liquidações).

perguntas_prioritarias:
  - Tap to Pay: crescimento de contatos via e-mail (possível migração do C2C)?
  - Perfil PJ Ouro/Prata está acima do normal em algum produto?
  - Link de Pagamento: alguma variação relevante no encerramento do mês?
```

---

## Como editar este arquivo

**Ciclo recomendado:**
1. Todo domingo à tarde, antes da Routine rodar na segunda às 08h BRT
2. Revisar os campos `foco_periodo` e `contexto_estrategico` de cada canal
3. Atualizar `perguntas_prioritarias` com base nos alertas da semana anterior
4. Fazer commit no repositório GitHub — a Routine já usa a versão mais recente

**Dicas de edição:**
- `foco_periodo`: 2–4 linhas. O que o Claude deve prestar atenção especial esta semana.
- `contexto_estrategico`: fatos concretos (números, datas, nomes de iniciativas). O Claude usa isso para contextualizar variações de volume ou CSAT que seriam interpretadas como anomalia sem o contexto.
- `perguntas_prioritarias`: máximo 3 perguntas. Se uma pergunta não tiver resposta nos dados, o Claude indica explicitamente.

**Quando deixar em branco:**
Semanas sem mudanças relevantes de estratégia ou produto, deixar os campos em branco.
A Routine usa o template padrão — funciona bem para semanas "normais".

**Quem mantém:**
Artur Nunes (artur.nunes@recargapay.com) — com inputs do Anderson Fernandes
e dos DRIs de cada squad quando houver contexto relevante de produto.
