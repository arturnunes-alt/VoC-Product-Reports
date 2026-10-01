# Rascunhos VoC mensal por produto — Setembro/2026 (dados até 29/09)

Status: **NÃO postados**. 18 sets (raiz + thread 1 + thread 2) prontos para revisão e envio em #the-voice-cx (C060F2QUJCD).
Base: volume, NPS e CSAT por vertical já calculados na sessão (agg_overview), mais eventos de Slack. Comparação: 01–29/09 vs 01–29/08. Faixas: S1 01–06 · S2 07–13 · S3 14–20 · S4 21–27 · S5 28–29 (parcial). Valores são contatos/dia.
Seções omitidas por falta de dado nesta rodada (precisam do Databricks de volta): ranking de motivos/causas raiz por produto, funil N1/N2/bot por produto, retenção do bot, Central de Ajuda por produto, perfil New/NewNew/Repeat, redes sociais. Onde o motivo do produto é citado abaixo, vem de leituras já feitas ou de relatos dos canais.
Zendesk ao vivo ficou indisponível; leitura qualitativa só via resumos de transcrição (parcial).

---

## 1. Minha Conta → #account_cx

**Raiz**
<!here> 📊 **[RASCUNHO → #account_cx] Report de VoC - Minha Conta — Setembro/2026 (01–29/09)**

Contatos estáveis no mês (4.132, 0% vs agosto), mas com pico em 07–20/09 (158–164/dia contra 124 na 1ª semana) e retorno a 121/dia em 21–27/09. CSAT N1 muito abaixo da meta: ~54% desde o início de setembro (agosto 64%). Instabilidade de Open Finance/abertura de conta (03–10/09) e plataforma P1 em 08/09 coincidem com o pico.
🔗 https://sites.google.com/recargapay.com/voc/
🔗 CXM - Briefing de Suporte: https://optimus.recargapay.com/PHP/dashboard_view.php?id=246
💬 Comentários e ajustes nesta thread — a versão final validada será publicada em #account_cx após a revisão do time.

**Thread 1 — Report**
**RESUMO DO MÊS**
• **4.132 contatos** em 01–29/09 (agosto: 4.132) | média ~142/dia nos dois meses.

**EVOLUÇÃO SEMANA A SEMANA** (contatos/dia)
ago: 142 | S1: 124 | S2: **158** | S3: **164** | S4: 121 | S5 (parcial): 146
Leitura: subida de ~30% da S1 para S2–S3 e retorno em S4; S5 volta a subir (2 dias, preliminar).

**EVENTOS E IMPACTOS**
• 03–10/09: falhas de infraestrutura em sequência deixaram a abertura de conta lenta ou fora do ar por quase uma semana; 6 mil conexões recusadas em 2 dias; conversão normalizada depois (>70%). Correlacionado a evento reportado em #lideres-cx-e-cxm.
• 08/09 14:03: plataforma inteira fora (P1), reportada em #escalation_incidents. Coincide com a semana de pico.
• 09/09 e 10/09: ajuste de UX de login (aprovação pendente) e novo texto para abertura de conta negada por fraude. 11/09: cliente com R$ 6,5 mil bloqueado por limite de upload de contratos de múltiplos parceiros (sem resolução no canal).
• 17/09: corrigido o botão "Preciso de ajuda" do QR de acesso web (antes caía em página errada).
• 25/09: nova mensagem no app para conta encerrada, com botão "Solicitar devolução" quando há saldo. No mesmo dia, bloqueio de Pix In por regra de documento em blocklist (regra desligada pela engenharia, religação em avaliação com Risco).
• Efeito acumulado: a queda de S4 é parcial; a religação da regra e a alta de S5 podem pressionar outubro.

**SATISFAÇÃO DO CLIENTE**
• CSAT N1: agosto **64,4%** → 01–13/09 **53,7%** → 14–29/09 **54,8%** (meta 80%). Base pequena (54 e 73 respostas): indicativo.

**DESTAQUES E OPORTUNIDADES**
• Esperar a próxima rodada de dados para motivos e causas raiz do produto antes de priorizar ações.

**Thread 2 — Alertas**
🚨 **ALERTAS — Minha Conta · Setembro/2026 (01–29/09)**

🔴 **CSAT N1 abaixo do piso**
Observado: **54,8%** (14–29/09) | Esperado: ≥75%
Mantém-se desde o início do mês; coincide com instabilidades de conta e plataforma (03–10/09).

✅ Volume total do mês dentro do padrão (0% vs agosto).

---

## 2. Cartão de Crédito → #cc-produto-e-cx

**Raiz**
<!here> 📊 **[RASCUNHO → #cc-produto-e-cx] Report de VoC - Cartão de Crédito — Setembro/2026 (01–29/09)**

**8.637 contatos (+15% vs agosto)**, maior vertical do mês. Pico em 07–13/09 (332/dia) e queda até 21–27/09 (235/dia), com rebote em 28–29/09 (319/dia) por causa da anuidade Gold/Standard. NPS Tx ~59–61 (meta 75) e CSAT N1 ~81% (meta 80%). Tema emergente: resgate de saldo garantido, ligado ao empréstimo no cartão e ao Cartão Empreendedor.
🔗 https://sites.google.com/recargapay.com/voc/
🔗 CXM - Briefing de Suporte: https://optimus.recargapay.com/PHP/dashboard_view.php?id=246
💬 Comentários e ajustes nesta thread — a versão final validada será publicada em #cc-produto-e-cx após a revisão do time.

**Thread 1 — Report**
**RESUMO DO MÊS**
• **8.637 contatos** vs 7.537 em agosto (**+15%**), média 298/dia (agosto: 260).

**EVOLUÇÃO SEMANA A SEMANA** (contatos/dia)
ago: 260 | S1: 324 | S2: **332** | S3: 299 | S4: **235** | S5 (parcial): 319
Leitura: começou alto, cedeu até S4 e voltou a subir com a cobrança de anuidade.

**EVOLUÇÃO DOS TEMAS** (empresa toda; o cartão concentra boa parte)
• **Bloquear/desbloquear/cancelar cartão:** 70 → 55 → 36 → **21** → 40 (S5). Queda forte até S4 sem causa confirmada; rebote com a anuidade (28→29/09: 4x segundo a squad).
• **Resgate de saldo garantido:** 14 → **31** → **35** → 25 → 24/dia (agosto: 9). Tema emergente, ligado ao empréstimo que passou a cair no cartão (09/09) e ao Cartão Empreendedor.
• **Cartão Empreendedor – resgatar saldo** (causa raiz): 2 → 13 → **20** → 14 → 14/dia (agosto: ~0). Clientes que venderam no Tap to Pay e viram o valor virar limite garantido, sem esperar e sem achar como resgatar. Sentimento frustrado.
• **Fatura:** "problema com pagamento da fatura" 11 → 15 → 12 → 9 → **34** (S5); "não entende por que recebeu fatura" 19 → 23 → 16 → 18 → **33** (S5).

**EVENTOS E IMPACTOS**
• 02/09: campanhas de aviso de anuidade: 1,5 M qualificados, 32% de visualização, 8,11 mil acessos à Central, 827 contatos de cancelamento (contact rate 0,18%); ~70% não viram a mensagem.
• 08/09: plataforma fora do ar (P1); 09/09: empréstimo passa a cair no cartão para 100% dos clientes (**origem de 8 dos 12 motivos que mais cresceram**, segundo o relatório executivo de 16/09).
• 14–16/09: >100 contatos por encerramento de conta-cartão por "desinteresse comercial" (15% dos contatos em 14/09; 23 casos no ReclameAqui; falta de aviso prévio). 15/09: recusas por regra antifraude (PFT-63) por ~1h. 20/09: push incorreto de fatura em aberto e negativação para ~80 clientes Platinum/Black com fatura quitada.
• 17/09: limite garantido não sincroniza ("limite zerado"); workaround de cashin simbólico; 6 casos até 22/09; tag em criação para quantificar.
• 23/09: CAP de parcelamento para 19 mil clientes de alto risco (códigos LP2/LP3/LP4, push na recusa).
• **28/09: início da anuidade Gold/Standard (R$ 9,90).** Até 18h30 de 29/09: 33 contatos de anuidade (26 humanos), 1 escalada ao ReclameAqui; fatura saiu com o valor da garantia em vez de R$ 9,90 (sem resposta no canal). Clientes cobrados: ~890 (squad) ou 3.800 (onda 1, relatório executivo): confirmar.
• Efeito acumulado: o mês termina em alta por conta da anuidade; outubro depende do desenho do bot e da decisão de estorno (Pismo ou carteira).

**SATISFAÇÃO DO CLIENTE**
• NPS Tx: agosto 57,9 → 01–13/09 **60,7** → 14–29/09 **59,2** (meta 75).
• CSAT N1: agosto 83,8% → 80,7% → **80,8%** (meta 80%): perto do limite.

**DESTAQUES E OPORTUNIDADES**
• Deflexão na home para artigos de anuidade e cancelamento (pedido de 25/09 pendente de confirmação).
• Tela de cancelamento via chatbot aprovada para teste (18/09).
• Aviso prévio e artigo sobre encerramento por desinteresse comercial aguardam decisão de produto.

**Thread 2 — Alertas**
🚨 **ALERTAS — Cartão de Crédito · Setembro/2026 (01–29/09)**

🔴 **Novo tema: Cartão Empreendedor / resgate de saldo garantido**
Observado: **20/dia** (S3) | Esperado: ~0 em agosto
Coincide com o rollout do Tap to CC e com o empréstimo no cartão (09/09). Squad de Subacquirer reporta contact rate de 1,9% entre usuários com a feature.

🔴 **Anuidade Gold/Standard**
Observado: 33 contatos em 29/09 (até 18h30) e "bloquear/cancelar cartão" 4x vs 28/09 | Esperado: 83–333 contatos escalados na onda 1
Fatura com valor divergente (R$ 9,90) sem resposta no canal.

✅ NPS e CSAT estáveis no mês. ✅ Volume em queda de S2 a S4.

---

## 3. Conta Desativada → #cx_fraud

**Raiz**
<!here> 📊 **[RASCUNHO → #cx_fraud] Report de VoC - Conta Desativada — Setembro/2026 (01–29/09)**

1.603 contatos (+16% vs agosto), estáveis em ~52–60/dia durante o mês. CSAT N1 em ~38%, muito abaixo do piso de 75%. Em 28 e 29/09 houve picos de tickets automáticos de "cashout Pix out – auto" que não entram no volume humano.
🔗 https://sites.google.com/recargapay.com/voc/
🔗 CXM - Briefing de Suporte: https://optimus.recargapay.com/PHP/dashboard_view.php?id=246
💬 Comentários e ajustes nesta thread — a versão final validada será publicada em #cx_fraud após a revisão do time.

**Thread 1 — Report**
**RESUMO DO MÊS**
• **1.603 contatos** vs 1.378 em agosto (**+16%**), média 55/dia (agosto: 48).

**EVOLUÇÃO SEMANA A SEMANA** (contatos/dia)
ago: 48 | S1: 60 | S2: 52 | S3: 58 | S4: 52 | S5 (parcial): 53
Leitura: patamar estável, ligeiramente acima de agosto.

**EVENTOS E IMPACTOS**
• Relatório diário de desvios (#lideres-cx-e-cxm): "cashout por Pix out – auto" em conta desativada chegou a 890 tickets em 28/09 (+532%) e 1.258 em 29/09 (+852%). São tickets automáticos, sem impacto no atendimento humano.
• 25/09: novas mensagens para conta encerrada com botão "Solicitar devolução" para quem tem saldo (#account_cx).
• 25/09: bloqueios de Pix In por regra de documento em blocklist; regra desligada pela engenharia, religação em avaliação (#escalation_incidents).
• 25/09 e 28/09: ver "Alertas" para impacto em outubro.

**SATISFAÇÃO DO CLIENTE**
• CSAT N1: agosto **37,7%** → 01–13/09 **40,9%** → 14–29/09 **37,9%** (meta 80%). Base de 22 e 29 respostas: indicativo.

**DESTAQUES E OPORTUNIDADES**
• Fluxo para esclarecer encerramento (treinamento de resposta "Encerramento de conta", prazo 13/10) é uma oportunidade direta para CSAT: 3 em cada 4 clientes que contatam sobre encerramento chegam frustrados por não entender o que aconteceu com saldo, Pix e fatura.

**Thread 2 — Alertas**
🚨 **ALERTAS — Conta Desativada · Setembro/2026 (01–29/09)**

🔴 **CSAT N1 abaixo do piso**
Observado: **37,9%** (14–29/09) | Esperado: ≥75%
Persistente desde agosto (37,7%); base pequena.

🔴 **Risco de volume: religação da regra de Pix In**
Observado: regra desligada em 25/09, religação em avaliação | Esperado: sem religação
Se religada sem comunicação, pode gerar contatos de saldo bloqueado.

✅ Volume humano estável no mês.

---

## 4. Carteira Desativada → #cx_fraud

**Raiz**
<!here> 📊 **[RASCUNHO → #cx_fraud] Report de VoC - Carteira Desativada — Setembro/2026 (01–29/09)**

2.226 contatos (+26% vs agosto). Pico no início do mês (87/dia em S1) por ajustes de regras antifraude (RC6, desde 27/08), queda até 60/dia em S4 e rebote em S5 (84/dia). CSAT N1 em 48–53%, bem abaixo do piso.
🔗 https://sites.google.com/recargapay.com/voc/
🔗 CXM - Briefing de Suporte: https://optimus.recargapay.com/PHP/dashboard_view.php?id=246
💬 Comentários e ajustes nesta thread — a versão final validada será publicada em #cx_fraud após a revisão do time.

**Thread 1 — Report**
**RESUMO DO MÊS**
• **2.226 contatos** vs 1.769 em agosto (**+26%**), média 77/dia (agosto: 61).

**EVOLUÇÃO SEMANA A SEMANA** (contatos/dia)
ago: 61 | S1: **87** | S2: 75 | S3: 85 | S4: **60** | S5 (parcial): 84

**EVENTOS E IMPACTOS**
• 09/09 (#cx_fraud): após o ajuste de regras RC6, que atinge contas PF com participação societária em empresas, subiu "saldo da carteira bloqueado – todo o saldo"; patamar de ~70 contatos/dia desde 27/08; expectativa de alta temporária porque a regra cobre base antes nunca afetada.
• Relatório semanal (S36): 91,8% dos contatos eram de saldo bloqueado; revisão manual COPS +80%; Movimentações Financeiras caiu 38% no mesmo período, possivelmente por migração de classificação para Carteira Desativada.
• Leitura empresa: "saldo da carteira bloqueado" 72 → 60 → 61 → **39** → 61/dia (agosto: 42).

**SATISFAÇÃO DO CLIENTE**
• CSAT N1: agosto **61,0%** → 01–13/09 **53,1%** → 14–29/09 **47,6%** (meta 80%). Base de 32 e 21 respostas: indicativo.

**Thread 2 — Alertas**
🚨 **ALERTAS — Carteira Desativada · Setembro/2026 (01–29/09)**

🔴 **CSAT N1 abaixo do piso e em queda**
Observado: **47,6%** (14–29/09) | Esperado: ≥75%
Piora ao longo do mês; base pequena.

🔴 **Volume +26% vs agosto**
Observado: **2.226** | Esperado: 1.769 (agosto)
Coincide com a regra RC6. Parte do aumento pode vir de reclassificação de Movimentações Financeiras.

---

## 5. Chargeback Recovery → #cx_fraud

**Raiz**
<!here> 📊 **[RASCUNHO → #cx_fraud] Report de VoC - Chargeback Recovery — Setembro/2026 (01–29/09)**

1.202 contatos (−2% vs agosto), estáveis em ~40–46/dia. CSAT N1 em ~53%, abaixo do piso. Sem evento específico do produto nos canais.
🔗 https://sites.google.com/recargapay.com/voc/
🔗 CXM - Briefing de Suporte: https://optimus.recargapay.com/PHP/dashboard_view.php?id=246
💬 Comentários e ajustes nesta thread — a versão final validada será publicada em #cx_fraud após a revisão do time.

**Thread 1 — Report**
**RESUMO DO MÊS**
• **1.202 contatos** vs 1.221 em agosto (**−2%**), média 41/dia (agosto: 42).

**EVOLUÇÃO SEMANA A SEMANA** (contatos/dia)
ago: 42 | S1: 42 | S2: 39 | S3: 43 | S4: 40 | S5 (parcial): 46

**EVENTOS E IMPACTOS**
• Nenhum evento específico do produto nos canais em setembro. Na empresa toda, causas de chargeback ("cbk devido") seguem estáveis em ~16/dia.

**SATISFAÇÃO DO CLIENTE**
• CSAT N1: agosto **60,7%** → 01–13/09 **53,8%** → 14–29/09 **52,8%** (meta 80%). Base de 39 e 36 respostas: indicativo.

**Thread 2 — Alertas**
🚨 **ALERTAS — Chargeback Recovery · Setembro/2026 (01–29/09)**

🔴 **CSAT N1 abaixo do piso**
Observado: **52,8%** (14–29/09) | Esperado: ≥75%
Queda de ~8 p.p. vs agosto; base pequena.

✅ Volume dentro do padrão.

---

## 6. CDB → #investments-e-cx

**Raiz**
<!here> 📊 **[RASCUNHO → #investments-e-cx] Report de VoC - CDB — Setembro/2026 (01–29/09)**

1.249 contatos (−15% vs agosto), estáveis em ~44/dia desde S2. NPS Tx subiu de 61 para 68 na 2ª quinzena; CSAT N1 oscila em torno de 70–76%. Mudança de produto em 14/09 (teto de R$ 10 mil no CDB 107%) não provocou aumento de volume até 29/09.
🔗 https://sites.google.com/recargapay.com/voc/
🔗 CXM - Briefing de Suporte: https://optimus.recargapay.com/PHP/dashboard_view.php?id=246
💬 Comentários e ajustes nesta thread — a versão final validada será publicada em #investments-e-cx após a revisão do time.

**Thread 1 — Report**
**RESUMO DO MÊS**
• **1.249 contatos** vs 1.465 em agosto (**−15%**), média 43/dia (agosto: 51).

**EVOLUÇÃO SEMANA A SEMANA** (contatos/dia)
ago: 51 | S1: 38 | S2: 44 | S3: 44 | S4: 44 | S5 (parcial): 50
Leitura: abaixo de agosto, estável depois da 1ª semana; S5 volta a ~50 (2 dias).

**EVENTOS E IMPACTOS**
• 04/09: mudança de faixas de CDB anunciada (#investments-e-cx).
• 14/09: teto de R$ 10 mil por conta no CDB 107% e novo CDB 12 meses a 103% do CDI sem limite; **a partir de 01/10** o reinvestimento automático do 107% fica limitado a R$ 10 mil e o excedente volta ao saldo.
• 23/09: 50% dos usuários com mínimos reduzidos (Platinum R$ 1,5 mil, Titan R$ 15 mil) em teste A/B (#cc-produto-e-cx).
• 21/09: lentidão no resgate (Matera OpenMarket) de 29 min. 11/09: dificuldade para investir por 25 min.
• Resgate de CDB antes do vencimento: **+287%** em 26–27/09 (10 vs 3,5 por dia, relatório diário de desvios); causa "solicita resgate antecipado" 95–109 por faixa semanal nas semanas finais.

**SATISFAÇÃO DO CLIENTE**
• NPS Tx: agosto 61,6 → 01–13/09 **61,2** → 14–29/09 **67,6** (meta 75).
• CSAT N1: agosto 75,0% → **67,7%** → **76,1%** (meta 80%). Base de 31 e 46 respostas: indicativo.

**DESTAQUES E OPORTUNIDADES**
• Preparar comunicação do limite de R$ 10 mil de reinvestimento antes de 01/10 (excedente voltará ao saldo).

**Thread 2 — Alertas**
🚨 **ALERTAS — CDB · Setembro/2026 (01–29/09)**

🔴 **Risco para outubro: reinvestimento limitado em 01/10**
Observado: regra vigente a partir de 01/10 | Esperado: sem aumento de contatos
Clientes com saldo acima de R$ 10 mil verão o excedente retornar ao saldo.

✅ NPS em alta; CSAT recuperando na 2ª quinzena.

---

## 7. Rendimento CDI → #investments-e-cx

**Raiz**
<!here> 📊 **[RASCUNHO → #investments-e-cx] Report de VoC - Rendimento CDI — Setembro/2026 (01–29/09)**

Volume muito baixo (a vertical é agregada a cashback): 59 contatos no grupo "cashback e rendimento" (agosto: 92). Amostra pequena; sem tendência confiável.
🔗 https://sites.google.com/recargapay.com/voc/
🔗 CXM - Briefing de Suporte: https://optimus.recargapay.com/PHP/dashboard_view.php?id=246
💬 Comentários e ajustes nesta thread — a versão final validada será publicada em #investments-e-cx após a revisão do time.

**Thread 1 — Report**
**RESUMO DO MÊS**
• Grupo "cashback e rendimento": **59 contatos** vs 92 em agosto. Rendimento CDI isolado: 5 tickets na semana de 31/08–06/09 (relatório S36); o restante do mês exige a separação por vertical.

**EVOLUÇÃO SEMANA A SEMANA** (grupo, contatos/dia)
ago: 3,2 | S1: 1,3 | S2: 2,3 | S3: 2,7 | S4: 1,7 | S5 (parcial): 2,0

**EVENTOS E IMPACTOS**
• INC aberto de cancelamento de ordem sem repasse de valor (Rendimento/Itaú): 2 INCs, o mais antigo com 32 dias em 11/09 (#melhoria-continua-verticais).
• Bug de resgate do CDB Titan (19/08) não gerou novos tickets.

**Thread 2 — Alertas**
🚨 **ALERTAS — Rendimento CDI · Setembro/2026 (01–29/09)**

✅ Todos os indicadores dentro do padrão neste mês (amostra pequena).

---

## 8. Movimentações Financeiras → #investments-e-cx

**Raiz**
<!here> 📊 **[RASCUNHO → #investments-e-cx] Report de VoC - Movimentações Financeiras — Setembro/2026 (01–29/09)**

570 contatos (−17% vs agosto), mas com tendência de alta ao longo do mês (16/dia em S1 para 21/dia em S4 e 30/dia em S5). A queda inicial pode refletir migração de classificação para Carteira Desativada.
🔗 https://sites.google.com/recargapay.com/voc/
🔗 CXM - Briefing de Suporte: https://optimus.recargapay.com/PHP/dashboard_view.php?id=246
💬 Comentários e ajustes nesta thread — a versão final validada será publicada em #investments-e-cx após a revisão do time.

**Thread 1 — Report**
**RESUMO DO MÊS**
• **570 contatos** vs 690 em agosto (**−17%**), média 20/dia (agosto: 24).

**EVOLUÇÃO SEMANA A SEMANA** (contatos/dia)
ago: 24 | S1: 16 | S2: 19 | S3: 20 | S4: 21 | S5 (parcial): **30**
Leitura: subida contínua a cada faixa; S5 é preliminar (2 dias).

**EVENTOS E IMPACTOS**
• S36: −38% WoW, possível migração de classificação para Carteira Desativada (#cc-produto-e-cx).
• Relatório diário de desvios: "acesso ao extrato" +460% em 25/09 (12 vs 3).

**DESTAQUES E OPORTUNIDADES**
• Monitorar a tendência de alta nos últimos dias e validar se a classificação voltou ao normal.

**Thread 2 — Alertas**
🚨 **ALERTAS — Movimentações Financeiras · Setembro/2026 (01–29/09)**

🔴 **Tendência de alta**
Observado: **30/dia** (S5, 2 dias) | Esperado: 16–21/dia em S1–S4
Leitura preliminar.

---

## 9. Transporte → #melhoria-continua-verticais

**Raiz**
<!here> 📊 **[RASCUNHO → #melhoria-continua-verticais] Report de VoC - Transporte — Setembro/2026 (01–29/09)**

885 contatos (+13% vs agosto), com pico em 07–13/09 (40/dia contra 24 em S1) e queda até 26/dia em S4. NPS Tx em 78–80 (meta 75). CSAT N1 caiu de 84,5% para ~58–61% (base de ~30 respostas). Vários alertas de recarga em São Paulo ao longo do mês.
🔗 https://sites.google.com/recargapay.com/voc/
🔗 CXM - Briefing de Suporte: https://optimus.recargapay.com/PHP/dashboard_view.php?id=246
💬 Comentários e ajustes nesta thread — a versão final validada será publicada em #melhoria-continua-verticais após a revisão do time.

**Thread 1 — Report**
**RESUMO DO MÊS**
• **885 contatos** vs 783 em agosto (**+13%**), média 31/dia (agosto: 27).

**EVOLUÇÃO SEMANA A SEMANA** (contatos/dia)
ago: 27 | S1: 24 | S2: **40** | S3: 31 | S4: 26 | S5 (parcial): 30

**EVENTOS E IMPACTOS**
• 10/09 15:20–16:16: alerta de recarga em São Paulo (7 atendimentos humanos N1; recargas pagas e não creditadas imediatamente, em análise com o parceiro); relatos de Curitiba e Mogi das Cruzes fora do escopo do aviso. A métrica oficial de retenção do bot marcou 0 sessões, embora a transcrição mostre o aviso exibido.
• 13/09 (00:23–06:22), 17/09 (15:53–16:49) e 19–20/09 (~24h): novos alertas em São Paulo. 01/09: alerta em Campinas (14 min).
• 14/09: recarga de transporte sem crédito: 24 vs 7 por dia, com "não recebeu a venda" em Tap to Pay e Link no mesmo dia (indício de instabilidade ampla; causa não mapeada).
• 01–11/09: INCs abertos há mais de 5 dias (comprovante de pagamento indisponível, o mais antigo com 45 dias).
• Principal motivo no relatório S36: crédito não disponibilizado após validação (Bilhete Único).

**SATISFAÇÃO DO CLIENTE**
• NPS Tx: agosto 79,2 → 01–13/09 **80,2** → 14–29/09 **77,7** (meta 75).
• CSAT N1: agosto 84,5% → **60,7%** → **58,1%** (meta 80%). Base de 28 e 31 respostas: indicativo.

**Thread 2 — Alertas**
🚨 **ALERTAS — Transporte · Setembro/2026 (01–29/09)**

🔴 **CSAT N1 abaixo do piso**
Observado: **58,1%** (14–29/09) | Esperado: ≥75%
Queda de ~26 p.p. vs agosto; base pequena; coincide com os alertas de recarga em SP.

✅ NPS Tx acima da meta.

---

## 10. Contas e Boletos → #melhoria-continua-verticais

**Raiz**
<!here> 📊 **[RASCUNHO → #melhoria-continua-verticais] Report de VoC - Contas e Boletos — Setembro/2026 (01–29/09)**

Grupo "utilities" (Contas e Boletos + Boleto de Cobrança): 455 contatos (+23% vs agosto), concentrados no início (23/dia em S1) e em queda até 13–14/dia. A instabilidade geral de 03–04/09 e o problema de pagamento de boleto de 03/09 explicam o pico inicial. Não foi possível separar os dois produtos nesta rodada.
🔗 https://sites.google.com/recargapay.com/voc/
🔗 CXM - Briefing de Suporte: https://optimus.recargapay.com/PHP/dashboard_view.php?id=246
💬 Comentários e ajustes nesta thread — a versão final validada será publicada em #melhoria-continua-verticais após a revisão do time.

**Thread 1 — Report**
**RESUMO DO MÊS**
• Grupo "utilities": **455 contatos** vs 369 em agosto (**+23%**), média 16/dia (agosto: 13).

**EVOLUÇÃO SEMANA A SEMANA** (grupo, contatos/dia)
ago: 13 | S1: **23** | S2: 15 | S3: 14 | S4: 13 | S5 (parcial): 15

**EVENTOS E IMPACTOS**
• 03/09 13:35–~15:49: ~12 clientes PJ não conseguiam pagar boleto (tela adicional), causa não identificada (#escalation_incidents).
• 03–04/09: instabilidade geral do app; Contas e Boletos teve 116 tickets na S36 (+214% WoW), 66 só em 03/09.
• 16/09: automação do bloqueio preventivo de fraude em boleto (desde 13/08): 1.923 tickets, 469 contas, ~R$ 730 mil retidos.
• Efeito acumulado: o volume retornou ao patamar de agosto na S4 (13/dia).

**Thread 2 — Alertas**
🚨 **ALERTAS — Contas e Boletos · Setembro/2026 (01–29/09)**

🔴 **Pico no início do mês**
Observado: **23/dia** (S1) | Esperado: 13/dia (agosto)
Coincide com a instabilidade de 03–04/09 e o problema de boleto PJ; normalizado depois.

✅ Volume em S4 dentro do padrão.

---

## 11. Boleto de Cobrança → #melhoria-continua-verticais

**Raiz**
<!here> 📊 **[RASCUNHO → #melhoria-continua-verticais] Report de VoC - Boleto de Cobrança — Setembro/2026 (01–29/09)**

Volume baixo (21 tickets na semana de 31/08–06/09, contra 8 antes), com dúvidas de lojistas PJ sobre emissão e recebimento. Não foi possível isolar o produto do grupo "utilities" nesta rodada.
🔗 https://sites.google.com/recargapay.com/voc/
🔗 CXM - Briefing de Suporte: https://optimus.recargapay.com/PHP/dashboard_view.php?id=246
💬 Comentários e ajustes nesta thread — a versão final validada será publicada em #melhoria-continua-verticais após a revisão do time.

**Thread 1 — Report**
**RESUMO DO MÊS**
• Relatório S36: **21 tickets** (8 na semana anterior); tema principal: dúvidas de lojistas PJ.

**EVENTOS E IMPACTOS**
• 03/09: boleto não pago por ~12 clientes PJ (tela adicional), ~2h (#escalation_incidents).
• 16/09: automação de bloqueio preventivo de fraude em boleto (1.923 tickets, 469 contas bloqueadas, ~R$ 730 mil retidos, 256 h/mês economizadas).

**Thread 2 — Alertas**
🚨 **ALERTAS — Boleto de Cobrança · Setembro/2026 (01–29/09)**

✅ Todos os indicadores dentro do padrão neste mês (amostra pequena).

---

## 12. Recarga de Celular → #melhoria-continua-verticais

**Raiz**
<!here> 📊 **[RASCUNHO → #melhoria-continua-verticais] Report de VoC - Recarga de Celular — Setembro/2026 (01–29/09)**

Volume muito baixo: 72 contatos (+31% vs agosto, base de 55). NPS 78 na primeira semana. Amostra pequena; sem tendência confiável.
🔗 https://sites.google.com/recargapay.com/voc/
🔗 CXM - Briefing de Suporte: https://optimus.recargapay.com/PHP/dashboard_view.php?id=246
💬 Comentários e ajustes nesta thread — a versão final validada será publicada em #melhoria-continua-verticais após a revisão do time.

**Thread 1 — Report**
**RESUMO DO MÊS**
• **72 contatos** vs 55 em agosto (**+31%**), média 2,5/dia (agosto: 1,9).

**EVOLUÇÃO SEMANA A SEMANA** (contatos/dia)
ago: 1,9 | S1: 2,7 | S2: 1,9 | S3: 2,9 | S4: 2,0 | S5 (parcial): 4,5

**EVENTOS E IMPACTOS**
• Dúvida recorrente: "recarga realizada e crédito não disponibilizado" (+ de 300 em agosto na empresa toda; 316 em causas "validei meus créditos mas a recarga não caiu" no mês, segundo ranking empresa).

**Thread 2 — Alertas**
🚨 **ALERTAS — Recarga de Celular · Setembro/2026 (01–29/09)**

✅ Todos os indicadores dentro do padrão neste mês (amostra pequena).

---

## 13. Pix → #pixcc-home-raf-cx

**Raiz**
<!here> 📊 **[RASCUNHO → #pixcc-home-raf-cx] Report de VoC - Pix — Setembro/2026 (01–29/09)**

5.152 contatos (+1% vs agosto), com pico em 07–13/09 (206/dia) e queda até 142/dia em 28–29/09. Mês marcado por incidentes: 03–04/09, 08/09 (P1), 10/09 (Pix Out, 19,4 mil pagamentos recusados) e 21/09 (P1). NPS Tx 70–71,5 (meta 75); CSAT N1 71–73%.
🔗 https://sites.google.com/recargapay.com/voc/
🔗 CXM - Briefing de Suporte: https://optimus.recargapay.com/PHP/dashboard_view.php?id=246
💬 Comentários e ajustes nesta thread — a versão final validada será publicada em #pixcc-home-raf-cx após a revisão do time.

**Thread 1 — Report**
**RESUMO DO MÊS**
• **5.152 contatos** vs 5.120 em agosto (**+1%**), média 178/dia (agosto: 177).

**EVOLUÇÃO SEMANA A SEMANA** (contatos/dia)
ago: 177 | S1: 183 | S2: **206** | S3: 173 | S4: 159 | S5 (parcial): 142

**EVOLUÇÃO DOS TEMAS** (empresa toda)
• **Problema com transação Pix:** 30 → 34 → **19** → 24 → 21/dia (pico na 2ª semana, depois cede).
• **"Não consegue realizar o Pix":** 35 → **43** → 34 → 26 → 25/dia (agosto: 43); 1.261 em agosto → 975 no mês.
• Novos temas emergentes nos relatórios diários: cadastro/exclusão de chave Pix (22/09 e 23/09), acesso ao extrato (+460% em 25/09), "ccerror empty message" (+106% em 26–27/09; 24 vs 8,5 em 28/09).

**EVENTOS E IMPACTOS**
• 03/09 20:24–20:59: queda de Pix envio/recebimento. 04/09 12:58–~14:49 (~3h20 de alerta): erros no checkout do Pix Out; deploy revertido; causa final inconclusiva. CSAT N1 do Pix em 65,3% e "problema com transação Pix" +42% WoW na S36.
• **08/09 14:03: plataforma inteira fora (P1)**, alertas de Pix até 14:38.
• **10/09 00:09–03:28: queda do Pix Out** (BAD_GATEWAY/timeouts, possível problema na adquirente REDE): 19,4 mil pagamentos recusados (10,2 mil clientes, R$ 1,9 mi), 170 contatos (144 humanos N1), absorção −5,8 p.p.; aviso no app desativado às 02:08, ~1h20 antes da resolução. 11/09: correção do QR Code sem casos novos.
• **21/09 16:52–~18:03: queda P1 de Pix** (envio, recebimento, DICT; locks no banco). 22/09: sem conciliação com o banco parceiro desde 18:00. 23/09: migração da base do Pix (alertas 01:26–05:37 contra janela planejada de 01:00–03:00).
• 25/09: bloqueio de Pix In por regra de documento em blocklist (regra desligada; religação em avaliação). 28/09: pergunta em aberto sobre a MP das bets.
• Efeito acumulado: o volume cede em S4 e S5 apesar de 21/09 (P1); a conciliação e a religação da regra são riscos para outubro.

**SATISFAÇÃO DO CLIENTE**
• NPS Tx: agosto 70,0 → 01–13/09 **70,7** → 14–29/09 **71,5** (meta 75).
• CSAT N1: agosto 71,3% → **64,5%** → **72,9%** (meta 80%): recuperou na 2ª quinzena, mas ainda abaixo do piso de 75%.

**DESTAQUES E OPORTUNIDADES**
• Aviso no app durante incidentes: manter até a resolução total (10/09 foi desligado 1h20 antes).
• Alertas automáticos do RecargaBot não dispararam em 09/09, 10/09 (0 sessões) e 16/09.
• Atendimento personalizado em Pix está previsto para setembro (retenção +8 p.p., segundo o relatório executivo).

**Thread 2 — Alertas**
🚨 **ALERTAS — Pix · Setembro/2026 (01–29/09)**

🔴 **CSAT N1 abaixo do piso**
Observado: **72,9%** (14–29/09) e **64,5%** (01–13/09) | Esperado: ≥75%
Coincide com os incidentes de 03–04/09, 08/09 e 10/09.

🔴 **Incidentes de Pix com impacto financeiro**
Observado: 19,4 mil pagamentos recusados (R$ 1,9 mi) em 10/09; P1 em 08/09 e 21/09 | Esperado: sem queda
Aviso de app e alertas do bot falharam em parte dos casos.

✅ NPS Tx estável. ✅ Volume em queda de S2 a S5.

---

## 14. Pix CC → #pixcc-home-raf-cx

**Raiz**
<!here> 📊 **[RASCUNHO → #pixcc-home-raf-cx] Report de VoC - Pix CC — Setembro/2026 (01–29/09)**

Única leitura disponível: 108 tickets na semana de 31/08–06/09 (−45% WoW, a maior queda da série de 5 semanas), com fricção na aprovação pelo cartão (recusa, erro técnico, limite, KYC). A partir de 09/09 o empréstimo passou a cair no cartão (+5 p.p. de uso de Pix com cartão). Sem série mensal por produto nesta rodada.
🔗 https://sites.google.com/recargapay.com/voc/
🔗 CXM - Briefing de Suporte: https://optimus.recargapay.com/PHP/dashboard_view.php?id=246
💬 Comentários e ajustes nesta thread — a versão final validada será publicada em #pixcc-home-raf-cx após a revisão do time.

**Thread 1 — Report**
**EVENTOS E IMPACTOS**
• 09/09: o valor do empréstimo passou a cair no cartão de crédito; +5 p.p. de uso de Pix com cartão e queda equivalente nos saques.
• 14–16/09: aumento de "problemas com uso do cartão" (60 vs 13,5) e "resgate de saldo garantido" (60 vs 18,5) em 15/09.
• 23/09: CAP de parcelamento para 19 mil clientes de alto risco; push na recusa.
• Pix com cartão aparece em depoimentos do Dia do Cliente (15/09) com notas 9–10.
• "ccerror empty message" no Pix: 589 contatos no mês (empresa) e +106% em 26–27/09.

**Thread 2 — Alertas**
🚨 **ALERTAS — Pix CC · Setembro/2026 (01–29/09)**

✅ Sem alerta confirmável com os dados disponíveis (série mensal por produto pendente).

---

## 15. RAF → #pixcc-home-raf-cx

**Raiz**
<!here> 📊 **[RASCUNHO → #pixcc-home-raf-cx] Report de VoC - RAF — Setembro/2026 (01–29/09)**

Volume mínimo: 22 contatos no mês (agosto: 106; −79%), em patamar de menos de 1 por dia desde o fim do bônus "Indique e Ganhe" (~12/08). Todos do lado Indicador na semana de 31/08–06/09.
🔗 https://sites.google.com/recargapay.com/voc/
🔗 CXM - Briefing de Suporte: https://optimus.recargapay.com/PHP/dashboard_view.php?id=246
💬 Comentários e ajustes nesta thread — a versão final validada será publicada em #pixcc-home-raf-cx após a revisão do time.

**Thread 1 — Report**
**RESUMO DO MÊS**
• **22 contatos** (agosto: 106). Média: 0,8/dia (agosto: 3,7).

**EVOLUÇÃO SEMANA A SEMANA** (contatos/dia)
ago: 3,7 | S1: 1,2 | S2: 0,7 | S3: 0,6 | S4: 0,9 | S5 (parcial): 0

**EVENTOS E IMPACTOS**
• Fim do bônus "Indique e Ganhe" (~12/08) explica o patamar baixo; 100% dos contatos do lado Indicador na S36.

**Thread 2 — Alertas**
🚨 **ALERTAS — RAF · Setembro/2026 (01–29/09)**

✅ Todos os indicadores dentro do padrão neste mês (amostra pequena).

---

## 16. Empréstimo → #squad_loan_seguimento

**Raiz**
<!here> 📊 **[RASCUNHO → #squad_loan_seguimento] Report de VoC - Empréstimo — Setembro/2026 (01–29/09)**

5.016 contatos (−5% vs agosto), com consignado (309, −11%) à parte. Volume cai de 204/dia (S1) para 158/dia (S4), mas o mês foi marcado por cinco quedas da Matera (01, 09, 15, 24 e 29/09) e pela mudança de 09/09 que fez o valor cair no cartão de crédito. NPS Tx 70,5 (meta 75); CSAT N1 ~77%.
🔗 https://sites.google.com/recargapay.com/voc/
🔗 CXM - Briefing de Suporte: https://optimus.recargapay.com/PHP/dashboard_view.php?id=246
💬 Comentários e ajustes nesta thread — a versão final validada será publicada em #squad_loan_seguimento após a revisão do time.

**Thread 1 — Report**
**RESUMO DO MÊS**
• **5.016 contatos** vs 5.256 em agosto (**−5%**), média 173/dia (agosto: 181). Consignado: 309 vs 347 (−11%), média 10,7/dia.

**EVOLUÇÃO SEMANA A SEMANA** (contatos/dia)
Empréstimo — ago: 181 | S1: **204** | S2: 169 | S3: 166 | S4: 158 | S5 (parcial): 171
Consignado — ago: 12 | S1: 12 | S2: 10 | S3: 10 | S4: 11 | S5: 8,5

**EVOLUÇÃO DOS TEMAS** (empresa toda)
• **Como resgatar o saldo do empréstimo:** 28 → 24 → 26 → 20 → 17/dia (cedendo desde a mudança de 09/09).
• **Não consegue contratar:** 46 → 39 → 43 → 34 → 46/dia (sensível às quedas da Matera).
• **"Discorda do limite"**: +241% em 18/09 e +237% em 26–27/09 (21 vs 8). Tem relação com o erro da Serasa (~3 mil clientes) e reclamações de limite baixo (R$ 10) nas lojas de aplicativo.
• **Cancelar empréstimo:** +108% em 21/09 (25 vs 12,5).
• **Instabilidade no app:** 27 → 20 → 3 → 12 → 8/dia.

**EVENTOS E IMPACTOS**
• 31/08–01/09: virada da Matera travou por ≥9h45; contratação indisponível; "instabilidade no app" foi de 4 para 73 tickets (S36: 1.325 contatos, +21,7% WoW).
• 04/09 (05:54–07:01) e 05/09 (05:24–06:41): alertas na virada.
• **09/09: virada de 15h17** (08/09 22:37 → 09/09 13:54), 105 contatos humanos, 42% citando bloqueio; absorção 95,1%; alerta do bot não disparou. No mesmo dia o valor do empréstimo passou a cair no cartão para 100% dos clientes.
• 15/09 (21 min, 20 contatos, falso positivo) e 16/09 (manutenção 21:00–00:21, 151 contatos, retenção do bot 27,8%).
• ~até 16/09: erro de integração com a Serasa (R$ 10/20 exibidos como R$ 1.000 para ~3 mil clientes; 20 tickets, 7 ReclameAqui, 2 Consumidor.gov); corrigido.
• 18/09: pagamento com 4 janelas intermitentes (01:09–06:08). 21/09: ajuste do bot com CTAs e artigos (8 de Empréstimo, 1 de Consignado).
• **24/09: virada da Matera ~8h14** após migração de servidores (contratação, negociação e pagamento indisponíveis). **29/09: indisponibilidade de 4h30.** 30/09 (fora do período): P1 de ~15 min por migration mal aplicada.
• Efeito acumulado: o volume cai ao longo do mês, mas S5 já mostra alta (171/dia) após a queda de 29/09.

**SATISFAÇÃO DO CLIENTE**
• NPS Tx: agosto 68,0 → 01–13/09 **70,5** → 14–29/09 **70,6** (meta 75).
• CSAT N1: agosto 75,9% → 76,7% → **77,5%** (meta 80%).

**DESTAQUES E OPORTUNIDADES**
• Reforço do alerta automático do RecargaBot durante viradas (falhou em 09/09 e 16/09).
• Pesquisa de motivação de contratação por faixa (R$ 10, >R$ 200, >R$ 1.000) concluída em 24/09.
• Avaliações de app store com "limite de R$ 10", "taxas altas" e "não consigo liberar empréstimo" aparecem como tickets sem motivo.

**Thread 2 — Alertas**
🚨 **ALERTAS — Empréstimo · Setembro/2026 (01–29/09)**

🔴 **Instabilidades recorrentes da Matera**
Observado: 5 quedas em 29 dias (01, 09, 15, 24 e 29/09), a maior de 15h17 | Esperado: sem indisponibilidade
Cada queda coincide com picos de "não consegue contratar" e "instabilidade no app".

🔴 **"Discorda do limite" em alta**
Observado: +241% (18/09) e +237% (26–27/09) | Esperado: 8/dia
Relacionado ao erro da Serasa e ao limite de R$ 10.

✅ NPS e CSAT dentro do padrão. ✅ Volume em queda.

---

## 17. Tap to Pay → #subacquirer-cx

**Raiz**
<!here> 📊 **[RASCUNHO → #subacquirer-cx] Report de VoC - Tap to Pay — Setembro/2026 (01–29/09)**

**1.081 contatos (+41% vs agosto)**, com pico em S3 (49/dia, 14–20/09, contra 22 em S1) e patamar de ~38/dia nas faixas seguintes. NPS Tx 85,6 → 79,8 (meta 75). Incidentes: Android 22–23/09 (~29h; 853 comerciantes bloqueados) e atrasos de repasse em 07, 08, 10, 24 e 28/09. Novo tema: venda virando limite do Cartão Empreendedor.
🔗 https://sites.google.com/recargapay.com/voc/
🔗 CXM - Briefing de Suporte: https://optimus.recargapay.com/PHP/dashboard_view.php?id=246
💬 Comentários e ajustes nesta thread — a versão final validada será publicada em #subacquirer-cx após a revisão do time.

**Thread 1 — Report**
**RESUMO DO MÊS**
• **1.081 contatos** vs 765 em agosto (**+41%**), média 37/dia (agosto: 26).

**EVOLUÇÃO SEMANA A SEMANA** (contatos/dia)
ago: 26 | S1: 22 | S2: 36 | S3: **49** | S4: 39 | S5 (parcial): 38
Leitura: dobrou de S1 para S3 e ficou em patamar alto, sem voltar ao nível de agosto.

**EVOLUÇÃO DOS TEMAS**
• **"Não recebeu a venda":** 12 → 21 → **26** → 15 → 23/dia (agosto: 13). Em 14/09: 33 vs 4 (+446%); em 17/09: 22 vs 9.
• **"Dúvidas de utilização":** 3,5 → 12 → 15 → 12 → 8/dia (agosto: 2).
• **Cartão Empreendedor – resgate de saldo** (causa raiz): 2 → 13 → **20** → 14 → 14/dia. Cliente vendeu pelo Tap to Pay, o valor virou limite garantido do Cartão Empreendedor, ele não esperava e não encontra como transferir para a carteira. Resumos de transcrição (23–24/09): todos com sentimento frustrado, vários pedem para mudar a forma de recebimento.
• **"Não consegue concluir a cobrança":** 19 vs 3 em 23/09 (+762%).

**EVENTOS E IMPACTOS**
• 31/08: liberada a visibilidade de transações rejeitadas; a causa "venda negada" caiu.
• 03/09: novo artigo sobre descredenciamento (Tap to Pay e Link). 08/09: caso de usuário validado sem conseguir usar: precisa informar atividade comercial e faturamento (renovação anual; exigência regulatória; Sub-Acquirer e Accounts corresponsáveis).
• Atrasos de repasse: 07/09 (13:08–14:17), 08/09 (15:01–15:25), **10/09 (00:31–09:45, ~9h)**, 24/09 (17:16–17:40), **28/09 (01:31–10:05, ~8h30)**.
• 14/09: volume humano 1.157 vs ~844 de baseline; "não recebeu a venda" em Tap to Pay e Link no mesmo dia (causa não mapeada).
• **22/09 09:00 → 23/09 ~14:20 (~29h): release Android 5.11.12 quebrou o SDK de cobrança**; nenhuma cobrança concluída; ~853 comerciantes bloqueados, ~52 mil abriram o Tap no build afetado; release pausada 23/09 ~09:33; versão 5.11.13; aviso na Central pedindo reinstalação. Coincide com a S4.
• 23/09 ~09:00: pico de erros (causa: mudança do Core Mobile); normalizado ~09:21.
• **28/09: relatório de CX do Tap to CC / Cartão Empreendedor:** contact rate 1,9% nos usuários com a feature (6 a 9x a média); 56,5% dos tickets são "como acessar o valor"; 17,2% contestam ativação sem consentimento claro; 2,2% escalaram a ReclameAqui, Procon ou Bacen. Propostas: consentimento explícito na venda, jornada de criação do cartão mais simples, push ou in-app após a venda.
• Efeito acumulado: o volume não voltou ao patamar de agosto; o rollout do Tap to CC e as quedas de repasse devem seguir pressionando outubro.

**SATISFAÇÃO DO CLIENTE**
• NPS Tx: agosto 81,3 → 01–13/09 **85,6** → 14–29/09 **79,8** (meta 75).
• CSAT N1: agosto 89,8% → 78,6% → **89,9%** (meta 80%). Base de 42 e 79 respostas: indicativo.

**DESTAQUES E OPORTUNIDADES**
• Consentimento explícito antes de converter a venda em limite do Cartão Empreendedor (evidência: 17,2% de contestação e 2,2% de escalada externa).
• Mensagem proativa durante atrasos de repasse e incidentes de SDK.
• Pergunta aberta (22/09): a classificação de usuários descredenciados continua manual?

**Thread 2 — Alertas**
🚨 **ALERTAS — Tap to Pay · Setembro/2026 (01–29/09)**

🔴 **Volume +41% vs agosto**
Observado: **1.081** (49/dia em S3) | Esperado: 765 (agosto)
Coincide com atrasos de repasse, incidente Android e rollout do Tap to CC.

🔴 **Novo cluster: Cartão Empreendedor / saldo na carteira**
Observado: **20/dia** (S3) | Esperado: ~0 em agosto
2,2% de escalada externa (ReclameAqui, Procon, Bacen) segundo o relatório de 28/09.

🔴 **Incidente Android com impacto de ~29h**
Observado: 853 comerciantes bloqueados | Esperado: sem queda de SDK
Resolvido com 5.11.13; exige atualização do app.

✅ NPS Tx acima da meta. ✅ CSAT N1 recuperado na 2ª quinzena.

---

## 18. Link de Pagamento → #subacquirer-cx

**Raiz**
<!here> 📊 **[RASCUNHO → #subacquirer-cx] Report de VoC - Link de Pagamento — Setembro/2026 (01–29/09)**

425 contatos (+28% vs agosto), com pico em S2 (19/dia) e 13–16/dia depois. NPS Tx abaixo do piso de 55 em todo o período (37,8 em 01–13/09; 47,1 em 14–29/09; agosto 51,7); base de ~100 respostas.
🔗 https://sites.google.com/recargapay.com/voc/
🔗 CXM - Briefing de Suporte: https://optimus.recargapay.com/PHP/dashboard_view.php?id=246
💬 Comentários e ajustes nesta thread — a versão final validada será publicada em #subacquirer-cx após a revisão do time.

**Thread 1 — Report**
**RESUMO DO MÊS**
• **425 contatos** vs 333 em agosto (**+28%**), média 15/dia (agosto: 11).

**EVOLUÇÃO SEMANA A SEMANA** (contatos/dia)
ago: 11 | S1: 10 | S2: **19** | S3: 16 | S4: 13 | S5 (parcial): 15

**EVENTOS E IMPACTOS**
• 03/09: novo artigo de descredenciamento. Relatório S36: 68 atendimentos (−15%), NPS 41,5, CSAT 60%, abaixo do piso em 4 das últimas 5 semanas.
• 14/09: "não recebeu a venda" em Link: 10 vs 1 por dia, junto com Tap to Pay e transporte (indício de instabilidade ampla; causa não mapeada).
• Atrasos de repasse e incidentes do Tap to Pay (10/09, 22–23/09, 28/09) compartilham a mesma squad; sem confirmação de impacto no Link.

**SATISFAÇÃO DO CLIENTE**
• NPS Tx: agosto 51,7 → 01–13/09 **37,8** → 14–29/09 **47,1** (meta 75, piso 55). Base de 98 e 121 respostas: indicativo.
• CSAT N1: ~79–80% no mês (12 e 10 respostas por período; indicativo).

**Thread 2 — Alertas**
🚨 **ALERTAS — Link de Pagamento · Setembro/2026 (01–29/09)**

🔴 **NPS Tx abaixo do piso**
Observado: **47,1** (14–29/09), **37,8** (01–13/09) | Esperado: ≥55
Abaixo do piso em todo o período; recuperação parcial na 2ª quinzena.

🔴 **Volume +28% vs agosto**
Observado: **425** | Esperado: 333 (agosto)
Pico em 07–13/09; coincide com incidente de 14/09.
