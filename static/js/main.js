// JavaScript principal para o Gerador de Recibos

document.addEventListener('DOMContentLoaded', function() {
    
    // Inicializa todos os tooltips
    initializeTooltips();
    
    // Configura formatação de campos
    setupFieldFormatting();
    
    // Configura validações customizadas
    setupCustomValidations();
    
    // Configura animações
    setupAnimations();
    
    // Configura atalhos de teclado
    setupKeyboardShortcuts();
});

/**
 * Inicializa tooltips do Bootstrap
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Configura formatação de campos específicos
 */
function setupFieldFormatting() {
    // Formatação de valor monetário
    const valorInput = document.querySelector('#valor');
    if (valorInput) {
        valorInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value) {
                // Converte para centavos e formata
                value = parseInt(value) / 100;
                e.target.value = value.toFixed(2).replace('.', ',');
            }
        });
        
        valorInput.addEventListener('blur', function() {
            let value = this.value.replace(',', '.');
            if (value && !isNaN(value)) {
                // Armazena o valor numérico para o backend
                this.setAttribute('data-numeric-value', parseFloat(value));
                this.value = parseFloat(value).toFixed(2).replace('.', ',');
            }
        });
        
        // Corrigir valor antes do envio
        const form = valorInput.closest('form');
        if (form) {
            form.addEventListener('submit', function() {
                const numericValue = valorInput.getAttribute('data-numeric-value');
                if (numericValue) {
                    valorInput.value = numericValue;  // Envia valor numérico para backend
                }
            });
        }
    }
    
    // Configura data atual como padrão
    const dataInput = document.querySelector('#data');
    if (dataInput && !dataInput.value) {
        const today = new Date().toISOString().split('T')[0];
        dataInput.value = today;
    }
    
    // Limitador de caracteres para textarea
    const detalhesTextarea = document.querySelector('#detalhes');
    if (detalhesTextarea) {
        const maxLength = 500;
        const counter = document.createElement('small');
        counter.className = 'form-text text-muted';
        counter.textContent = `0/${maxLength} caracteres`;
        
        detalhesTextarea.parentNode.appendChild(counter);
        
        detalhesTextarea.addEventListener('input', function() {
            const length = this.value.length;
            counter.textContent = `${length}/${maxLength} caracteres`;
            
            if (length >= maxLength) {
                counter.classList.add('text-danger');
                counter.classList.remove('text-muted');
            } else {
                counter.classList.remove('text-danger');
                counter.classList.add('text-muted');
            }
        });
    }
}

/**
 * Configura validações customizadas
 */
function setupCustomValidations() {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            // Validação customizada antes do envio
            const valorInput = document.querySelector('#valor');
            if (valorInput) {
                const valor = parseFloat(valorInput.value.replace(',', '.'));
                if (valor <= 0) {
                    e.preventDefault();
                    showAlert('Por favor, informe um valor maior que zero.', 'danger');
                    valorInput.focus();
                    return;
                }
            }
            
            // Mostra loading durante o processamento
            showLoading();
        });
    }
}

/**
 * Configura animações da página
 */
function setupAnimations() {
    // Animação de fade-in para cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Animação para alertas
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        alert.style.animation = 'slideInRight 0.5s ease';
    });
}

/**
 * Configura atalhos de teclado
 */
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl+N para novo recibo
        if (e.ctrlKey && e.key === 'n') {
            e.preventDefault();
            window.location.href = '/';
        }
        
        // Ctrl+L para lista de recibos
        if (e.ctrlKey && e.key === 'l') {
            e.preventDefault();
            window.location.href = '/recibos';
        }
        
        // Escape para fechar modais
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                const modalInstance = bootstrap.Modal.getInstance(modal);
                if (modalInstance) {
                    modalInstance.hide();
                }
            });
        }
    });
}

/**
 * Mostra alerta personalizado
 */
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    if (!alertContainer) return;
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.insertBefore(alert, alertContainer.firstChild);
    
    // Auto-remove após 5 segundos
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

/**
 * Mostra indicador de loading
 */
function showLoading() {
    const submitButton = document.querySelector('button[type="submit"]');
    if (submitButton) {
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="spinner me-2"></span>Processando...';
    }
}

/**
 * Remove indicador de loading
 */
function hideLoading() {
    const submitButton = document.querySelector('button[type="submit"]');
    if (submitButton) {
        submitButton.disabled = false;
        submitButton.innerHTML = submitButton.getAttribute('data-original-text') || 'Gerar Recibo';
    }
}

/**
 * Formata valor para exibição em brasileiro
 */
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

/**
 * Formata data para brasileiro
 */
function formatDate(date) {
    return new Intl.DateTimeFormat('pt-BR').format(new Date(date));
}

/**
 * Copia texto para área de transferência
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showAlert('Copiado para área de transferência!', 'success');
    }).catch(() => {
        // Fallback para navegadores antigos
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showAlert('Copiado para área de transferência!', 'success');
    });
}

/**
 * Valida CPF/CNPJ
 */
function validateDocument(doc) {
    doc = doc.replace(/\D/g, '');
    
    if (doc.length === 11) {
        return validateCPF(doc);
    } else if (doc.length === 14) {
        return validateCNPJ(doc);
    }
    
    return false;
}

function validateCPF(cpf) {
    // Implementação simplificada de validação de CPF
    if (cpf.length !== 11) return false;
    
    // Verifica se todos os dígitos são iguais
    if (/^(\d)\1{10}$/.test(cpf)) return false;
    
    // Implementação do algoritmo de validação de CPF
    let sum = 0;
    for (let i = 0; i < 9; i++) {
        sum += parseInt(cpf.charAt(i)) * (10 - i);
    }
    let remainder = 11 - (sum % 11);
    let digit = remainder === 10 || remainder === 11 ? 0 : remainder;
    
    if (digit !== parseInt(cpf.charAt(9))) return false;
    
    sum = 0;
    for (let i = 0; i < 10; i++) {
        sum += parseInt(cpf.charAt(i)) * (11 - i);
    }
    remainder = 11 - (sum % 11);
    digit = remainder === 10 || remainder === 11 ? 0 : remainder;
    
    return digit === parseInt(cpf.charAt(10));
}

function validateCNPJ(cnpj) {
    // Implementação simplificada de validação de CNPJ
    if (cnpj.length !== 14) return false;
    
    // Verifica se todos os dígitos são iguais
    if (/^(\d)\1{13}$/.test(cnpj)) return false;
    
    // Implementação do algoritmo de validação de CNPJ seria mais complexa
    // Por enquanto, apenas verifica o formato
    return true;
}

// Exporta funções para uso global
window.GeradorRecibos = {
    showAlert,
    showLoading,
    hideLoading,
    formatCurrency,
    formatDate,
    copyToClipboard,
    validateDocument
};
