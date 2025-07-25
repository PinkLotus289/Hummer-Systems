import time
import random

from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import PhoneSerializer, VerifySerializer, ProfileSerializer, UseInviteSerializer


verification_codes = {}

@extend_schema(
    request=PhoneSerializer,
    responses={200: PhoneSerializer},
    description="Отправка проверочного кода на номер телефона."
)
class SendCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone_number']

            code = f"{random.randint(1000, 9999)}"
            verification_codes[phone] = code

            time.sleep(2)

            return Response({
                "message": "Код отправлен",
                "phone_number": phone,
                "test_code": code
            })
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=VerifySerializer,
    responses={200: VerifySerializer},
    description="Проверка кода и выдача access токена."
)
class VerifyCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifySerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone_number']
            code = serializer.validated_data['code']

            saved_code = verification_codes.get(phone)
            if not saved_code or saved_code != code:
                return Response({"error": "Неверный код"}, status=status.HTTP_400_BAD_REQUEST)

            # удаляем код после использования
            verification_codes.pop(phone, None)

            user, created = User.objects.get_or_create(phone_number=phone)

            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "phone_number": phone,
                "invite_code": user.invite_code,
                "created": created
            })

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    responses={200: ProfileSerializer},
    description="Получение информации о профиле авторизованного пользователя."
)
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

@extend_schema(
    request=UseInviteSerializer,
    responses={200: UseInviteSerializer},
    description="Активация инвайт-кода. Можно выполнить только один раз."
)
class UseInviteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UseInviteSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['invite_code']
            user = request.user

            if user.used_invite_code:
                return Response({"error": "Вы уже активировали чужой код ранее."},
                                status=status.HTTP_400_BAD_REQUEST)

            if user.invite_code == code:
                return Response({"error": "Нельзя активировать свой собственный инвайт‑код."},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                owner = User.objects.get(invite_code=code)
            except User.DoesNotExist:
                return Response({"error": "Такого инвайт‑кода не существует."},
                                status=status.HTTP_400_BAD_REQUEST)

            user.used_invite_code = code
            user.save()
            return Response({"message": f"Инвайт‑код {code} успешно активирован."})

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
