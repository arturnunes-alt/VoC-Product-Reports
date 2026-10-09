# Briefing — atualizar a automação de reports para squads sem erro

Para o Artur levar à conversa que vai alterar a automação. Complementa o handover (`Handover-Reports-VoC-Automacao-e-HTML.md`), que explica **como tudo funciona**; aqui está **o que fazer, o que anexar e onde já se errou**.

Estado: 09/10/2026 · `SKILL.md` v3.11 · `SKILL-INTRADAY.md` v3.8.

---

## 1. Antes de abrir a conversa (ações suas, fora do chat)

| # | Ação | Por quê |
|---|---|---|
| 1 | **Subir esta versão ao GitHub** e conferir que o repositório ficou igual aos arquivos do pacote (`MANIFEST.sha256`) | Os arquivos foram editados na conversa de construção. Não consegui ler o repositório (chutei dois donos e deram 404), então não sei se ele está em dia |
| 2 | **Informar à conversa nova o `owner/nome` e a branch** do repositório | Sem isso ela não consegue ler nem comparar |
| 3 | **Recolar os prompts das Routines A e B** em `claude.ai/code/routines` (texto nos blocos "Prompt da Routine A/B" do `README.md`) | A Routine segue o prompt armazenado ao pé da letra, e três coisas mudaram nele desde a última colagem (ver abaixo) |
| 4 | **Decidir, ou mandar a conversa não tocar**, nas pendências da seção 5 | Várias mexem no comportamento da automação |
| 5 | Confirmar **que ferramentas a conversa nova tem**: Slack, Databricks e um jeito de gravar no GitHub | Existem ferramentas do conector da empresa que criam PR (`github_create_pr`), mas **não testei escrita**. Se ela não gravar, você aplica o diff |

**O que mudou nos prompts (recolar A e B) — versão 3.11, 09/10/2026:**
- **Routine A:** cada set do rascunho ganhou a **thread 3** com a estrutura de dados do painel (JSON). Continua sem escrever em canal real.
- **Routine B:** agora (1) monta os reports de squad, (2) **atualiza o painel Arturito 156** (`arturito_update_dashboard`, só `html` e `rationale_md`) e (3) envia o **Slack simplificado** (alertas, NPS Transacional, suporte, menções + links). Novo parâmetro `PAINEL_ID=156` no prompt (use `485` para testar). O conector `MCP Data - RecargaPay` precisa estar autenticado com a conta do dono do painel.
- **Também no `README.md`:** o fallback do prompt A ainda dizia "sinalizar de forma discreta nos reports" — corrigido para só notificação interna.
- **Pausar** a Routine antiga "Atualização semanal - CXM - VoC - Experiência Produto" (escreve em variáveis que o JS novo do painel 156 não tem mais).

**Mudanças anteriores nos prompts (versão 3.10):**
1. **"20 sets" virou "21 sets"** em três trechos (a Routine A e a descrição de arquitetura). Vem da separação de Empréstimo em Pessoal e Consignado.
2. **Sinalização de skill ausente agora é SOMENTE interna.** O texto antigo do prompt A dizia "sinalizar explicitamente no report", o oposto do `SKILL.md` e do que você pediu. Se esse texto antigo está colado, a Routine pode voltar a escrever "Exclusões/tags desta rodada calculadas via repositório interno" nos reports das squads. Corrigi hoje.
3. **Lista de arquivos de referência** ganhou `mapeamento-produtos-painel141.json` (prompts A e B e `SKILL.md`). Antes ele só era citado no meio da Fase 3.

⚠️ Não vejo o que está colado hoje nas Routines. Se você colou algo diferente do `README.md`, a recolagem sobrescreve.

---

## 2. O que anexar

**Opção mais simples:** o `pacote-atualizacao-automacao-voc.zip` (tudo abaixo, com checksum). A conversa precisa de execução de código para abrir; se não tiver, anexe os arquivos soltos.

| Item | Arquivos |
|---|---|
| **Este briefing** e o **handover** | `00-Briefing-Atualizacao-Automacao.md`, `Handover-Reports-VoC-Automacao-e-HTML.md` |
| **Repositório** (13 arquivos na raiz de `repo/`) | `SKILL.md`, `SKILL-INTRADAY.md`, `README.md`, `README-INTRADAY.md`, `canais.json`, `orientacoes-editoriais.md`, `skill-databricks-mcp.md`, `skill-zendesk-cx.md`, `skill-bot-retention-scenarios.md`, `skill-amplitude.md`, `mapeamento-responsaveis.json`, `mapeamento-produtos-painel141.json`, `watchlist-artigos-central-ajuda.json` |
| **Painel 156** (8 arquivos, em `repo/painel-156/`) | `contrato-report-v1.md`, `registro-painel.json`, `montar_html_reports.py`, `validar_report.py`, `html-esqueleto.html`, `rationale-painel-156.md`, `modelo-report.json`, `exemplo-seguros-s40.json` |
| **Verificador** | `verificar_repo.py` (v2: inclui o painel 156) |
| **HTML** (só se for mexer nele) | pasta `html-report/` (3 arquivos) |
| **Referências** | `handoff_painel_141_experiencia_recargapay.md`, `Governanca-Dados-VoC-CXM.md` (desatualizado em alguns pontos, ver seção 6.3 do handover) |
| **Integridade** | `MANIFEST.sha256` |

