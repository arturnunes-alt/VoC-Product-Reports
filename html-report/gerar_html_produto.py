# -*- coding: utf-8 -*-
"""Gera o HTML de exemplo do report de Cartão de Crédito (Semana 40) no layout RecargaPay.
Tudo inline (CSS + SVG), sem JS e sem dependências externas. CSS escopado em .rpv."""

import os


def spark(vals, ref=None, w=116, h=34, pad=4, label=""):
    lo, hi = min(vals), max(vals)
    if ref is not None:
        lo, hi = min(lo, ref), max(hi, ref)
    span = (hi - lo) or 1
    lo -= span * 0.08
    hi += span * 0.08
    span = hi - lo
    n = len(vals)
    def x(i): return pad + i * (w - 2 * pad) / (n - 1)
    def y(v): return h - pad - (v - lo) * (h - 2 * pad) / span
    pts = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(vals))
    refline = ""
    if ref is not None:
        refline = f'<line x1="{pad}" x2="{w-pad}" y1="{y(ref):.1f}" y2="{y(ref):.1f}" class="ref"/>'
    cx, cy = x(n - 1), y(vals[-1])
    return (f'<svg class="spark" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">'
            f'{refline}<polyline points="{pts}" fill="none"/>'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3"/></svg>')


def bars():
    data = [("22–25/09", 280, "média/dia"), ("28/09", 250, ""), ("29/09", 392, ""),
            ("30/09", 316, ""), ("01/10", 328, ""), ("02/10", 260, ""), ("03/10", 242, "sáb")]
    W, H, top, bot = 560, 170, 22, 34
    bw, gap = 52, 21
    mx = 420
    ch = H - top - bot
    out = [f'<svg class="bars" viewBox="0 0 {W} {H}" role="img" aria-label="Tickets N1 por dia em torno das ondas de anuidade">']
    base_y = top + ch - 280 / mx * ch
    out.append(f'<line x1="0" x2="{W}" y1="{base_y:.1f}" y2="{base_y:.1f}" class="ref"/>')
    for i, (lab, v, note) in enumerate(data):
        bx = 35 + i * (bw + gap)
        bh = v / mx * ch
        by = top + ch - bh
        cls = "peak" if v == 392 else ("base" if i == 0 else "")
        out.append(f'<rect x="{bx}" y="{by:.1f}" width="{bw}" height="{bh:.1f}" rx="4" class="{cls}"/>')
        out.append(f'<text x="{bx + bw/2}" y="{by - 5:.1f}" class="v">{v}</text>')
        out.append(f'<text x="{bx + bw/2}" y="{H - 18}" class="d">{lab}</text>')
        if note:
            out.append(f'<text x="{bx + bw/2}" y="{H - 5}" class="n">{note}</text>')
    # marcadores das ondas
    for i, txt in ((1, "1ª onda"), (5, "2ª onda")):
        bx = 35 + i * (bw + gap) + bw / 2
        out.append(f'<text x="{bx}" y="11" class="w">▼ {txt}</text>')
    out.append('</svg>')
    return "".join(out)


CSS = """
.rpv{--navy:#0a2540;--blue:#1a73e8;--sky:#5ba7f5;--orange:#f5a623;--amber:#f5c842;--text:#1e293b;--sub:#64748b;--panel:#f0f2f5;--line:#e2e8f0;--crit:#d64545;--ok:#1f9d6b;
font-family:'Barlow',-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif;color:var(--text);font-size:14px;line-height:1.55;max-width:980px;margin:0 auto;background:#fff}
.rpv *{box-sizing:border-box}
.rpv h1,.rpv h2,.rpv h3,.rpv p,.rpv ul{margin:0;padding:0}
.rpv ul{list-style:none}
.rpv a{color:var(--blue);text-decoration:none}.rpv a:hover{text-decoration:underline}
.rpv-hero{background:var(--navy);color:#fff;padding:30px 32px 26px;border-radius:0 0 14px 14px}
.rpv-tag{font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--orange);line-height:1}
.rpv-hero h1{font-size:30px;font-weight:800;letter-spacing:-.02em;line-height:1.15;margin:10px 0 4px}
.rpv-hero h1 span{font-weight:400;font-size:18px;color:var(--sky);margin-left:8px;white-space:nowrap}
.rpv-meta{font-size:12px;color:#a9bdd6}
.rpv-lede{margin-top:16px;font-size:14.5px;line-height:1.65;color:rgba(255,255,255,.92);max-width:820px}
.rpv-lede b{color:#fff}
.rpv-nav{display:flex;flex-wrap:wrap;gap:6px;padding:14px 32px 4px}
.rpv-nav a{font-size:12px;font-weight:600;color:var(--sub);background:var(--panel);border-radius:999px;padding:5px 12px}
.rpv-nav a:hover{background:var(--blue);color:#fff;text-decoration:none}
.rpv section{padding:22px 32px 6px}
.rpv h2{font-size:20px;font-weight:700;color:var(--navy);letter-spacing:-.01em;line-height:1.2;margin-top:8px}
.rpv .eyebrow{font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--orange);line-height:1}
.rpv .sub{font-size:12.5px;color:var(--sub);margin-top:4px}
.rpv .grid{display:grid;gap:12px;margin-top:14px}
.rpv .g3{grid-template-columns:repeat(auto-fit,minmax(270px,1fr))}
.rpv .g5{grid-template-columns:repeat(auto-fit,minmax(170px,1fr))}
.rpv .card{background:var(--panel);border-radius:10px;padding:14px 16px}
.rpv .alert{background:#fff;border:1px solid var(--line);border-left:5px solid var(--crit);border-radius:10px;padding:14px 16px}
.rpv .alert .top{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.rpv .pill{font-size:11px;font-weight:700;border-radius:999px;padding:2px 9px;line-height:1.5;white-space:nowrap}
.rpv .pill.crit{background:#fbe6e6;color:var(--crit)}.rpv .pill.warn{background:#fdf0d5;color:#9a6200}.rpv .pill.ok{background:#dff3ea;color:#16704c}.rpv .pill.info{background:#e3eefc;color:var(--blue)}.rpv .pill.mute{background:#e8ecf1;color:var(--sub)}
.rpv .alert h3{font-size:15px;font-weight:700;color:var(--navy);margin-top:6px;line-height:1.3}
.rpv .alert .num{font-size:26px;font-weight:800;letter-spacing:-.02em;color:var(--navy);line-height:1.1;margin-top:6px}
.rpv .alert .num small{font-size:12px;font-weight:500;color:var(--sub);letter-spacing:0;margin-left:6px}
.rpv .alert p{font-size:13px;color:var(--text);margin-top:6px}
.rpv .alert .open{font-size:12.5px;color:var(--sub);margin-top:8px;padding-top:8px;border-top:1px dashed var(--line)}
.rpv .watch li{display:flex;gap:10px;padding:9px 0;border-bottom:1px solid var(--line);font-size:13.5px}
.rpv .watch li:last-child{border-bottom:0}
.rpv .watch .dot{flex:none;width:9px;height:9px;border-radius:50%;background:var(--orange);margin-top:7px}
.rpv .watch b{color:var(--navy)}
.rpv .okrow{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.rpv .kpi{background:var(--panel);border-radius:10px;padding:13px 14px 10px;position:relative}
.rpv .kpi .l{font-size:12px;font-weight:600;color:var(--sub)}
.rpv .kpi .v{font-size:28px;font-weight:800;letter-spacing:-.02em;color:var(--navy);line-height:1.1;margin:4px 0 2px}
.rpv .kpi .d{font-size:12px;color:var(--sub)}
.rpv .spark{width:100%;height:34px;margin-top:6px;display:block}
.rpv .spark polyline{stroke:var(--blue);stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.rpv .spark circle{fill:var(--orange)}
.rpv .spark .ref{stroke:#94a3b8;stroke-width:1;stroke-dasharray:3 3}
.rpv .up{color:var(--crit);font-weight:700}.rpv .down{color:var(--ok);font-weight:700}.rpv .flat{color:var(--sub);font-weight:700}
.rpv .stack{display:flex;height:16px;border-radius:8px;overflow:hidden;margin-top:12px}
.rpv .stack i{display:block;height:100%}
.rpv .leg{display:flex;flex-wrap:wrap;gap:6px 18px;margin-top:10px;font-size:13px}
.rpv .leg b{color:var(--navy)}.rpv .leg span::before{content:"";display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:6px;background:var(--c)}
.rpv table{width:100%;border-collapse:collapse;font-size:13px}
.rpv th{font-size:11px;text-transform:uppercase;letter-spacing:1px;color:var(--sub);text-align:left;font-weight:700;padding:8px 8px;border-bottom:2px solid var(--line)}
.rpv td{padding:9px 8px;border-bottom:1px solid var(--line);vertical-align:middle}
.rpv td.n,.rpv th.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.rpv .bar{height:8px;border-radius:4px;background:var(--line);position:relative;min-width:90px}
.rpv .bar i{position:absolute;left:0;top:0;height:8px;border-radius:4px;background:var(--blue)}
.rpv .bar i.prev{background:#c3d4ea;height:8px}
.rpv .cause{padding:12px 0;border-bottom:1px solid var(--line)}
.rpv .cause:last-child{border-bottom:0}
.rpv .cause .h{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:baseline}
.rpv .cause b{color:var(--navy);font-size:14px}
.rpv .cause p{font-size:13px;color:var(--text);margin-top:4px}
.rpv .chart{background:var(--panel);border-radius:10px;padding:12px 14px;margin-top:14px}
.rpv .bars{width:100%;height:auto;display:block}
.rpv .bars rect{fill:var(--sky)}.rpv .bars rect.base{fill:#c3d4ea}.rpv .bars rect.peak{fill:var(--orange)}
.rpv .bars text{font-family:inherit;text-anchor:middle}
.rpv .bars .v{font-size:12px;font-weight:700;fill:#0a2540}.rpv .bars .d{font-size:11px;fill:#64748b}.rpv .bars .n{font-size:10px;fill:#94a3b8}.rpv .bars .w{font-size:11px;font-weight:700;fill:#9a6200}
.rpv .bars .ref{stroke:#94a3b8;stroke-width:1;stroke-dasharray:4 4}
.rpv .facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;margin-top:12px}
.rpv .fact{border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.rpv .fact b{display:block;font-size:20px;color:var(--navy);font-weight:800;letter-spacing:-.01em;line-height:1.2}
.rpv .fact span{font-size:12px;color:var(--sub)}
.rpv .tl{position:relative;margin-top:14px;padding-left:20px}
.rpv .tl::before{content:"";position:absolute;left:5px;top:6px;bottom:6px;width:2px;background:var(--line)}
.rpv .tl li{position:relative;padding:0 0 14px}
.rpv .tl li::before{content:"";position:absolute;left:-20px;top:5px;width:12px;height:12px;border-radius:50%;background:#fff;border:3px solid var(--sky)}
.rpv .tl li.hot::before{border-color:var(--orange)}.rpv .tl li.bad::before{border-color:var(--crit)}
.rpv .tl .when{font-size:12px;font-weight:700;color:var(--navy)}
.rpv .tl .tg{font-size:10.5px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;color:var(--sub);background:var(--panel);border-radius:4px;padding:1px 6px;margin-left:6px}
.rpv .tl p{font-size:13px;margin-top:2px}
.rpv details{margin-top:12px}
.rpv summary{cursor:pointer;font-size:13px;font-weight:600;color:var(--blue);padding:6px 0}
.rpv .upd{border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin-top:14px;background:#fff}
.rpv .upd li{font-size:13.5px;padding:5px 0 5px 16px;position:relative}
.rpv .upd li::before{content:"";position:absolute;left:0;top:13px;width:6px;height:6px;border-radius:50%;background:var(--blue)}
.rpv .two{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;margin-top:14px}
.rpv .chip{display:inline-block;font-size:11px;font-weight:700;border-radius:4px;padding:1px 7px;white-space:nowrap}
.rpv .chip.p{background:#fdf0d5;color:#9a6200}.rpv .chip.n{background:#e8ecf1;color:var(--sub)}.rpv .chip.s{background:#dff3ea;color:#16704c}
.rpv footer{margin:26px 32px 0;padding:14px 0 22px;border-top:1px solid var(--line);display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-size:12px;color:var(--sub)}
.rpv footer .conf{font-size:10px;font-weight:500;letter-spacing:2px;text-transform:uppercase;color:#94a3b8}

.rpv .rc{border:1px solid var(--line);border-radius:10px;margin-top:10px;background:#fff}
.rpv .rc summary{list-style:none;display:flex;flex-wrap:wrap;gap:6px 12px;align-items:center;padding:12px 16px;cursor:pointer;color:var(--navy);font-weight:700;font-size:14px}
.rpv .rc summary::-webkit-details-marker{display:none}
.rpv .rc summary::before{content:"▸";color:var(--orange);font-size:13px;margin-right:-4px}
.rpv .rc[open] summary::before{content:"▾"}
.rpv .rc .m{font-weight:500;color:var(--sub);font-size:12.5px}
.rpv .rcb{padding:2px 16px 14px}
.rpv .rcg{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}
.rpv .rc h4{font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--orange);margin:12px 0 6px;line-height:1}
.rpv .mb{display:grid;grid-template-columns:150px 1fr 46px;gap:8px;align-items:center;font-size:12.5px;padding:3px 0}
.rpv .mb .t{background:var(--line);height:8px;border-radius:4px;position:relative}.rpv .mb .t i{position:absolute;left:0;top:0;height:8px;border-radius:4px;background:var(--blue)}
.rpv .mb b{text-align:right;color:var(--navy);font-variant-numeric:tabular-nums}
.rpv .exp li,.rpv .cor li{font-size:13px;padding:4px 0 4px 14px;position:relative}
.rpv .exp li::before{content:"";position:absolute;left:0;top:11px;width:6px;height:6px;border-radius:50%;background:var(--orange)}
.rpv .cor li::before{content:"↔";position:absolute;left:0;top:4px;color:var(--blue);font-weight:700;font-size:12px}
.rpv .cor li{padding-left:18px}
.rpv .src{font-size:11.5px;color:var(--sub)}
.rpv .quote{border-left:3px solid var(--sky);background:var(--panel);border-radius:0 8px 8px 0;padding:6px 10px;margin-top:6px;font-size:12.5px;color:var(--text)}
.rpv .quote span{display:block;font-size:11px;color:var(--sub);margin-top:2px}
.rpv .note{font-size:12px;color:var(--sub);background:#fff8e6;border:1px dashed #f0cf85;border-radius:8px;padding:8px 12px;margin-top:12px}
.rpv .mcards{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:12px;margin-top:14px}
.rpv .mcard{background:var(--panel);border-radius:10px;padding:14px 16px}
.rpv .mcard .l{font-size:12px;font-weight:700;color:var(--navy);display:flex;justify-content:space-between;gap:8px}
.rpv .mcard .v{font-size:26px;font-weight:800;color:var(--navy);letter-spacing:-.02em;line-height:1.1;margin-top:4px}
.rpv .mcard .d{font-size:12px;color:var(--sub)}
.rpv .mcard ul li{font-size:13px;padding:2px 0 2px 12px;position:relative}
.rpv .mcard ul li::before{content:"•";position:absolute;left:0;color:var(--orange)}
@media(max-width:600px){.rpv-hero,.rpv section,.rpv-nav{padding-left:16px;padding-right:16px}.rpv footer{margin-left:16px;margin-right:16px}.rpv-hero h1{font-size:24px}}
@media print{.rpv-nav{display:none}.rpv details{display:block}}
"""


def pc(n, d):
    return f"{round(n * 100 / d):d}%"

def mb(label, n, d):
    w = n * 100 / d
    return (f'<div class="mb"><span>{label}</span><div class="t"><i style="width:{w:.0f}%"></i></div>'
            f'<b>{pc(n, d)}</b></div>')

def rc(nome, tickets, var, n, nr, temas, exp, cor, ex, cobertura, aberto=False):
    barras = "".join(mb(l, v, n) for l, v in temas)
    exps = "".join(f"<li>{e}</li>" for e in exp)
    cors = "".join(f"<li>{x}</li>" for x in cor)
    exs = "".join(f'<div class="quote">{q}</div>' for q in ex)
    op = " open" if aberto else ""
    return (f'<details class="rc"{op}><summary><span>{nome}</span>'
            f'<span class="m">{tickets} tickets · {var}</span>'
            f'<span class="pill warn">{pc(nr, n)} com motivo de não resolução registrado</span></summary>'
            f'<div class="rcb"><div class="rcg">'
            f'<div><h4>O que gera o contato</h4>{barras}</div>'
            f'<div><h4>Expectativa que falhou (nas palavras do relato)</h4><ul class="exp">{exps}</ul></div></div>'
            f'<h4>Correlações com eventos e mudanças</h4><ul class="cor">{cors}</ul>'
            f'<h4>Relatos de exemplo (resumo da transcrição)</h4>{exs}'
            f'<p class="src" style="margin-top:8px">Base: resumos de {n} tickets ({cobertura} dos tickets do motivo).</p>'
            f'</div></details>')

def kpi(label, value, delta, sub, status=None, series=None, ref=None, lab=""):
    st = f'<div style="margin-top:6px"><span class="pill {status[0]}">{status[1]}</span></div>' if status else ""
    sp = spark(series, ref, label=lab) if series else ""
    return (f'<div class="kpi"><div class="l">{label}</div><div class="v">{value}</div>'
            f'<div class="d">{delta}</div>{sp}<div class="d">{sub}</div>{st}</div>')


def motivo(nome, atual, ant, pct, up=True):
    mx = 216
    cls = "up" if up else "down"
    sign = "▲" if up else "▼"
    return (f'<tr><td>{nome}</td><td class="n"><b>{atual}</b> <span style="color:#64748b">(vs {ant})</span></td>'
            f'<td><div class="bar"><i class="prev" style="width:{ant/mx*100:.0f}%"></i><i style="width:{atual/mx*100:.0f}%;opacity:.92"></i></div></td>'
            f'<td class="n"><span class="{cls}">{sign} {pct}</span></td></tr>')


HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'blocos_cartao.py'), encoding='utf-8').read())

