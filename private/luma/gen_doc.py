from docx import Document

doc = Document()

# Dados da transcrição da reunião de diretoria Luma - tarefas identificadas
tasks = [
    {
        "tarefa": "Puxar lista de clientes próximos de completar um ano de contrato",
        "responsavel": "Letícia",
        "prazo": "até o fim do dia",
        "status": "a definir"
    },
    {
        "tarefa": "Realizar reuniões de noventa dias com clientes",
        "responsavel": "Rafael",
        "prazo": "18/12",
        "status": "a definir"
    },
    {
        "tarefa": "Analisar clientes de saúde",
        "responsavel": "Diego",
        "prazo": "27/11",
        "status": "a definir"
    },
    {
        "tarefa": "Criar modelo único de relatório mensal (uma página)",
        "responsavel": "Diego",
        "prazo": "19/11",
        "status": "a definir"
    },
    {
        "tarefa": "Treinar analistas sobre modelo de relatório",
        "responsavel": "Rafael",
        "prazo": "04/12",
        "status": "a definir"
    },
    {
        "tarefa": "Revisar capítulo de como cuidamos dos clientes do manual e transformar em processo",
        "responsavel": "Letícia",
        "prazo": "18/12",
        "status": "a definir"
    },
    {
        "tarefa": "Levantar custo de dashboard para 140 contas",
        "responsavel": "Letícia",
        "prazo": "13/11",
        "status": "a definir"
    },
    {
        "tarefa": "Desenvolver proposta de pacote branding com tráfego",
        "responsavel": "Bianca",
        "prazo": "27/11",
        "status": "a definir"
    },
    {
        "tarefa": "Criar lista de empresas para prospecção 2027",
        "responsavel": "Diego",
        "prazo": "19/11",
        "status": "a definir"
    },
    {
        "tarefa": "Definir meta de novos clientes para 2027",
        "responsavel": "Marcelo",
        "prazo": "01/12",
        "status": "a definir"
    },
    {
        "tarefa": "Definir local e data do offsite",
        "responsavel": "Letícia",
        "prazo": "13/11",
        "status": "a definir"
    },
    {
        "tarefa": "Montar pauta do offsite",
        "responsavel": "Marcelo",
        "prazo": "18/12",
        "status": "a definir"
    },
    {
        "tarefa": "Implementar alerta de NPS baixo (nota abaixo de sete)",
        "responsavel": "Diego",
        "prazo": "15/01",
        "status": "a definir"
    }
]

# Criar tabela com cabeçalhos
headers = ["tarefa", "responsável", "prazo", "status"]
table = doc.add_table(rows=1, cols=4)

# Adicionar cabeçalhos
for i, header in enumerate(headers):
    cell = table.rows[0].cells[i]
    cell.text = header

# Adicionar linhas de dados extraídos da transcrição
for task in tasks:
    row_cells = table.add_row().cells
    row_cells[0].text = task["tarefa"]
    row_cells[1].text = task["responsavel"]
    row_cells[2].text = task["prazo"]
    row_cells[3].text = task["status"]

# Salvar documento
doc.save("Luma_Tarefas_Diretoria.docx")