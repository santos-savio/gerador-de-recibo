#!/usr/bin/env python3
"""
Script para iniciar a aplicação Gerador de Recibos
"""

import os
import sys

# Adicionar o diretório 'app' ao Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import app

if __name__ == '__main__':
    # Criar diretórios necessários se não existirem
    os.makedirs('static', exist_ok=True)
    os.makedirs('recibos_json', exist_ok=True)
    os.makedirs('recibos_pdf', exist_ok=True)
    
    print("=" * 60)
    print("🧾 GERADOR DE RECIBOS - SISTEMA WEB")
    print("=" * 60)
    print("🚀 Iniciando servidor Flask...")
    print("📍 URL local: http://localhost:5000")
    print("📍 URL rede: http://0.0.0.0:5000")
    print("=" * 60)
    print("⚠️  Pressione Ctrl+C para parar o servidor")
    print("=" * 60)
    
    try:
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n👋 Servidor encerrado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)
