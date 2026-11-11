import openpyxl
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

wb = openpyxl.load_workbook('03 - Arquivo Apoio - Planilha Resultados Luma.xlsx', data_only=True)

def get_val(sheet, label):
    ws = wb[sheet]
    for row in ws.iter_rows(values_only=True):
        if row and len(row)>=2 and row[0] and isinstance(row[0], str) and label.lower() in row[0].lower():
            return row[1]
    return None

fat = get_val('Resumo','Faturamento total') or 6800000
cresc = get_val('Resumo','Crescimento vs 1S 2025') or 0.121
traf = None; brand = None
ws = wb['Resumo']
# Serviços começam na coluna E (índice 4)
for row in ws.iter_rows(values_only=True):
    if row and row[4]=='Tráfego pago': traf=row[5]
    if row and row[4]=='Branding': brand=row[5]

perd = get_val('Resumo','Clientes perdidos') or 13
taxa = get_val('Resumo','Taxa de clientes perdidos') or 0.09
novos = get_val('Resumo','Novos clientes') or 9
nps = get_val('Resumo','NPS médio') or 8.26

prs = Presentation()
prs.slide_width = Inches(13.33); prs.slide_height = Inches(7.5)
BG = RGBColor(0x0C,0x1E,0x3B); MENTA = RGBColor(0x6D,0xE2,0xC3); TEXTO = RGBColor(0xEE,0xF4,0xF8); CINZA = RGBColor(0xA3,0xBA,0xC6); ROXO = RGBColor(0x52,0x1F,0xFF); AMBAR = RGBColor(0xF2,0xB5,0x3A)

def blank():
    return prs.slides.add_slide(prs.slide_layouts[6])
def set_bg(slide, color):
    slide.background.fill.solid(); slide.background.fill.fore_color.rgb = color
def add_text(slide, l,t,w,h, text, size=18, color=TEXTO, bold=False, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text; p.font.size = Pt(size); p.font.color.rgb = color; p.font.bold = bold; p.alignment = align
    return box
def add_bullets(slide, l,t,w,h, items, size=15):
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame; tf.word_wrap = True
    for i,(b,r) in enumerate(items):
        p = tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.space_after = Pt(8)
        run1 = p.add_run(); run1.text = "• "+b; run1.font.size=Pt(size); run1.font.bold=True; run1.font.color.rgb=TEXTO
        run2 = p.add_run(); run2.text = r; run2.font.size=Pt(size); run2.font.color.rgb=CINZA
    return box

# Slide 1 - Capa
s = blank(); set_bg(s, BG)
add_text(s,0.6,0.6,12,0.3,"LUMA MARKETING · DIRETORIA",11,MENTA,True)
add_text(s,0.6,1.2,12,1.5,"Resultados do 1º semestre de 2026",40,TEXTO,True)
add_text(s,0.6,2.4,12,0.5,"Fechamento do semestre · base para o plano de 2027",18,CINZA)
add_text(s,0.6,6.6,12,0.3,"Fonte: Planilha Resultados Luma (abas Resumo, Receita mensal, Clientes, Metas) — dados fictícios didáticos. Sem números inventados.",9,CINZA)

# Slide 2 - Faturamento
s = blank(); set_bg(s, BG)
add_text(s,0.6,0.4,12,0.6,"01 — Faturamento",30,TEXTO,True)
add_text(s,0.6,1.1,7,0.4,"R$ 6,8 milhões no semestre · +12,1% vs 1S 2025 (R$ 6,07 mi)",16,MENTA,True)
add_bullets(s,0.6,1.8,7.5,3.5,[
 ("97,1% da meta: ","meta R$ 7,0 mi — perto, mas abaixo (aba Metas)."),
 ("Crescimento abaixo da meta: ","12,1% vs 15% esperado."),
 ("Junho foi o melhor mês: ","R$ 1,175 mi — receita cresceu mês a mês (aba Receita mensal)."),
 ("Motor do semestre: ","tráfego pago R$ 2,52 mi, +34% — única meta batida (135,9%)."),
])
add_text(s,0.6,6.3,12,0.3,"Fonte: Resumo + Receita mensal + Metas",9,CINZA)

# Slide 3 - Mix
s = blank(); set_bg(s, BG)
add_text(s,0.6,0.4,12,0.6,"02 — Mix por serviço",30,TEXTO,True)
items = [
 ("Tráfego pago — R$ 2,52 mi (37%) ","meta batida com folga."),
 ("Social media — R$ 2,02 mi (30%) ","+8%, estável."),
 ("Conteúdo — R$ 1,39 mi (20%) ","+5%, estável."),
 ("Branding — R$ 881 mil (13%) ","−12%: cliente pequeno não compra branding sozinho; quer resultado rápido."),
]
add_bullets(s,0.6,1.4,12,3.0,items,17)
add_text(s,0.6,6.3,12,0.3,"Fonte: Resumo e Receita mensal",9,CINZA)

# Slide 4 - Clientes
s = blank(); set_bg(s, BG)
add_text(s,0.6,0.4,12,0.6,"03 — Clientes: perder menos",30,TEXTO,True)
add_bullets(s,0.6,1.4,12,3.4,[
 ("140 contas ativas em 30/06: ","144 no início, 13 perdidos (9%) e 9 novos — meta de retenção era máx. 5% (aba Metas)."),
 ("11 dos 13 que saíram ","tinham menos de 18 meses de contrato (61% a 90% do padrão de saída 12–18 meses)."),
 ("Motivos: ","resultado abaixo (4) + relatório pouco claro (3) somam 7 de 13 — parte do “resultado” pode ser resultado que existiu mas o cliente não enxergou."),
 ("Saúde é o alerta: ","4 perdas em 34 contas (R$ 1,34 mi) — Farmácia Saudara, Ótica Lentivia e Construtora Bravicon citaram “não entender o que vocês mandam”."),
])
add_text(s,0.6,6.3,12,0.3,"Fonte: Clientes + Resumo; NPS médio 8,26 vs meta 8,5 (clientes que saíram tinham NPS 3–6)",9,CINZA)

# Slide 5 - Plano
s = blank(); set_bg(s, BG)
add_text(s,0.6,0.4,12,0.6,"04 — O que fazemos até o fim do ano → 2027",30,TEXTO,True)
add_bullets(s,0.6,1.3,12,3.6,[
 ("Segurar quem está perto de 1 ano: ","ligação uma a uma (Letícia puxa a lista hoje; dono da ligação definido até sexta, antes de novembro)."),
 ("Arrumar como mostramos resultado: ","relatório de 1 página (Diego+Bianca, 19/11), treinamento do atendimento (Rafael, 04/12) e alerta de NPS < 7 (Diego, 15/01)."),
 ("Virar manual em processo: ","checklist do capítulo de cuidado com o cliente (Letícia+Rafael, 18/12)."),
 ("Crescer 25% em 2027: ","projeção 2S com outubro fechado (Letícia, 30/11); pacote branding+tráfego (Bianca, 27/11); lista de prospecção Campinas/Sorocaba/Ribeirão (Diego, 19/11); offsite na 1ª quinzena de jan."),
],14)
add_text(s,0.6,6.4,12,0.3,"Fonte: Transcrição da reunião de diretoria (26/10/2026) — nenhuma meta inventada",9,CINZA)

prs.save('Luma_Resultados_1S2026.pptx')
print('PPT criado com sucesso: Luma_Resultados_1S2026.pptx')
