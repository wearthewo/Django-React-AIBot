from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, MessageSerializer
from .models import Message
import requests
from django.views.decorators.csrf import csrf_exempt
import os
from dotenv import load_dotenv
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response 
from django.utils.decorators import method_decorator




load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")
@method_decorator(csrf_exempt, name='dispatch')
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
@method_decorator(csrf_exempt, name='dispatch')
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
@method_decorator(csrf_exempt, name='dispatch')
class CustomTokenRefreshView(TokenRefreshView):
    """Refreshes JWT using Cookies"""
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token missing"}, status=400)
        request.data["refresh"] = refresh_token
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            response.set_cookie("access", response.data["access"], httponly=True, samesite="None", secure=False)
            response.data = {"message": "Token refreshed!"}
        return response
@method_decorator(csrf_exempt, name='dispatch')
class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user_message = serializer.validated_data["message"]
        HF_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}

        response = requests.post(HF_API_URL, headers=headers, json={"inputs": user_message})
        ai_response = response.json()[0].get("generated_text", "Error getting response.")
        serializer.save(user=self.request.user, response=ai_response)

@api_view(["POST"])
@csrf_exempt
def logout(request):
    response = Response({"message": "Logged out successfully"}, status=200)
    response.delete_cookie("access")
    response.delete_cookie("refresh")
    return response 

@api_view(["GET"])
@csrf_exempt
#@permission_classes([IsAuthenticated])
def check_auth(request):
    """Check if the user is authenticated."""
    return Response({"authenticated": True}, status=200)
