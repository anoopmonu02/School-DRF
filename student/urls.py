from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
urlpatterns = [
    path('student-registration/', StudentRegistrationView.as_view(), name='student-registration'),
]
urlpatterns+=router.urls