html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>VoC · Cartão de Crédito · Semana 40</title>
<style>{CSS}</style>
</head>
<body>
<div class="rpv">

<header class="rpv-hero">
  <div class="rpv-tag">VoC · Cartão de Crédito</div>
  <h1>Semana 40 <span>28/09 – 04/10/2026</span></h1>
  <p class="rpv-meta">Dados até 03/10 (sáb) · comparações seg–sáb vs seg–sáb · report publicado em 05/10</p>
  <p class="rpv-lede"><b>1.788 atendimentos</b> (+16,7% vs semana anterior, −9% vs média de 4 semanas), com <b>1.360 no N1 humano</b> (+22%) e pico de 392 tickets em 29/09, um dia após a 1ª onda da anuidade Gold/Standard. Pedidos de cancelamento de cartão foram de 60 para <b>133</b>, e “não concorda com encargos” de 17 para <b>74</b>. NPS em <b>56,6 pts</b> (perto do piso de 55) e CSAT em <b>80,1%</b>.</p>
</header>

<nav class="rpv-nav">
  <a href="#atencao">Atenção</a><a href="#resultados">Resultados</a><a href="#motivos">Motivos e causas</a><a href="#reclamacoes">Reclamações</a><a href="#mencoes">Menções</a><a href="#cenario">Cenário da semana</a><a href="#eventos">Eventos</a><a href="#updates">Atualizações</a>
