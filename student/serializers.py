import datetime
from rest_framework import serializers
from .models import *
import re


#Custom validation methods
def checkSpecialCharsInString(obj_field_name, obj_label):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if not regex.search(obj_field_name) == None:
        raise serializers.ValidationError(f"{obj_label} can't contains special characters")
    

def checkValidLenthofField(obj_field_name, char_length, obj_label):
    if len(obj_field_name)<char_length:
        raise serializers.ValidationError(f"{obj_label} length must be greater than {char_length-1} char.")
    
def checkAadharNoLength(obj_field_name, obj_label):
    if len(obj_field_name)<12 or len(obj_field_name)>12:
        raise serializers.ValidationError(f"{obj_label} length is not valid.")
    

def checkAnyNumberInString(obj_field_name, obj_label):
    if bool(re.search(r'\d', obj_field_name)):
        raise serializers.ValidationError(f"{obj_label} can't contains numeric(s).")


class BankAndAadharSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAndAadhar
        exclude = ['created_at','updated_at','updated_by']

        def validate_aadhar_number(self, data):
            if data:
                aadhar_number = data
                checkSpecialCharsInString(aadhar_number, 'Aadhar number')
                checkAadharNoLength(aadhar_number, 'Aadhar number')
            return data

class AcademicStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicStudent
        exclude = ['created_at','updated_at','updated_by']

class StudentRegistrationSerializer(serializers.ModelSerializer):
    bankAndAadhar = BankAndAadharSerializer(many=False)
    academicStudent = AcademicStudentSerializer(many=True)

    class Meta:
        model = RegisterStudent
        exclude = ['created_at','updated_at','updated_by']

    def create(self, validated_data):
        bankAndAadhar = validated_data.pop('BankAndAadhar')
        academicStudent = validated_data.pop('AcademicStudent')
        user = self.context['request'].user
        student = RegisterStudent.objects.create(user=user, **validated_data)
        academicStudent.objects.create(student=student, **academicStudent)
        bankAndAadhar.objects.create(student=student, **bankAndAadhar)
        return student