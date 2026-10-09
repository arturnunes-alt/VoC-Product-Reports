# -*- coding: utf-8 -*-
"""Valida um report do painel 156 (contrato v1): estrutura, limites de tamanho e regras de conteudo.

Uso:  python3 validar_report.py arquivo1.json [arquivo2.json ...]
Sai com codigo 1 se algum report tiver erro. Avisos nao reprovam.
"""
import json, re, sys

SQUADS = {'geral', 'pix', 'cartao', 'emprestimo', 't2p', 'link', 'account', 'seguros', 'cdb', 'transporte', 'fraude', 'outros'}
TOP = {'squad', 'sub', 'rot', 'periodo', 'meta', 'pub', 'resumo', 'alertas', 'monit', 'ok', 'kpis', 'funil', 'motivos',
       'causas', 'recl', 'mencoes', 'cenario', 'eventos', 'atualiz', 'rodape'}
MAXN = {'alertas': 4, 'monit': 5, 'ok': 4, 'kpis': 6, 'motivos': 6, 'causas': 5, 'recl': 5, 'eventos': 14}
HARD, ALVO = 20000, 10000
CLS = {'up', 'down', 'flat', None}


def chave_de(d):
    return d.get('squad', '') + (('/' + d['sub']) if d.get('sub') else '')


def textos(o, path=''):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, list):
        for i, x in enumerate(o):
            yield from textos(x, path + '[%d]' % i)
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from textos(v, path + '.' + k)


def validar(d):
    e, w = [], []
    n = len(json.dumps(d, ensure_ascii=False, separators=(',', ':')).encode())
    if n > HARD:
        e.append('tamanho %d B acima do limite duro (%d B)' % (n, HARD))
    elif n > ALVO:
        w.append('tamanho %d B acima do alvo (%d B); considere enxugar' % (n, ALVO))
    for k in d:
        if k not in TOP:
            e.append('chave desconhecida: ' + k)
    if d.get('squad') not in SQUADS:
        e.append('squad invalida: %r (use %s)' % (d.get('squad'), ', '.join(sorted(SQUADS))))
    for k in ('rot', 'periodo', 'pub', 'resumo'):
        if not d.get(k):
            e.append('campo obrigatorio ausente: ' + k)
    if d.get('pub') and not re.fullmatch(r'\d{4}-\d{2}-\d{2}', d['pub']):
        e.append('pub deve ser AAAA-MM-DD')
    for k, m in MAXN.items():
        if len(d.get(k) or []) > m:
            e.append('%s: %d itens (max. %d)' % (k, len(d[k]), m))
    if len(d.get('resumo', '')) > 520:
        e.append('resumo > 520 caracteres')
    for i, a in enumerate(d.get('alertas') or []):
        for k in ('t', 'v', 'n'):
            if not a.get(k):
                e.append('alertas[%d].%s e obrigatorio' % (i, k))
    for i, r in enumerate(d.get('recl') or []):
        if len(r.get('temas', [])) > 6:
            e.append('recl[%d].temas > 6' % i)
        for k in ('exp', 'cor', 'ex'):
            if len(r.get(k, [])) > 3:
                e.append('recl[%d].%s > 3' % (i, k))
        for j, c in enumerate(r.get('cor', [])):
            if '[[' not in c and 'sem evento' not in c.lower():
                w.append('recl[%d].cor[%d]: correlacao sem fonte [[...]]' % (i, j))
    mc = d.get('mencoes') or {}
    if len(mc.get('cards', [])) > 3:
        e.append('mencoes.cards > 3')
    if len(mc.get('trechos', [])) > 3:
        e.append('mencoes.trechos > 3')
    for i, x in enumerate(d.get('kpis') or []):
        s = x.get('serie') or []
        if s and not (3 <= len(s) <= 8 and all(isinstance(v, (int, float)) for v in s)):
            e.append('kpis[%d].serie deve ter 3-8 numeros' % i)
        if x.get('cls') not in CLS:
            e.append('kpis[%d].cls deve ser up, down ou flat' % i)
    fu = d.get('funil') or {}
    if fu.get('partes'):
        soma = sum(p.get('p', 0) for p in fu['partes'])
        if abs(soma - 100) > 1.5:
            w.append('funil.partes: percentuais somam %.1f (esperado ~100)' % soma)
    lk = (d.get('atualiz') or {}).get('link')
    if lk and not str(lk.get('u', '')).startswith('https://'):
        e.append('atualiz.link.u deve ser https://')
    for i, ev in enumerate(d.get('eventos') or []):
        if not ev.get('d') or not ev.get('tag') or not ev.get('txt'):
            e.append('eventos[%d]: d, tag e txt sao obrigatorios' % i)
    for p, t in textos(d):
        if p.endswith('link.u'):
            continue
        if len(t) > 360 and not p.endswith('resumo'):
            w.append('%s: texto com %d caracteres (>360)' % (p, len(t)))
        if re.search(r'<(?!/?b>)', t):
            e.append('%s: HTML nao permitido (so <b>)' % p)
        if re.search(r'[\w.+-]+@[\w-]+\.[\w.]+', t):
            e.append('%s: possivel e-mail (PII)' % p)
        if re.search(r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b', t):
            e.append('%s: possivel CPF (PII)' % p)
        if re.search(r'\(?\b\d{2}\)?\s?9?\d{4}-\d{4}\b', t):
            e.append('%s: possivel telefone (PII)' % p)
        if re.search(r'\b\d{9,}\b', t):
            w.append('%s: sequencia longa de digitos (ID/conta?)' % p)
        if re.search(r'rascunho|nota de valida[cç][aã]o|validamos|reconfirmamos|conforme o rascunho|revis(ao|ão|ado) do time|(squad|time) comentou|skill (ausente|indispon)|modo degradado|integra[cç][aã]o de fallback|gateway', t, re.I):
            e.append('%s: menciona processo interno de validacao/ferramenta' % p)
        if re.search(r'prod\.|dim_|fat_|agg_|flg_|::', t):
            w.append('%s: possivel nome de tabela/tag interna' % p)
        if re.search(r'\b(causou|provocou|foi causad[oa])\b', t, re.I) and '[[' not in t:
            w.append('%s: afirma causalidade sem fonte [[...]]' % p)
    return {'erros': e, 'avisos': w, 'bytes': n}


if __name__ == '__main__':
    falhou = False
    for f in sys.argv[1:]:
        r = validar(json.load(open(f, encoding='utf-8')))
        print(f, r['bytes'], 'B')
        for m in r['erros']:
            print('  ERRO ', m)
        for m in r['avisos']:
            print('  aviso', m)
        falhou = falhou or bool(r['erros'])
    sys.exit(1 if falhou else 0)