</nav>

<section id="atencao">
  <div class="eyebrow">Para a squad tratar</div>
  <h2>O que pede atenção agora</h2>
  <p class="sub">3 alertas de pico em motivo (esperado: até +30% vs semana anterior).</p>
  <div class="grid g3">
    <div class="alert">
      <div class="top"><span class="pill crit">Pico +122%</span><span class="pill mute">Bot: parcial</span></div>
      <h3>Cancelar o cartão</h3>
      <div class="num">133<small>vs 60 na semana anterior</small></div>
      <p>Cobrança de anuidade Gold/Standard (28/09 e 02/10). Cartão físico só cancela com humano; no virtual é preciso pagar a fatura fechada antes, e o cliente confunde cancelar o cartão com encerrar a conta-cartão.</p>
      <div class="open"><b>Em aberto:</b> tela de cancelamento do cartão físico em definição com Produto (02/10). É o principal gargalo de transbordo para humano nesta onda.</div>
    </div>
    <div class="alert">
      <div class="top"><span class="pill crit">Pico +123%</span><span class="pill mute">Bot: não</span></div>
      <h3>Problema com o pagamento da fatura</h3>
      <div class="num">134<small>vs 60 · inclui “não concorda com encargos”: 17 → 74</small></div>
      <p>Tema emergente. Anuidade cobrada após cancelamento ou em cartão que o cliente achava pré-pago. Valores parciais (R$ 8,70 / R$ 9,53) geram desconfiança, com pedidos de estorno e ameaça de jurídico.</p>
      <div class="open"><b>Risco reputacional:</b> já houve escalada para Reclame Aqui ligada à anuidade em 29/09.</div>
    </div>
    <div class="alert">
      <div class="top"><span class="pill crit">Pico +50%</span><span class="pill mute">Bot: não</span></div>
      <h3>Não entende por que recebeu uma fatura</h3>
      <div class="num">179<small>vs 119 na semana anterior</small></div>
      <p>O alerta não traz uma causa isolada. Nas causas raiz aparece confusão entre saldo garantido, rendimento e limite (“o limite é meu dinheiro?”): “entende que o saldo garantido quita a fatura automaticamente” subiu de 72 para 111.</p>
    </div>
  </div>

  <h3 style="font-size:15px;color:#0a2540;margin-top:22px">Em monitoramento</h3>
  <ul class="watch">
    <li><span class="dot"></span><div><b>NPS Transacional 56,6 pts</b> — acima do piso de 55, mas com margem curta. Detratores em 18,1%, o maior nível da série.</div></li>
    <li><span class="dot"></span><div><b>2ª onda da anuidade (02/10)</b> — só 13 contatos (0,35%) até D+2, contra 1,82% na mesma altura da 1ª onda. Leitura ainda preliminar.</div></li>
    <li><span class="dot"></span><div><b>Falha na criação do cartão virtual (03/10)</b> — o fluxo de alerta de instabilidade do bot não foi ativado.</div></li>
    <li><span class="dot"></span><div><b>Loans → Cartão (A/B em 100% desde 01/10)</b> — pode reduzir “resgate de saldo garantido”, que já caiu 21%.</div></li>
  </ul>
  <div class="okrow">
    <span class="pill ok">CSAT N1 80,1% — na meta</span>
    <span class="pill ok">Volume N1 −5% vs média 4 sem.</span>
    <span class="pill ok">Retenção do bot 63,8%</span>
  </div>
