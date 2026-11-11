import openpyxl
from openpyxl import Workbook

# Dados a serem inseridos: (DATA, FORNECEDOR, CATEGORIA, VALOR)
dados = [
    ("2026-02-27", "Fornecedor A", "Mao de obra", 11600),
    ("2026-04-30", "Fornecedor A", "Mao de obra", 25200),
    ("2026-05-29", "Fornecedor A", "Telhado", 10400),
    ("2026-07-31", "Fornecedor A", "JunhoJulho", 19200),
    ("2026-09-15", "Fornecedor A", "Reembolso", 480),
    ("2026-09-30", "Fornecedor A", "AgoSet", 20800),
    ("2026-10-30", "Fornecedor A", "Outubro", 8400),
]

# Criar workbook e selecionar aba
wb = Workbook()
ws = wb.active
ws.title = "Lançamentos"

# Escrever cabeçalho
ws.append(["DATA", "FORNECEDOR", "CATEGORIA", "VALOR"])

# Inserir linhas de dados
for linha in dados:
    ws.append(list(linha))

# Linha de total (soma dos valores)
total_valores = sum(linha[3] for linha in dados)
ws.append(["", "Total", "", total_valores])

# Salvar arquivo
wb.save("controle_custos_obra.xlsx")
print("Arquivo controle_custos_obra.xlsx criado com sucesso.")
print(f"Total de linhas (excluindo cabeçalho e total): {len(dados)}")
print(f"Soma total dos valores: {total_valores}")