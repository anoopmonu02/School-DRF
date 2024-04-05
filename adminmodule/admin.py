from django.contrib import admin
from .models import *

admin.site.register(Grade)
admin.site.register(Section)
admin.site.register(Feehead)
admin.site.register(Discounthead)

admin.site.register(Academicyear)
admin.site.register(Finehead)
admin.site.register(Fine)