</section>

<section id="resultados">
  <div class="eyebrow">Resultados</div>
  <h2>Como a semana fechou</h2>
  <p class="sub">Pontinho laranja = semana atual. Linha tracejada = meta ou piso.</p>
  <div class="grid g5">
    {kpi("Atendimentos", "1.788", '<span class="up">▲ 16,7%</span> vs sem. ant.', "−9% vs média 4 sem.", None, [2248,2132,1981,1532,1788], None, "Atendimentos nas últimas 5 semanas")}
    {kpi("CSAT N1", "80,1%", '<span class="up">▼ 2,2 pp</span> vs sem. ant. (82,3%)', "Meta 80%", ("ok","Na meta"), [84.7,76.5,79.5,82.3,80.1], 80, "CSAT N1 nas últimas 5 semanas")}
    {kpi("NPS Transacional", "56,6", '<span class="down">▲ 1,1</span> vs sem. ant.', "Piso 55 · meta 75", ("warn","Margem curta"), [60.8,60.4,63.3,55.5,56.6], 55, "NPS nas últimas 5 semanas")}
    {kpi("Retenção do bot", "63,8%", '<span class="flat">▼ 3,7 pp</span> vs sem. ant. (67,5%) · report', "gráfico: série na base, seg–sex", None, [61.3,61.1,63.4,64.0,63.4], None, "Retenção do bot no tema Cartão nas últimas 5 semanas")}
    {kpi("Central de Ajuda", "26.586", '<span class="flat">▲ 18%</span> visitas únicas', "coincide com a mensagem sobre cobranças (02/10)", None, [22384,24120,23384,22509,26586], None, "Visitas únicas nas últimas 5 semanas")}
  </div>

  <div class="note"><b>Nota de validação (remover na versão final):</b> o gráfico de retenção do bot não vinha no report, que traz só a semana atual e a anterior. Calculei a série na base (fórmula de sessão: não transbordou e não foi abandono passivo; tema Cartão; seg–sex; semanas S36 a S40): 61,3% · 61,1% · 63,4% · 64,0% · 63,4%. O report publicou 63,8% (sem. ant. 67,5%). Testei 14 variações (por estágio, tema de entrada e tema de conversa, nas tabelas agregada e de sessão) e nenhuma reproduz esses dois valores. Na base, a queda da S39 para a S40 é de 0,6 pp, não 3,7 pp.</div>
  <div class="card" style="margin-top:12px">
    <b style="color:#0a2540">Funil de suporte</b> <span class="sub">· total 1.788</span>
    <div class="stack"><i style="width:21.3%;background:#5ba7f5"></i><i style="width:76.1%;background:#1a73e8"></i><i style="width:2.6%;background:#f5a623"></i></div>
    <div class="leg">
      <span style="--c:#5ba7f5"><b>RecargaBot</b> 381 (21,3%)</span>
      <span style="--c:#1a73e8"><b>N1 humano</b> 1.360 (76,1%) <span class="up" style="margin-left:4px">▲ 21,6%</span></span>
      <span style="--c:#f5a623"><b>N2 special cases</b> 47 (2,6%)</span>
    </div>
    <p class="sub">N2 está subestimado: parte dos casos da semana ainda estava sem vertical. Perfil: New 6% · Repeat 93% · PF 95% · PJ 3% — base quase toda de clientes antigos, coerente com o público “cartão parado, app vivo” da anuidade.</p>
  </div>

  <details>
    <summary>Ver série das 5 semanas</summary>
    <table>
      <tr><th></th><th class="n">S36</th><th class="n">S37</th><th class="n">S38</th><th class="n">S39</th><th class="n">S40</th></tr>
      <tr><td>Atendimentos</td><td class="n">2.248</td><td class="n">2.132</td><td class="n">1.981</td><td class="n">1.532</td><td class="n"><b>1.788</b></td></tr>
      <tr><td>CSAT N1</td><td class="n">84,7%</td><td class="n">76,5%</td><td class="n">79,5%</td><td class="n">82,3%</td><td class="n"><b>80,1%</b></td></tr>
      <tr><td>NPS Transacional</td><td class="n">60,8</td><td class="n">60,4</td><td class="n">63,3</td><td class="n">55,5</td><td class="n"><b>56,6</b></td></tr>
      <tr><td>Visitas únicas (Central)</td><td class="n">22.384</td><td class="n">24.120</td><td class="n">23.384</td><td class="n">22.509</td><td class="n"><b>26.586</b></td></tr>
    </table>
  </details>
