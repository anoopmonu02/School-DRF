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
    medium_id = serializers.IntegerField(write_only=True)
    grade_id = serializers.IntegerField(write_only=True)
    section_id = serializers.IntegerField(write_only=True)
    branch_id = serializers.IntegerField(write_only=True)
    academic_year_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = AcademicStudent
        exclude = ['created_at','updated_at','updated_by']

    def create(self, validated_data):
        medium_id = validated_data.pop('medium', None)
        grade_id = validated_data.pop('grade', None)
        section_id = validated_data.pop('section', None)
        branch_id = validated_data.pop('branch', None)
        academic_year_id = validated_data.pop('academic_year', None)

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

        return academic_student

    
    

class StudentRegistrationSerializer(serializers.ModelSerializer): 
    print("-----------------------------------------11111")
    academicStudent = AcademicStudentSerializer(many=True)
    bankAndAadhar = BankAndAadharSerializer()
    print("-----------------------------------------")
    class Meta:
        model = RegisterStudent
        exclude = ['created_at','updated_at','updated_by']    

    """ def to_internal_value(self, data):
        if 'grade' in data:
            grade_id = data.pop('grade')
            data['grade'] = Grade.objects.get(id=grade_id)
        if 'section' in data:
            section_id = data.pop('section')
            data['section'] = Section.objects.get(name=section_id)
        if 'medium' in data:
            medium_id = data.pop('medium')
            data['medium'] = Medium.objects.get(id=medium_id)
        if 'branch' in data:
            branch_id = data.pop('branch')
            data['branch'] = Branch.objects.get(id=branch_id)
        return super().to_internal_value(data) """

    def create(self, validated_data):
        print("---------------------------------------------------------------------",validated_data)
        medium_id = validated_data.pop('medium', None)
        grade_id = validated_data.pop('grade', None)
        section_id = validated_data.pop('section', None)
        branch_id = validated_data.pop('branch', None)

        #register_student = super().create(validated_data)

        if medium_id:
            medium = Medium.objects.get(pk=medium_id)
            #register_student.medium = medium

        if grade_id:
            grade = Grade.objects.get(pk=grade_id)
            #register_student.grade = grade

        if section_id:
            section = Section.objects.get(pk=section_id)
            #register_student.section = section

        if branch_id:
            branch = Branch.objects.get(pk=branch_id)
            #register_student.branch = branch

        academic_students_data = validated_data.pop('academicStudent', [])
        bank_students_data = validated_data.pop('bankAndAadhar', [])

        register_student = RegisterStudent.objects.create(
            medium=medium,
            grade=grade,
            section=section,
            branche=branch,
            **validated_data)

        for academic_student_data in academic_students_data:
            AcademicStudent.objects.create(student=register_student, **academic_student_data)

        for bank_student_data in bank_students_data:
            BankAndAadhar.objects.create(student=register_student, **bank_student_data)

        return register_student