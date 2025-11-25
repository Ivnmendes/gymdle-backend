from rest_framework import authentication
from rest_framework import exceptions
from .models import APIKey

class APIKeyAuthentication(authentication.BaseAuthentication):
    """
    Autentica requisições verificando o cabeçalho 'X-API-Key'.
    """
    
    def authenticate(self, request):
        api_key_header = request.META.get('HTTP_X_API_KEY')
        
        if not api_key_header:
            return None 

        try:
            api_key_obj = APIKey.objects.get(
                key=api_key_header, 
                is_active=True
            )
        except APIKey.DoesNotExist:
            raise exceptions.AuthenticationFailed('Chave de API inválida ou inativa.')

        service = api_key_obj.service if api_key_obj.service else None
        
        return (api_key_obj, api_key_header)