</section>

<section id="motivos">
  <div class="eyebrow">N1 humano · 1.360 tickets</div>
  <h2>Motivos e causas raiz</h2>
  <p class="sub">Barra clara = semana anterior · barra azul = semana atual.</p>
  <table style="margin-top:10px">
    <tr><th>Motivo</th><th class="n">Semana</th><th></th><th class="n">Var.</th></tr>
    {motivo("Bloquear, desbloquear ou cancelar cartão", 216, 139, "55%")}
    {motivo("Não entende por que recebeu uma fatura", 179, 119, "50%")}
    {motivo("Problema com o pagamento da fatura", 134, 60, "123%")}
    {motivo("Resgate de saldo garantido", 127, 160, "21%", up=False)}
    {motivo("Quer pagar sua fatura", 111, 76, "46%")}
  </table>

  <h3 style="font-size:15px;color:#0a2540;margin-top:22px">Causas raiz</h3>
  <div>
    <div class="cause"><div class="h"><b>Cancelar o cartão de crédito</b><span><b>133</b> <span class="sub">(vs 60)</span> <span class="chip p">Bot: parcial</span></span></div>
      <p>Cartão físico só cancela com humano. No virtual, é preciso pagar a fatura fechada antes, e o cliente confunde cancelar o cartão com encerrar a conta-cartão.</p></div>
    <div class="cause"><div class="h"><b>Entende que o saldo garantido quita a fatura automaticamente</b><span><b>111</b> <span class="sub">(vs 72)</span> <span class="chip n">Bot: não</span></span></div>
      <p>Confusão entre saldo garantido, rendimento e limite (“o limite é meu dinheiro?”).</p></div>
    <div class="cause"><div class="h"><b>Não concorda com a cobrança de encargos</b><span><b>74</b> <span class="sub">(vs 17)</span> <span class="chip n">Bot: não</span></span></div>
      <p>Anuidade cobrada após cancelamento ou em cartão que o cliente achava pré-pago. Valores parciais geram desconfiança, com pedidos de estorno e ameaça de jurídico.</p></div>
  </div>
