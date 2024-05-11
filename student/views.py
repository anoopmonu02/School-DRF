from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated

class StudentRegistrationView(APIView):
    permission_classes = [IsAuthenticated]
    #parser_classes = [MultiPartParser, FormParser]
    def post(self, request, *args, **kwargs):
        print("REQUEST:::::: ", request.user)
        print("Request Data: ",request.data)
        serializer = StudentRegistrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():           
            registerStudent = serializer.save(updated_by=request.user)
            print("SERIALIZER DATA: ", serializer.data)
            def perform_create(self, serializer):
                print("SERIALIZER DATA: ", serializer.data)
                serializer.save(updated_by=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
""" class StudentRegistrationView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] """

class AcademicStudentView(viewsets.ModelViewSet):
    pass
    """ permission_classes = [IsAuthenticated]
    serializer_class = AcademicStudentSerializer
    queryset = AcademicStudent.objects.all()
    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user) """

class BankAndAadharView(viewsets.ModelViewSet):
    pass
    """ permission_classes = [IsAuthenticated]
    serializer_class = BankAndAadharSerializer
    queryset = BankAndAadhar.objects.all()
    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user) """