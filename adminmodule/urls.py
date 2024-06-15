from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('grade',GradeViewSet, basename='grade')
router.register('section',SectionViewSet, basename='section')
router.register('feehead',FeeHeadViewSet, basename='feehead')
router.register('discounthead',DiscountHeadViewSet, basename='discounthead')
router.register('finehead',FineheadViewSet, basename='finehead')
router.register('academicyear',AcademicyearViewSet, basename='academicyear')
router.register('fine',FineViewSet, basename='fine')
router.register('fee-month-map',FeeMonthMappingView, basename='fee-month-map')

urlpatterns = [
    path('month-mapping/', MonthMappingView.as_view(), name='month-mapping'),
    path('fee-class-mapping/', FeeClassMappingView.as_view(), name='fee-class-mapping'),
]
urlpatterns += router.urls