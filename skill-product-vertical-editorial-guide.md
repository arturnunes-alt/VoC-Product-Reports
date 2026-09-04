# Guia Editorial — Textos da Análise VoC (dashboard 156)

Adaptado de `voc-weekly-analysis/references/voc-analysis-editorial-guide.md` (dashboard
141). As regras fixas e o tom são os mesmos padrões já aplicados em todos os relatórios de
VoC do Artur — seguir à risca, não é opcional. A diferença principal desta versão é a
estrutura de blocos (5, não 2-4 soltos) e a seção nova sobre uso de identificadores.

## Regras fixas

- **Nunca "chatbot" ou "Botmaker"** — sempre **"RecargaBot"**.
- **CSAT** deve ser referido como **"Satisfação com o atendimento"**, não "CSAT" cru,
  na primeira menção de cada texto (pode abreviar depois se o texto for longo).
- **Nenhuma atribuição nominal** — nunca citar nome de pessoa (nem de squad
  específico) como responsável por um evento ou resultado. Falar em termos de
  "o time de X", "a área de Y", "a squad Z", nunca "fulano fez/decidiu".
- **VoC é diagnóstico, não executor** — a análise **relata e sinaliza**
  problemas/tendências; nunca afirma que "vamos corrigir" ou se atribui ações
  de produto/engenharia. Frases como "isso indica necessidade de revisão em X"
  são corretas; "vamos ajustar X" não são.
- **Sem roxo/purple** em qualquer elemento visual que a rotina eventualmente
  crie (a saída aqui é só texto dentro de um card já estilizado, mas vale lembrar).

## Estrutura obrigatória — 5 blocos

Diferente da versão mais livre do dashboard 141, aqui o painel já espera (e o CSS já
está desenhado para) 5 blocos fixos, na mesma ordem, com os mesmos títulos em `<b>`,
separados por `<br><br>` — é o mesmo formato que o painel já usava quando esse texto era
calculado por SQL (ver histórico das funções `gerarVocConsolidado`/`gerarVocNps`, hoje
removidas do JS, mas o formato de saída esperado é o mesmo):

```
<b>Cenário</b><br><br>
[evolução dos indicadores no período vs. anterior, cruzando com eventos mapeados quando a janela bater]<br><br>
<b>Principais Temas</b><br><br>
[pareto dos 2-3 motivos/categorias de maior volume no período]<br><br>
<b>Alerta de Novo Tema</b><br><br>
[resultado da Fase 3 — citar o(s) tema(s) sinalizado(s), ou dizer explicitamente que nenhum foi identificado]<br><br>
<b>Destaque Positivo</b><br><br>
[algo favorável identificado no período — queda de um motivo problemático, tema em alta entre promotores, melhoria de indicador, etc.]<br><br>
<b>Exemplos Reais</b><br><br>
[2-3 casos citados nos blocos acima, cada um com user_id e ticket_id — ver seção de identificadores abaixo]
```

Cada bloco: 2-4 frases, igual ao padrão de sempre — a diferença aqui é ter 5 blocos em
vez de um texto único ou 2-4 blocos livres.

## Tom e formato

- Direto e objetivo — Artur prefere saídas de ação concreta a textos longos.
- Português do Brasil, sem jargão de BI não explicado (evitar "p.p.", preferir
  "pontos percentuais" por extenso na primeira menção; pode abreviar depois).
- HTML permitido: **só `<b>`** para os títulos dos blocos e para destacar um número ou
  nome de tema/produto dentro do texto. Nada de `<ul>`, `<h1>`-`<h6>`, links, ou
  qualquer estrutura de bloco.
- Não repetir números que já aparecem nos gráficos/KPIs ao lado do card (ex: não
  reafirmar o valor de Acessos Central se ele já está no card de KPI acima) — focar em
  **interpretação**, não em redizer o que já está visível.
- Quando não houver dado suficiente para uma leitura confiável (baixo volume na
  vertical, primeira execução para essa vertical, etc.), dizer isso diretamente em cada
  bloco afetado em vez de forçar uma conclusão.

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
- Se nenhum evento mapeado explica a variação, escrever isso explicitamente ("não foi
  identificado um evento específico que explique essa variação no período") em vez de
  inventar uma causa ou omitir a limitação.

## Uso de identificadores (user_id / ticket_id) nos Exemplos Reais

Este é um requisito novo desta automação (o dashboard 141 não usa identificadores).
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
- 2-3 exemplos por análise é a expectativa (não forçar 3 se só houver 1-2 casos
  representativos genuinamente úteis no período).

## Exemplo de bloco completo (Cenário, Análise Geral, ilustrativo — números fictícios)

> <b>Cenário</b><br><br>
> Nos últimos 3 dias, a vertical registrou <b>1.240</b> acessos únicos à Central (alta
> de <b>18%</b> sobre o mesmo intervalo da semana anterior) e <b>340</b> atendimentos
> humanos (estável). O aumento de acessos coincide com o lançamento de uma nova política
> de limite anunciado em 12/03 no canal da squad — ainda não é possível afirmar se o
> volume vai se sustentar nas próximas execuções.

Note: números e datas do exemplo acima são ilustrativos, não reais.
