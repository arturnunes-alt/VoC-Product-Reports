# Skill — API IndeCX · NPS Transacional, NPS Relacional e CSAT
<!-- Fonte: api_indecx_guia_routine.md, adaptado para a Routine VoC RecargaPay -->
<!-- Adaptação: Artur Nunes — Jul/2026 -->

---

## 1. QUANDO USAR ESTA API vs DATABRICKS

A Routine tem **duas fontes** para NPS/CSAT — cada uma com um papel específico.
Não são substitutas uma da outra; são complementares.

| Necessidade | Fonte | Motivo |
|---|---|---|
| Número oficial de NPS Tx / CSAT (headline do report) | `prod.cx.agg_overview` (Databricks) | Fonte batch consistente com os dashboards oficiais — ver `skill-zendesk-cx.md` §3 |
| Verbatims / feedback textual dos detratores | **API IndeCX** | Databricks não armazena o texto do feedback |
| Pergunta de Resolutividade (CSAT N1 e CSAT Bot) | **API IndeCX** | `additionalQuestions[]` não existe no `agg_overview` |
| NPS Relacional segmentado PF vs PJ | **API IndeCX** | Segmentação direta pelo nome da ação, sem depender de JOIN |
| Menções a produtos nos feedbacks abertos (NPS Relacional) | **API IndeCX** | Requer leitura de texto livre — só a API tem o campo `feedback` |
| Dado do dia corrente / semana em andamento | **API IndeCX** | Tempo real — o DaaP tem defasagem D-1 |
| Cross-check de divergência entre fontes | Ambas | Se a diferença entre API e Databricks for >10%, sinalizar e usar Databricks como referência oficial |

**Na prática, a Routine semanal usa a API IndeCX para:**
1. Extrair a pergunta de Resolutividade de CSAT Atendimento e CSAT RecargaBot
2. Extrair verbatims representativos dos detratores de NPS Transacional por produto
3. Calcular NPS Relacional PF vs PJ com menções a produtos nos feedbacks
4. Servir como fallback se o Databricks estiver indisponível

O número final de NPS/CSAT apresentado no report **continua vindo do `agg_overview`**
para manter consistência com os dashboards oficiais — a API IndeCX enriquece, não substitui.

---

## 2. AUTENTICAÇÃO

```
GET https://indecx.com/v3/integrations/authorization/token
Header: Company-Key: {COMPANY_KEY}
```

Resposta: `{ "authToken": "eyJ..." }`

**Company-Key deve estar em variável de ambiente da Routine — nunca hardcoded no repositório.**
Nome da variável: `INDECX_COMPANY_KEY`. Configurar em `claude.ai/code/routines` na seção
de Environment Variables ao criar/editar a Routine.

O token é obtido **uma vez por execução** — não é persistente entre rodadas.
Não há rate limit documentado; implementar backoff exponencial em erro 429 ou timeout.

---

## 3. ENDPOINTS

### 3.1 `/actions-info` — Mapa de ações (produtos/pesquisas)

```
GET /actions-info
Header: Authorization: Bearer {token}
```

Retorna `[{ "_id": "...", "name": "NPS Transacional Cartão RP" }, ...]`.

**Fallback:** se falhar, o nome também vem em `action.name` dentro de cada resposta
de `/answers-info/all` — sempre combinar as duas fontes (ver função `enrich_actions_map`).

Tentar headers nesta ordem: `Authorization: Bearer {token}` → `Company-Key: {COMPANY_KEY}` (fallback).

---

### 3.2 `/answers-info/all` — Respostas de pesquisa (dado principal)

```
GET /answers-info/all?page=1&limit=1000&startDate=DD-MM-YYYY&endDate=DD-MM-YYYY&dateType=createdAt
Header: Authorization: Bearer {token}
Header: Treatments-Details: true
```

**Header `Treatments-Details: true` é obrigatório** — sem ele, o objeto `action` não vem populado.

