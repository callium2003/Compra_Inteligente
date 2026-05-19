"""
Sistema de cache para preços de produtos
"""
import json
import hashlib
import time
import logging
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class PriceCache:
    """Cache de preços com TTL (Time To Live)"""
    
    def __init__(self, cache_dir: str = "/tmp/price_cache", ttl: int = 3600):
        """
        Inicializa o cache
        
        Args:
            cache_dir: Diretório para armazenar cache
            ttl: Tempo de vida do cache em segundos (padrão: 1 hora)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = ttl
        logger.info(f"Cache inicializado: {self.cache_dir} (TTL: {self.ttl}s)")
    
    def _get_cache_key(self, store: str, product: str) -> str:
        """
        Gera chave única para o cache
        
        Args:
            store: Nome da loja
            product: Nome do produto
        
        Returns:
            Hash MD5 da combinação loja+produto
        """
        key = f"{store.lower()}_{product.lower()}"
        return hashlib.md5(key.encode()).hexdigest()
    
    def _get_cache_file(self, store: str, product: str) -> Path:
        """
        Retorna caminho do arquivo de cache
        
        Args:
            store: Nome da loja
            product: Nome do produto
        
        Returns:
            Path object para o arquivo de cache
        """
        cache_key = self._get_cache_key(store, product)
        return self.cache_dir / f"{cache_key}.json"
    
    def get(self, store: str, product: str) -> Optional[Dict[str, Any]]:
        """
        Recupera dados do cache
        
        Args:
            store: Nome da loja
            product: Nome do produto
        
        Returns:
            Dados do cache ou None se não existir/expirado
        """
        cache_file = self._get_cache_file(store, product)
        
        if not cache_file.exists():
            logger.debug(f"Cache miss: {store} - {product}")
            return None
        
        try:
            data = json.loads(cache_file.read_text())
            
            # Verificar se expirou
            timestamp = data.get('timestamp', 0)
            age = time.time() - timestamp
            
            if age > self.ttl:
                logger.debug(f"Cache expirado: {store} - {product} (idade: {age:.0f}s)")
                cache_file.unlink()  # Remover arquivo expirado
                return None
            
            logger.debug(f"Cache hit: {store} - {product} (idade: {age:.0f}s)")
            return data.get('result')
        
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Erro ao ler cache: {e}")
            return None
    
    def set(self, store: str, product: str, result: Dict[str, Any]):
        """
        Salva dados no cache
        
        Args:
            store: Nome da loja
            product: Nome do produto
            result: Dados a serem cacheados
        """
        cache_file = self._get_cache_file(store, product)
        
        try:
            data = {
                'timestamp': time.time(),
                'store': store,
                'product': product,
                'result': result
            }
            
            cache_file.write_text(json.dumps(data, ensure_ascii=False, indent=2))
            logger.debug(f"Cache salvo: {store} - {product}")
        
        except IOError as e:
            logger.error(f"Erro ao salvar cache: {e}")
    
    def clear(self, store: Optional[str] = None):
        """
        Limpa o cache
        
        Args:
            store: Se especificado, limpa apenas cache dessa loja
        """
        if store:
            # Limpar apenas cache de uma loja específica
            count = 0
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    data = json.loads(cache_file.read_text())
                    if data.get('store', '').lower() == store.lower():
                        cache_file.unlink()
                        count += 1
                except Exception:
                    pass
            logger.info(f"Cache limpo: {count} arquivos de {store}")
        else:
            # Limpar todo o cache
            count = 0
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
                count += 1
            logger.info(f"Cache limpo: {count} arquivos")
    
    def cleanup_expired(self):
        """Remove todos os arquivos de cache expirados"""
        count = 0
        now = time.time()
        
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                data = json.loads(cache_file.read_text())
                timestamp = data.get('timestamp', 0)
                
                if now - timestamp > self.ttl:
                    cache_file.unlink()
                    count += 1
            
            except Exception:
                # Se não conseguir ler, remover também
                cache_file.unlink()
                count += 1
        
        if count > 0:
            logger.info(f"Limpeza de cache: {count} arquivos expirados removidos")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do cache
        
        Returns:
            Dicionário com estatísticas
        """
        total_files = 0
        total_size = 0
        expired_files = 0
        now = time.time()
        
        for cache_file in self.cache_dir.glob("*.json"):
            total_files += 1
            total_size += cache_file.stat().st_size
            
            try:
                data = json.loads(cache_file.read_text())
                timestamp = data.get('timestamp', 0)
                
                if now - timestamp > self.ttl:
                    expired_files += 1
            except Exception:
                expired_files += 1
        
        return {
            'total_files': total_files,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / 1024 / 1024, 2),
            'expired_files': expired_files,
            'valid_files': total_files - expired_files,
            'ttl_seconds': self.ttl,
            'cache_dir': str(self.cache_dir)
        }
