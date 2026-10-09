# -*- coding: utf-8 -*-
# Reclamações por motivo (resumos de transcrição, 28/09–03/10, N1 humano, vertical Cartão)
RC_HTML = "".join([
 rc("Bloquear, desbloquear ou cancelar cartão", 216, "▲ 55%", 202, 64,
    [("Cancelamento (cartão ou conta-cartão)", 132), ("Menciona cartão físico ou entrega", 76),
     ("Cita anuidade", 55), ("Cobrança tratada como indevida", 28),
     ("Não encontra a opção no app", 14), ("Compra não reconhecida, fraude ou perda", 14)],
    ["Cancelar o cartão (ou a conta-cartão) sem continuar sendo cobrado de anuidade, e achar a opção no app.",
     "Cancelar mesmo com saldo zerado, sem ser barrado por débito pendente."],
    ["<b>Ondas de anuidade (28/09 e 02/10)</b> <span class='src'>Report S40</span> coincidem com 27% dos relatos citando anuidade. Pedidos de cancelamento foram de 60 para 133 <span class='src'>Report S40</span>.",
     "<b>Tela de cancelamento do cartão físico em definição com Produto</b> <span class='src'>Report S40, 02/10</span> coincide com 38% dos relatos citando cartão físico ou entrega e 7% que não acham a opção."],
    ["“Dificuldade em encontrar a opção de cancelar a conta cartão e evitar cobrança de anuidade”",
     "“Cartão não foi cancelado corretamente e anuidade continuou sendo cobrada”",
     "“Dificuldade em cancelar o cartão devido à informação de dívida pendente, mesmo com saldo zerado”"],
    "95%", True),
 rc("Não entende por que recebeu uma fatura", 179, "▲ 50%", 173, 86,
    [("Cita empréstimo", 68), ("Cobrança tratada como indevida", 44), ("Cita venda ou aproximação", 20),
     ("Cobrança duplicada", 15), ("Cita saldo ou limite garantido", 14), ("Débito, dívida ou pendência", 12)],
    ["Não ver cobrança na fatura depois de pagar ou quitar o empréstimo.",
     "Receber o valor da venda como dinheiro ou cashback, e não como limite do cartão.",
     "Entender por que cobram “um valor que já é seu” (saldo garantido)."],
    ["<b>Reunião CXM + Cartão RP (07/10)</b> <span class='src'>#cc-produto-e-cx</span> registra +40% nos contatos de “não entende por que recebeu uma fatura” no início de outubro, em casos de Loans to CC e Tap to CC com Pix no cartão. No mesmo tema: 39% dos relatos citam empréstimo e 12% citam venda.",
     "<b>A/B Loans → Cartão em 100% desde 01/10</b> <span class='src'>Report S40</span>."],
    ["“Cobrança na fatura do cartão após pagamento antecipado da parcela do empréstimo”",
     "“Valor da venda foi convertido automaticamente em limite de crédito do cartão, e não foi recebido como cashback”",
     "“O cliente não entende por que está sendo cobrado por um valor que já é seu”"],
    "100%"),
 rc("Problema com o pagamento da fatura", 134, "▲ 123%", 120, 54,
    [("Cobrança tratada como indevida", 77), ("Juros, multa ou encargos", 57), ("Cita anuidade", 24),
     ("Vencimento em domingo ou feriado", 20), ("Cita vencimento", 14), ("Pagamento em duplicidade", 4)],
    ["Pagar no primeiro dia útil, quando o vencimento cai em domingo ou feriado, sem juros e multa.",
     "Não pagar anuidade depois de pedir o cancelamento."],
    ["<b>Ondas de anuidade (28/09 e 02/10)</b> <span class='src'>Report S40</span> coincidem com 20% dos relatos citando anuidade. “Não concorda com encargos” foi de 17 para 74 <span class='src'>Report S40</span>.",
     "<b>Vencimento em domingo ou feriado:</b> 17% dos relatos citam essa situação; nos exemplos lidos, a queixa é a cobrança de juros e multa. Não há evento sobre isso nos reports nem no Slack da semana. Em 08/10 a squad respondeu, no #cc-produto-e-cx, que não há faturas com vencimento no feriado de 12/10."],
    ["“Pagamento realizado no primeiro dia útil após vencimento em feriado, mas cobrança indevida foi aplicada”",
     "“Cobrança de anuidade após solicitação de cancelamento do cartão e falta de resposta rápida”",
     "“Pagou duas vezes a mesma fatura, uma via Pix e outra com o limite garantido”"],
    "92%"),
 rc("Resgate de saldo garantido", 127, "▼ 21%", 122, 61,
    [("Transferir, sacar, resgatar ou retirar", 52), ("Cita venda", 37), ("Cita empréstimo", 15),
     ("Cita saldo ou limite garantido", 14), ("Cancelamento (cartão ou conta)", 9), ("Não encontra a opção", 9)],
    ["Ter o valor da venda na carteira e conseguir transferir ou sacar.",
     "Resgatar o saldo mesmo com o cartão ou a conta cancelados."],
    ["<b>A/B Loans → Cartão em 100% desde 01/10</b> <span class='src'>Report S40</span>: o motivo caiu 21% (160 → 127). O report afirma que isso “pode reduzir” o motivo; é uma hipótese dele.",
     "<b>Tap to CC ativado para o segmento 5 PJ em 24/08</b> <span class='src'>Report S35</span> e <b>“fatura zero” para Tap to CC</b> entre os TO-DOs de 07/10 <span class='src'>#cc-produto-e-cx</span>. No mesmo tema: 30% dos relatos citam venda."],
    ["“Dificuldade em resgatar o valor de venda que foi creditado como saldo de cartão”",
     "“Dificuldade em entender por que o saldo foi parar no cartão empreendedor e não na carteira”",
     "“Cartão cancelado e não consegue sacar o dinheiro”"],
    "97%"),
 rc("Quer pagar sua fatura", 111, "▲ 46%", 94, 46,
    [("Antecipar ou adiantar pagamento", 19), ("Não encontra a opção", 15), ("Cobrança tratada como indevida", 14),
     ("Débito, dívida ou pendência", 10), ("Cita saldo ou limite garantido", 9), ("Cita vencimento", 4)],
    ["Antecipar parcelas ou todas as faturas futuras, inclusive para cancelar sem mensalidade.",
     "Alterar a data de vencimento pelo app (exemplo citado: dia 20)."],
    ["Sem evento correlato nos reports nem no Slack da semana."],
    ["“Dificuldade em antecipar pagamentos de faturas futuras e cancelar o cartão sem ter que pagar mensalidades”",
     "“A opção de alterar a data de vencimento para o dia 20 não está disponível”",
     "“Não consegue encontrar a opção para adiantar o pagamento”"],
    "85%"),
])


