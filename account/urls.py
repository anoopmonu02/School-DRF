from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

""" router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('login', UserLoginViewSet, basename='login')
router.register('profile', UserProfileViewSet, basename='profile')
#urlpatters = router.urls
urlpatterns = [
    path('api/', include(router.urls)),
] """

router = DefaultRouter()
router.register(r'customers', CustomerProfileView, basename='customers')
router.register(r'branches', BranchView, basename='branches')

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-email/', VerifyUserEmail.as_view(), name='verify-email'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('profile/', TestAuthenticationView.as_view(), name='granted'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password-reset-confirm'),
    path('set-new-password/', SetNewPassword.as_view(), name='set-new-password'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]

urlpatterns+=router.urls