from django.shortcuts import render
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import *
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from base.models import *
from rest_framework.generics import ListAPIView

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
        """ category = self.request.data.get('category')
        if category is not None:
            category = Category.objects.get(id=category)
            serializer.save(updated_by=self.request.user, category=category)
        else:
            serializer.save(updated_by=self.request.user) """
        serializer.save(updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
   
    
""" class CastsByCategory(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]    
    def list(self, request, category_pk=None):       
        
        queryset = Cast.objects.all()
        print("-----------------------",category_pk)
        #category_id = self.kwargs.get('category_id')
        if category_pk is not None:
            categoryids = Category.objects.filter(id=category_pk)
            print("-------------------", categoryids[0])
            queryset = queryset.filter(category=categoryids[0])
            serializer_class = CastCategorySerializer(queryset, many=True)
            print("---------------------", queryset)
        return Response(serializer_class.data) """

class CastByCategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        print("-----------------------------------------",request.data)
        category_id = request.data.get('category_id')
        if category_id is None:
            return Response({"error": "Category ID is required in the payload."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not category_id.isdigit():
            return Response({"error": "Category ID must be a valid number."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

        queryset = Cast.objects.filter(category=category)
        serializer = CastSerializer(queryset, many=True)
        return Response(serializer.data)


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
    """ def get_queryset(self):
        
        province_id = self.request.query_params.get('province_id', None)
        if province_id is not None:
            queryset = queryset.filter(province=province_id)
        return queryset """
    
    @action(detail=False, url_path='province/(?P<province_id>\d+)')
    def province_cities(self, request, province_id=None):
        if province_id is None:
            return Response({"error": "Province is required in the payload."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not province_id.isdigit():
            return Response({"error": "Province must be valid"}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = City.objects.filter(province=province_id)
        serializer = CitySerializer(queryset, many=True)
        return Response(serializer.data)