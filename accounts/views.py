from django.shortcuts import render
from rest_framework.generics import GenericAPIView

from accounts.utils import send_code_to_user
from .serializers import UserRegisterSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import OneTimePassword

# Create your views here.
class RegisterUserView(GenericAPIView):
    serializer_class=UserRegisterSerializer
    def post(self,request):
        user_data=request.data
        serializer=self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user=serializer.data
            send_code_to_user(user['email'])
            #send email function user['email']
            print(user)
            return Response({
                'data':user,
                'message':f'hi thanks for signip up a passcode'
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class VerifyUserEmail(GenericAPIView):
    def post(self,request):
        otpcode=request.data.get('otp')
        try:
            user_code_obj=OneTimePassword.objects.get(code=otpcode)
            user = user_code_obj.user
            if not user.is_verified:
                user.is_verified=True
                user.save()
                return Response({
                    'message':'account email verified successfully'
                },status=status.HTTP_200_OK)
            return Response({
                'message':'code is is invalid user already verified'
            },status=status.HTTP_204_NO_CONTENT)
        except OneTimePassword.DoesNotExist:
            return Response({'message':'passcode not provided'},status=status.HTTP_404_NOT_FOUND)
class LoginUserView(GenericAPIView):
    serializer_class=LoginSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
            