def mcard(titulo, valor, sub, spark_html, lis):
    ul = "".join(f"<li>{x}</li>" for x in lis)
    return (f'<div class="mcard"><div class="l"><span>{titulo}</span></div><div class="v">{valor}</div>'
            f'<div class="d">{sub}</div>{spark_html}<ul style="margin-top:6px">{ul}</ul></div>')


MENC_HTML = '<div class="mcards">' + "".join([
 mcard("NPS Relacional", "51", "comentários citam Cartão (11% dos 464) · 5 sem.: 50 · 64 · 61 · 53 · 51",
       spark([50, 64, 61, 53, 51], None, label="Comentários do NPS Relacional que citam Cartão, 5 semanas"),
       ["35 promotores · 8 neutros · 8 detratores",
        "NPS de quem cita: <b>+52,9</b> (sem. ant. +15,1) <span class='src'>não é o NPS oficial</span>",
        "Temas: acesso a limite e a cartão concedido · taxas do Pix com cartão e IOF · dinheiro caindo no cartão virtual"]),
 mcard("Lojas de apps", "23", "reviews citam Cartão (2,8% de 807) · 5 sem.: 26 · 29 · 24 · 18 · 23",
       spark([26, 29, 24, 18, 23], None, label="Reviews que citam Cartão, 5 semanas"),
       ["Nota média <b>2,39</b> contra 4,20 do app todo",
        "14 com 1–2★ (61%) · 7 com 4–5★ (30%)",
        "Temas (10 dos 14 reviews de 1–2★ lidos): taxa do Pix com limite do cartão · valor de venda caindo no cartão · fatura de ~R$ 10 sem demonstrativo · dinheiro do empréstimo “preso” no cartão · ajuda que “não resolve”"]),
 mcard("Redes sociais (público)", "14", "interações citam Cartão (7,4% de 190) · 5 sem.: 20 · 32 · 29 · 16 · 14",
       spark([20, 32, 29, 16, 14], None, label="Interações públicas que citam Cartão, 5 semanas"),
       ["9 negativas (64%) · 4 positivas · 14 com ticket",
        "Temas (10 das 14 lidas): limite zerado apesar de bom histórico · não conseguir entrar no app para pagar o cartão (28/09) · compra não reconhecida · Pix com limite do cartão com valor recebido menor · bloqueio ao pedir cartão com garantia de CDB · empréstimo “forçando” cartão",
        "O report publicado citou 12 comentários (critério anterior); aqui vale a regex do painel 141."]),
]) + '</div>'

