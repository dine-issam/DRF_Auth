from base64 import urlsafe_b64encode
from readline import get_current_history_length
from rest_framework import serializers

from accounts.utils import send_normal_email
from .models import User        
from django.contrib.auth import authenticate
from django.urls import reverse
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes


class UserRegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=68,min_length=6,write_only=True)
    password2=serializers.CharField(max_length=68,min_length=6,write_only=True)

    class Meta:
        model = User
        fields=['email','first_name','last_name','password','password2']

    def validate(self, attrs):
        password=attrs.get('password','')
        password2=attrs.get('password2','')
        if password != password2:
            raise serializers.ValidationError("passwords not match")
        return attrs
    


    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data.get('password')
            )
        return user

class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255,min_length=6)
    password=serializers.CharField(max_length=68,write_only=True)
    full_name=serializers.CharField(max_length=255,read_only=True)
    access_token=serializers.CharField(max_length=255,read_only=True)
    refresh_token=serializers.CharField(max_length=255,read_only=True)

    class Meta:
        model=User
        fields=['email','password','full_name','access_token','refresh_token']
    def validate(self, attrs):
        email = attrs.get('email')
        password=attrs.get('password')
        request=self.context.get('request')
        user=authenticate(request,email=email,password=password)
        if not user:
            raise AuthenticationFailed("invalide credentials try again fuck you")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified ")
        user_tokens=user.tokens()

        return {
            'email':user.email,
            'full_name':user.get_full_name,
            "access_token": str(user_tokens.get('access')),
            "refresh_token":str(user_tokens.get('refresh'))
        }

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user= User.objects.get(email=email)
            uidb64=urlsafe_b64encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request=self.context.get('request')
            current_site=get_current_history_length(request).domain
            relative_link =reverse('reset-password-confirm', kwargs={'uidb64':uidb64, 'token':token})
            abslink=f"http://{current_site}{relative_link}"
            print(abslink)
            email_body=f"Hi {user.first_name} use the link below to reset your password {abslink}"
            data={
                'email_body':email_body, 
                'email_subject':"Reset your Password", 
                'to_email':user.email
                }
            send_normal_email(data)

        return super().validate(attrs)
    

