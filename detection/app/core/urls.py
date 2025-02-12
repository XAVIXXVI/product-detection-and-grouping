from django.urls import path
from .views import DetectionView

urlpatterns = [
    path('detection/', DetectionView.as_view(), name='detection'),
]