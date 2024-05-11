from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
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

    @action(detail=False, url_path='csession/(?P<branch_id>\d+)')
    def branch_currtent_session(self, request, branch_id=None):
        if branch_id is None:
            return Response({"error": "Branch is required in the payload."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not branch_id.isdigit():
            return Response({"error": "Branch ID must be valid"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            academicyear = Academicyear.objects.filter(branch=branch_id).first()
            if academicyear:
                serializer = AcademicyearSerializer(academicyear)
                return Response(serializer.data)
            else:
                return Response({"error": "Academic year not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

class FineViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FineSerializer
    queryset = Fine.objects.all()

class MonthMappingView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MonthMappingSerializer
    queryset = MonthMapping.objects.all()
    def post(self, request):
        print(request.data)
        serializer = MonthMappingSerializer(data=request.data, many=True, context={'request': request})        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Mapping created successfully.'}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
        
    def delete(self, request):
        try:
            print(request.data)
            mapping = MonthMapping.objects.filter(academicYear=request.data.get('academicYear'), branch=request.data.get('branch'))
            if mapping.exists():
                mapping.delete()
                monthmappingcount = MonthMapping.objects.filter(academicYear=request.data.get('academicYear'), branch=request.data.get('branch')).count()
                if monthmappingcount == 0:
                    return Response({'message': 'Mapping deleted successfully.'}, status=status.HTTP_200_OK)
                return Response({'error': 'Mapping not deleted successfully. Error occurred!'}, status=status.HTTP_206_PARTIAL_CONTENT)
            else:
                return Response({'error': 'No mappings found for the specified Academic year and Branch.'}, status=status.HTTP_404_NOT_FOUND)
        except MonthMapping.DoesNotExist:
            return Response({'error': 'Mapping does not exist.'}, status=status.HTTP_404_NOT_FOUND) 
        
    def get(self, request):
        print(request.query_params)
        print(request.query_params.get('academicYear'))
        print(request.query_params.get('branch'))
        mapping = MonthMapping.objects.filter(academicYear=request.query_params.get('academicYear'), branch=request.query_params.get('branch'))
        print(mapping)
        serializer = MonthMappingSerializer(mapping, many=True)        
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'No Data found'}, status=status.HTTP_404_NOT_FOUND) 
    
class FeeClassMappingView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeeClassMapSerializer
    queryset = FeeClassMap.objects.all()
    def post(self, request):
        try:
            print(request.data)
            serializer = self.serializer_class(data=request.data, context={'request': request})
            print(serializer)
            if serializer.is_valid():
                serializer.save(updated_by=request.user)                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            serializer.errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get_fee_data(self, grade_id, academic_year_id, branch_id):
        try:
            fee_class_map = FeeClassMap.objects.get(grade_id=int(grade_id), academicYear_id=int(academic_year_id), branch_id=int(branch_id))
            fee_class_amounts = FeeClassAmountMap.objects.filter(feeClassMap_id=fee_class_map.id)
            serializer = FeeClassAmountMapSerializer(fee_class_amounts, many=True)
            return serializer.data
        except FeeClassMap.DoesNotExist:
            feeheads = Feehead.objects.all()
            default_fee_data = [{'feehead': feehead.id,'feename': feehead.feehead_name, 'amount': 0.00} for feehead in feeheads]
            return default_fee_data

    def get(self, request):
        print(request.query_params)
        grade_id = request.query_params.get('grade')
        academic_year_id = request.query_params.get('academicYear')
        branch_id = request.query_params.get('branch')

        if not (grade_id and academic_year_id and branch_id):
            return Response({'error': 'Please provide grade, academicYear, and branch'}, status=status.HTTP_400_BAD_REQUEST)

        fee_data = self.get_fee_data(grade_id, academic_year_id, branch_id)
        return Response(fee_data, status=status.HTTP_200_OK)