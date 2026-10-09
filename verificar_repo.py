# -*- coding: utf-8 -*-
"""Verificador de consistência do repositório da automação de reports VoC (v2: inclui painel 156).

Uso:  python3 verificar_repo.py [pasta_do_repositorio]
Rodar ANTES de editar (para saber o ponto de partida) e DEPOIS (para provar que nada quebrou).
Sai com código 1 se algum teste falhar. Não altera nenhum arquivo.
"""
import json, os, re, sys, unicodedata

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
falhas, avisos, ok = [], [], []


def norm(s):
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower().strip()


def ler(nome):
    with open(os.path.join(ROOT, nome), encoding="utf-8") as f:
        return f.read()


def check(cond, msg, aviso=False):
    (ok if cond else (avisos if aviso else falhas)).append(msg)


ARQUIVOS = ["SKILL.md", "SKILL-INTRADAY.md", "README.md", "README-INTRADAY.md", "canais.json",
            "orientacoes-editoriais.md", "skill-databricks-mcp.md", "skill-zendesk-cx.md",
            "skill-bot-retention-scenarios.md", "skill-amplitude.md", "mapeamento-responsaveis.json",
            "mapeamento-produtos-painel141.json", "watchlist-artigos-central-ajuda.json"]

# 1) arquivos existem e JSONs são válidos
dados = {}
for a in ARQUIVOS:
    existe = os.path.exists(os.path.join(ROOT, a))
    check(existe, f"arquivo presente: {a}")
    if existe and a.endswith(".json"):
        try:
            dados[a] = json.loads(ler(a))
            check(True, f"JSON válido: {a}")
        except Exception as e:
            check(False, f"JSON inválido: {a} ({e})")

# 2) cercas de código balanceadas nos .md
for a in [x for x in ARQUIVOS if x.endswith(".md") and os.path.exists(os.path.join(ROOT, x))]:
    check(ler(a).count("```") % 2 == 0, f"cercas ``` balanceadas: {a}")

# 3) cobertura das 19 verticais entre os três mapeamentos
try:
    canais = dados["canais.json"]["canais"]
    prods = []
    for c in canais:
        if c.get("tipo") in ("geral", "executivo"):
            continue
        for p in (c.get("produtos") or [c]):
            prods.append(norm(p["nome_report"].replace("Report de VoC - ", "")))
    resp = [norm(r["squad"]) for r in dados["mapeamento-responsaveis.json"]["responsaveis"]]
    painel = [norm(k) for k in dados["mapeamento-produtos-painel141.json"]["mapeamento_vertical_report_para_produto_painel"]]
    check(len(prods) == 19, f"canais.json tem 19 reports de produto (achou {len(prods)})")
    check(set(prods) == set(resp), "verticais de canais.json == mapeamento-responsaveis.json"
          + ("" if set(prods) == set(resp) else f"  só em canais: {sorted(set(prods)-set(resp))}  só em responsáveis: {sorted(set(resp)-set(prods))}"))
    check(set(prods) == set(painel), "verticais de canais.json == mapa do painel 141"
          + ("" if set(prods) == set(painel) else f"  diferenças: {sorted(set(prods)^set(painel))}"))
    n_sets = 2 + len(prods)
    check(n_sets == 21, f"total de sets = {n_sets} (esperado 21)")
except Exception as e:
    check(False, f"não foi possível cruzar verticais: {e}")

# 4) responsáveis e produtos do painel
try:
    for r in dados["mapeamento-responsaveis.json"]["responsaveis"]:
        uid = r.get("user_id_slack")
        check(uid is None or re.fullmatch(r"U[A-Z0-9]{8,12}", uid), f"Slack ID plausível: {r['squad']} ({uid})")
    ids = {p["id"] for p in dados["mapeamento-produtos-painel141.json"]["produtos"]}
    for k, v in dados["mapeamento-produtos-painel141.json"]["mapeamento_vertical_report_para_produto_painel"].items():
        check(all(i in ids for i in v["produtos"]), f"produto do painel existe: {k} -> {v['produtos']}")
    for p in dados["mapeamento-produtos-painel141.json"]["produtos"]:
        try:
            re.compile(p["regex"])
            check(True, f"regex compila: {p['id']}")
        except re.error as e:
            check(False, f"regex não compila em Python: {p['id']} ({e}); no Spark pode funcionar, conferir")
