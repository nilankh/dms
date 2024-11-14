from django.shortcuts import render
from rest_framework.views import APIView
from user.models import DMSUser
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response


# Create your views here.
class LoginAPIView(APIView):
    """
    API endpoint for user login.
    """

    def post(self, request):

        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = DMSUser.objects.get(email=email)
            print("line 242", user.password, user.check_password(password))
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)

                return Response({"token": token.key}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except DMSUser.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
