from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipmentDatasetViewSet, EquipmentViewSet, AnalyticsView

router = DefaultRouter()
router.register(r'datasets', EquipmentDatasetViewSet, basename='dataset')
router.register(r'equipment', EquipmentViewSet, basename='equipment')

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
]
