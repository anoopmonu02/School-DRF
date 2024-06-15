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
    def get_queryset(self):
        queryset = Feehead.objects.all()
        branch = self.request.query_params.get('branch', None)
        if branch is not None:
            queryset = queryset.filter(branch_id=branch)

        return queryset
    
    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    @action(detail=False, url_path='branch/(?P<branch_id>\d+)')
    def branch_feeheads(self, request, branch_id=None):
        if branch_id is None:
            return Response({"error": "Branch is required in the payload."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not branch_id.isdigit():
            return Response({"error": "Branch ID must be valid"}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = Feehead.objects.filter(branch=branch_id)   

        serializer_class = FeeHeadSerializer(queryset, many=True)
        print(serializer_class.data)
        return Response(serializer_class.data)

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
            existing_instance = FeeClassMap.objects.filter(
                grade_id=int(request.data.get('grade')),
                academicYear_id=int(request.data.get('academicYear')),
                branch_id=int(request.data.get('branch'))
            ).first()
            print("existing_instance ",existing_instance)
            if existing_instance:
                #check any value updated
                fee_class_map_amount_existing = existing_instance.fee_class_amount_map_fee_class.all()#FeeClassAmountMap.objects.filter(feeClassMap=existing_instance).first()
                print("fee_class_map_amount_existing ",existing_instance.fee_class_amount_map_fee_class.all())                
                fee_class_map_amount_existing.delete()
                fee_class_amount_map_fee_class_data = request.data.get('fee_class_amount_map_fee_class',[])
                serializer = FeeClassAmountMapSerializer(data=fee_class_amount_map_fee_class_data, context={'request': request}, many=True)#feeClassMap=existing_instance,
                if serializer.is_valid():
                    serializer.save(feeClassMap=existing_instance, updated_by=request.user)                
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                serializer.errors
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                #check any new value inserted
            else:
                serializer = self.serializer_class(data=request.data, context={'request': request})            
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

            fee_data = serializer.data

            # Retrieve existing child entries
            existing_heads_ids = fee_class_amounts.values_list('feehead', flat=True)

            # Query new heads introduced by the user (excluding existing heads)
            new_heads = Feehead.objects.exclude(id__in=existing_heads_ids)

            # Create a dictionary to hold the new heads data with amount set to 0
            new_heads_data = [{'feehead': head.id, 'head_name': head.feehead_name, 'amount': 0.00} for head in new_heads]

            # Combine the existing fee data with the new heads data
            fee_data += new_heads_data

            return fee_data
        except FeeClassMap.DoesNotExist:
            feeheads = Feehead.objects.all()
            default_fee_data = [{'feehead': feehead.id,'feename': feehead.feehead_name, 'amount': 0.00} for feehead in feeheads]
            return default_fee_data

    def get(self, request):
        print(request.query_params)
        grade_id = request.query_params.get('grade')
        academic_year_id = request.query_params.get('academicYear')
        branch_id = request.query_params.get('branch')
        tabledata = []        
        try:
            if request.query_params.get('filterdata') and request.query_params.get('filterdata') == '1':
                fee_class_maps = FeeClassMap.objects.select_related('grade').prefetch_related('fee_class_amount_map_fee_class').filter(academicYear_id=academic_year_id, branch_id=branch_id)                
                for fee_class_map in fee_class_maps:
                    grade = fee_class_map.grade
                    for fee_class_amount_map in fee_class_map.fee_class_amount_map_fee_class.all():
                        fee_head = fee_class_amount_map.feehead
                        amount = fee_class_amount_map.amount
                        tabledata.append({'grade': grade.grade_name, 'fee_head': fee_head.feehead_name, 'amount': amount})
                print("tabledata ",tabledata)
                if not tabledata:
                    return Response({'message': 'No data found for Fee-Class Map'}, status=status.HTTP_204_NO_CONTENT)
                data = {
                    "table_data": tabledata    
                }
                return Response(data, status=status.HTTP_200_OK)
            if not (grade_id and academic_year_id and branch_id):
                    return Response({'error': 'Please provide grade, academicYear, and branch'}, status=status.HTTP_400_BAD_REQUEST)
            fee_data = self.get_fee_data(grade_id, academic_year_id, branch_id)
            if not fee_data:
                return Response({'error': 'No data found for given class, branch'}, status=status.HTTP_204_NO_CONTENT)    
            data = {
                "fee_data": fee_data 
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class FeeMonthMappingView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FeeMonthMappingSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        print("data ",data)
        # Ensure data is a list of records
        if not isinstance(data, list):
            return Response({"detail": "Expected a list of records"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=data, many=True)  # Initialize the serializer with the data
        serializer.is_valid(raise_exception=True)  # Validate the data

        # Perform bulk creation
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def list(self, request, *args, **kwargs):
        print(request.query_params);
        academic_year_id = request.query_params.get('academicYear')
        branch_id = request.query_params.get('branch')
        feehead_id = request.query_params.get('feeHead')
        feemonthmapdata = []
        try:
            if request.query_params.get('filtertabledata') and request.query_params.get('filtertabledata') == '1':
                pass
            else:
                if not (feehead_id and academic_year_id and branch_id):
                    return Response({'error': 'Please provide feeHead, academicYear, and branch'}, status=status.HTTP_400_BAD_REQUEST)
                feeMonthMaps = FeeMonthMap.objects.filter(academicYear_id=academic_year_id, branch_id=branch_id, feeHead_id = feehead_id)
                print(feeMonthMaps)
                serializer = FeeMonthMappingSerializer(feeMonthMaps, many=True)
                if not feeMonthMaps:
                    months = Month_Master.objects.all()
                    months_data = [{'month_id': month.id, 'month_name': month.month_name} for month in months]
                    #feeMonthMaps += months_data
                    print(f"months_data: {months_data}")
                    if not months_data:
                        return Response({'error': 'No data found for given fee, branch'}, status=status.HTTP_204_NO_CONTENT)    
                    data = {
                        "months_data": months_data 
                    }
                    return Response(data, status=status.HTTP_200_OK)
                
                return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        pass
    
    """ def get_queryset(self):
        queryset = FeeMonthMap.objects.all()
        branch = self.request.query_params.get('branch', None)
        if branch is not None:
            queryset = queryset.filter(branch_id=branch)

        return queryset """
    
    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)        
