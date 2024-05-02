from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('casts/by-category/', CastByCategoryViewSet.as_view({'post': 'list'}), name='casts-by-category'),
]
router = DefaultRouter()
router.register('medium',MediumView, basename='medium')
router.register('bank',BankView, basename='bank')
router.register('category',CategoryView, basename='category')
router.register('cast',CastView, basename='cast')
router.register('month_master',MonthMasterView, basename='month_master')
router.register('province',ProvinceView, basename='province')
router.register('city',CityView, basename='city')
urlpatterns += router.urls