# Reports de squad no painel 156 — contrato de dados (v1) e procedimento semanal

Lido pela **Routine B** (Fase 4B do `SKILL.md`). A Routine A usa o mesmo contrato para postar a estrutura de dados na thread 3 de cada set em `#the-voice-cx`.

## 1. Formato: dados em JSON, layout fixo no painel
O layout (CSS e JS) já está publicado no painel 156 e desenha qualquer report que siga este contrato. A automação entrega só **conteúdo**.

- Cada report é um bloco oculto no campo `html` do painel: `<div hidden data-px-report="cartao">{...JSON...}</div>`.
- A atualização semanal envia **somente `html` e `rationale_md`**. Nunca `js`, `css` nem `queries` (um JS truncado já derrubou o painel em 04/09).
- Seção ausente no JSON = seção não aparece. Nunca escrever "N/D" nem placeholder.
- No JSON enviado ao painel e à thread 3, os caracteres `&`, `<` e `>` saem como `\u0026`, `\u003c` e `\u003e` (o `montar_html_reports.py` já faz isso). Dentro do texto só `<b>…</b>` é permitido.

## 2. Campos
| Campo | Obrig. | Conteúdo | Limite |
|---|---|---|---|
| `squad` | ✔ | `geral, pix, cartao, emprestimo, t2p, link, account, seguros, cdb, transporte, fraude, outros` | |
| `sub` | | sub-produto (ex.: `conta desativada`, `cartao`); `executivo` quando `squad=geral` | |
| `rot`, `periodo`, `pub` | ✔ | `"Semana 41"`, `"05/10 – 11/10/2026"`, `pub` = AAAA-MM-DD do dia da publicação | |
| `meta` | | linha de dados (período, janela de comparação, data de publicação) | |
| `resumo` | ✔ | mesma mensagem raiz do set | 520 car. |
| `alertas` | | `{t, v, bot, n, ctx, txt, aberto}` (só limiares atingidos) | 4 |
| `monit` / `ok` | | `{t, txt}` / texto curto | 5 / 4 |
| `kpis` | | `{l, v, d, sub, serie[3–8], ref, st, sc, cls}`; `cls` = `up` (ruim), `down` (bom) ou `flat` | 6 |
| `funil` | | `{partes:[{l,n,p,wow}], total, nota}` | |
| `motivos` / `causas` | | `{t, n, ant, var}` / `{t, n, ant, bot, txt}` | 6 / 5 |
| `recl` | | `{motivo, n, var, resumos, nr, cob, temas[[nome,n]], exp[], cor[], ex[], aberto}` | 5 (temas 6; exp/cor/ex 3) |
| `mencoes` | | `{cards[{f,v,sub,serie,lis[]}], cor[], trechos[{txt,f}], fonte}` — NPS Relacional, Lojas de apps e Redes sociais | 3 cards, 3 trechos |
| `cenario` | | `{t, sub, serie[[rótulo,valor,nota]], base, marc{rótulo:texto}, fatos[{v,t}], fecho}` | |
| `eventos` | | `{d, tag, g(bad/hot), txt, old}`; `old:true` vai para "semanas anteriores" | 14 |
| `atualiz` | | `{t, itens[], nota, link{t,u(https)}, fonte}` | 5 itens |
| `rodape` | | `{fonte}` | |

Fonte de correlação vai como `[[Report S41]]` ou `[[#canal, 07/10]]`. Mesmas regras de inferência do `SKILL.md`: só afirmar o que tem fonte e data; correlação é "coincide com", nunca "causou".

**Arquivos de apoio desta pasta:** `modelo-report.json` (mínimo; falha na validação de propósito, para não ser publicado com placeholder) e `exemplo-seguros-s40.json` (exemplo real e completo, de uma semana passada: copiar a estrutura, nunca o conteúdo).

## 3. Orçamento de tamanho
- Alvo por report: 10 KB. Limite duro: 20 KB (o Cartão, o maior, chegou a 18 KB).
- Total dos blocos de dados: até 110 KB. Com 21 reports de ~4–5 KB e o Cartão maior, a semana fica em torno de 100 KB.
- Para caber: `recl` com 3 motivos, `eventos` dos últimos 14 dias, `trechos` com 2.
- Se passar do limite, o `montar_html_reports.py` aborta e nada é enviado.

## 4. Registro e links (`registro-painel.json`)
Cada saída da automação tem uma **chave do painel** (`squad[/sub]`):
- 21 saídas do Slack (Geral, Executivo e 19 verticais) → 20 chaves, porque **Boleto de Cobrança é fundido em Contas e Boletos** (chave `outros/utilities`, um report só).
- **Seguros** (`seguros`) é só-painel: gerado pela Routine B, sem set no Slack.
- Total: 21 chaves de report.

**Link de um report:** `https://optimus.recargapay.com/PHP/dashboard_view.php?id=156&r=<chave>/rep` (sub-produto com espaço vira `%20`; acento vira percent-encoding). O painel roda em iframe isolado: o `#` da URL não chega ao JS, mas a query da página principal chega pelo `document.referrer`, por isso o parâmetro é `r`. Exemplos: `&r=cartao/rep`, `&r=pix/cartao/rep`, `&r=fraude/carteira%20desativada/rep`, `&r=geral/rep`.

## 5. Procedimento semanal da Routine B
1. Para cada report, gravar um arquivo `.json` em um diretório novo (ex.: `/tmp/painel-saida/`), uma chave por arquivo. A chave vem do próprio JSON (`squad` + `sub`).
2. Rodar:
   `python3 painel-156/montar_html_reports.py --skeleton painel-156/html-esqueleto.html --registro painel-156/registro-painel.json --reports-dir /tmp/painel-saida --out /tmp/painel-saida/html_final.html --manifest /tmp/painel-saida/manifest.json`
   Ele valida cada report, confere o total, monta o campo `html` e grava o manifesto (`publicados`, `ausentes`). Qualquer erro aborta sem gravar nada.
3. Enviar ao Arturito: `arturito_update_dashboard(dashboard_id=156, html=<conteúdo de html_final.html, sem alterar>, rationale_md=<conteúdo de rationale-painel-156.md>)`. **Só esses dois campos.**
4. Conferir a resposta (`status: success`, `snapshot_version`). Se a ferramenta devolver o dashboard de volta, conferir tamanho do `html`, quantidade de blocos `data-px-report` e o marcador final `<!--px-reports-end-->`; se faltar o marcador, o envio foi cortado: reenviar uma vez.
5. Usar o manifesto: só quem está em `publicados` recebe o link do report no Slack. Se a atualização falhou, nenhum link de report é enviado (ver Fase 4C do `SKILL.md`).

## 6. O que ainda não foi testado
- ❌ Uma Routine chamando `arturito_update_dashboard` (só o **dono** do painel atualiza; a Routine roda com a conexão do dono). Testar primeiro no rascunho 485.
- ❌ Envio de ~100 KB de HTML numa única chamada por uma Routine (cópia fiel do arquivo gerado).
- ⚠️ O formato de link `&r=` depende do navegador enviar o referrer da página principal ao iframe; foi medido no rascunho 485, mas o clique de um link do Slack ainda precisa ser validado no Arturito.
- ⚠️ O painel foi renderizado apenas em navegador antigo (wkhtmltoimage); conferir em navegador moderno.
