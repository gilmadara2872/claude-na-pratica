# Central de Pessoas Kora Foods - Premissas e Diretrizes

## Sistema
- Servidor local (stdlib + openpyxl) na porta 8765, lendo o arquivo `03 - Arquivo Apoio - Pessoas_RH.xlsx`.
- Data de referência fixa: **2026-10-15**.
- Rotas: `GET /api/dados`, `POST /api/promocao`, `POST /api/ferias`.
- A página (`index.html`) é servida pelo hub na porta 8000 e busca os dados na 8765 via `${location.hostname}`.

## Regras de Negócio (implementadas no app.py, derivadas da planilha)

### Férias
- Dias de direito e limite para gozo vêm da aba **Férias** (não são recalculados).
- **Vencida**: status `Pendente` e limite para gozo anterior à data de referência.
- **Vencendo (60 dias)**: status diferente de `Realizada` e limite entre a referência e referência + 60 dias.
- **Custo de férias**: salário atual × dias de direito ÷ 30.
- **Programar férias**: grava a data de início do gozo e muda o status de `Pendente` para `Programada`.

### Promoção
- Altera cargo e salário na aba **Colaboradores**.
- Registra a movimentação (tipo `Promoção`, cargo anterior → novo, salário anterior → novo) na aba **Movimentações**.

### Desligamento
- Apenas leitura da aba **Desligamentos** (o sistema não grava desligamentos).

### Entrada de dados
- Validação no backend: matrícula e cargo obrigatórios, salário numérico, data em AAAA-MM-DD.
- Erros devolvem mensagem amigável e **não alteram** a planilha.

## Formatos
- **Moeda**: R$ 1.234,56 (ponto milhar, vírgula decimal).
- **Data**: dd/mm/aaaa.

## Como Trabalhar
1. **Não alterar regras sem antes perguntar** ao responsável/prompt. Toda mudança de regra de férias, promoção ou desligamento deve ser validada antes de ser aplicada nos cálculos.
2. **Confirmar números no navegador**: após gerar qualquer saída numérica ou de data, conferir os valores contra o arquivo `03 - Arquivo Apoio - Pessoas_RH.xlsx`.
3. **Utilizar os formatos descritos** (moeda e data) ao apresentar resultados ao usuário ou ao exportar arquivos.

## Observações
- Sempre que houver dúvida sobre qual regra aplicar, pare e pergunte antes de prosseguir.
- Os cálculos devem ser transparentes e rastreáveis até a linha do dado original no Excel.
