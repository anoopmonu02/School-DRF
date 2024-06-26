from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import uuid

STATUS_ACTIVE = 1
STATUS_INACTIVE = 2
STATUS_DISABLED = 3
STATUS_CHOICES = (
    (STATUS_ACTIVE, 'Active'),
    (STATUS_INACTIVE, 'Inactive'),
    (STATUS_DISABLED, 'Disabled')
)

class CustomerProfile(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(_("Customer Name"), max_length=255, unique = True)
    mobile = models.CharField(_("Mobile"), max_length=15)
    address = models.TextField(_("Address"), null=True, blank=True)
    pincode = models.CharField(_("Pincode"), max_length=6, null=True, blank=True)
    pic = models.ImageField(_("Profile Picture"), upload_to='customer_pics/', null=True, blank=True)
    logo = models.ImageField(_("Logo"), upload_to='customer_logos/', null=True, blank=True)
    mobile1 = models.CharField(_("Alternate Mobile"), max_length=15, null=True, blank=True)
    email = models.EmailField(_("Email"))
    website = models.CharField(_("Website"), max_length=100, null=True, blank=True)
    contact_person = models.CharField(_("Contact Person"), max_length=255)
    conatct_person_mobile = models.CharField(_("Contact Person Mobile"), max_length=15, null=True, blank=True)  
    description = models.TextField(_("Description"), null=True, blank=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.name
    
class Branch(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='branches')
    branch_name = models.CharField(max_length=255)
    branch_code = models.CharField(max_length=50)
    address = models.TextField()
    pincode = models.CharField(max_length=6)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    mobile1 = models.CharField(_("Alternate Mobile"), max_length=15, null=True, blank=True) 
    contact_person = models.CharField(_("Contact Person"), max_length=255)
    contact_person_mobile = models.CharField(_("Contact Person Mobile"), max_length=15, null=True, blank=True)
    description = models.TextField(_("Description"), null=True, blank=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    logo1 = models.ImageField(_("Logo"), upload_to='branch_logos/', null=True, blank=True)
    logo2 = models.ImageField(_("Logo"), upload_to='branch_logos/', null=True, blank=True)

    class Meta:
        unique_together = ['customer', 'branch_name']

    def __str__(self) -> str:
        return self.branch_name

class MyCustomUserManager(BaseUserManager):

    def validate_email(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Invalid email address"))

    def create_user(self, email, password, **extra_fields):
        if email:
            email = self.normalize_email(email)
            self.validate_email(email)
        else:        
            raise ValueError(_('Users must have an email address'))
        if not password:
            raise ValueError('Password must be set')
        
        user = self.model(email=email, **extra_fields)
        print("User created")
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 1)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') != 1:
            raise ValueError('is_staff must be True for admin user')
        
        if extra_fields.get('is_verified') != 1:
            raise ValueError('is_verified must be True for admin user')
        
        if extra_fields.get('is_superuser') != 1:
            raise ValueError('is_superuser must be True for admin user')

        if extra_fields.get('role') != 1:
            raise ValueError('Superuser must have role of Global Admin')
        #extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class MyCustomUser(AbstractBaseUser, PermissionsMixin):
    ADMIN = 1
    MANAGER = 2
    EMPLOYEE = 3
    STUDENT = 4

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager'),
        (EMPLOYEE, 'Employee'),
        (STUDENT, 'Student')
    )    

    username = None
    name = models.CharField(_("Users Full Name"), max_length=150, blank=True, null=True)
    email = models.EmailField(_("Email Address"),unique=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    role = models.SmallIntegerField(choices=ROLE_CHOICES, default=EMPLOYEE)
    dob = models.DateField(blank=True, null=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=20, choices=(('N','No Prefrence'),('M', 'Male'), ('F', 'Female'), ('O', 'Other')), default='N')
    pincode = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    branch = models.ForeignKey('Branch', on_delete=models.SET_NULL, null=True, blank=True, default=None)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    objects = MyCustomUserManager()

    def __str__(self) -> str:
        return self.email
        
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name or self.email.split("@")[0]




