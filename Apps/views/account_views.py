from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from ..Serializers.account_serializers import AccountSerializer
from django.contrib.auth.models import User
from datetime import timedelta, datetime
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import send_mail
from decouple import config


class Account_view:
    @api_view(["GET"])
    @permission_classes([IsAuthenticated])
    def get_Account(request):
        Accounts = User.objects.all()
        serializer = AccountSerializer(Accounts, many=True)
        return Response(serializer.data)

    @api_view(["GET"])
    @permission_classes([IsAuthenticated])
    def get_Accountid(request):
        user = request.user

        # Nếu bạn chỉ muốn trả về thông tin của user hiện tại
        serializer = AccountSerializer(user)
        return Response(serializer.data)

    @api_view(["POST"])
    def create_Account(request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response( {"message": "Create Account success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(["POST"])
    @permission_classes([AllowAny])
    def login(request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Tìm user trong database
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Kiểm tra mật khẩu đã mã hóa
        if not check_password(password, user.password):
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Tạo JWT token
        refresh = RefreshToken.for_user(user)
        # refresh.set_exp(lifetime=timedelta(seconds=10))
        res = Response(
            {"access_token": str(refresh.access_token)},
            status=status.HTTP_200_OK,
        )
        res.set_cookie(
            key="refreshToken",
            value=str(refresh),
            httponly=True,  # Chặn JavaScript truy cập
            # httponly=False,
            # secure=os.getenv("DJANGO_ENV") == "production",
            samesite="Lax",
            secure=False,
            # samesite="Strict",  # Chống CSRF
            # path="/",
            # domain="127.0.0.1",
            # max_age=60 * 60 * 24 * 7,  # Cookie sống 7 ngày
            expires=datetime.utcnow() + timedelta(days=7),
        )
        return res

    @api_view(["Post"])
    def ForgotPassword(request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{config('LINK_RESET_PASSWORD')}/reset/{uid}/{token}/"
            send_mail(
                f"{config('EMAIL_TITLE')}",
                f"{config('EMAIL_MESSAGE')} {reset_link}",
                "noreply@example.com",
                [email],
            )
            return Response({"message": "Check your email."})
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=400)
    @api_view(["PATCH"])
    def ResetPassword(request):
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("password")

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            serializer = AccountSerializer(user,data={"password": new_password},partial=True)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"error": ["Invalid or expired token."]}, status=400)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Password reset successful."})  
            else:
                return Response(serializer.errors, status=400)

        except Exception as e:
            return Response({"error": str(e)}, status=400)
    @api_view(["GET"])
    def Logout(request):
        res = Response({"message": "Logged out"})
        res.delete_cookie("refreshToken")
        return res