except Exception as e:
    check(False, f"verificação de responsáveis/painel falhou: {e}")

# 5) textos que NÃO podem existir
proibidos = [
    (r"#the-cxm-house", "canal arquivado (só pode aparecer na nota histórica 'arquivado')", lambda l: "arquivado" in l),
    (r"\b20 sets\b", "contagem antiga de sets (só vale na frase histórica do incidente)", lambda l: "travou" in l),
    (r"\b2 tentativas\b", "regra antiga de 2 tentativas para o Zendesk", lambda l: False),
    (r"como se (fosse|estivesse em) `MODO=RASCUNHO`", "bug antigo: sem rascunho, voltar a #the-voice-cx", lambda l: False),
    (r"sinalizar isso explicitamente no report", "sinalização de fallback no texto do report (deve ser só interna)", lambda l: False),
]
for a in ARQUIVOS:
    if not os.path.exists(os.path.join(ROOT, a)):
        continue
    for i, linha in enumerate(ler(a).splitlines(), 1):
        for rx, desc, excecao in proibidos:
            if re.search(rx, linha) and not excecao(linha):
                check(False, f"{a}:{i} contém texto proibido — {desc}")

# 6) textos que DEVEM existir
try:
    readme, skill = ler("README.md"), ler("SKILL.md")
    check(readme.count("21 sets") >= 3, f"README: contagem '21 sets' nos prompts/arquitetura (achou {readme.count('21 sets')})")
    corpo = skill.split("**Arquivos de skill obrigatórios — ler na Fase 0:**")[1].split("**Skills organizacionais")[0]
    check("mapeamento-produtos-painel141.json" in corpo, "SKILL.md: arquivo do painel 141 na lista de leitura obrigatória da Fase 0")
    check(readme.count("mapeamento-produtos-painel141.json") >= 2, "README: arquivo do painel 141 listado nos prompts A e B")
    check("#cxm-team" in skill, "SKILL.md usa #cxm-team")
    for a in ("SKILL.md", "SKILL-INTRADAY.md"):
        check(re.search(r'^version: "[\d.]+"', ler(a), re.M) is not None, f"versão no cabeçalho: {a}")
    check("NUNCA é motivo para abortar" in readme, "README: prompts dizem que Zendesk nunca bloqueia")
    check("Hierarquia de importância dos 3 MCPs" in skill, "SKILL.md: hierarquia de MCPs presente")
except Exception as e:
    check(False, f"verificação de textos obrigatórios falhou: {e}")

# 6b) painel 156: arquivos, registro, contrato e textos obrigatórios (v2)
import subprocess, tempfile, shutil
PAINEL = ["painel-156/contrato-report-v1.md", "painel-156/registro-painel.json", "painel-156/montar_html_reports.py",
          "painel-156/validar_report.py", "painel-156/html-esqueleto.html", "painel-156/rationale-painel-156.md",
          "painel-156/modelo-report.json", "painel-156/exemplo-seguros-s40.json"]
for a in PAINEL:
    check(os.path.exists(os.path.join(ROOT, a)), f"arquivo presente: {a}")
