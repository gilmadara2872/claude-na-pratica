# Verificação de Erros — Projeto "Claude na Prática" (hub)

Orquestrado por Hermes; análise de código executada pelo Claude Code (via `claude -p`, sem Bash, em chunks) e revisão manual do Hermes. Escopo: `01-luma`, `02-kora`, `03-central`.

## Resumo

- `03-central` (app.py + index.html): vários achados de **alta severidade (XSS)** por interpolação não escapada de dados do Excel em `innerHTML`/atributos; além de índices de coluna fixos nas rotas de escrita e falta de validação/locking.
- `01-luma/gen_ppt.py`: números dos slides estão **hardcoded** em vez de usar os valores lidos da planilha, contrariando a regra "nunca inventar números".
- `02-kora/gen_custos.py`: não foi possível analisar (cota diária esgotada durante a orquestração); revisar manualmente.
- Dashboards (`dashboard_luma.html`, `dashboard_custos.html`, `kora-foods.html`) não foram revisados nesta rodada.

## Findings — 03-central / app.py

| Severidade | Linha | Descrição | Correção sugerida |
|---|---|---|---|
| Alta | 28,32,35 | `KeyError` se colunas "Data"/"Matricula"/"Salario" faltarem em Movimentações/Desligamentos/Colaboradores | Validar cabeçalho e retornar erro controlado |
| Alta | 41,46 | `ValueError` se "Limite para gozo" tiver formato inválido; janela de 60 dias via `toordinal` confusa | Usar `date.fromisoformat` com try/except e cálculo explícito de dias |
| Média | 46 | Status amplo inclui "Concedida"/"Programada" em "vencendo" (`Status != "Realizada"`) | Restringir a "Pendente"/"Programada" conforme regra de negócio |
| Média | 46 | Fronteira `lm == ref`: entra em "vencendo", não em "vencidas" | Definir regra inclusiva de forma explícita |
| Média | 88 | Comparação `row[0].value == mat` sem normalização (acentos/maiúsculas) pode falhar | Normalizar ambos os lados |
| Média | 89,94 | Índices fixos `row[3]`/`row[6]` para cargo/salário e append com 8 posições fixas | Resolver colunas pelo cabeçalho em vez de índice |
| Média | 90 | `float(sal_n)` sem validação causa `ValueError` 500 | Validar entrada antes de converter |
| Média | 102 | `row[7]` para status de Férias fixo, pode estar incorreto | Resolver pelo cabeçalho |
| Média | 103 | `row[6]` para data de início de Férias fixo, risco de erro | Resolver pelo cabeçalho |
| Média | 106 | `cmap` usa `Object.fromEntries` e sobrescreve matrículas duplicadas (último vence) | Detectar duplicatas e avisar |
| Baixa | — | Servidor single-threaded; `wb.save()` não atômico; sem lock/backup | Considerar fila/lock e save atômico (arquivo temporário + rename) |
| Baixa | — | `ref` retornado hardcoded "15/10/2026" em vez de formatar `REF` | Derivar do `REF` |
| Baixa | — | Data de referência fixa hardcoded também no JS (`alerts`, `ranking`) | Injetar `D.ref` |

## Findings — 03-central / index.html

| Severidade | Linha | Descrição | Correção sugerida |
|---|---|---|---|
| Alta | 132-134 | `innerHTML` com `Nome`, `Cargo`, `Matricula`, `Area`, `Gestor`, desligamento, movimentações e férias sem escape — XSS | Escapar ou usar `textContent`/DOM API |
| Alta | 137-138 | `value="${c.Cargo}"` e `value="${c.Salario}"` sem escape em inputs — injeção | Escapar atributos |
| Alta | 118,160,170 | `title="..."` com `Nome`/`nome` sem escape — XSS em tooltip | Escapar |
| Média | 115 | `ranking()` usa data de admissão quando não há promoção, inflando "anos sem promoção" | Usar apenas quem tem movimentação de promoção, ou marcar separadamente |
| Média | 107 | Comparação de data como string (ISO vs. outras formas) pode dar bug lógico | Normalizar para ISO antes de comparar |
| Média | 170 | `AREAS[c.Area]` pode ser `undefined` sem fallback (cor inválida) | Fallback para cor neutra |
| Média | 132 | Data de admissão `undefined` pode aparecer na timeline | Guardar com fallback "—" |
| Baixa | 157 | Valores negativos de `tc` distorcem o gráfico de dispersão | Clamp em 0 |
| Baixa | — | Referência de data fixa pode expirar; acessibilidade (hover-only, sem `aria`, modal sem `role="dialog"`, bolhas sem `tabindex`) | Melhorias de a11y |

## Findings — 01-luma

| Severidade | Arquivo | Descrição | Correção sugerida |
|---|---|---|---|
| Alta | gen_ppt.py | Slides usam números hardcoded (6,8 mi, 2,52 mi, etc.) em vez dos valores lidos da planilha (`fat`, `traf`, `brand`, `novos`) | Substituir literais pelos valores calculados |
| Média | gen_ppt.py | `get_val` usa `label.lower() in row[0].lower()` (substring) — pode casar linha errada | Comparação exata/normalizada |
| Média | gen_ppt.py | `traf`/`brand` ficam `None` se não casarem e não caem no fallback | Aplicar `or` fallback como nos demais |
| Baixa | gen_doc.py | Tabela sem estilo (`Table Grid`) — sem bordas no .docx | `table.style = 'Table Grid'` |
| Baixa | gen_doc.py | Cabeçalho "responsável" (acentuado) vs. chave "responsavel" (só exibição) | Sem impacto funcional |

