from django.db import models
from base.models import BaseModel
from universal.models import *
from adminmodule.models import *
from account.models import *
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


choicesOfGender = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
    ('No Preference', 'No Preference')
)

choicesOfReligion = (
    ('Hindu', 'Hindu'),
    ('Muslim', 'Muslim'),
    ('Christian', 'Christian'),
    ('Sikh', 'Sikh'),
    ('Jain', 'Jain'),
    ('Buddhist', 'Buddhist'),
    ('Other', 'Other'),
    ('No Preference', 'No Preference')
)

choicesOfBloodGroup = (
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('None','None')    
)

choicesOfBodyType = (
    ('Normal', 'Normal'),
    ('Blind', 'Blind'),
    ('Physically Challenged', 'Physically Challenged'),
    ('Other', 'Other')
)

ChoicesOfStatus = (
    (1, 'Active'),
    (2, 'In-Active')
)

choicesOfRelationship = (
    ('No Preference', 'No Preference'),
    ('Husband', 'Husband'),
    ('Wife', 'Wife'),
    ('Father', 'Father'),
    ('Mother', 'Mother'),
    ('Son', 'Son'),
    ('Daughter', 'Daughter'),
    ('Brother', 'Brother'),
    ('Sister', 'Sister'),
    ('Grandfather', 'Grandfather'),
    ('Grandmother', 'Grandmother'),
    ('Grandson', 'Grandson'),
    ('Granddaughter', 'Granddaughter'),
    ('Uncle', 'Uncle'),
    ('Aunt', 'Aunt'),
    ('Nephew', 'Nephew'),
    ('Niece', 'Niece'),
    ('Cousin', 'Cousin'),
    ('Father-in-law', 'Father-in-law'),
    ('Mother-in-law', 'Mother-in-law'),
    ('Son-in-law', 'Son-in-law'),
    ('Daughter-in-law', 'Daughter-in-law'),
    ('Brother-in-law', 'Brother-in-law'),
    ('Sister-in-law', 'Sister-in-law'),
    ('Stepfather', 'Stepfather'),
    ('Stepmother', 'Stepmother'),
    ('Stepson', 'Stepson'),
    ('Stepdaughter', 'Stepdaughter'),
    ('Stepbrother', 'Stepbrother'),
    ('Stepsister', 'Stepsister'),
    ('Foster father', 'Foster father'),
    ('Foster mother', 'Foster mother'),
    ('Foster son', 'Foster son'),
    ('Foster daughter', 'Foster daughter'),
    ('Guardian', 'Guardian'),
    ('Legal guardian', 'Legal guardian'),
    ('Adoptive father', 'Adoptive father'),
    ('Adoptive mother', 'Adoptive mother'),
    ('Adopted son', 'Adopted son'),
    ('Adopted daughter', 'Adopted daughter'),
    ('Foster brother', 'Foster brother'),
    ('Foster sister', 'Foster sister'),
    ('Foster uncle', 'Foster uncle'),
    ('Foster aunt', 'Foster aunt'),
    ('Foster nephew', 'Foster nephew'),
    ('Foster niece', 'Foster niece'),
    ('Godfather', 'Godfather'),
    ('Godmother', 'Godmother'),
    ('Godson', 'Godson'),
    ('Goddaughter', 'Goddaughter'),
    ('Foster parent', 'Foster parent'),
    ('Foster child', 'Foster child')
)


