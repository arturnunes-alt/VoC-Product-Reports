# Guia Editorial — Textos da Análise VoC (dashboard 156)

Adaptado de `voc-weekly-analysis/references/voc-analysis-editorial-guide.md` (dashboard
141). As regras fixas e o tom são os mesmos padrões já aplicados em todos os relatórios de
VoC do Artur — seguir à risca, não é opcional.

> **v1.1 (04/09/2026)**: revisão pós-feedback. A estrutura deixou de ser 5 blocos fixos
> sempre presentes — "Alerta de Novo Tema" e "Destaque Positivo" agora só aparecem
> quando há algo genuíno a dizer, nunca como frase de preenchimento. Toda explicação de
> variação/tema passa a se apoiar no que o cliente disse de fato (fala real, mesmo que
> parafraseada), não em números isolados. Exemplos Reais passam de 2-3 para 4-5.

## Regra mais importante: nunca escrever uma frase que não agrega

Esta é a regra que mais separa uma análise útil de uma análise que só preenche espaço.
Frases como "nenhum tema novo confirmado nesta execução" ou "não foi identificado um
destaque genuinamente positivo distinto" **não geram valor nenhum** para quem lê —
apenas registram a ausência de algo, sem ajudar ninguém a agir. Quando não há um achado
genuíno para um bloco opcional (ver estrutura abaixo), **o bloco inteiro é omitido**,
começando o próximo bloco na sequência — nunca se escreve uma frase reconhecendo a
ausência do achado.

Isso vale também dentro dos blocos obrigatórios: se uma frase só existe para preencher
espaço sem trazer um número, uma causa ou uma fala real do cliente, ela não deveria
existir. Cada frase escrita precisa passar no teste: "isso ajuda alguém do squad ou da
liderança a agir ou entender algo que não sabia?" Se a resposta for não, a frase sai.

## Estrutura — blocos obrigatórios e opcionais

Três blocos são **sempre escritos**; dois só aparecem **quando há achado real**:

```
<b>Cenário</b><br><br>
[sempre presente — evolução dos indicadores no período vs. anterior, cruzando com
eventos mapeados quando a janela bater, fundamentada em fala real do cliente quando
uma variação precisa de explicação — ver seção "Fundamentar em fala real" abaixo]<br><br>

<b>Principais Temas</b><br><br>
[sempre presente — pareto dos motivos/categorias de maior volume, explicando a dúvida
ou quebra de expectativa por trás de cada um, com fala real do cliente — ver seção
específica abaixo]<br><br>

<b>Alerta de Novo Tema</b><br><br>
[SÓ SE a Fase 3 confirmou um tema novo/em crescimento — se não confirmou, omitir o
bloco inteiro, incluindo o título]<br><br>

<b>Destaque Positivo</b><br><br>
[SÓ SE há algo genuinamente favorável a reportar — se não há, omitir o bloco inteiro,
incluindo o título]<br><br>

<b>Exemplos Reais</b><br><br>
[sempre presente — 4-5 casos citados nos blocos acima, cada um com user_id e
ticket_id — ver seção de identificadores abaixo]
```

Isso significa que o texto final de cada vertical pode ter 3, 4 ou 5 blocos,
dependendo do que a Fase 3 e a leitura de Destaque Positivo realmente encontraram —
nunca force os 5 para manter uma aparência de completude.

## Fundamentar em fala real do cliente, não só em números

Ao explicar por que um indicador variou ou por que um motivo tem determinado volume,
apoiar a explicação no que os clientes **de fato disseram** nos contatos — puxando de
`customer_issue`/`customer_complaint`/`support_solution`
(`fat_tickets_transcription_summary`) ou `feedback` (`fat_indecx_metrics`), parafraseado
com fidelidade ao sentido original. Uma variação percentual sozinha não conta a história
toda; a fala do cliente mostra o quê e o porquê.

Isso vale especialmente para **Principais Temas**: cada motivo relevante deveria
explicar, com base em fala real, qual dúvida ou expectativa quebrada está gerando o
contato — não apenas nomear o motivo e o volume. Exemplos do tipo de leitura esperada
(ilustrativos, não reais):

- Fraco (só número, sem explicar o porquê): "Bloquear/desbloquear cartão segue líder
  (371 tickets, queda de 44%)."
