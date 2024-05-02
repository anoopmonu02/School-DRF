from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class GradeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GradeSerializer
    queryset = Grade.objects.all()
    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    @action(detail=False, url_path='branch/(?P<branch_id>\d+)')
    def branch_grades(self, request, branch_id=None):
        if branch_id is None:
            return Response({"error": "Branch is required in the payload."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not branch_id.isdigit():
            return Response({"error": "Branch ID must be valid"}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = Grade.objects.filter(branch=branch_id)
        serializer = GradeSerializer(queryset, many=True)
        return Response(serializer.data)

class SectionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    @action(detail=False, url_path='branch/(?P<branch_id>\d+)')
    def branch_sections(self, request, branch_id=None):
        if branch_id is None:
            return Response({"error": "Branch is required in the payload."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not branch_id.isdigit():
            return Response({"error": "Branch ID must be valid"}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = Section.objects.filter(branch=branch_id)
        serializer = SectionSerializer(queryset, many=True)
        return Response(serializer.data)

class FeeHeadViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FeeHeadSerializer
    queryset = Feehead.objects.all()
    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class DiscountHeadViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DiscountheadSerializer
    queryset = Discounthead.objects.all()
    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class FineheadViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FineheadSerializer
    queryset = Finehead.objects.all()
    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class AcademicyearViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AcademicyearSerializer
    queryset = Academicyear.objects.all()
    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    

class FineViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FineSerializer
    queryset = Fine.objects.all()