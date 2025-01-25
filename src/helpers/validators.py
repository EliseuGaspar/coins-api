import ipaddress
from urllib.parse import urlparse

from src.api.core import Settings


class Urls:
    
    ALLOWED_PORTS = {80, 443}
    
    @classmethod
    def is_valid_url(cls, url: str) -> bool:
        """Verifica se a URL tem um esquema válido (http ou https)."""
        parsed = urlparse(url)
        return parsed.scheme in {"http", "https"}

    @classmethod
    def is_private_or_local(cls, url: str) -> bool:
        """Verifica se a URL aponta para IP ou host local/privado."""
        parsed = urlparse(url)
        try:
            ip = ipaddress.ip_address(parsed.hostname)
            return ip.is_private or ip.is_loopback
        except ValueError:
            return parsed.hostname in {"localhost"}

    @classmethod
    def has_valid_hostname(cls, url: str) -> bool:
        """Verifica se a URL possui um hostname válido."""
        parsed = urlparse(url)
        return bool(parsed.hostname)

    @classmethod
    def has_safe_port(cls, url: str) -> bool:
        """Verifica se a URL usa uma porta permitida."""
        parsed = urlparse(url)
        return not parsed.port or parsed.port in cls.ALLOWED_PORTS

    @classmethod
    def has_safe_query(cls, url: str) -> bool:
        """Verifica se a query string da URL não contém elementos perigosos."""
        parsed = urlparse(url)
        return not any(x in parsed.query for x in {"<", ">", "script", "onerror"})

    @classmethod
    def is_length_valid(cls, url: str) -> bool:
        """Verifica se a URL não excede o comprimento máximo permitido."""
        return len(url) <= 2000
