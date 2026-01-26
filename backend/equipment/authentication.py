from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from django.conf import settings

class SimpleAPIKeyAuthentication(BaseAuthentication):
    """
    Simple API key authentication for demo purposes.
    In production, use proper authentication methods.
    """
    
    def authenticate(self, request):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            # No API key provided, allow anonymous access for demo
            return None
        
        # Simple validation - in production, use proper API key management
        if api_key != settings.SIMPLE_API_KEY:
            raise AuthenticationFailed('Invalid API key')
        
        # Return a dummy user for API key authentication
        try:
            user = User.objects.get(username='api_user')
        except User.DoesNotExist:
            user = User.objects.create_user('api_user', 'api@example.com', 'api_password')
        
        return (user, None)
