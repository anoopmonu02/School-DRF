import datetime
from rest_framework import serializers
from .models import *
import re


def checkSpecialCharsInString(obj_field_name, obj_label):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if not regex.search(obj_field_name) == None:
        raise serializers.ValidationError(f"{obj_label} can't contains special characters")
    

def checkValidLenthofField(obj_field_name, char_length, obj_label):
    if len(obj_field_name)<char_length:
        raise serializers.ValidationError(f"{obj_label} length must be greater than {char_length-1} char.")
    

def checkAnyNumberInString(obj_field_name, obj_label):
    if bool(re.search(r'\d', obj_field_name)):
        raise serializers.ValidationError(f"{obj_label} can't contains numeric(s).")
    

class CustomDateFormatField(serializers.DateField):
    def to_representation(self, value):
        # Convert date to the "DD-MMM-YYYY" format when serializing
        if value:
            return value.strftime('%d-%b-%Y')
        return None

    def to_internal_value(self, data):
        # Convert input data in "DD-MMM-YYYY" format to a Python date object
        try:
            return datetime.strptime(data, '%d-%b-%Y').date()
        except ValueError:
            self.fail('invalid')

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        exclude = ['created_at','updated_at','updated_by']

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        exclude = ['created_at','updated_at','updated_by']

class FeeHeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feehead
        exclude = ['created_at','updated_at','updated_by']

    def validate_feehead_name(self, data):
        if data:
            feehead_name = data
            checkSpecialCharsInString(feehead_name, 'Feehead name')
            checkValidLenthofField(feehead_name, 3, 'Feehead name')
            checkAnyNumberInString(feehead_name, 'Feehead name')            

        return data

class DiscountheadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discounthead
        exclude = ['created_at','updated_at','updated_by']

    def validate_discount_name(self, data):
        if data:
            discount_name = data
            checkSpecialCharsInString(discount_name, 'Discounthead name')
            checkValidLenthofField(discount_name, 3, 'Discounthead name')
            checkAnyNumberInString(discount_name, 'Discounthead name')            

        return data
    
class FineheadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finehead
        exclude = ['created_at','updated_at','updated_by']

    def validate_fine_name(self, data):
        if data:
            fine_name = data
            checkSpecialCharsInString(fine_name, 'Fine name')
            checkValidLenthofField(fine_name, 3, 'Fine name')
            checkAnyNumberInString(fine_name, 'Fine name')            

        return data

class AcademicyearSerializer(serializers.ModelSerializer):
    """ session_startdate = serializers.DateField(format='%d-%b-%Y')
    session_enddate = serializers.DateField(format='%d-%b-%Y') """
    #print(f'{session_startdate}======{session_enddate}')

    # Using default format - YYYY-MM-DD
    class Meta:
        model = Academicyear
        exclude = ['created_at','updated_at','updated_by']
        read_only_fields = ['slug']

    def validate(self, data):
        if data['session_startdate'] > data['session_enddate']:
            raise serializers.ValidationError("Start date cannot be after end date")
        return data
    
class FineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fine
        exclude = ['created_at','updated_at']

    def validate(self, data):
        if data['fine_amount']<0:
            raise serializers.ValidationError("Fine amount cannot be negative.")        
        return data
    
class MonthMappingSerializer(serializers.ModelSerializer):
    priority = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    academicYear_format = serializers.CharField(source='academicYear.session_displayformat', read_only=True)
    class Meta:
        model = MonthMapping
        fields = ['id','monthName','monthCode','branch','academicYear', 'priority','academicYear_format']
    def create(self, validated_data):        
        print("validated data ",validated_data)
        user = self.context['request'].user
        validated_data['updated_by'] = user      

        return super().create(validated_data)      

""" class FeeClassMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeClassMap
        fields = '__all__'

    def validate(self, attrs):
        print("attrs<><<> ",attrs)
        return super().validate(attrs)
    
    def create(self, validated_data):
        print("validated data::: ",validated_data)
        validated_data['updated_by'] = self.context['request'].user
        return validated_data


class FeeClassAmountMapSerializer(serializers.ModelSerializer):
    head_name = serializers.CharField(source='feehead.feehead_name', read_only=True)
    class Meta:
        model = FeeClassAmountMap
        fields = ['id','feehead','head_name', 'amount']

    def create(self, validated_data):
        print("validated data>>>> ",validated_data)
        validated_data['updated_by'] = self.context['request'].user
        return validated_data """
    

class FeeClassAmountMapSerializer(serializers.ModelSerializer):
    head_name = serializers.CharField(source='feehead.feehead_name', read_only=True)
    class Meta:
        model = FeeClassAmountMap
        fields = ['id','feehead','head_name', 'amount']

class FeeClassMapSerializer(serializers.ModelSerializer):
    fee_class_amount_map_fee_class = FeeClassAmountMapSerializer(many=True, required=False)  # Nested serializer for child model

    class Meta:
        model = FeeClassMap
        fields = ['id','grade', 'academicYear', 'branch', 'fee_class_amount_map_fee_class']

    def create(self, validated_data):
        user = self.context['request'].user
        fee_class_amount_maps_data = validated_data.pop('fee_class_amount_map_fee_class',[])  # Extract child data

        existing_instance = FeeClassMap.objects.filter(
            grade=validated_data['grade'],
            academicYear=validated_data['academicYear'],
            branch=validated_data['branch']
        ).first()
        print("existing_instance ",existing_instance)
        if existing_instance:
            existing_instance.fee_class_amount_map_fee_class.all().delete()  # Delete all child objects
            fee_class_amount_maps_data = [
                fee_data for fee_data in fee_class_amount_maps_data if fee_data.get('amount', 0) != 0
            ]
            for fee_data in fee_class_amount_maps_data:
                fee_data['updated_by'] = user
                FeeClassAmountMap.objects.create(feeClassMap=existing_instance, **fee_data)  # Create child objects
            return existing_instance
        else:
            fee_class_map = FeeClassMap.objects.create(**validated_data)  # Create parent object        
            # Filter out records with amount 0
            fee_class_amount_maps_data = [
                fee_data for fee_data in fee_class_amount_maps_data if fee_data.get('amount', 0) != 0
            ]
            print("fee_class_amount_maps_data after ", fee_class_amount_maps_data)
            for fee_class_amount_map_data in fee_class_amount_maps_data:
                fee_class_amount_map_data['updated_by'] = user
                FeeClassAmountMap.objects.create(feeClassMap=fee_class_map, **fee_class_amount_map_data)  # Create child objects

            return fee_class_map
        
class FeeMonthMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeMonthMap
        exclude = ['created_at','updated_at']   