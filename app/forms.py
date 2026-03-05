from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FloatField, SubmitField, DateField
from wtforms.validators import DataRequired, NumberRange, Length
from datetime import datetime


class ReciboForm(FlaskForm):
    """Formulário para geração de recibos"""
    
    data = DateField('Data', validators=[DataRequired(message='Data é obrigatória')])
    
    cliente_nome = StringField('Nome do Cliente', validators=[
        DataRequired(message='Nome do cliente é obrigatório'),
        Length(min=3, max=100, message='Nome deve ter entre 3 e 100 caracteres')
    ])
    
    valor = FloatField('Valor (R$)', validators=[
        DataRequired(message='Valor é obrigatório'),
        NumberRange(min=0.01, message='Valor deve ser maior que zero')
    ])
    
    forma_pagamento = SelectField('Forma de Pagamento', choices=[
        ('Pix', 'Pix'),
        ('Transferência Bancária', 'Transferência Bancária'),
        ('Dinheiro', 'Dinheiro'),
        ('Cartão de Crédito', 'Cartão de Crédito'),
        ('Cartão de Débito', 'Cartão de Débito'),
        ('Boleto Bancário', 'Boleto Bancário'),
        ('Outros', 'Outros')
    ], validators=[DataRequired(message='Forma de pagamento é obrigatória')])
    
    detalhes = TextAreaField('Detalhes Adicionais', validators=[
        Length(max=500, message='Detalhes devem ter no máximo 500 caracteres')
    ])
    
    # Serviços predefinidos
    servicos_predefinidos = [
        'Desenvolvimento de software',
        'Manutenção de sistemas',
        'Consultoria em TI',
        'Suporte técnico',
        'Instalação e configuração de redes',
        'Outros serviços relacionados à TI'
    ]
    
    submit = SubmitField('Gerar Recibo')
    
    def __init__(self, *args, **kwargs):
        super(ReciboForm, self).__init__(*args, **kwargs)
        # Definir data atual como padrão
        if not self.data.data:
            self.data.data = datetime.now().date()
