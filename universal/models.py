from django.db import models
from base.models import BaseModel

class Bank(BaseModel):
    bank_name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.bank_name

class Medium(BaseModel):
    medium_name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.medium_name
    
class Category(BaseModel):
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.category_name
    
class Cast(BaseModel):
    category = models.ForeignKey(Category, related_name="casts", on_delete=models.CASCADE)
    cast_name = models.CharField(max_length=255)    

    def __str__(self) -> str:
        return self.cast_name

    class Meta:
        unique_together = ['category', 'cast_name']


class Month_Master(BaseModel):
    month_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.month_name
    
class Province(models.Model):
    province_name = models.CharField(max_length=100, unique=True)
    province_code = models.CharField(max_length=3, null=True)

    def __str__(self) -> str:
        return self.province_name

class City(models.Model):
    province = models.ForeignKey(Province, related_name="cities", on_delete=models.CASCADE)
    city_name = models.CharField(max_length=100)
    city_code = models.CharField(max_length=3, null=True)

    def __str__(self) -> str:
        return self.city_name
    
    class Meta:
        unique_together = ['province', 'city_name']
