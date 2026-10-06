// usage: node merge.js <dashboard_dump.json> <lot_number> <out_prefix>
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const DIR = __dirname;
const DATA = '05/10/2026';

const LOTS = {
  1: ['PIX', 'PIX::Pix Out - Wallet', 'PIX::Pix Out - Cartão', 'EMPRESTIMO', 'EMPRESTIMO::Geral', 'EMPRESTIMO::Consignado', 'MINHA_CONTA', 'SEGUROS'],
  2: ['CARTAO_CREDITO', 'TRANSPORTE', 'CONTAS_BOLETOS', 'LINK_PAGAMENTO', 'RECARGA_CELULAR', 'TAP_TO_PAY', 'CDB_INVESTIMENTOS'],
  3: ['CARTEIRA_BLOQUEADA', 'CONTA_DESATIVADA', 'CHARGEBACK', 'MOVIMENTACOES', 'ADICIONAR_DINHEIRO', 'EXCLUSIVAS', 'OPEN_FINANCE', 'RAF'],
  4: ['TAREFAS_APP', 'MAQUININHA', 'PRIME_PLUS', 'CASHBACK_RENDIMENTO', 'CONTAS_PJ', 'PARCERIA_BENEFICIOS', 'CATALOGO_PRODUTOS'],
};

function load(f) { return JSON.parse(fs.readFileSync(path.join(DIR, f), 'utf8')); }
const GERAL = Object.assign({}, load('geral_1.json'), load('geral_2.json'), load('geral_3.json'), load('geral_4.json'));
const NPS = load('nps.json');

function getJs(dumpPath) {
  let d = JSON.parse(fs.readFileSync(dumpPath, 'utf8'));
  if (d.data) d = d.data;
  if (typeof d.js !== 'string') throw new Error('js field not found');
  return d.js;
}

// locate `var NAME = {...};` using a string-aware brace scanner
function locate(js, name) {
  const marker = 'var ' + name + ' = ';
  const start = js.indexOf(marker);
  if (start < 0 || js.indexOf(marker, start + 1) >= 0) throw new Error(name + ': expected exactly one declaration');
  const objStart = start + marker.length;
  if (js[objStart] !== '{') throw new Error(name + ': object literal not found');
  let depth = 0, i = objStart, q = null;
  for (; i < js.length; i++) {
    const c = js[i];
    if (q) { if (c === '\\') { i++; continue; } if (c === q) q = null; continue; }
    if (c === '"' || c === "'" || c === '`') { q = c; continue; }
    if (c === '{') depth++;
    else if (c === '}') { depth--; if (depth === 0) break; }
  }
  if (depth !== 0) throw new Error(name + ': unbalanced braces');
  const objEnd = i + 1;
  if (js[objEnd] !== ';') throw new Error(name + ': missing ; after literal');
  return { objStart, objEnd, literal: js.slice(objStart, objEnd) };
}

function serialize(obj) {
  const keys = Object.keys(obj);
  if (!keys.length) return '{}';
  return '{\n' + keys.map(k => JSON.stringify(k) + ': ' + JSON.stringify(obj[k])).join(',\n') + '\n}';
}

function main() {
  const [dump, lotArg, outPrefix] = process.argv.slice(2);
  const lot = LOTS[lotArg];
  if (!lot) throw new Error('unknown lot');
  const js = getJs(dump);
  const before = path.join(DIR, outPrefix + '_before.js');
  fs.writeFileSync(before, js);
  execFileSync('node', ['--check', before]);
  if (!js.trimEnd().endsWith('})();')) throw new Error('base js does not end with })();');

  let out = js;
  const report = {};
  for (const [name, src, nps] of [['VOC_ANALISE_GERAL', GERAL, false], ['VOC_ANALISE_NPS', NPS, true]]) {
    const loc = locate(out, name);
    const cur = JSON.parse(loc.literal);
    const prevKeys = Object.keys(cur);
    const touched = [];
    for (const k of lot) {
      if (!(k in src)) { if (!nps) throw new Error('missing geral text for ' + k); continue; }
      cur[k] = { texto: src[k], atualizado_em: DATA };
      touched.push(k);
    }
    for (const k of prevKeys) if (!(k in cur)) throw new Error('lost key ' + k);
    out = out.slice(0, loc.objStart) + serialize(cur) + out.slice(loc.objEnd);
    report[name] = { before: prevKeys.length, after: Object.keys(cur).length, touched };
  }
  const after = path.join(DIR, outPrefix + '_after.js');
  fs.writeFileSync(after, out);
  execFileSync('node', ['--check', after]);
  if (!out.trimEnd().endsWith('})();')) throw new Error('result js does not end with })();');
  const outsideBefore = js.length - locate(js, 'VOC_ANALISE_GERAL').literal.length - locate(js, 'VOC_ANALISE_NPS').literal.length;
  const outsideAfter = out.length - locate(out, 'VOC_ANALISE_GERAL').literal.length - locate(out, 'VOC_ANALISE_NPS').literal.length;
  if (outsideBefore !== outsideAfter) throw new Error('content outside the two objects changed');
  console.log(JSON.stringify({ ok: true, lot: lotArg, report, len_before: js.length, len_after: out.length }, null, 1));
}
main();
