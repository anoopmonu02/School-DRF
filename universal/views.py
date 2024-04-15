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
    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class MediumView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MediumSerializer
    queryset = Medium.objects.all()

    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class CategoryView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class CastView(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated]
    serializer_class = CastSerializer
    queryset = Cast.objects.all()
    def perform_create(self, serializer):
        category = self.request.data.get('category')
        if category is not None:
            category = Category.objects.get(id=category)
            serializer.save(updated_by=self.request.user, category=category)
        else:
            serializer.save(updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class MonthMasterView(viewsets.ModelViewSet):   
    permission_classes = [IsAuthenticated] 
    serializer_class = Month_MasterSerializer
    queryset = Month_Master.objects.all()
    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class ProvinceView(viewsets.ModelViewSet):   
    #permission_classes = [IsAuthenticated] 
    serializer_class = ProvinceSerializer
    queryset = Province.objects.all()
    """ def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user) """

class CityView(viewsets.ModelViewSet):    
    #permission_classes = [IsAuthenticated]
    serializer_class = CitySerializer
    queryset = City.objects.all()
    """ def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user) """