- Bom (número + a dúvida/expectativa real por trás, com fala do cliente): "Bloquear/
  desbloquear cartão segue líder (371 tickets, queda de 44% após o fim do ciclo de
  anuidade) — clientes relatam surpresa com a cobrança ('não sabia que ia cobrar
  anuidade esse ano') e dificuldade em encontrar a opção de cancelamento no app."

A mesma lente vale para o Cenário quando uma variação de indicador precisa de
explicação: não bastam os números de Acessos/Bot/Humano — se a transcrição ou o
feedback mostrar um padrão de confusão ou expectativa quebrada por trás do volume,
citar isso.

## Tom e formato

- Direto e objetivo — Artur prefere saídas de ação concreta a textos longos, mas
  concisão nunca justifica cortar uma explicação que agrega (número + causa + fala do
  cliente). O corte é sempre de frases sem substância, não de conteúdo real.
- Português do Brasil, sem jargão de BI não explicado (evitar "p.p.", preferir
  "pontos percentuais" por extenso na primeira menção; pode abreviar depois).
- HTML permitido: **só `<b>`** para os títulos dos blocos e para destacar um número ou
  nome de tema/produto dentro do texto. Nada de `<ul>`, `<h1>`-`<h6>`, links, ou
  qualquer estrutura de bloco.
- Não repetir números que já aparecem nos gráficos/KPIs ao lado do card (ex: não
  reafirmar o valor de Acessos Central se ele já está no card de KPI acima) — focar em
  **interpretação**, não em redizer o que já está visível.
- Quando não houver dado suficiente para uma leitura confiável (baixo volume na
  vertical, primeira execução para essa vertical, etc.), reportar o número real e o que
  os poucos casos existentes mostram — nunca uma frase genérica tipo "dados
  insuficientes para uma leitura confiável" sem nenhum número ou conteúdo junto.

## Cobertura de subverticais — sempre, não só quando há volume alto

Pix (Wallet/Cartão) e Empréstimo (Geral/Consignado) sempre recebem análise própria
(chave composta `VERTICAL_KEY::SubvertLabel`) tanto na Análise Geral quanto na de NPS —
não é mais uma cobertura opcional condicionada a um piso de volume. Se o volume for
genuinamente baixo, reportar o número real e o conteúdo dos poucos casos existentes
(ver regra do parágrafo anterior) em vez de pular a subvertical ou escrever uma frase
vazia sobre a falta de dados.

## Exceções de domínio — aplicar antes de escrever

Ver `skill-product-vertical-domain-knowledge.md` para o detalhe de cada uma. As mais relevantes na
hora de redigir o texto:

- "Atendimento não prestado" nunca aparece em "Principais Temas" nem em "Alerta de Novo
  Tema" (conta no volume total do Cenário, não no ranking qualitativo).
- Ao descrever perfil de cliente em Minha Conta, Conta Desativada, Carteira Bloqueada ou
  Chargeback Recovery: usar só New/Repeat (sem NewNew).
- Acessos à Central de Ajuda: comparar mês corrente parcial vs. mês anterior fechado,
  nunca semana a semana.
- Conta/Carteira Desativada: ao descrever tipo de bloqueio, usar as 3 categorias reais
  (Regra automática, Revisão manual COps, Ofício judicial) — nunca simplificar para
  AUTO/MANUAL.
- Retenção do RecargaBot: sempre líquida de abandono passivo (ver fórmula em
  `skill-product-vertical-domain-knowledge.md` §2) — nunca o número bruto.

## Correlação com eventos — regra de honestidade

- Só citar um evento mapeado (Fase 2) se a **janela de tempo bater** (evento aconteceu
  dentro da janela de análise, ou logo antes) — não forçar uma correlação distante no
  tempo só porque parece plausível.
- Se nenhum evento mapeado explica a variação e a fala do cliente também não sugere uma
  causa clara, **omitir a tentativa de explicação** em vez de forçar uma ou escrever uma
  frase reconhecendo a ausência ("não foi identificado...") — reportar o número e seguir
  para o próximo ponto que realmente tem substância.

## Uso de identificadores (user_id / ticket_id) nos Exemplos Reais

Regras:

- **Nunca inventar** um `user_id` ou `id_ticket` — todo identificador citado precisa vir
  de uma query real rodada na Fase 1/4/5 (ver `skill-product-vertical-example-queries.sql`).
- Citar o identificador de forma neutra, sem contexto adicional que identifique a pessoa
  além do necessário para rastreabilidade interna (ex: "ticket #123456 (usuário
  u_98765)" é suficiente — não citar nome, e-mail, ou qualquer outro dado pessoal que a
  query eventualmente retorne mas que não seja o identificador em si).
- O texto ao redor do identificador (o que foi dito/feito no atendimento, ou o
  feedback) pode ser parafraseado/resumido — não precisa ser a transcrição literal
  completa, mas o **sentido** deve corresponder ao que a query retornou, sem
  distorcer.
- **4-5 exemplos por análise** é a expectativa (não forçar 5 se só houver 2-3 casos
  representativos genuinamente úteis no período — mas puxar mais linhas da query
  ad-hoc quando os primeiros resultados não derem exemplos distintos o suficiente).
  Priorizar exemplos que ilustrem diferentes temas/motivos citados no texto, não 5
  variações do mesmo caso.

## Exemplo de bloco completo (Cenário + Principais Temas, ilustrativo — dados fictícios)

> <b>Cenário</b><br><br>
> Nos últimos 3 dias, a vertical registrou <b>1.240</b> acessos únicos à Central (alta
> de <b>18%</b> sobre o mesmo intervalo da semana anterior) e <b>340</b> atendimentos
> humanos (estável). O aumento de acessos coincide com o lançamento de uma nova política
> de limite anunciado em 12/03 no canal da squad, e as transcrições confirmam: clientes
> relatam não terem sido avisados da mudança antes de tentarem uma transação e serem
> barrados.<br><br>
> <b>Principais Temas</b><br><br>
> <b>Bloquear/desbloquear cartão</b> segue líder (371 tickets, queda de 44% após o fim
> do ciclo de anuidade) — a fala recorrente é de surpresa com a cobrança ("não sabia
> que ia cobrar anuidade esse ano") e dificuldade em achar a opção de cancelamento no
> app, não insatisfação com o produto em si.

Note: números, datas e falas do exemplo acima são ilustrativos, não reais.
