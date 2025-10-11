"""
Conectores de supermercados
"""
from .base import SupermarketConnector
from .extra import ExtraConnector
from .carrefour import CarrefourConnector
from .mock import MamboConnector, MercadoLivreConnector

__all__ = [
    'SupermarketConnector',
    'ExtraConnector',
    'CarrefourConnector',
    'MamboConnector',
    'MercadoLivreConnector'
]
