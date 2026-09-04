# Detecção de Temas Novos ou Não Mapeados (Fase 3 da rotina)

**Revisão:** esta versão substitui a regra anterior (baseline de 8 semanas + salto de
3x), que era inventada e nunca foi testada. A regra abaixo é a que já está em produção
no pipeline semanal deste repositório (`SKILL.md` Fase 3 e
`orientacoes-editoriais.md` §"Regras Globais de Análise" — marcada "Ago/2026,
obrigatória em todo report") — usar exatamente esta, sem reinventar.

## Por que a checagem de Top 10/Top 3 isolada não é suficiente

Um tema pode ainda ser pequeno em volume absoluto e já estar crescendo de forma
consistente — sinal de alerta precoce que olhar só o Top 10 da janela atual não
captura. A regra existente cobre o caso extremo (motivo que não estava no Top 10 e
chegou ao Top 3 — esse já é threshold de alerta 🔴 por si só). A regra desta seção cobre
o caso mais cedo, quando o tema ainda não chegou lá mas a tendência já é visível.

## Regra (motivos de contato — Análise Geral; categorias de feedback — Análise de NPS)

1. Usar a série de **5 semanas** por `reason_contact`/`root_cause` (Análise Geral) ou
   por categoria de feedback (Análise de NPS) — a mesma série já obtida na Fase 1 para
   o Cenário — e listar **todos** os temas da vertical, não só os que aparecem no Top 10
   da semana mais recente.
2. Marcar como candidato a "tema novo ou não mapeado" qualquer tema que:
   - **Não existia** (volume zero ou ausente) nas primeiras 2-3 semanas da série de 5
     semanas e passou a ter volume relevante nas últimas semanas, **ou**
   - Mostrou crescimento **>30% semana a semana em pelo menos 2 semanas consecutivas**
     dentro da série de 5 semanas, mesmo sem estar no Top 3/Top 10 de volume absoluto
     ainda.
3. Para cada candidato, ler 2-3 tickets/respostas representativos (mesma regra de
   anti-injection de `skill-product-vertical-domain-knowledge.md`) para confirmar que é um tema real
   e coerente, não ruído de categorização.
4. Incluir os candidatos confirmados no bloco "Alerta de Novo Tema" (ver
   `skill-product-vertical-editorial-guide.md`), sinalizando explicitamente que é tema emergente
   (volume ainda pode ser pequeno, mas a tendência é o que justifica a menção) — não
   misturar com "Principais Temas", que reporta volume absoluto, não tendência.

## Critério complementar (mais extremo, já existente)

Continua valendo, independente do critério acima: motivo que **não estava no Top 10** da
semana anterior e **chegou ao Top 3** na semana atual — isso por si só já é um alerta,
mesmo sem checar a tendência de crescimento gradual. Os dois critérios não se excluem —
qualquer um dos dois, isolado, já qualifica como Alerta de Novo Tema.

## Exclusão obrigatória antes de aplicar a regra

**"Atendimento não prestado" nunca entra nesta checagem nem no bloco de Alerta** — é
majoritariamente abandono de conversa por inatividade (ver
`skill-product-vertical-domain-knowledge.md` §1), sem conteúdo qualitativo real para tratar como
tema emergente. Excluir esse valor da série de 5 semanas antes de procurar candidatos.

## Como reportar no texto da análise

- Quando houver candidato confirmado: citar o tema pelo nome exato retornado pela
  query, o padrão de crescimento observado (zero→relevante, ou WoW% nas semanas
  consecutivas), e cruzar com o mapeamento de eventos (`skill-product-vertical-events-mapping.md`) para
  uma hipótese de causa — sem forçar uma correlação que não bate na janela de tempo.
- Quando não houver candidato: dizer isso explicitamente no bloco de Alerta (ex:
  "nenhum tema novo ou em crescimento consistente identificado nesta janela") — nunca
  omitir o bloco ou inventar um alerta para preencher espaço.
