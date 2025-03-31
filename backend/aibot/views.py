from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, MessageSerializer
from .models import Message
import requests
import os
from dotenv import load_dotenv
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom Login: Sets JWT in HTTP-only cookies"""
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.pop("access")
            refresh_token = response.data.pop("refresh")

            response.set_cookie("access", access_token, httponly=True, samesite="None", secure=False)
            response.set_cookie("refresh", refresh_token, httponly=True, samesite="None", secure=False)
        return response

class CustomTokenRefreshView(TokenRefreshView):
    """Refreshes JWT using Cookies"""
    def post(self, request, *args, **kwargs):
        request.data["refresh"] = request.COOKIES.get("refresh")
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            response.set_cookie("access", response.data["access"], httponly=True, samesite="None", secure=False)
            response.data = {"message": "Token refreshed!"}
        return response

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user_message = serializer.validated_data["message"]
        HF_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}

        response = requests.post(HF_API_URL, headers=headers, json={"inputs": user_message})
        ai_response = response.json().get("generated_text", "Error getting response.")

        serializer.save(user=self.request.user, response=ai_response)

@api_view(["POST"])
def logout(request):
    response = Response({"message": "Logged out successfully"}, status=200)
    response.delete_cookie("access")
    response.delete_cookie("refresh")
    return response 

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_auth(request):
    """Check if the user is authenticated."""
    return Response({"authenticated": True}, status=200)
