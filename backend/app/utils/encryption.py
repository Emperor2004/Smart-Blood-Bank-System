"""Encryption utilities for sensitive data."""
from cryptography.fernet import Fernet
from app.config import settings
import base64
import hashlib


def get_encryption_key() -> bytes:
    """
    Get or generate encryption key.
    
    Returns:
        Encryption key bytes
    """
    if settings.encryption_key:
        # Use provided key, ensure it's properly formatted
        key = settings.encryption_key.encode() if isinstance(settings.encryption_key, str) else settings.encryption_key
        # Derive a proper Fernet key from the provided key
        return base64.urlsafe_b64encode(hashlib.sha256(key).digest())
    else:
        # Generate a new key (for development only)
        return Fernet.generate_key()


# Global cipher instance
_cipher = None


def get_cipher() -> Fernet:
    """Get or create cipher instance."""
    global _cipher
    if _cipher is None:
        _cipher = Fernet(get_encryption_key())
    return _cipher


def encrypt_value(value: str) -> str:
    """
    Encrypt a string value.
    
    Args:
        value: String to encrypt
        
    Returns:
        Encrypted string (base64 encoded)
    """
    if not value:
        return value
    
    cipher = get_cipher()
    encrypted = cipher.encrypt(value.encode())
    return encrypted.decode()


def decrypt_value(encrypted_value: str) -> str:
    """
    Decrypt an encrypted string value.
    
    Args:
        encrypted_value: Encrypted string to decrypt
        
    Returns:
        Decrypted string
    """
    if not encrypted_value:
        return encrypted_value
    
    cipher = get_cipher()
    decrypted = cipher.decrypt(encrypted_value.encode())
    return decrypted.decode()
