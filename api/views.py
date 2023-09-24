from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, Image
from .serializers import ImageSerializer
from PIL import Image as PILImage
from io import BytesIO
from django.core.files.base import ContentFile
from .utils import generate_thumbnail, generate_signed_url


class ImageUploadView(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        image = PILImage.open(serializer.validated_data['uploaded_image'])
        thumbnails = {}

        if user.account_tier in [User.BASIC, User.PREMIUM, User.ENTERPRISE]:
            thumbnails['thumbnail_200'] = generate_thumbnail(image, 200)

        if user.account_tier in [User.PREMIUM, User.ENTERPRISE]:
            thumbnails['thumbnail_400'] = generate_thumbnail(image, 400)

        for field, thumbnail in thumbnails.items():
            thumb_io = BytesIO()
            thumbnail.save(thumb_io, format=image.format)
            file_name = serializer.validated_data['uploaded_image'].name
            serializer.validated_data[field] = ContentFile(thumb_io.getvalue(), name=file_name)

        serializer.save(owner=user)


class ListImagesView(generics.ListAPIView):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(owner=self.request.user)


@api_view(['POST'])
def fetch_expiring_link(request, image_id):
    default_expiration = 300
    max_expiration = 30000

    user = request.user
    if not user.is_authenticated or user.account_tier != User.ENTERPRISE:
        return Response({"detail": "Permission denied."}, status=403)

    expiration = request.query_params.get('expiration', default_expiration)
    try:
        expiration = int(expiration)
        if not (300 <= expiration <= max_expiration):
            raise ValueError
    except ValueError:
        return Response({"detail": "Invalid expiration time."}, status=400)

    try:
        image = Image.objects.get(pk=image_id, owner=user)
    except Image.DoesNotExist:
        return Response({"detail": "Image not found."}, status=404)

    path = image.uploaded_image.url
    signed_url = generate_signed_url(path, expiration)

    return Response({"url": signed_url})

