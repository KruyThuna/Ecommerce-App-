from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from Karma.models import AccessToken

class QueryParamAccessTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('token')
        if not token:
            raise AuthenticationFailed('Token is required.')

        try:
            access_token = AccessToken.objects.get(token=token, is_active=True)
        except AccessToken.DoesNotExist:
            raise AuthenticationFailed('Invalid or inactive token.')

        # Return anonymous user + token info
        return (AnonymousUser(), access_token)