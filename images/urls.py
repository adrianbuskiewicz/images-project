from django.urls import path, include
from .views import (
    ImageUploadView,
    ImageListView,
)

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('', ImageListView.as_view(), name='image_list'),
    path('upload/', ImageUploadView.as_view(), name='image_upload'),
]

