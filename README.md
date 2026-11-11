# Claude na Prática — Hub de Projetos

Projeto desenvolvido durante o curso **Claude na Prática**, em parceria com o
Hermes (coordenação) e o Claude Code (execução). O repositório reúne três
módulos didáticos — **Luma Marketing**, **Kora Foods / Cowork** e **Central de
Pessoas** — unidos por um hub local que funciona 100% offline.

> Todos os dados usados nos módulos são **fictícios e didáticos**. Nomes de
> pessoas foram substituídos por nomes fictícios gerados, e nenhum dado real,
> credencial ou chave de API faz parte deste repositório.

---

## Índice

- [Visão geral](#visão-geral)
- [Estrutura do repositório](#estrutura-do-repositório)
- [O que foi construído](#o-que-foi-construído)
- [Stack técnica](#stack-técnica)
- [Como rodar](#como-rodar)
- [Fonte de dados](#fonte-de-dados)
- [Verificação e qualidade](#verificação-e-qualidade)
- [Segurança](#segurança)
- [Autor](#autor)

---

## Visão geral

O projeto é um conjunto de sistemas web locais (sem dependência de internet)
construídos a partir de planilhas de apoio. Cada módulo resolve um problema de
negócio diferente: análise de resultados de marketing, controle de custos de
obra e gestão de pessoas.

O hub na raiz é a porta de entrada: uma página única com os quatro sistemas e
os números-chave de cada um.

---

## Estrutura do repositório

```
.
├── index.html              # Hub — página única com os 4 sistemas
├── server.py               # Servidor do hub (porta 8000)
├── CLAUDE.md               # Diretrizes gerais do projeto
├── VERIFICACAO-ERROS.md    # Relatório de revisão de código (qualidade)
├── private/
│   ├── luma/
│   │   ├── dashboard_luma.html       # Dashboard de resultados (Chart.js offline)
│   │   ├── gen_ppt.py                # Gera a apresentação de resultados (.pptx)
│   │   ├── gen_doc.py                # Gera o documento de tarefas (.docx)
│   │   ├── Luma_Resultados_1S2026.pptx
│   │   ├── Luma_Tarefas_Diretoria.docx
│   │   ├── .claude/skills/identidade-luma/SKILL.md
│   │   └── vendor/                   # Chart.js e fonte Inter locais
│   ├── kora/
│   │   ├── dashboard_custos.html     # Dashboard de custos de obra
│   │   ├── kora-foods.html           # Site institucional + pedidos de orçamento
│   │   ├── gen_custos.py             # Gera a planilha de controle de custos
│   │   ├── controle_custos_obra.xlsx # Fonte de dados (anonimizada)
│   │   └── 03 - Projeto Claude Code - Kora Foods/
│   │       ├── empresa-kora.md
│   │       ├── frontend-design.md
│   │       └── identidade-visual.md
│   └── central/
│       ├── index.html                # Central de Pessoas (interface)
│       ├── app.py                    # API + servidor (porta 8765)
│       ├── CLAUDE.md                 # Regras de negócio da Central
│       ├── REVIEW.md / REVIEW_app.md
│       ├── findings-checklist.md
│       ├── 03 - Arquivo Apoio - Pessoas_RH.xlsx  # Fonte de dados (nomes fictícios)
│       └── 05 - Arquivo Apoio - identidade-visual.md
```

---

## O que foi construído

### Hub (raiz)

- `index.html`: página única com os quatro sistemas, cada um com ícone,
  descrição e número-chave.
- `server.py`: servidor HTTP local com `Cache-Control: no-store` (o navegador
  nunca fica com página velha) e `ThreadingHTTPServer` (uma conexão travada não
  derruba o servidor).
- Navegação em tela cheia: cada painel abre na própria página, sem iframe, e
  tem botão "Voltar" no canto superior esquerdo que retorna ao hub.

### Luma — Dashboard de Resultados (Aula 1)

- Dashboard com dados do 1º semestre de 2026, três gráficos interativos
  (receita mensal, churn por segmento e NPS médio) e tabelas de detalhamento.
- Filtros por serviço e segmento que recalculam todos os gráficos em tempo real.
- 100% offline: Chart.js e a fonte Inter são servidos localmente da pasta
  `vendor/` (sem CDN, sem Google Fonts).
- Geradores de documentação a partir dos dados:
  - `gen_ppt.py` → `Luma_Resultados_1S2026.pptx`
  - `gen_doc.py` → `Luma_Tarefas_Diretoria.docx`
- Análise de contrato de locação (`analise_contrato.md`) e minuta de e-mail
  para a imobiliária (`email_imobiliaria.md`).

### Kora — Custos de Obra (Aula 2)

- `dashboard_custos.html`: painel com o total realizado, número de lançamentos,
  categorias e gráficos de barras por categoria.
- `controle_custos_obra.xlsx`: fonte de dados com os lançamentos
  (fornecedor, categoria e valor).
- `gen_custos.py`: script que gera a planilha a partir dos dados.
- A planilha e o dashboard usam o mesmo total, sem números divergentes.

### Kora Foods — Site Institucional (Aula 2)

- `kora-foods.html`: site institucional com seções "O que fazemos", "Como
  produzimos", "Para quem" e formulário de pedido de orçamento.
- O formulário monta uma mensagem e abre o WhatsApp com o texto preenchido.
- Identidade visual escura com o laranja da marca, definida em
  `identidade-visual.md`.

### Central de Pessoas (Aula 3)

- Interface escura com menu lateral recolhível, mapa de pessoas por área
  (bolhas coloridas por área, com alertas de férias vencidas) e busca por nome
  ou matrícula.
- Telas: Início, Análises, "E se?" e Visão do gestor.
- Análises:
  - "Precisa de você": férias vencidas e férias vencendo em 60 dias, com custo
    estimado de cada uma.
  - Gráfico de dispersão: tempo de casa × tempo sem promoção, com pontos
    clicáveis que abrem a ficha da pessoa.
  - "E se?": controle deslizante de investimento que mostra quanto custa tirar
    quem está em risco (calculado com 15% de aumento de salário).
  - Visão do gestor: equipe por gestor, com férias a programar e pessoas há
    mais de 3 anos sem promoção.
- Ficha da pessoa com linha do tempo (admissão, promoções, férias,
  desligamento).
- Ações gravadas na planilha:
  - `POST /api/promocao`: altera cargo e salário e registra a movimentação.
  - `POST /api/ferias`: programa o início do gozo e muda o status.
- Validação no backend: matrícula e cargo obrigatórios, salário numérico,
  data em `AAAA-MM-DD`; erros devolvem mensagem amigável e não alteram a
  planilha.
- Regras de negócio documentadas em `private/central/CLAUDE.md`.

---

## Stack técnica

- **HTML, CSS e JavaScript** puros, sem framework e sem build.
- **Chart.js** servido localmente (vendor) para os gráficos do dashboard Luma.
- **Python 3** com biblioteca padrão (`http.server`) para os dois servidores.
- **openpyxl** para leitura e escrita das planilhas.
- **SVG inline** para os ícones do hub.
- Dois servidores independentes: hub na porta **8000** e Central na porta
  **8765**.

---

## Como rodar

Pré-requisito: Python 3 com `openpyxl` (`pip install openpyxl`).

```bash
# 1. Hub (porta 8000) — na pasta raiz do projeto
python3 server.py

# 2. Central de Pessoas (porta 8765) — em outra aba do terminal
cd private/central
python3 app.py
```

Depois abra no navegador:

- Hub: `http://localhost:8000`
- Central: `http://localhost:8765`

Os servidores escutam em `192.168.15.17` por padrão (IP da rede local). Para
usar `localhost`, ajuste o endereço em `server.py` e `app.py`.

Dica: depois de alterar qualquer arquivo, recarregue o navegador com
`Ctrl+Shift+R` — o hub já envia cabeçalho de cache desativado.

---

## Fonte de dados

Os módulos usam planilhas `.xlsx` como fonte de verdade:

- `private/central/03 - Arquivo Apoio - Pessoas_RH.xlsx` — base de pessoas da
  Central (colaboradores, movimentações, férias e desligamentos).
- `private/kora/controle_custos_obra.xlsx` — lançamentos de custo da obra.
- O dashboard Luma e o site Kora Foods usam os dados embutidos no próprio
  HTML, gerados a partir das planilhas de apoio.

**Todos os dados são fictícios e didáticos.** Os nomes de pessoas da planilha
de RH foram substituídos por nomes fictícios gerados, e o nome do fornecedor
da planilha de custos foi generalizado.

---

## Verificação e qualidade

- **52 verificações automatizadas** executadas, com 52 aprovações e 0 falhas.
- Navegação testada nas quatro telas do hub.
- Revisão de código documentada em `VERIFICACAO-ERROS.md`, com achados de
  segurança (XSS por interpolação não escapada), robustez das rotas de escrita
  e consistência de números.
- Os formulários da Central validam a entrada no backend e não gravam dados
  inválidos.

---

## Segurança

Este repositório foi preparado para ser público. Antes da publicação foi feita
uma auditoria de segurança que removeu:

- comprovantes de transferência, recibos e documentos de terceiros;
- contratos e transcrições com nomes de pessoas;
- dados financeiros de terceiros.

O repositório **não contém** senhas, tokens, chaves de API, variáveis de
ambiente, URLs de projetos ou qualquer credencial. As credenciais, quando
necessárias, devem ficar em variáveis de ambiente e nunca no código.

---

## Autor

**Gilberto de Sousa Barbosa Filho**

Projeto desenvolvido no curso Claude na Prática, com coordenação do Hermes
(Agente da Nous Research) e execução assistida por Claude Code.
