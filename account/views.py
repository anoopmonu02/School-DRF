from django.shortcuts import render
from .serializers import *
from rest_framework.response import Response
from .models import *
from rest_framework.generics import GenericAPIView
from rest_framework import status, viewsets
from account.renderers  import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
""" from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator """
from account.utils import Util


""" class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = MyCustomUser.objects.all()


class UserLoginViewSet(viewsets.ModelViewSet):   
    serializer_class = LoginSerializer
    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get_queryset(self):
        pass
    


class UserProfileViewSet(viewsets.ModelViewSet):    
    serializer_class = UserProfileSerializer
    queryset = MyCustomUser.objects.all()
    permission_classes = [IsAuthenticated]
 """
class RegisterUserView(GenericAPIView):

    serializer_class = UserRegisterSerializer
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            try:

                #if email needed - we can write here the logic
                """ uid = urlsafe_base64_encode(force_bytes(user.id))
                print('Encoded id ', uid)
                token = PasswordResetTokenGenerator().make_token(user)
                print('Password reset token: ', token)
                link = 'http://localhost:3000/api/users/password-reset/' + uid + '/' + token
                print('Password reset link: ', link) """
                #send email
                """ data = {
                    'subject': 'User Registration Successful',
                    'body': f'Hi {user.name}, Click the link below to reset your password \n\n{link}',
                    'to': [user.email]
                } """
                data = {
                    'subject': 'User Registration Successful',
                    'body': f'Hi {user.name}, Congratulation to register successfully. \n\n',
                    'to': [user.email]
                }
                Util.send_email(data)
                emailMessage = "Email sent successfully, Plesae check your inbox."
            except Exception as e:
                emailMessage = f"Error occurred: {e}"
            # if user created immediatly generate token for him or we can verify first and then generate token on login     
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserRegisterSerializer(user).data,
                    'message':'Signup Successful',
                    'emailMessage':emailMessage
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# to verify email     
class VerifyUserEmail(GenericAPIView):
    def post(self, request):
        otpcode = request.data.get('otpcode')
        try:
            user_obj = MyCustomUser.objects.get(email=otpcode)
            if not user_obj.is_verified:
                user_obj.is_verified = True
                user_obj.save() 
                # uncomment the email send code if want to verify via email
                return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid or expired OTP'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'message': f'Error occurred: {e}, Email not verified'}, status=status.HTTP_404_NOT_FOUND)
        
# for Login
class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        print(request.data)
        serializers = self.serializer_class(data=request.data, context={'request': request})
        serializers.is_valid(raise_exception=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
#for test view
class TestAuthenticationView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            'msg':'its working'
        }
        return Response(data, status=status.HTTP_200_OK)

# for reset password    
class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={ 'request': request })
        serializer.is_valid(raise_exception=True)
        return Response({'messsage': "Reset password link sent to your email successfully"}, status=status.HTTP_200_OK)
    
class PasswordResetConfirm(GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = MyCustomUser.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        except(TypeError, ValueError, OverflowError, MyCustomUser.DoesNotExist, DjangoUnicodeDecodeError):            
            return Response({'error': 'Token is not valid, please request a new one!'}, status=status.HTTP_401_UNAUTHORIZED)

class SetNewPassword(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
    
class LogoutUserView(GenericAPIView):
    serializer_class = LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'User logged out successfully'}, status=status.HTTP_204_NO_CONTENT)
    
#For Customer
class CustomerProfileView(viewsets.ModelViewSet):
    serializer_class = CustomerProfileSerializer
    queryset = CustomerProfile.objects.all()
    
""" 
    def get(self, request):
        serializer = self.serializer_class(data=request.data)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Customer Profile Created!'}, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        serializer = self.serializer_class(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data) """

#for Branch
class BranchView(viewsets.ModelViewSet):
    serializer_class = BranchSeralizer
    queryset = Branch.objects.all()