</section>

<section id="reclamacoes">
  <div class="eyebrow">Reclamações dos clientes</div>
  <h2>O que gera o contato nos 5 principais motivos</h2>
  <p class="sub">Contagem de quantos resumos de transcrição citam cada tema. Um ticket pode citar mais de um. Abra cada motivo para ver a expectativa que falhou e o que coincide com eventos.</p>
  {RC_HTML}
  <p class="src" style="margin-top:10px">Método: resumos por IA das transcrições (28/09–03/10, N1 humano, vertical Cartão), lidos em amostra e contados por termo. “Motivo de não resolução” é o motivo que o resumo registra para o ticket não ter sido resolvido na interação; não é taxa de resolução. Correlação não é causa: cada ligação cita a fonte.</p>
</section>

<section id="mencoes">
  <div class="eyebrow">Menções ao produto</div>
  <h2>O que dizem sobre Cartão no NPS Relacional, nas lojas e nas redes</h2>
  <p class="sub">Semana 28/09–04/10, mapeamento de produto do painel 141. As três fontes medem coisas diferentes; não somar.</p>
  {MENC_HTML}
</section>

<section id="cenario">
  <div class="eyebrow">Cenário da semana</div>
  <h2>Anuidade Gold/Standard: duas ondas de cobrança</h2>
  <p class="sub">Tickets N1 por dia. O pico veio um dia depois da 1ª onda e cedeu depois.</p>
  <div class="chart">{bars()}</div>
  <div class="facts">
    <div class="fact"><b>4.883</b><span>clientes cobrados na 1ª onda (28/09) · 84% com valor parcial, por saldo abaixo de R$ 9,90</span></div>
    <div class="fact"><b>2,42%</b><span>contact rate da 1ª onda em D+6 (118 contatos)</span></div>
    <div class="fact"><b>3.680</b><span>clientes na 2ª onda (02/10) · 86% com cobrança parcial · mais 142 em 04/10</span></div>
    <div class="fact"><b>57% / 43%</b><span>dos 131 contatos de clientes cobrados desde 28/09 chegaram ao humano (maioria via transbordo do bot) / ficaram no bot</span></div>
  </div>
  <p class="sub" style="margin-top:10px">O volume total ficou dentro do projetado, mas a demanda migrou para <b>cancelamento e encargos</b>.</p>