try:
    registro = json.loads(ler("painel-156/registro-painel.json"))
    reg = registro["registro"]
    check(registro.get("painel_id") == 156 and "id=156" in registro.get("url_base", ""), "registro-painel: painel 156")
    check("id=141" in registro.get("link_experiencia_recargapay", ""), "registro-painel: link da Experiência RecargaPay (141)")
    chaves = []
    for r_ in reg:
        if r_["chave"] not in chaves:
            chaves.append(r_["chave"])
    check(len(chaves) == 21, f"registro-painel: 21 chaves de report (achou {len(chaves)})")
    for r_ in reg:
        if r_["chave"] != (r_["squad"] + (("/" + r_["sub"]) if r_["sub"] else "")):
            check(False, f"registro-painel: chave {r_['chave']} não bate com squad/sub ({r_['squad']}/{r_['sub']})")
    dup = [r_ for r_ in reg if r_.get("fundido")]
    check(all(r_["chave"] == "outros/utilities" for r_ in dup) and len(dup) == 1, "registro-painel: só Boleto de Cobrança é fundido (em outros/utilities)")
    nomes_reg = {norm(r_["nome_report"]) for r_ in reg if r_["origem"] == "produto"}
    check(nomes_reg == set(prods), "registro-painel: os 19 produtos == canais.json"
          + ("" if nomes_reg == set(prods) else f"  diferenças: {sorted(nomes_reg ^ set(prods))}"))
    check(sum(1 for r_ in reg if r_["origem"] in ("geral", "executivo")) == 2, "registro-painel: Geral e Executivo presentes")
    check([r_["chave"] for r_ in reg if r_["origem"] == "so_painel"] == ["seguros"], "registro-painel: Seguros é o único só-painel")
    canais_json = dados["canais.json"]
    p = canais_json.get("painel", {})
    check(p.get("dashboard_id") == 156 and "id=156" in p.get("url_painel", ""), "canais.json: bloco painel (156)")
    check("id=141" in p.get("link_experiencia_recargapay", ""), "canais.json: link da Experiência RecargaPay (141)")
    check(p.get("campos_atualizados") == ["html", "rationale_md"], "canais.json: atualização só de html e rationale_md")
    check(set(p.get("campos_proibidos_na_atualizacao_semanal", [])) == {"js", "css", "queries"}, "canais.json: js, css e queries proibidos na atualização semanal")
    check("slack_simplificado" in canais_json and canais_json["slack_simplificado"].get("limite_linhas"), "canais.json: bloco slack_simplificado")
    check("thread 3" in canais_json["pipeline_duas_etapas"]["routine_a_rascunho"].get("estrutura_de_cada_set", ""), "canais.json: Routine A com thread 3 (dados do painel)")
except Exception as e:
    check(False, f"verificação do painel 156 (registro/canais) falhou: {e}")
try:
    sys.path.insert(0, os.path.join(ROOT, "painel-156"))
    import importlib
    vr = importlib.import_module("validar_report")
    ex = json.loads(ler("painel-156/exemplo-seguros-s40.json"))
    check(not vr.validar(ex)["erros"], "exemplo-seguros-s40.json passa no validador")
    mo = json.loads(ler("painel-156/modelo-report.json"))
    check(bool(vr.validar(mo)["erros"]), "modelo-report.json FALHA no validador (de propósito, para não publicar placeholder)")
    tmp = tempfile.mkdtemp()
    try:
        shutil.copy(os.path.join(ROOT, "painel-156/exemplo-seguros-s40.json"), os.path.join(tmp, "seguros.json"))
        out = subprocess.run([sys.executable, os.path.join(ROOT, "painel-156/montar_html_reports.py"),
                              "--skeleton", os.path.join(ROOT, "painel-156/html-esqueleto.html"),
                              "--registro", os.path.join(ROOT, "painel-156/registro-painel.json"),
                              "--reports-dir", tmp, "--out", os.path.join(tmp, "o.html"), "--manifest", os.path.join(tmp, "m.json")],
                             capture_output=True, text=True)
        check(out.returncode == 0 and os.path.exists(os.path.join(tmp, "o.html")), "montar_html_reports.py roda com o exemplo e gera o html")
        if out.returncode == 0:
            html = open(os.path.join(tmp, "o.html"), encoding="utf-8").read()
            check(html.rstrip().endswith("<!--px-reports-end-->") and html.count("data-px-report=") == 1, "html montado: 1 bloco e marcador final")
            check(json.load(open(os.path.join(tmp, "m.json")))["publicados"] == ["seguros"], "manifesto lista só o que foi publicado")
        # erro não pode gerar saída
        bad = os.path.join(tmp, "bad"); os.makedirs(bad)
        d = json.loads(ler("painel-156/exemplo-seguros-s40.json")); d["squad"] = "inexistente"
        json.dump(d, open(os.path.join(bad, "x.json"), "w", encoding="utf-8"))
        out2 = subprocess.run([sys.executable, os.path.join(ROOT, "painel-156/montar_html_reports.py"),
                               "--skeleton", os.path.join(ROOT, "painel-156/html-esqueleto.html"),
                               "--registro", os.path.join(ROOT, "painel-156/registro-painel.json"),
                               "--reports-dir", bad, "--out", os.path.join(bad, "o.html"), "--manifest", os.path.join(bad, "m.json")],
                              capture_output=True, text=True)
        check(out2.returncode != 0 and not os.path.exists(os.path.join(bad, "o.html")), "montar_html_reports.py aborta sem gravar saída quando há erro")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