Se a conversa não receber o repositório inteiro, ela vai editar sobre uma versão incompleta. Os 13 arquivos se referenciam entre si.

---

## 3. Prompt para colar na conversa

> Vou te passar o material da automação de reports VoC da RecargaPay (pacote anexo). Quero que você **altere a automação** conforme eu descrever abaixo. Antes de editar qualquer coisa:
> 1. Leia o briefing e as seções 2, 3, 4, 9 e 10 do handover, e me diga em poucas linhas o que entendeu.
> 2. Confira a integridade do que recebeu: compare os arquivos com o `MANIFEST.sha256` e rode `python3 verificar_repo.py <pasta>`. Me diga o resultado (hoje o esperado é 0 falhas e 1 aviso).
> 3. Liste **quais arquivos você pretende alterar e por quê**, e espere minha confirmação.
>
> Regras: trabalhe só sobre os arquivos anexados; não reescreva queries de memória (copie do arquivo); depois de cada substituição, confirme que ela aconteceu; mantenha `SKILL.md`, `README.md` e `canais.json` consistentes entre si; suba a versão no cabeçalho do `SKILL.md`; se mudar regra de validação de MCP, fallback ou o que bloqueia a execução, aplique **também** no texto dos prompts do `README.md` e me avise para recolar nas Routines. Não afirme nada como testado se não testou. Ao final me entregue os arquivos alterados, um resumo do que mudou por arquivo e o resultado do `verificar_repo.py` depois da edição.
>
> O que quero alterar: [DESCREVER AQUI]

---

## 4. Protocolo que a conversa deve seguir

1. **Ponto de partida:** checksum + `verificar_repo.py` antes de tocar em qualquer arquivo.
2. **Escopo:** listar os arquivos que vai mudar e esperar confirmação.
3. **Editar** com substituição exata e conferir a cada passo (já houve substituição que não aconteceu por diferença de quebra de linha ou de barra invertida, sem erro visível).
4. **Propagar:** toda mudança de contagem, nome de canal, ID, responsável ou vertical precisa ser feita em todos os lugares (use `grep`). Casos reais: "20 sets" sobrando em `canais.json`; frase contraditória entre `README.md` e `SKILL.md`.
5. **Prompt:** se tocou em validação de MCP, fallback, o que bloqueia ou modo de execução, atualizar também os blocos de prompt do `README.md`.
6. **Pós-checagem:** `verificar_repo.py` com 0 falhas; JSONs válidos; versão subida.
7. **Entrega:** arquivos alterados + resumo por arquivo + resultado do verificador.
8. **Você:** `git push` → recolar prompts (se a conversa avisar) → **"Run now" na Routine A** → ler o resultado em `#the-voice-cx`.

**Cuidado ao testar:** a **Routine A só posta em `#the-voice-cx`** (rascunho), então é segura. A **Routine B atualiza o painel 156 e publica nos canais reais das squads**. Para testar a B, use o "MODO TESTE ADICIONAL" do `README.md` (seção 4): `PAINEL_ID=485` e Slack redirecionado para `#the-voice-cx`. Só depois faça **uma** execução real, avisando as squads.

**Checklist do resultado da Routine B (primeira execução real):**
- [ ] Painel 156: aba "Report da squad" de cada squad com a nova "Semana NN"; Seguros presente
- [ ] Mensagens simplificadas nos canais: só alertas, NPS Transacional, suporte e menções; sem threads; ≤ 14 linhas
- [ ] Links `...id=156&r=<chave>/rep` abrem o report certo (conferir 3) e o link do 141 abre; `&amp;` renderiza como `&`
- [ ] Números do Slack iguais aos do painel; nenhuma frase sobre rascunho, validação ou falha de ferramenta
- [ ] Se o painel falhar de propósito (teste): a mensagem sai só com o link do 156 geral

**Checklist do resultado da Routine A (depois do "Run now"):**
- [ ] 21 sets em `#the-voice-cx`, cada um marcado `[RASCUNHO → #canal-real]`, Empréstimo em dois sets
- [ ] Mensagem raiz até 5 linhas + Thread 1 (report) + Thread 2 (alertas) + Thread 3 (JSON do painel; Boleto de Cobrança só referencia Contas e Boletos)
- [ ] Nenhum "N/D" ou erro visível; nenhuma tabela markdown
- [ ] Nenhuma frase sobre skill indisponível ou "dados parciais" no texto
- [ ] Seções novas presentes: Reclamações nos principais motivos e Menções ao produto (omitidas só quando sem dado)
- [ ] Números iguais aos do Databricks; sem PII em trechos de clientes
- [ ] Notificação interna recebida (e anotar se vier o erro de `status`)