#Student Details
class RegisterStudent(models.Model):
    #Personal Info  
    name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=50, choices=choicesOfGender, default='No Preference')
    dob = models.DateField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name='categories')
    cast = models.ForeignKey(Cast, on_delete=models.RESTRICT, related_name='casts')
    nationality = models.CharField(max_length=50, default='Indian')
    registration_date = models.DateField(auto_now_add=True)
    registration_no = models.CharField(max_length=50, unique=True)
    religion = models.CharField(max_length=50, choices=choicesOfReligion, default='No Preference')
    father_occupation = models.CharField(max_length=255, blank=True, null=True)    
    mother_occupation = models.CharField(max_length=255, blank=True, null=True)
    student_pic = models.ImageField(upload_to='student_pic/', blank=True, null=True)
    status = models.IntegerField(default=1, choices=ChoicesOfStatus)
    comments = models.TextField(blank=True, null=True)

    #physical
    blood_group = models.CharField(max_length=50, choices=choicesOfBloodGroup, default='None')
    height = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    bodytype = models.CharField(max_length=50, choices=choicesOfBodyType, default='Normal')

    #Contact Info
    #address_communication = models.TextField(blank=True, null=True)
    address_permanent = models.TextField(blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    province = models.ForeignKey(Province, on_delete=models.RESTRICT, related_name='provinces')
    city = models.ForeignKey(City, on_delete=models.RESTRICT, related_name='cities')
    pincode = models.CharField(max_length=6, blank=True, null=True)
    mobile1 = models.CharField(max_length=15, blank=True, null=True)
    mobile2 = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)

    #Previous Academic Details
    previous_school_name = models.CharField(max_length=255, blank=True, null=True)
    previous_class = models.CharField(max_length=255, blank=True, null=True)
    passing_year = models.IntegerField(default=0, null=True, blank=True)
    tc_no = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    student_type = models.CharField(max_length=20, default='Old', choices=(('Old', 'Old'), ('New', 'New')))

    #Guardian Details
    guardian_name = models.CharField(max_length=255, blank=True, null=True)
    relationship = models.CharField(max_length=100, default='No Preference', choices=choicesOfRelationship)
    guardian_contact = models.CharField(max_length=255, blank=True, null=True)

    #Current Class
    """ grade = models.ForeignKey(Grade, on_delete=models.RESTRICT, related_name='studentgrades')
    section = models.ForeignKey(Section, on_delete=models.RESTRICT, related_name='studentsections')
    branch = models.ForeignKey(Branch, on_delete=models.RESTRICT, related_name='studentbranches')
    medium = models.ForeignKey(Medium, on_delete=models.RESTRICT, related_name='studentmediums') """
    status_school = models.CharField(max_length=20, default='Own', choices=(('Own', 'Own'), ('Grant', 'Grant'), ('Other', 'Other')))

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(MyCustomUser, on_delete=models.RESTRICT)

    def __str__(self) -> str:
        return self.name


#Academic Student Details
class AcademicStudent(models.Model):
    student = models.ForeignKey(RegisterStudent, on_delete=models.RESTRICT, related_name='academicstudents')
    #Academic Details
    migration_date = models.DateField(auto_now_add=True)
    classsrno = models.CharField(max_length=255, blank=True, null=True)
    boardsrno = models.CharField(max_length=255, blank=True, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.RESTRICT, related_name='academicstudentgrades')
    section = models.ForeignKey(Section, on_delete=models.RESTRICT, related_name='academicstudentsections')
    branch = models.ForeignKey(Branch, on_delete=models.RESTRICT, related_name='branches')
    academic_year = models.ForeignKey(Academicyear, on_delete=models.RESTRICT, related_name='academic_years')
    medium = models.ForeignKey(Medium, on_delete=models.RESTRICT, related_name='academicstudentmediums', default=None)
    roll_no = models.CharField(max_length=50, blank=True, null=True)
    status = models.IntegerField(default=1, choices=ChoicesOfStatus)
    comments = models.TextField(blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(MyCustomUser, on_delete=models.RESTRICT)

class BankAndAadhar(models.Model):
    student = models.ForeignKey(RegisterStudent, on_delete=models.RESTRICT, related_name='bankstudents')
    #Bank & Aadhar details
    bank = models.ForeignKey(Bank, on_delete=models.RESTRICT, related_name='banks')
    account_no = models.CharField(max_length=255, blank=True, null=True)
    aadhar_no = models.CharField(max_length=255, blank=True, null=True)
    bank_branch = models.CharField(max_length=255, blank=True, null=True)
    ifsc_code = models.CharField(max_length=255, blank=True, null=True)
    aadhar_front = models.ImageField(upload_to='student_aadhar_front/', blank=True, null=True)
    aadhar_back = models.ImageField(upload_to='student_aadhar_back/', blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(MyCustomUser, on_delete=models.RESTRICT)




