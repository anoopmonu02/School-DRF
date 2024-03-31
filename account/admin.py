from django.contrib import admin

from .models import *

# Register the CustomUser model
admin.site.register(MyCustomUser)
admin.site.register(CustomerProfile)
admin.site.register(Branch)