import datetime
from rest_framework import serializers
from .models import *
from universal.models import *
from adminmodule.models import *
from account.models import *
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
    medium_id = serializers.IntegerField(write_only=True)
    grade_id = serializers.IntegerField(write_only=True)
    section_id = serializers.IntegerField(write_only=True)
    branch_id = serializers.IntegerField(write_only=True)
    academic_year_id = serializers.IntegerField(write_only=True)
    registerFlag = serializers.BooleanField(write_only=True)

    class Meta:
        model = AcademicStudent
        exclude = ['created_at','updated_at','updated_by','registerflag']

    def create(self, validated_data):
        print("In create method of AcademicStudentSerializer------------",validated_data)
        registerflag = validated_data.pop('registerflag', None)
        medium_id = validated_data.pop('medium', None)
        grade_id = validated_data.pop('grade', None)
        section_id = validated_data.pop('section', None)
        branch_id = validated_data.pop('branch', None)
        academic_year_id = validated_data.pop('academic_year', None)

        if(registerflag):
            academic_student = AcademicStudent.objects.create(**validated_data)
        else:
            academic_student = super().create(validated_data)
            if medium_id:
                medium = Medium.objects.get(pk=medium_id)
                academic_student.medium = medium

            if grade_id:
                grade = Grade.objects.get(pk=grade_id)
                academic_student.grade = grade

            if section_id:
                section = Section.objects.get(pk=section_id)
                academic_student.section = section

            if branch_id:
                branch = Branch.objects.get(pk=branch_id)
                academic_student.branch = branch    
            
            if academic_year_id:
                academicYear = Academicyear.objects.get(pk=academic_year_id)
                academic_student.academic_year = academicYear
                academic_student.save()
            #academic_student = AcademicStudent.objects.create(**validated_data)
        #academic_student = super().create(validated_data)

        

        

        return academic_student

class bankAadharViaRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAndAadhar
        fields = ['bank', 'account_no', 'ifsc_code', 'aadhar_no','bank_branch']

class academicStudentViaRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicStudent
        fields = ['grade', 'section', 'branch', 'academic_year','medium','comments']


class StudentRegistrationSerializer(serializers.ModelSerializer): 
    academicstudents = academicStudentViaRegistrationSerializer(many=True,required=True)
    print("-----------------------------------------")
    class Meta:
        model = RegisterStudent
        #exclude = ['created_at','updated_at','updated_by'] 
        fields = ['id','name','father_name','mother_name','father_occupation','mother_occupation','gender','category','cast','address_permanent','province','city','mobile1','mobile2',
                  'email','academicstudents','registration_no']   
    

    def create(self, validated_data):          
        user = self.context['request'].user
        print("---------------------------------------------------------------------",validated_data,"  :::::::: ",user)      
        academic_student_data = validated_data.pop('academicstudents', [])
        #bank_students_data = validated_data.pop('bankAndAadhar', [])
        print("academic_student_data: ",academic_student_data)       

        register_student = RegisterStudent.objects.create(**validated_data)
        print("register_student: ",register_student)
        
        for academicStudentData in academic_student_data:
            academicStudentData['updated_by'] = user
            AcademicStudent.objects.create(student=register_student, **academicStudentData)
        
        return register_student