from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

class StudentRegistrationView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request, *args, **kwargs):
        print("REQUEST:::::: ", request)
        print("Request Data: ",request.data)
        serializer = StudentRegistrationSerializer(data=request.data, files=request.FILES)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
""" class StudentRegistrationView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] """