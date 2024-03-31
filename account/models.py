from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import validate_email



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

        if extra_fields.get('is_staff') != 1:
            raise ValueError('is_staff must be True for admin user')
        
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

    class Role:
        pass

    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 2
    STATUS_DISABLED = 3
    STATUS_CHOICES = (
        (STATUS_ACTIVE, 'Active'),
        (STATUS_INACTIVE, 'Inactive'),
        (STATUS_DISABLED, 'Disabled')
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyCustomUserManager()

    def __str__(self) -> str:
        return self.email
        
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name or self.email.split("@")[0]


