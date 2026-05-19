import logging
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)
history_bp = Blueprint('history', __name__)

@history_bp.route('/history/price-evolution', methods=['GET'])
def price_evolution():
    """
    Retorna dados de evolução de preços para um produto específico.
    Como o banco de dados Supabase é gerenciado pelo frontend, 
    este endpoint simula a agregação de dados históricos baseada nas cotações salvas.
    """
    product_name = request.args.get('product_name', 'Leite')
    days = int(request.args.get('days', 30))
    
    # Simulação de dados históricos (em um cenário real, buscaríamos na tabela 'quotes' do Supabase)
    # Aqui geramos dados realistas para os 4 supermercados
    stores = ["Extra", "Carrefour", "Mambo", "Mercado Livre"]
    data = []
    
    base_prices = {
        "Extra": 5.20,
        "Carrefour": 4.90,
        "Mambo": 5.50,
        "Mercado Livre": 5.10
    }
    
    end_date = datetime.now()
    for i in range(days, -1, -1):
        date = end_date - timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')
        
        entry = {"date": date_str}
        for store in stores:
            # Variação aleatória de preço para o gráfico
            variation = random.uniform(-0.5, 0.5)
            entry[store] = round(base_prices[store] + variation, 2)
            
        data.append(entry)
        
    return jsonify({
        "success": True,
        "product": product_name,
        "history": data
    })
