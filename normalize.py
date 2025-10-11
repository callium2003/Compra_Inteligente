"""
Rota de Normalização
POST /api/normalize - Normaliza texto de lista de compras
"""
from flask import Blueprint, request, jsonify
from src.normalizer import normalize_shopping_list

normalize_bp = Blueprint('normalize', __name__)


@normalize_bp.route('/normalize', methods=['POST'])
def normalize():
    """
    Normaliza texto de lista de compras
    
    Body:
    {
        "raw_text": "2 leite 1l\narroz 5kg\n..."
    }
    
    Response:
    {
        "success": true,
        "items": [
            {
                "qty": 2,
                "product_name": "leite",
                "size_value": 1,
                "size_unit": "l",
                "brand": null,
                "preference": "any",
                "notes": null
            },
            ...
        ]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'raw_text' not in data:
            return jsonify({
                'success': False,
                'error': 'Campo raw_text é obrigatório'
            }), 400
        
        raw_text = data['raw_text']
        
        if not raw_text.strip():
            return jsonify({
                'success': False,
                'error': 'Lista de compras não pode estar vazia'
            }), 400
        
        # Normalizar lista
        items = normalize_shopping_list(raw_text)
        
        if not items:
            return jsonify({
                'success': False,
                'error': 'Nenhum item válido encontrado na lista'
            }), 400
        
        return jsonify({
            'success': True,
            'items': items
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao normalizar lista: {str(e)}'
        }), 500