</section>

<section id="eventos">
  <div class="eyebrow">Histórico de eventos</div>
  <h2>O que aconteceu e pode explicar os números</h2>
  <ul class="tl">
    <li class="bad"><span class="when">03/10</span><span class="tg">Instabilidade</span><p>Falha na criação do cartão virtual (14:15–16:49, ~2h30): 61 contatos na janela, 45 no N1 humano (~1,3x o normal). O bot reteve 26,2% (vs 20,1% no mesmo horário dos sábados anteriores).</p></li>
    <li class="hot"><span class="when">02/10</span><span class="tg">Anuidade</span><p>2ª onda de cobrança: 3.680 clientes, 86% com valor parcial.</p></li>
    <li><span class="when">02/10</span><span class="tg">Central</span><p>Mensagem sobre cobranças, exibida para ~16 mil clientes (inclusive sem cobrança), foi desativada. Coincide com +18% de visitas à Central de Cartão.</p></li>
    <li><span class="when">01/10</span><span class="tg">Loans</span><p>A/B Loans → Cartão foi a 100%: clientes novos de empréstimo escolhem entre cartão e carteira.</p></li>
    <li class="bad"><span class="when">29/09</span><span class="tg">N2</span><p>Escalada para Reclame Aqui ligada à anuidade.</p></li>
    <li class="hot"><span class="when">28/09</span><span class="tg">Anuidade</span><p>1ª onda Gold/Standard: 4.883 clientes cobrados, 84% com valor parcial.</p></li>
    <li><span class="when">23/09</span><span class="tg">Crédito</span><p>Teto de parcelamento para ~19 mil clientes de alto risco. Pode explicar parte dos casos de “transação declinada”.</p></li>
  </ul>
  <details>
    <summary>Ver eventos de semanas anteriores (jun–ago)</summary>
    <ul class="tl">
      <li class="hot"><span class="when">25–28/08</span><span class="tg">Anuidade</span><p>Onda de comunicados de cobrança e autosserviço de cancelamento, que chegou a 100% dos usuários na manhã de 28/08. O fluxo de bot foi de ~180 contatos/dia para 533 no pico (26/08) e voltou a 191 em 30/08.</p></li>
      <li><span class="when">24/08</span><span class="tg">Produto</span><p>Tap to CC ativado para o segmento 5 PJ, sem sinal de fricção nos dados.</p></li>
      <li><span class="when">18/08</span><span class="tg">Loans</span><p>Reativado o dreno automático de saldo de empréstimo para cartão não usado em 10 dias. “Como resgatar o saldo do empréstimo” subiu 62%.</p></li>
      <li class="hot"><span class="when">17/08</span><span class="tg">Bot</span><p>Hiperpersonalização do bot em 100% das conversas: retenção de 63,8% para 69,6% e CSAT do bot de 67,5% para 77,4% na primeira semana completa.</p></li>
      <li><span class="when">14/08</span><span class="tg">Anuidade</span><p>Comunicação de anuidade do Cartão RP, com efeito residual: +188% em pedidos de desbloqueio na semana seguinte.</p></li>
      <li><span class="when">07/08</span><span class="tg">Lending</span><p>CDB Platinum/Titan: garantia executada em 14 dias (antes 58) e liberação de múltiplos aportes para aumento de limite.</p></li>
      <li class="hot"><span class="when">29/06</span><span class="tg">Produto</span><p>Nova regra de cashback para 100% da base (−14% no spending, pico de intenção de cancelamento) e lançamento do Cartão Concedido Standard.</p></li>
    </ul>
  </details>