---

## 5. Pendências que podem afetar a edição (decidir ou mandar não mexer)

| Pendência | Impacto na edição |
|---|---|
| **Retenção do bot**: report (63,8% / 67,5%) ≠ base (63,4% / 64,0%) | Se a definição mudar, alterar `SKILL.md` (seção Retenção de Bot), `skill-databricks-mcp.md` §12 e `skill-bot-retention-scenarios.md` juntos |
| **Canais divergentes da planilha** (Pix, Consignado, Cartão) | Mudar canal exige `canais.json`, `mapeamento-responsaveis.json`, ordem de envio e checklist do `SKILL.md`, além do ID |
| **Duas "Patty" no Slack** (usada `U019WQT2KFU`) e Link de Pagamento sem responsável explícito | Só `mapeamento-responsaveis.json` |
| **Intraday**: Empréstimo Pessoal/Consignado fora da tabela de potencial; nomes novos | `SKILL-INTRADAY.md` (tabela de potencial) |
| **Movimentações Financeiras** sem produto no painel 141 | O bloco de menções dela é omitido (é o aviso do verificador) |
| **Gateway Zendesk "[TEST]"** | Se houver gateway de produção, trocar nome em `SKILL.md`, `README.md` e `canais.json` |
| **Notificação interna com erro `status: "proactive"`** | Problema da plataforma de Routines; não se resolve por arquivo |
| **Routine B gravando no Arturito** (permissão do dono, ~100 KB por chamada, `arturito_get_dashboard` grande demais para reler) | Não testado. Testar com `PAINEL_ID=485` antes do 156; se a releitura não couber, a conferência fica no status de sucesso e no checklist manual |
| **Links `&r=` e escape `&amp;` no Slack** | Não testados no Arturito/Slack; conferir na primeira execução real |
| **Seguros só no painel** (sem canal no Slack) | Se criar um canal/vertical de Seguros, mexer em `canais.json`, `registro-painel.json` e nos 21 sets (contagens) |

---

## 6. Armadilhas que já custaram caro

1. **Repositório e prompt são coisas diferentes.** Editar o arquivo não muda o prompt da Routine.
2. **A Routine B publica nas squads.** Nada de testar com ela sem aviso.
3. **Zendesk nunca bloqueia.** Fallback `MCP-Proxy-RecargaPay` e Modo Degradado; só Databricks e Slack abortam. Não reintroduzir regra de "2 tentativas".
4. **Sem rascunho, a B publica direto na squad**, nunca de volta em `#the-voice-cx`.
5. **Não citar o processo de validação nem falhas de ferramenta no texto dos reports.** Isso vai só para a notificação interna.
6. **`agg_overview` é a fonte oficial.** Não recalcular número oficial por tabela granular.
7. **Databricks via MCP:** somente leitura, `UNION` no topo falha, a prévia corta em 10 linhas (usar `databricks_run_query` para ler mais).
8. **Disponibilidade de ferramenta varia por sessão.** Falha pontual não é estrutural.
9. **Regex do painel 141 não se redigita:** vêm de `mapeamento-produtos-painel141.json`.
10. **Regra de inferência:** só afirmar o que tem fonte e data; correlação não é causa.
11. **`#the-cxm-house` está arquivado**; o canal geral é `#cxm-team` (`C0BLU1T02AK`).

---

## 7. O que eu alterei ao montar este pacote (para você saber que mudou)

- **Versão 3.11 (09/10/2026, painel 156 + Slack simplificado):** `SKILL.md` (Fase 4 em 4A/4B/4C, estrutura de dados do painel, template Slack simplificado, checklist), `README.md` (arquitetura, prompts A e B, testes), `canais.json` (blocos `painel`, `slack_simplificado`, `pipeline_duas_etapas`), `orientacoes-editoriais.md` (o que vai ao Slack e ao painel), nova pasta `repo/painel-156/` e `verificar_repo.py` v2.
- Versão 3.10: `README.md`: frase de sinalização do fallback de skill (agora só interna); lista de arquivos dos prompts A e B (`mapeamento-produtos-painel141.json`).
- `SKILL.md`: arquivo do painel 141 na lista de leitura obrigatória da Fase 0; versão 3.9 → 3.10.
- Handover: versão e referência ao verificador e a este briefing.
- Novo: `verificar_repo.py` (94 testes passam hoje; testei contra uma cópia estragada de propósito e ele reprovou as 5 falhas que provoquei).

O verificador **não** substitui a leitura do diff: ele só pega inconsistência mecânica (JSON, contagens, IDs, textos proibidos, lista de leitura). Não valida se uma regra de análise está certa.
