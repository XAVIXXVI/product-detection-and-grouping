from django.urls import path
from .views import ImageProcessView
from .views import upload_image

urlpatterns = [
    path('image_process/', ImageProcessView.as_view(), name='image_process'),
    path('upload/', upload_image, name='upload_image')
]