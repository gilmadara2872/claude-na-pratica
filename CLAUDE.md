# Claude na Prática — Hub de Projetos

Pasta-mãe com os projetos separados, unidos por um hub.

## Estrutura real

- `index.html`: hub na raiz — 4 cartões com os números-chave e acesso aos sistemas.
- `server.py`: servidor do hub (porta 8000), com cache desativado e threads.
- `private/luma/`: Luma Marketing (Aula 1) — analise_contrato.md, email_imobiliaria.md, Luma_Resultados_1S2026.pptx, Luma_Tarefas_Diretoria.docx, dashboard_luma.html, vendor/ (Chart.js e fonte Inter locais), .claude/skills/identidade-luma/
- `private/kora/`: Cowork Custos Obra (Aula 2) — controle_custos_obra.xlsx, dashboard_custos.html, kora-foods.html
- `private/central/`: Central de Pessoas (Aula 3) — app.py, index.html, CLAUDE.md

## Como rodar

- Hub: `python3 server.py` (da pasta raiz) → http://192.168.15.17:8000
- Central: `python3 app.py` (da pasta `private/central`) → http://192.168.15.17:8765

Os dois servidores escutam apenas em 192.168.15.17.

## Navegação

- O hub abre cada sistema em tela cheia (página própria, sem iframe).
- Cada painel tem uma seta "Voltar" no canto superior esquerdo que retorna ao hub.
- A Central busca os dados nela mesma (porta 8765); o hub serve a página na porta 8000.

## Regras gerais

- Nunca inventar números: a fonte é sempre a planilha do projeto.
- Começar cada projeto antes de ir para o próximo.
- Parceria Hermes coordena + Claude Code executa.

## Regras de negócio da Central (não alterar sem validar com o responsável)

- Data de referência fixa: 15/10/2026.
- Churn/turnover e promoções: ver `private/central/CLAUDE.md`.
- Toda mudança de regra de férias, promoção ou desligamento deve ser aprovada antes de ser implementada.

## Pendências conhecidas

- WhatsApp da Kora Foods está como placeholder (5511999999999) — substituir pelo número real quando disponível.