**Paginação:** máx 1000 registros/página. Paginar até `len(batch) < 1000`.
Limite de segurança: máx 100 páginas por execução.

**Timezone:** todas as datas em `America/Sao_Paulo` (BRT) — mesmo fuso da Routine.

**Campos-chave de cada resposta:**
- `metric` — contém `"nps"` ou `"csat"` (case-insensitive)
- `review` — nota numérica (NPS: 0–10 · CSAT: 1–5)
- `feedback` — texto livre (pode ser vazio)
- `additionalQuestions[]` — cada item tem `text` + (`review` numérico OU `answerText`)
- `actionId` / `action.name` / `actionName` — resolução de produto

---

## 4. CÁLCULO DE NPS E CSAT

```python
# NPS (0-10)
promotores = contagem(nota >= 9)
detratores = contagem(nota <= 6)
nps = round((promotores - detratores) / total * 100, 1)

# CSAT (1-5)
satisfeitos = contagem(nota in [4, 5])
csat_pct = round(satisfeitos / total * 100, 1)
```

Estas fórmulas devem produzir números **próximos** aos do `agg_overview` — divergência
>10% indica problema de filtro (ex: período errado, ação não mapeada) e deve ser investigada
antes de usar o dado no report, nunca ignorada silenciosamente.

---

## 5. RESOLUÇÃO DE PRODUTO/VERTICAL — MAPA CALIBRADO RECARGAPAY

A IndeCX não tem campo estruturado de produto — resolver por substring match no nome
da ação, ordem de prioridade (mais específico primeiro). Mapa calibrado para as 18
verticais do `canais.json`:

```python
ACAO_MAP = [
    # Pix
    ("pix out - cc",        "Pix CC"),
    ("pix cc",               "Pix CC"),
    ("pix cartão",           "Pix CC"),
    ("pix out - wallet",     "Pix Out"),
    ("pix in",               "Pix In"),
    ("pix saldo",            "Pix Out"),
    ("pix",                  "Pix Out"),  # fallback genérico — sempre por último dentro do grupo Pix

    # RAF
    ("raf indicado",         "RAF Indicado"),
    ("raf indicador",        "RAF Indicador"),
    ("raf",                  "RAF Indicado"),  # fallback

    # Cartão de Crédito
    ("cartão rp",            "Cartao de Credito"),
    ("cartao rp",            "Cartao de Credito"),
    ("cartão de crédito",    "Cartao de Credito"),

    # Empréstimo
    ("loans consignado",     "Credito Consignado"),
    ("consignado",           "Credito Consignado"),
    ("loans",                "Emprestimo"),
    ("empréstimo",           "Emprestimo"),

    # Recarga
    ("topup",                "Recarga de Celular"),
    ("recarga",              "Recarga de Celular"),

    # Transporte
    ("transport",            "Transporte"),

    # Contas & Boletos
    ("boleto de cobrança",   "Boleto de Cobranca"),
    ("boletos",              "Contas e Boletos"),
    ("utilities",            "Contas e Boletos"),

    # Tap to Pay / Link de Pagamento
    ("tap to pay",           "Tap to Pay"),
    ("tap",                  "Tap to Pay"),
    ("link de pagamento",    "Link de Pagamento"),
    ("link pagamento",       "Link de Pagamento"),

    # Investimentos
    ("cdb",                  "CDB"),
    ("rendimento cdi",       "Rendimento CDI"),
    ("movimentações",        "Movimentacoes Financeiras"),

    # Conta / Fraude
    ("minha conta",          "Minha Conta"),
    ("conta desativada",     "Conta Desativada"),
    ("carteira desativada",  "Carteira Desativada"),
    ("chargeback",           "Chargeback Recovery"),
]

def resolver_produto(nome_acao: str) -> str | None:
    lower = (nome_acao or "").lower()
    for fragmento, produto in ACAO_MAP:
        if fragmento in lower:
            return produto
    return None  # ação não reconhecida — logar para revisão, nunca ignorar silenciosamente
```

