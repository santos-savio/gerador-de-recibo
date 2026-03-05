import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_wtf.csrf import CSRFProtect
from forms import ReciboForm
from utils import (
    numero_para_extenso, gerar_numero_recibo, salvar_recibo_json, 
    gerar_pdf, listar_recibos, obter_recibo
)
from datetime import datetime

app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'
app.config['WTF_CSRF_ENABLED'] = True

csrf = CSRFProtect(app)

# Servir arquivos estáticos
@app.route('/static/<path:filename>')
def static_files(filename):
    filepath = os.path.join('../static', filename)
    if not os.path.exists(filepath):
        # Retornar 404 para arquivos não encontrados
        return f"Arquivo estático não encontrado: {filename}", 404
    return send_file(filepath)

@app.route('/')
def index():
    """Página principal com formulário"""
    form = ReciboForm()
    return render_template('formulario.html', form=form)

@app.route('/gerar-recibo', methods=['POST'])
def gerar_recibo():
    """Processa formulário e gera recibo"""
    form = ReciboForm()
    
    if form.validate_on_submit():
        try:
            # Gerar número do recibo
            numero = gerar_numero_recibo()
            
            # Preparar dados do recibo
            dados = {
                'logo_url': '/static/logo.png',
                'data': form.data.data.strftime('%d/%m/%Y'),
                'cliente': {
                    'nome': form.cliente_nome.data
                },
                'valor_extenso': numero_para_extenso(f"{form.valor.data:.2f}"),
                'total': f"{form.valor.data:.2f}".replace('.', ','),
                'forma_pagamento': form.forma_pagamento.data,
                'detalhes': form.detalhes.data or 'Serviços prestados conforme combinado.',
                'servicos': form.servicos_predefinidos
            }
            
            # Salvar dados JSON
            json_path = salvar_recibo_json(dados, numero)
            
            # Gerar PDF
            pdf_path = gerar_pdf(dados, numero)
            
            flash(f'Recibo #{numero:04d} gerado com sucesso!', 'success')
            
            # Redirecionar para visualização do recibo
            return redirect(url_for('visualizar_recibo', numero=numero))
            
        except Exception as e:
            flash(f'Erro ao gerar recibo: {str(e)}', 'error')
            return render_template('formulario.html', form=form)
    
    else:
        # Formulário inválido, mostrar erros
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{getattr(form, field).label.text}: {error}', 'error')
        
        return render_template('formulario.html', form=form)

@app.route('/recibo/<int:numero>')
def visualizar_recibo(numero):
    """Visualiza um recibo específico"""
    dados = obter_recibo(numero)
    
    if not dados:
        flash('Recibo não encontrado', 'error')
        return redirect(url_for('lista_recibos'))
    
    return render_template('recibo.html', **dados)

@app.route('/recibo/<int:numero>/pdf')
def download_pdf(numero):
    """Download do PDF do recibo"""
    pdf_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'recibos_pdf')
    filename = f"recibo_{numero:04d}.pdf"
    filepath = os.path.join(pdf_dir, filename)
    
    if not os.path.exists(filepath):
        flash('PDF não encontrado', 'error')
        return redirect(url_for('lista_recibos'))
    
    return send_file(filepath, as_attachment=True, download_name=filename)

@app.route('/recibo/<int:numero>/json')
def download_json(numero):
    """Download do JSON do recibo"""
    json_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'recibos_json')
    filename = f"recibo_{numero:04d}.json"
    filepath = os.path.join(json_dir, filename)
    
    if not os.path.exists(filepath):
        flash('Arquivo JSON não encontrado', 'error')
        return redirect(url_for('lista_recibos'))
    
    return send_file(filepath, as_attachment=True, download_name=filename)

@app.route('/recibos')
def lista_recibos():
    """Lista todos os recibos gerados"""
    recibos = listar_recibos()
    return render_template('lista_recibos.html', recibos=recibos)

@app.route('/api/recibos')
def api_recibos():
    """API endpoint para listar recibos em formato JSON"""
    recibos = listar_recibos()
    return jsonify(recibos)

if __name__ == '__main__':
    # Criar diretórios necessários
    os.makedirs('static', exist_ok=True)
    os.makedirs('recibos_pdf', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