MENC_HTML += """
<h3 style="font-size:15px;color:#0a2540;margin-top:20px">Correlações com eventos e mudanças</h3>
<ul class="cor">
  <li><b>Pix com cartão e taxa:</b> relatos nas três fontes (lojas, NPS, redes). Contexto registrado: o bot informa taxa de 4,99% (3,99% via Google/Apple Pay) <span class="src">Report S32</span>; a reunião de 07/10 <span class="src">#cc-produto-e-cx</span> cita a taxa do Pix cobrada depois na fatura em Loans to CC e Tap to CC.</li>
  <li><b>Empréstimo virando limite no cartão:</b> “dinheiro preso para usar só no cartão” (lojas), “empréstimo forçando cartão” (redes) e “dinheiro parar de cair no cartão virtual” (NPS). Contexto: o empréstimo virou limite no Cartão RP desde junho <span class="src">Report S32</span> e o A/B Loans → Cartão foi a 100% em 01/10 <span class="src">Report S40</span>.</li>
  <li><b>Venda caindo no cartão:</b> relato em lojas (“o valor vai pro cartão de crédito que eu não solicitei”). Contexto: Tap to CC ativado para o segmento 5 PJ em 24/08 <span class="src">Report S35</span>; “fatura zero” para Tap to CC entre os TO-DOs de 07/10.</li>
  <li><b>Fatura de ~R$ 10 em cartão sem uso:</b> relato em lojas. O review <b>não cita anuidade</b>; a ligação é só de tema e de janela com as ondas de 28/09 e 02/10 <span class="src">Report S40</span>.</li>
</ul>
<h3 style="font-size:15px;color:#0a2540;margin-top:18px">Trechos de clientes</h3>
<div class="quote">“o app já foi bom antes me dava limite de empréstimo agora não dá mais”<span>NPS Relacional · nota 0 · 29/09</span></div>
<div class="quote">“diminuiria as taxas do cartão de crédito, do pix com cartão de crédito”<span>NPS Relacional · nota 5 · 29/09</span></div>
<div class="quote">“fiz uma venda e o valor vai pro cartão de crédito que eu não solicitei. quero o valor em dinheiro na conta”<span>Google Play · 1★ · 30/09</span></div>
<div class="quote">“me apareceu fatura fechada com um valor de 9,80, não tem demostrativo”<span>Google Play · 1★ · 30/09</span></div>
<div class="quote">“fiz um Pix ! De 190 recebi 184 usei meu limite do cartão”<span>Instagram · 30/09</span></div>
<p class="src" style="margin-top:8px">Fonte: mapeamento de produto do painel Arturito 141 (regex “Cartão de Crédito”) sobre NPS Relacional, avaliações das lojas e interações públicas das redes, semana 28/09–04/10 vs 4 semanas anteriores. Trechos sem identificação.</p>
"""