except Exception as e:
    check(False, f"verificação dos scripts do painel falhou: {e}")
try:
    readme, skill = ler("README.md"), ler("SKILL.md")
    check("arturito_update_dashboard" in readme and "PAINEL_ID" in readme, "README: prompt B usa arturito_update_dashboard e PAINEL_ID")
    check("485" in readme, "README: teste da Routine B no rascunho 485")
    check("THREAD" in readme.upper() and "TRÊS threads" in readme, "README: prompt A manda raiz + 3 threads")
    for t in ("TEMPLATE SLACK SIMPLIFICADO", "FASE 4C", "PAINEL_OK", "montar_html_reports.py", "nunca `js`, `css` nem `queries`"):
        check(t.lower() in skill.lower() or t.replace("`", "").lower() in skill.lower(), f"SKILL.md contém: {t}")
    check("somente o link do painel 156 geral" in skill.lower().replace("**", "") or "só o link do painel 156 geral" in skill.lower(), "SKILL.md: formato de falha do painel (só o link do 156 geral)")
    check("id=141" in readme or "141" in readme, "README: menciona o link do painel 141")
    ver = re.search(r'^version: "([\d.]+)"', skill, re.M)
    check(ver is not None and tuple(int(x) for x in ver.group(1).split(".")) >= (3, 11), "SKILL.md: versão >= 3.11")
except Exception as e:
    check(False, f"verificação dos textos do painel falhou: {e}")
for a in ("README.md", "SKILL.md", "orientacoes-editoriais.md", "canais.json"):
    for i, linha in enumerate(ler(a).splitlines(), 1):
        for rx, desc in ((r"sinalizar de forma discreta", "sinalização de fallback no texto do report (deve ser só interna)"),
                         (r"raiz \+ 2 threads", "estrutura antiga de 2 threads (agora o rascunho tem 3 e o Slack final é uma mensagem)"),
                         (r"Thread Reply 1 — Report completo", "bloco antigo de publicação com threads nos canais reais")):
            if re.search(rx, linha):
                check(False, f"{a}:{i} contém texto antigo — {desc}")

# 7) avisos (não reprovam)
try:
    vazios = [k for k, v in dados["mapeamento-produtos-painel141.json"]["mapeamento_vertical_report_para_produto_painel"].items() if not v["produtos"]]
    check(not vazios, f"verticais sem produto no painel 141 (bloco de menções será omitido): {vazios}", aviso=True)
except Exception:
    pass

print(f"\nPASSOU: {len(ok)}   AVISOS: {len(avisos)}   FALHOU: {len(falhas)}\n")
for m in falhas:
    print("  ✗ FALHA :", m)
for m in avisos:
    print("  ! AVISO :", m)
if not falhas:
    print("  ✓ nenhuma falha")
sys.exit(1 if falhas else 0)
