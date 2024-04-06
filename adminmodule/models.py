from django.db import models
from .utils import *
from base.models import BaseModel
from universal.models import Month_Master
from django.core.validators import MaxValueValidator, MinValueValidator
from account.models import Branch
# Create your models here.

ACTIVE_STATUS = 1
INACTIVE_STATUS = 2
ChoicesOfStatus = (
    (ACTIVE_STATUS, 'Active'),
    (INACTIVE_STATUS, 'In-Active')
)

# Create your models here.
class Grade(BaseModel):
    grade_name = models.CharField(max_length=100, unique=True)
    grade_comments = models.TextField(blank=True, null=True)
    branch = models.ForeignKey(Branch, related_name="grades", on_delete=models.RESTRICT)

    def __str__(self) -> str:
        return self.grade_name
    
class Section(BaseModel):
    section_name = models.CharField(max_length=100, unique=True)
    section_comments = models.TextField(blank=True, null=True)
    branch = models.ForeignKey(Branch, related_name="sections", on_delete=models.RESTRICT)

    def __str__(self) -> str:
        return self.section_name
    

class Feehead(BaseModel):
    feehead_name = models.CharField(max_length=100, unique=True)
    feehead_description = models.CharField(max_length=255)
    feehead_status = models.IntegerField(default=1, choices=ChoicesOfStatus)
    branch = models.ForeignKey(Branch, related_name="feeheads", on_delete=models.RESTRICT)

    def __str__(self) -> str:
        return self.feehead_name
    
class Discounthead(BaseModel):
    discount_name = models.CharField(max_length=100, unique=True)
    discount_description = models.CharField(max_length=255, null=True)
    discount_status = models.IntegerField(default=1, choices=ChoicesOfStatus)
    branch = models.ForeignKey(Branch, related_name="discountheads", on_delete=models.RESTRICT)

    def __str__(self) -> str:
        return self.discount_name


class Academicyear(BaseModel):
    session_startdate = models.DateField()
    session_enddate = models.DateField()
    session_displayformat = models.CharField(max_length=100)
    session_description = models.CharField(max_length=255, null=True)
    session_status = models.IntegerField(default=1, choices=ChoicesOfStatus)
    slug = models.SlugField(unique=True, null=True)    
    branch = models.ForeignKey(Branch, related_name="sessions", on_delete=models.RESTRICT)

    def __str__(self) -> str:
        return self.session_displayformat
    
    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.session_displayformat, self)
        super(Academicyear, self).save(*args, **kwargs)

    
# todo - We need to figure out fine is dependant on class-wise or same for school?
        
class Finehead(BaseModel):
    fine_name = models.CharField(max_length=100, unique=True)
    fine_description = models.TextField(null=True)
    fine_status = models.IntegerField(default=1, choices=ChoicesOfStatus)
    branch = models.ForeignKey(Branch, related_name="fineheads", on_delete=models.RESTRICT)

    def __str__(self) -> str:
        return self.fine_name
    
# TODO-Save later
class Fine(BaseModel):
    MONTHLY = 1
    QUATERLY = 2
    HALFYEARLY = 3
    YEARLY = 4
    DAILY = 5
    freq_choices = (
        (DAILY, 'Daily'),
        (MONTHLY, 'Monthly'),
        (QUATERLY, 'Quaterly'),
        (HALFYEARLY, 'Half-Yearly'),
        (YEARLY, 'Yearly')
    )
    finehead = models.ForeignKey(Finehead, on_delete=models.RESTRICT, related_name='fines')
    fine_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    grade = models.ForeignKey(Grade, on_delete=models.RESTRICT, related_name='grades')    
    frequency = models.IntegerField(default=1, choices=freq_choices, null=True)
    fine_max_calculated = models.IntegerField(default=1, null=True)
    fine_session = models.ForeignKey(Academicyear, related_name='fines', on_delete=models.RESTRICT)
    description = models.TextField(null=True, blank=True)
    #branch = models.ForeignKey(Branch, related_name="branch_fine", on_delete=models.CASCADE) - Do we need to hold this

    class Meta:
        unique_together = ['finehead', 'grade','fine_session']

    def get_fine_value(self):
        return self.fine_amount
    