</section>

<section id="updates">
  <div class="eyebrow">Atualizações depois do report</div>
  <h2>Alinhamento CXM + Cartão RP (07/10)</h2>
  <div class="upd">
    <ul>
      <li>Contatos de quem <b>não entende por que recebeu uma fatura</b> cresceram <b>40%</b> nos primeiros dias de outubro, principalmente em casos de Loans to CC e Tap to CC com Pix no cartão (a taxa do Pix aparece depois na fatura).</li>
      <li>O sistema de “fatura zero” falha quando há saldo residual de cashback e não cobre todas as vendas do Tap to CC.</li>
      <li>Bugs do produto resolvidos em menos de 7 dias: <b>70% (ago) → 42% (set)</b>, meta de 95%.</li>
    </ul>
    <p class="sub" style="margin-top:8px">6 TO-DOs definidos, entre eles revisar a regra de cobrança com cashback, “fatura zero” para Tap to CC, redirecionamentos para a Central de Ajuda nos detalhes da transação e artigos para “Tap to CC” e “Loans to CC”. <a href="https://docs.google.com/document/d/1XGXqec4Y4yJDGvldipvUvWlZ_JWgr0HPBuXt9G20lZ8/edit?tab=t.es4r7xryzu6z">Material completo</a> · fonte: #cc-produto-e-cx</p>
  </div>
</section>

<footer>
  <div>Fonte: Report VoC · Cartão de Crédito · Semana 40 (05/10/2026) · menções: painel 141 · reclamações: resumos de transcrição · <a href="https://sites.google.com/recargapay.com/voc/">Hub VoC</a> · <a href="https://optimus.recargapay.com/PHP/dashboard_view.php?id=246">CXM - Briefing de Suporte</a></div>
  <div class="conf">Strictly confidential</div>
</footer>

</div>
</body>
</html>
"""

open(os.path.join(HERE, "report-cartao-rp-exemplo.html"), "w", encoding="utf-8").write(html)
print("bytes:", len(html.encode("utf-8")))
