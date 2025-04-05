from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Get the access token from cookies
        access_token = request.COOKIES.get('access')
        
        if access_token:
            # If the access token is in cookies, authenticate it
            return self.get_user_and_token(access_token)
        return None