⚠️ **Antes da primeira execução em produção:** chamar `/actions-info` isoladamente e listar
todos os nomes de ação reais da conta RecargaPay. Os fragmentos acima são um ponto de
partida — ações não mapeadas são **silenciosamente ignoradas** e subestimam o NPS geral.
Se qualquer ação relevante não bater com o mapa, adicionar o fragmento correspondente.

---

## 6. NPS RELACIONAL — SEGMENTAÇÃO PF/PJ

O NPS Relacional segue nome de ação, não produto. Filtrar por substring:

```python
ACOES_PF = ["NPS Relacional PF V2", "NPS Relacional PF"]
ACOES_PJ = ["Relacional PJ MEI", "NPS Relacional PJ"]
```

Para menções a produtos no feedback aberto do NPS Relacional: aplicar o `ACAO_MAP`
(seção 5) como busca de substring dentro do texto de `feedback`, não do nome da ação —
é assim que a Routine identifica qual produto o cliente mencionou espontaneamente.

---

## 7. PERGUNTAS ADICIONAIS — RESOLUTIVIDADE E CES

Usadas para CSAT Atendimento (N1) e CSAT RecargaBot — ambos têm pergunta de
Resolutividade embutida em `additionalQuestions[]`.

```python
def agregar_pergunta(respostas, fragmento_texto):
    soma, count = 0, 0
    contagem_textual = {}
    for r in respostas:
        for q in r.get("additionalQuestions", []):
            if fragmento_texto.lower() not in q.get("text", "").lower():
                continue
            if q.get("review") not in (None, ""):
                soma += float(q["review"])
                count += 1
            else:
                val = q.get("answerText") or ""
                if val:
                    contagem_textual[val] = contagem_textual.get(val, 0) + 1
    if count > 0:
        return {"tipo": "media", "valor": round(soma / count, 2)}
    return {"tipo": "ranking", "valores": contagem_textual}

# Uso para Resolutividade
resolutividade_n1 = agregar_pergunta(respostas_csat_n1, "resolutividade")
resolutividade_bot = agregar_pergunta(respostas_csat_bot, "resolutividade")
```

⚠️ O texto exato de `additionalQuestions[].text` varia por ação — validar periodicamente
contra `/actions-info` + amostra de respostas antes de confiar no fragmento `"resolutividade"`.

---

## 8. FLUXO DE EXECUÇÃO NA ROUTINE (Fase 2 do SKILL.md)

```
1. Obter token          → GET /authorization/token (usar INDECX_COMPANY_KEY do ambiente)
2. Obter mapa de ações   → GET /actions-info (+ enriquecer com action.name dos answers)
3. Definir período       → semana anterior BRT, formato DD-MM-YYYY
4. Paginar respostas      → GET /answers-info/all (loop até batch < 1000, máx 100 páginas)
5. Classificar por metric → NPS (0-10) vs CSAT (1-5)
6. Resolver produto       → ACAO_MAP (seção 5)
7. Agrupar por produto/vertical
8. Calcular NPS/CSAT por grupo — usar como cross-check do agg_overview, não como número final
9. Extrair Resolutividade (CSAT N1 e Bot) via additionalQuestions
10. Extrair até 3 verbatims representativos por produto (detratores primeiro)
11. NPS Relacional: segmentar PF/PJ + menções a produtos no feedback
```

**Se a API IndeCX falhar:** omitir Resolutividade e verbatims do report — os números
headline de NPS/CSAT continuam disponíveis via `agg_overview`, então o report não fica
sem indicador, apenas sem o enriquecimento qualitativo.

---

## 9. PSEUDOCÓDIGO BASE (adaptar para bash_tool / Python na Routine)

