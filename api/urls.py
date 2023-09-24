from django.urls import path
from .views import ImageUploadView, ListImagesView, fetch_expiring_link

urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='upload-image'),
    path('list/', ListImagesView.as_view(), name='list-images'),
    path('fetch-expiring-link/<int:image_id>/', fetch_expiring_link, name='fetch-expiring-link'),
]
