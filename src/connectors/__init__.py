"""
Conectores de supermercados
"""
from .base import SupermarketConnector
from .extra import ExtraConnector
from .carrefour import CarrefourConnector
from .mambo import MamboConnector
from .mercadolivre import MercadoLivreConnector

__all__ = [
    'SupermarketConnector',
    'ExtraConnector',
    'CarrefourConnector',
    'MamboConnector',
    'MercadoLivreConnector'
]
