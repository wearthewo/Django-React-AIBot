from django.contrib.auth.models import User
from rest_framework import serializers 
from .models import Message  # Import the Message model

class UserSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = ['id', 'username', 'password']  # Specify the fields you want to include in the serialized output 
        extra_kwargs = {
            'password': {'write_only': True}  # do not include password in the serialized output
        } 
    def create(self, validated_data): 
        user = User.objects.create_user(**validated_data) #hash the password
        return user 
    

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'user', 'message', 'response', 'created_at']
        extra_kwargs = {
            'user': {'read_only': True}
        } 
        """  Prevents users from manually setting the user field in API requests.
            The user field will be automatically assigned based on the authenticated user.
            Ensures users can only create messages under their own account. """