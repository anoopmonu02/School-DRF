from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import send_normal_email

from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, min_length=8, write_only=True)
    password2 = serializers.CharField(max_length=100, min_length=8, write_only=True)

    class Meta:
        model = MyCustomUser
        fields = ['email','name', 'password','password2']

    def validate(self, attrs):
        password = attrs.get('password','')        
        password2 = attrs.get('password2','')
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        return attrs
    
    def create(self, validated_data):
        user = MyCustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name']
        )

        return user
    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(max_length=100, min_length=8, write_only=True)
    name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model=MyCustomUser
        fields=['email','password','name','access_token','refresh_token']

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }
    
    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')
        request = self.context['request']
        user=authenticate(request, username=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        token = self.get_tokens(user)
        return {
            "email": user.email,
            "name": user.get_full_name,
            "access_token": str(token.get('access_token')),
            "refresh_token": str(token.get('refresh_token'))
        }
    
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=6)

    class Meta:
        fields=['email']
    
    def validate(self, attrs):
        email = attrs.get('email')
        if not MyCustomUser.objects.filter(email=email).exists():
            raise AuthenticationFailed('No user found with this email')
        user = MyCustomUser.objects.get(email=email)
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        request = self.context.get('request')
        site_domain = get_current_site(request=request).domain
        relativeLink = reverse('password-reset-confirm',kwargs={'uidb64':uidb64,'token':token})
        absolute_url = f"http://{site_domain}{relativeLink}"
        email_body = 'Hello, \n Use link below to reset your password  \n' + absolute_url
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Reset your password'
        }
        send_normal_email(data)

        return super().validate(attrs)
    
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100, min_length=8, write_only=True)
    confirm_password = serializers.CharField(max_length=100, min_length=8, write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = ['password', 'confirm_password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            uidb64 = attrs.get('uidb64')
            token = attrs.get('token')

            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = MyCustomUser.objects.get(id=user_id)
            """ print(user)
            print(PasswordResetTokenGenerator().check_token(user, token))
            print('password:',password)
            print('confirm_password:',confirm_password) 
            print(password != confirm_password) """
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError({'token': 'Reset link is invalid or has expired!'})
                #raise AuthenticationFailed('Reset link is invalid or has expired!')  
            if password != confirm_password:
                raise serializers.ValidationError({'token':'Passwords do not match!', })
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            print(e)
            raise serializers.ValidationError({'token': f'Reset link is invalid or has expired.{e}'}) 
        

class LogoutUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Invalid or expired refresh token.')
    }

    def validate(self, attrs):
        self.token = attrs['refresh_token']
        return attrs
    
    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')
        

class CustomerProfileSerializer(serializers.ModelSerializer):   
    class Meta:
        model = CustomerProfile
        fields = '__all__'


class BranchSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

    def validate(self, attrs):
        return super().validate(attrs)

        