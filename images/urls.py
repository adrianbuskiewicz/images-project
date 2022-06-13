from django.urls import path, include
from .views import (
    ImageUploadView,
    ImageListView,
    ExpiringLinkCreateView,
    expiring_image_view,
)

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('', ImageListView.as_view(), name='image_list'),
    path('upload/', ImageUploadView.as_view(), name='image_upload'),
    path('expiring/', ExpiringLinkCreateView.as_view(), name='image_expiring_link'),
    path('<token>/', expiring_image_view, name='expiring_image')
]