## Findings — 02-kora

| Severidade | Arquivo | Descrição | Correção sugerida |
|---|---|---|---|
| — | gen_custos.py | Não analisado nesta rodada (cota diária esgotada) | Revisar manualmente: 34 linhas, leitura de `controle_custos_obra.xlsx` |
| — | dashboard_custos.html, kora-foods.html | Não revisados nesta rodada | Revisar XSS e consistência de números |

## Recomendações

1. Priorizar a correção dos XSS em `03-central/index.html` (escape de `Nome`, `Cargo`, etc.).
2. Tornar as rotas `/api/promocao` e `/api/ferias` robustas (validação, resolução de colunas por cabeçalho, lock).
3. Alinhar `gen_ppt.py` aos dados da planilha (sem números inventados).
4. Revisar manualmente `02-kora/gen_custos.py` e os dashboards HTML.
5. Repetir a verificação de `02-kora` e dos dashboards quando a cota diária do modelo for renovada.

Fonte da análise de código: Claude Code (claude 2.0.72 via OpenRouter) em 9 chamadas segmentadas; revisão de consistência e achados adicionais pelo Hermes.


## Findings — 02-kora (revisão manual Hermes)

### gen_custos.py

| Severidade | Descrição | Correção sugerida |
|---|---|---|
| Baixa | Dados hardcoded (7 lançamentos de "Fornecedor A"); fonte real são os recibos/planilhas de apoio | Documentar origem de cada lançamento |
| Baixa | Sem formatação de data/moeda na planilha gerada | Aplicar number_format nas células |
| Baixa | `wb = Workbook()` cria aba "Sheet" renomeada; inofensivo | Usar `Workbook()` direto com title |

### dashboard_custos.html

| Severidade | Descrição | Correção sugerida |
|---|---|---|
| Alta | Números inconsistentes com `controle_custos_obra.xlsx`: "Mão de obra R$ 51.680" mas a soma real é R$ 85.200 | Recalcular a partir da planilha |
| Alta | "Orçado R$ 100.000" é número inventado (não existe no fonte) | Definir orçamento na planilha ou remover |
| Média | Categoria "Reembolso" (R$ 480) ausente do dashboard | Incluir todas as categorias |
| Média | Barra "Mão de obra" com largura 51,68% (deveria ser ~88,68%) | Recalcular percentuais |
| Baixa | CSS `.bar` position absolute faz as barras se sobreporem | Ajustar layout |
| Baixa | `.realized-bar` width 96,08% hardcoded | Calcular dinamicamente |

### kora-foods.html

| Severidade | Descrição | Correção sugerida |
|---|---|---|
| Média | Atributo `placeholder` duplicado no input "quantidade" (segundo ignorado) | Remover duplicata |
| Baixa | Formulário `action="#"` sem backend — não envia nada | Conectar a endpoint ou usar mailto |
| Baixa | Link WhatsApp com número placeholder (5511999999999) | Substituir pelo número real |
| Baixa | Rodapé "© 2024" mas projeto é de 2026 | Atualizar ano |
| Baixa | Ícone do botão WhatsApp não é o logo do WhatsApp | Usar ícone correto |

### dashboard_luma.html

| Severidade | Descrição | Correção sugerida |
|---|---|---|
| Alta | Ano no cabeçalho "Desempenho Comercial • 2024" mas gen_ppt usa 1S 2026 — inconsistência | Alinhar para 2026 |
| Alta | Filtro por serviço não funciona: dropdown usa minúsculas ('assinatura') mas tabela usa capitalizado ('Assinatura') — comparação case-sensitive | Normalizar (toLowerCase em ambos) |
| Média | `receitaMensal: [4.2, 4.5, 5.0, 5.3, 5.8, 6.8]` parece acumulado mas é apresentado como mensal; soma 31,6 ≠ 6,8 | Esclarecer se são acumulados ou corrigir |
| Média | `tabelaDados` faturamentos (3.2+1.8+1.5+2.1+1.2+2.4 = 12,2) não somam aos R$ 6,8M | Alinhar com a planilha |
| Média | `atualizarGauge(dadosLuma.churnRate * 0.8 + 5)` resulta em 12,2 → gauge sempre cheio (vermelho) | Usar score de risco real |
| Média | Dependências externas (Google Fonts + Chart.js CDN) — quebra sem internet | Hospedar localmente ou documentar |
| Baixa | Classes CSS 'alta'/'media'/'baixa' referenciadas mas não definidas — spans de risco sem estilo | Definir as classes |
| Baixa | `riscoPorServico` definido mas não utilizado | Remover ou usar |
| Baixa | `document.getElementById('tráfego')` com ID acentuado — funciona mas incomum | Renomear para 'trafego' |
