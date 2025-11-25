import uuid
from django.db import models

def generate_api_key():
    """Gera uma string UUIDv4 de 32 caracteres para a chave de API."""
    return uuid.uuid4().hex

class APIKey(models.Model):
    service = models.CharField(max_length=100)
    key = models.CharField(max_length=40, unique=True, default=generate_api_key)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Key for {self.service} ({self.key[:8]}...)"

    @property
    def is_authenticated(self):
        return True
    
    class Meta:
        verbose_name = "Chave de API"
        verbose_name_plural = "Chaves de API"