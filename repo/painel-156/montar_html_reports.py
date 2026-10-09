# -*- coding: utf-8 -*-
"""Monta o campo `html` do painel 156 a partir dos reports da semana (um JSON por report).

Uso:
  python3 montar_html_reports.py --skeleton html-esqueleto.html --registro registro-painel.json \
      --reports-dir /tmp/painel-saida --out /tmp/painel-saida/html_final.html --manifest /tmp/painel-saida/manifest.json

- A chave de cada report (squad[/sub]) vem do proprio JSON e precisa existir no registro.
- Erro (exit 1): JSON invalido, chave fora do registro, chave duplicada, report com erro de contrato,
  total acima do limite. Nada e gravado quando ha erro.
- Report ausente NAO e erro: entra em `ausentes` no manifesto (o squad fica sem report no painel e sem link no Slack).
- O manifesto (`publicados`, `ausentes`) e o que a Routine B usa para decidir quais links entram no Slack.
- A atualizacao semanal envia SO o campo html (+ rationale_md). Nunca js, css ou queries.
"""
import argparse, glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validar_report import validar, chave_de

ap = argparse.ArgumentParser()
ap.add_argument('--skeleton', required=True)
ap.add_argument('--registro', required=True)
ap.add_argument('--reports-dir', required=True)
ap.add_argument('--out', required=True)
ap.add_argument('--manifest', required=True)
ap.add_argument('--max-total', type=int, default=110000, help='limite do total dos blocos de dados, em bytes')
a = ap.parse_args()

sk = open(a.skeleton, encoding='utf-8').read()
reg = json.load(open(a.registro, encoding='utf-8'))['registro']
chaves_reg = []
for r in reg:
    if r['chave'] not in chaves_reg:
        chaves_reg.append(r['chave'])

erros, blocos, vistos, rots, total = 0, [], {}, set(), 0
for f in sorted(glob.glob(os.path.join(a.reports_dir, '*.json'))):
    if os.path.basename(f) in ('manifest.json',):
        continue
    try:
        d = json.load(open(f, encoding='utf-8'))
    except Exception as ex:
        print('ERRO  %s: JSON invalido (%s)' % (os.path.basename(f), ex)); erros += 1; continue
    k = chave_de(d)
    if k not in chaves_reg:
        print('ERRO  %s: chave %r nao existe no registro' % (os.path.basename(f), k)); erros += 1; continue
    if k in vistos:
        print('ERRO  chave duplicada %r (%s e %s)' % (k, vistos[k], os.path.basename(f))); erros += 1; continue
    vistos[k] = os.path.basename(f)
    r = validar(d)
    for m in r['erros']:
        print('ERRO  %s: %s' % (k, m)); erros += 1
    for m in r['avisos']:
        print('aviso %s: %s' % (k, m))
    rots.add(d.get('rot'))
    j = json.dumps(d, ensure_ascii=False, separators=(',', ':')).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
    blocos.append((k, '<div hidden data-px-report="%s">%s</div>' % (k, j)))
    total += len(j.encode())
    print('%-36s %6d bytes' % (k, len(j.encode())))
if len(rots) > 1:
    print('aviso: reports de semanas diferentes na mesma saida: %s' % ', '.join(sorted(str(x) for x in rots)))
if total > a.max_total:
    print('ERRO  total %d bytes > limite %d bytes' % (total, a.max_total)); erros += 1
publicados = [k for k in chaves_reg if k in vistos]
ausentes = [k for k in chaves_reg if k not in vistos]
print('\nCobertura: %d de %d chaves do registro. Ausentes: %s' % (len(publicados), len(chaves_reg), ', '.join(ausentes) or '-'))
if erros:
    print('ABORTADO: corrija os erros antes de enviar ao painel.'); sys.exit(1)

ordem = {k: i for i, k in enumerate(chaves_reg)}
blocos.sort(key=lambda x: ordem[x[0]])
html = sk.rstrip() + '\n' + '\n'.join(b for _, b in blocos) + '\n<!--px-reports-end-->\n'
# autoconferencia: reler o que sera enviado
ach = re.findall(r'<div hidden data-px-report="([^"]+)">(.*?)</div>', html, re.S)
assert len(ach) == len(blocos), 'blocos perdidos na montagem'
for k, j in ach:
    json.loads(j)
assert html.rstrip().endswith('<!--px-reports-end-->'), 'marcador final ausente'
open(a.out, 'w', encoding='utf-8').write(html)
json.dump({'publicados': publicados, 'ausentes': ausentes, 'blocos': len(blocos), 'bytes_html': len(html.encode()),
           'bytes_dados': total, 'rot': sorted(x for x in rots if x)}, open(a.manifest, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('OK: %d blocos, %d bytes de dados, campo html = %d bytes' % (len(blocos), total, len(html.encode())))
