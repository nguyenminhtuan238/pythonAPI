import jwt
from django.http import JsonResponse
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User

class JWTAndAPIKeyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.headers.get('Authorization')
        api_key = request.headers.get('X-API-Key')
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                decoded_token = AccessToken(token)
                user = get_object_or_404(User, id=decoded_token['user_id'])
                request.user = user
                return
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=401)
        
        elif api_key and api_key == settings.API_KEY:
            request.user = AnonymousUser()
            return
        
        return JsonResponse({'error': 'Unauthorized'}, status=401)