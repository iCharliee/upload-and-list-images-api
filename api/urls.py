from django.urls import path
from .views import ImageUploadView, ListImagesView, get_expiring_link

urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='upload-image'),
    path('list/', ListImagesView.as_view(), name='list-images'),
    path('get-expiring-link/<int:image_id>/', get_expiring_link, name='get-expiring-link'),
]
