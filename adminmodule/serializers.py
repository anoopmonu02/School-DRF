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
        exclude = ['created_at','updated_at']

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        exclude = ['created_at','updated_at']

class FeeHeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feehead
        exclude = ['created_at','updated_at']

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
        exclude = ['created_at','updated_at']

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
        exclude = ['created_at','updated_at']

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
        exclude = ['created_at','updated_at']
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