```python
import requests
from datetime import datetime, timedelta
import os

BASE_URL = "https://indecx.com/v3/integrations"
COMPANY_KEY = os.environ["INDECX_COMPANY_KEY"]  # nunca hardcoded

def get_token():
    r = requests.get(f"{BASE_URL}/authorization/token",
                      headers={"Company-Key": COMPANY_KEY})
    r.raise_for_status()
    return r.json()["authToken"]

def get_actions_map(token):
    actions_map = {}
    for headers in [{"Authorization": f"Bearer {token}"}, {"Company-Key": COMPANY_KEY}]:
        try:
            r = requests.get(f"{BASE_URL}/actions-info", headers=headers)
            if r.status_code in (200, 201):
                for a in r.json():
                    if a.get("_id") and a.get("name"):
                        actions_map[a["_id"]] = a["name"]
                break
        except Exception:
            continue
    return actions_map

def get_answers(token, start_date, end_date):
    all_answers, page = [], 1
    while True:
        r = requests.get(
            f"{BASE_URL}/answers-info/all",
            params={"page": page, "limit": 1000,
                    "startDate": start_date.strftime("%d-%m-%Y"),
                    "endDate": end_date.strftime("%d-%m-%Y"),
                    "dateType": "createdAt"},
            headers={"Authorization": f"Bearer {token}", "Treatments-Details": "true"},
        )
        if r.status_code != 200:
            break
        batch = r.json().get("answers", [])
        all_answers.extend(batch)
        if len(batch) < 1000 or page > 100:
            break
        page += 1
    return all_answers

def enrich_actions_map(answers, actions_map):
    for a in answers:
        aid = a.get("actionId")
        if aid and aid not in actions_map:
            nome = (a.get("action") or {}).get("name") or a.get("actionName")
            if nome:
                actions_map[aid] = nome
    return actions_map

def calc_nps(notas):
    total = len(notas)
    if total == 0:
        return {"nps": None, "n": 0}
    prom = sum(1 for n in notas if n >= 9)
    det = sum(1 for n in notas if n <= 6)
    return {"nps": round((prom - det) / total * 100, 1), "n": total,
            "prom_pct": round(prom / total * 100, 1), "det_pct": round(det / total * 100, 1)}

def calc_csat(notas):
    total = len(notas)
    if total == 0:
        return {"csat": None, "n": 0}
    sat = sum(1 for n in notas if n in (4, 5))
    return {"csat": round(sat / total * 100, 1), "n": total}

# ── Execução semanal da Routine ──────────────────────────────────────────
token = get_token()
actions_map = get_actions_map(token)

hoje = datetime.now()
segunda_passada = hoje - timedelta(days=hoje.weekday() + 7)
domingo_passado = segunda_passada + timedelta(days=6)

answers = get_answers(token, segunda_passada, domingo_passado)
actions_map = enrich_actions_map(answers, actions_map)

nps_answers = [a for a in answers if "nps" in (a.get("metric") or "").lower()]
csat_answers = [a for a in answers if "csat" in (a.get("metric") or "").lower()]

grupos_nps = {}
for a in nps_answers:
    nome_acao = actions_map.get(a["actionId"], "")
    produto = resolver_produto(nome_acao)
    if produto and a.get("review") not in (None, ""):
        grupos_nps.setdefault(produto, []).append(float(a["review"]))

resultado_nps_por_produto = {p: calc_nps(notas) for p, notas in grupos_nps.items()}
```

---

## 10. BOAS PRÁTICAS

1. **Backoff exponencial** em erro 429/timeout — sem rate limit documentado
2. **Token novo por execução** — não persistir entre rodadas da Routine
3. **Paginar completamente** antes de calcular qualquer métrica — nunca confiar só na 1ª página
4. **Timezone `America/Sao_Paulo`** em todos os cálculos de data
5. **Validar `ACAO_MAP` periodicamente** — ações não mapeadas são ignoradas silenciosamente
   e subestimam o NPS geral; revisar a cada mudança de produto ou pesquisa nova no IndeCX
6. **Cross-check obrigatório:** se o NPS/CSAT calculado via API divergir >10% do `agg_overview`,
   sinalizar internamente e usar o `agg_overview` como número oficial no report
