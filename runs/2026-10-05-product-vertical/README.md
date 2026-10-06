# Análise VoC — dashboard 156 — rascunho de 05/10/2026 (NÃO PUBLICADO)

Janela: 01–04/10/2026 vs 27–30/09/2026 (dados consolidados até 04/10; agg_overview até 03/10).
`atualizado_em` a usar na publicação: `05/10/2026`.

Status: textos prontos, publicação bloqueada — o Bash ficou indisponível na sessão da rotina (classificador do modo automático fora do ar), e a Fase 6 proíbe publicar sem `node --check`.

## Como publicar

1. `arturito_get_dashboard(156)` → salvar a resposta em arquivo.
2. `node merge.js <dump.json> <lote> <prefixo>` para cada lote (1–4). O script valida o JS base, faz merge só das chaves do lote em `VOC_ANALISE_GERAL`/`VOC_ANALISE_NPS`, roda `node --check`, confere o `})();` final e confere que nada fora dos dois objetos mudou.
3. Publicar `<prefixo>_after.js` só no campo `js` e reconferir (Fase 6, passo 7).

Lotes: 1 = Pix + subverticais, Empréstimo + subverticais, Minha Conta, Seguros · 2 = verticais com NPS restantes · 3 = Carteira, Conta Desativada, Chargeback, Movimentações, Adicionar Dinheiro, Exclusivas, Open Finance, RAF · 4 = caudas longas.
