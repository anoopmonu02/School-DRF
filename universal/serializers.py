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
    

def checkAnyNumberInString(obj_field_name, obj_label):
    if bool(re.search(r'\d', obj_field_name)):
        raise serializers.ValidationError(f"{obj_label} can't contains numeric(s).")
    
class MediumSerializer(serializers.ModelSerializer):
    #slug = serializers.SerializerMethodField()
    class Meta:
        model = Medium
        #fields = ['medium_name','slug','uuid','id']
        exclude = ['id','created_at','updated_at','updated_by']

    # Can write any functionlity
    """ def get_slug(self, obj):
        return "ANOOP" """
    # We can write validation method here
    def validate_medium_name(self, data):
        if data:
            medium_name = data
            checkSpecialCharsInString(medium_name, 'Medium name')
            checkValidLenthofField(medium_name, 3, 'Medium name')
            checkAnyNumberInString(medium_name, 'Medium name')

        return data


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        exclude = ['id','created_at','updated_at']

    def validate_bank_name(self, data):
        if data:
            bank_name = data
            checkSpecialCharsInString(bank_name, 'Bank name')
            checkValidLenthofField(bank_name, 3, 'Bank name')
            checkAnyNumberInString(bank_name, 'Bank name')

        return data

# Cast Serializer with Parent  - Category Serializer
class CastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cast
        #fields = ('uuid', 'category', 'cast_name')
        exclude = ['id','created_at','updated_at']         
    

    def validate_cast_name(self, data):
        if data:
            cast_name = data
            checkSpecialCharsInString(cast_name, 'Cast name')
            checkValidLenthofField(cast_name, 3, 'Cast name')
            checkAnyNumberInString(cast_name, 'Cast name')
            
        return data

class CategorySerializer(serializers.ModelSerializer):
    casts = CastSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id','uuid','category_name','casts']
        #exclude = ['id','created_at','updated_at']
    
    def validate_category_name(self, data):
        if data:
            category_name = data
            checkSpecialCharsInString(category_name, 'Category name')
            checkValidLenthofField(category_name, 2, 'Category name')
            checkAnyNumberInString(category_name, 'Category name')
            
        return data

class CitySerializer(serializers.ModelSerializer):    
    class Meta:
        model = City
        fields = ['id','city_name']

    def validate_city_name(self, data):
        if data:
            city_name = data
            checkSpecialCharsInString(city_name, 'City name')
            checkValidLenthofField(city_name, 2, 'City name')
            checkAnyNumberInString(city_name, 'City name')

        return data

class ProvinceSerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)
    class Meta:
        model = Province
        fields = ['id','province_name','cities']

    def validate_province_name(self, data):
        if data:
            province_name = data
            checkSpecialCharsInString(province_name, 'State name')
            checkValidLenthofField(province_name, 3, 'State name')
            checkAnyNumberInString(province_name, 'State name')
        return data


class Month_MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Month_Master
        exclude = ['id','created_at','updated_at']

    def validate_month_name(self, data):
        if data:
            month_name = data
            checkSpecialCharsInString(month_name, 'Month name')
            checkValidLenthofField(month_name, 2, 'Month name')
            checkAnyNumberInString(month_name, 'Month name')

        return data
    
