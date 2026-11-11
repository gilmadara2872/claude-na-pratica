# Findings Checklist — Central de Pessoas (03-central)

## 1) As 4 abas existem e trocam com `hidden`?

- **Sim.** O HTML define 4 sections com `id` e atributo `hidden`:
  - `#t-início` (padrão, visível ao carregar)
  - `#t-analises`
  - `#t-ese`
  - `#t-gestor`
- A troca é feita pelos botões do navbar (`data-t="inicio"|"analises"|"ese"|"gestor"`), que removem/add o `hidden` via:
  ```js
  ['inicio','analises','ese','gestor'].forEach(t=>$('#t-'+t).hidden=(t!==b.dataset.t))
  ```
- Cada aba carrega seu próprio conteúdo (cards, mapa, análises, simulação, visão do gestor).

## 2) Os IDs c-ativos, c-venc, mapa, precisa, scatter, ese-slider, g-sel existem?

| ID | Elemento | Localização |
|----|----------|-------------|
| `c-ativos` | `<b id="c-ativos">–</b>` | Linha 68 — card "Pessoas ativas" |
| `c-venc` | `<b id="c-venc">–</b>` | Linha 69 — card "Custo férias vencidas" |
| `mapa` | `<div id="mapa" class="mapa"></div>` | Linha 73 — mapa de pessoas por área |
| `precisa` | `<ul class="list" id="precisa"></ul>` | Linha 74 — quem precisa de ação |
| `scatter` | `<svg id="scatter" viewBox="0 0 720 340">` | Linha 79 — gráfico dispersão |
| `ese-slider` | `<input type="range" id="ese-slider" min="0" max="8000" step="100" value="0">` | Linha 85 — slider simulação ESE |
| `g-sel` | `<select id="g-sel" ...>` | Linha 92 — seleção de gestor |

Todos os 7 IDs estão presentes no HTML e são referenciados pelo JavaScript.

## 3) Os endpoints `/api/dados`, `/api/promocao`, `/api/ferias` estão implementados?

- **`/api/dados`** (GET): Carrega os dados do `Pessoas_RH.xlsx` via `_load()` e retorna `{ref, cards, colaboradores, movimentacoes, ferias, desligamentos}`. Lançado na rota `/` e `/index.html`.
- **`/api/promocao`** (POST): Atualiza cargo e salário de um colaborador na planilha e adiciona registro na tabela "Movimentações". Valida se a matrícula existe.
- **`/api/ferias`** (POST): Programa férias de um colaborador (define data de início e muda status de "Pendente" para "Programada").

Todos os três endpoints estão implementados em `app.py` e funcionam com o servidor Python stdlib.

## 4) Alguma dependência externa (CDN Tailwind, Google Fonts) que quebra sem internet?

- **Não.** O HTML não contém nenhuma tag `<link>` para CDNs, fonts externas ou frameworks CSS.
- A tipografia vem da stack nativa do sistema: `font:16px/1.5 system-ui,"Segoe UI",sans-serif`.
- Todo o estilo é injetado via `<style>` inline (CSS puro, variáveis CSS).
- Não há risco de quebra por falta de internet.

## 5) Risco de inventar número?

- **Alto risco se não houver validação cruzada.** As diretrizes do CLAUDE.md (Aula 3) estabelecem regras rigorosas:
  - `"Nunca inventar números: fonte é sempre a planilha do projeto."`
  - `"Confirmar números no navegador: Após gerar qualquer saída numérica ou de data, verificar os valores abrindo o Excel (ou compatível) e conferindo os resultados contra o arquivo Pessoas_RH.xlsx."`
- O sistema lê exclusivamente do `Pessoas_RH.xlsx` (`app.py:XLSX = "03 - Arquivo Apoio - Pessoas_RH.xlsx"`) e todos os cálculos (férias vencidas, custos, contagem de 60 dias, promoções, desligamentos) são derivados dessas linhas de dado.
- **Atenção:** os endpoints `/api/promocao` e `/api/ferias` gravam alterações **diretamente no arquivo Excel**. Se alguém chamar esses endpoints sem dados consistentes ou com valores inventados, a planilha de referência será corrompida. Todos os números apresentados na UI vêm de `D` (dados carregados da planilha) e devem ser conferidos visualmente no Excel após qualquer operação.