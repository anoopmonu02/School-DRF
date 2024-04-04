from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .serializers import *
from .models import *

# Create your views here.

class GradeViewSet(viewsets.ModelViewSet):
    serializer_class = GradeSerializer
    queryset = Grade.objects.all()

class SectionViewSet(viewsets.ModelViewSet):
    serializer_class = SectionSerializer
    queryset = Section.objects.all()

class FeeHeadViewSet(viewsets.ModelViewSet):
    serializer_class = FeeHeadSerializer
    queryset = Feehead.objects.all()

class DiscountHeadViewSet(viewsets.ModelViewSet):
    serializer_class = DiscountheadSerializer
    queryset = Discounthead.objects.all()

class FineheadViewSet(viewsets.ModelViewSet):
    serializer_class = FineheadSerializer
    queryset = Finehead.objects.all()


class AcademicyearViewSet(viewsets.ModelViewSet):
    serializer_class = AcademicyearSerializer
    queryset = Academicyear.objects.all()

class FineViewSet(viewsets.ModelViewSet):
    serializer_class = FineSerializer
    queryset = Fine.objects.all()