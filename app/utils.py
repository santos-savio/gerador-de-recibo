import os
import json
from datetime import datetime
from num2words import num2words
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io


def numero_para_extenso(valor):
    """Converte valor numérico para extenso em português brasileiro"""
    try:
        valor_float = float(valor.replace(',', '.'))
        return num2words(valor_float, lang='pt_BR', to='currency').replace(' real', ' reais').replace(' real', ' real')
    except:
        return valor


def gerar_numero_recibo():
    """Gera número sequencial do recibo baseado nos arquivos existentes"""
    recibos_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'recibos_json')
    
    if not os.path.exists(recibos_dir):
        os.makedirs(recibos_dir)
        return 1
    
    arquivos = [f for f in os.listdir(recibos_dir) if f.startswith('recibo_') and f.endswith('.json')]
    
    if not arquivos:
        return 1
    
    numeros = []
    for arquivo in arquivos:
        try:
            num = int(arquivo.replace('recibo_', '').replace('.json', ''))
            numeros.append(num)
        except:
            continue
    
    return max(numeros) + 1 if numeros else 1


def salvar_recibo_json(dados, numero):
    """Salva dados do recibo em arquivo JSON"""
    recibos_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'recibos_json')
    os.makedirs(recibos_dir, exist_ok=True)
    
    filename = f"recibo_{numero:04d}.json"
    filepath = os.path.join(recibos_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    
    return filepath


def gerar_pdf(dados, numero):
    """Gera PDF usando ReportLab a partir dos dados do recibo"""
    recibos_pdf_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'recibos_pdf')
    os.makedirs(recibos_pdf_dir, exist_ok=True)
    
    filename = f"recibo_{numero:04d}.pdf"
    filepath = os.path.join(recibos_pdf_dir, filename)
    
    # Criar PDF usando ReportLab
    doc = SimpleDocTemplate(filepath, pagesize=A4,
                           rightMargin=2*cm, leftMargin=2*cm,
                           topMargin=2*cm, bottomMargin=2*cm)
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    heading_style = styles['Heading2']
    
    # Conteúdo do PDF
    story = []
    
    # Título
    story.append(Paragraph("RECIBO", title_style))
    story.append(Spacer(1, 1*cm))
    
    # Data
    story.append(Paragraph(f"<b>Data:</b> {dados['data']}", normal_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Cliente
    story.append(Paragraph(f"<b>Recebi de:</b> {dados['cliente']['nome']}", normal_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Valor
    story.append(Paragraph(f"<b>A quantia de:</b> {dados['valor_extenso']}", normal_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Serviços
    story.append(Paragraph("<b>Referente a:</b> Serviços de Tecnologia da Informação (TI), incluindo, mas não se limitando a:", normal_style))
    story.append(Spacer(1, 0.3*cm))
    
    for servico in dados['servicos']:
        story.append(Paragraph(f"• {servico}", normal_style))
    
    story.append(Spacer(1, 0.5*cm))
    
    # Detalhes
    story.append(Paragraph(f"<b>Detalhes adicionais ou especificações:</b> {dados['detalhes']}", normal_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Total
    story.append(Paragraph(f"<b>Total: R$ {dados['total']}</b>", heading_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Forma de pagamento
    story.append(Paragraph(f"<b>Forma de pagamento:</b> {dados['forma_pagamento']}", normal_style))
    story.append(Spacer(1, 3*cm))
    
    # Assinaturas
    story.append(Paragraph("_________________________________", normal_style))
    story.append(Paragraph("Assinatura do cliente", normal_style))
    story.append(Spacer(1, 2*cm))
    
    story.append(Paragraph("_________________________________", normal_style))
    story.append(Paragraph("Assinatura do prestador de serviços", normal_style))
    
    # Construir PDF
    doc.build(story)
    
    return filepath


def listar_recibos():
    """Lista todos os recibos existentes"""
    recibos_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'recibos_json')
    
    if not os.path.exists(recibos_dir):
        return []
    
    recibos = []
    for arquivo in sorted(os.listdir(recibos_dir)):
        if arquivo.startswith('recibo_') and arquivo.endswith('.json'):
            filepath = os.path.join(recibos_dir, arquivo)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    dados['arquivo'] = arquivo
                    dados['numero'] = arquivo.replace('recibo_', '').replace('.json', '')
                    recibos.append(dados)
            except:
                continue
    
    return sorted(recibos, key=lambda x: x['numero'], reverse=True)


def obter_recibo(numero):
    """Obtém dados de um recibo específico"""
    recibos_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'recibos_json')
    filename = f"recibo_{numero:04d}.json"
    filepath = os.path.join(recibos_dir, filename)
    
    if not os.path.exists(filepath):
        return None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None
