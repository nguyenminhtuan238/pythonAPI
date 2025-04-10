from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class Jwt_view:
    @api_view(["POST"])
    def RefreshTokenView(request):
        refresh_token = request.COOKIES.get("refreshToken")
        if not refresh_token:
            return Response({"error": "No refresh token"}, status=403)

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = refresh.access_token
            return Response({"access_token": str(new_access_token)})
        except:
            return Response({"error": "Invalid refresh token"}, status=403)

 