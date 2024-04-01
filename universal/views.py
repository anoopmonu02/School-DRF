from django.shortcuts import render
from .serializers import *
from rest_framework.response import Response
from .models import *
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from base.models import *

class BankView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BankSerializer
    queryset = Bank.objects.all()

class MediumView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MediumSerializer
    queryset = Medium.objects.all()

class CategoryView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class CastView(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated]
    serializer_class = CastSerializer
    queryset = Cast.objects.all()

class MonthMasterView(viewsets.ModelViewSet):   
    permission_classes = [IsAuthenticated] 
    serializer_class = Month_MasterSerializer
    queryset = Month_Master.objects.all()


class ProvinceView(viewsets.ModelViewSet):   
    permission_classes = [IsAuthenticated] 
    serializer_class = ProvinceSerializer
    queryset = Province.objects.all()

class CityView(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated]
    serializer_class = CitySerializer
    queryset = City.objects.all()