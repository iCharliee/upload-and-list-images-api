from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from .models import User, AccountTier, Image
from .serializers import UserSerializer, AccountTierSerializer, ImageSerializer
from PIL import Image as PILImage

from .utils import generate_signed_url, generate_thumbnail
import io


class UserTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser", account_tier=User.BASIC)

    def test_user_created(self):
        user = User.objects.get(username="testuser")
        self.assertEqual(user.account_tier, User.BASIC)

    def test_account_tier_choices(self):
        self.assertIn((User.BASIC, 'Basic'), User.ACCOUNT_TIER_CHOICES)
        self.assertIn((User.PREMIUM, 'Premium'), User.ACCOUNT_TIER_CHOICES)
        self.assertIn((User.ENTERPRISE, 'Enterprise'), User.ACCOUNT_TIER_CHOICES)


class AccountTierTestCase(APITestCase):

    def setUp(self):
        self.account_tier = AccountTier.objects.create(
            name="TestTier",
            thumbnail_sizes="200x200",
            has_original_link=True,
            can_generate_expiring_links=False
        )

    def test_account_tier_created(self):
        tier = AccountTier.objects.get(name="TestTier")
        self.assertEqual(tier.thumbnail_sizes, "200x200")
        self.assertTrue(tier.has_original_link)
        self.assertFalse(tier.can_generate_expiring_links)


class ImageTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser", account_tier=User.BASIC)

        image_content = b"dummy_image_content"
        image_file = SimpleUploadedFile("test_image.jpg", image_content, content_type="image/jpeg")

        self.image = Image.objects.create(owner=self.user, uploaded_image=image_file)

    def test_image_created(self):
        image = Image.objects.get(owner=self.user)
        self.assertIsNotNone(image.uploaded_image)


class UserSerializerTestCase(APITestCase):

    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "account_tier": User.BASIC
        }
        self.user = User.objects.create(**self.user_data)

    def test_user_serializer_retrieve(self):
        serializer = UserSerializer(self.user)
        data = serializer.data
        self.assertEqual(data["username"], self.user_data["username"])


class AccountTierSerializerTestCase(APITestCase):

    def setUp(self):
        self.tier_data = {
            "name": "TestTier",
            "thumbnail_sizes": "200x200",
            "has_original_link": True,
            "can_generate_expiring_links": False
        }
        self.tier = AccountTier.objects.create(**self.tier_data)

    def test_account_tier_serializer_retrieve(self):
        serializer = AccountTierSerializer(self.tier)
        data = serializer.data
        self.assertEqual(data["name"], self.tier_data["name"])


class ImageSerializerTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser", account_tier=User.BASIC)
        image_content = b"dummy_image_content"
        self.image_file = SimpleUploadedFile("test_image.jpg", image_content, content_type="image/jpeg")
        self.image = Image.objects.create(owner=self.user, uploaded_image=self.image_file)
        self.image_data = {
            "uploaded_image": self.image_file,
            "owner": self.user.id
        }
        self.factory = APIRequestFactory()

    def test_image_serializer_retrieve(self):
        request = self.factory.get('/')
        request.user = self.user
        serializer = ImageSerializer(self.image, context={"request": request})
        data = serializer.data
        self.assertNotIn("uploaded_image", data)

    def test_image_serializer_retrieve_non_basic_user(self):
        self.user.account_tier = User.PREMIUM
        self.user.save()
        request = self.factory.get('/')
        request.user = self.user
        serializer = ImageSerializer(self.image, context={"request": request})
        data = serializer.data
        self.assertIn("uploaded_image", data)


class UtilsTestCase(APITestCase):

    def create_test_image(self):
        img_io = io.BytesIO()
        image = PILImage.new('RGB', (100, 50), color='red')
        image.save(img_io, format='JPEG')
        return SimpleUploadedFile("test_image.jpg", img_io.getvalue(), content_type='image/jpeg')

    def test_generate_thumbnail(self):
        image_file = self.create_test_image()
        image = PILImage.open(image_file)
        thumbnail = generate_thumbnail(image, 25)
        self.assertEqual(thumbnail.height, 25)
        self.assertEqual(thumbnail.width, 50)

    def test_generate_signed_url(self):
        path = "/test/path/"
        signed_url = generate_signed_url(path, 3600)
        self.assertIn("?token=", signed_url)


class ImageViewTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass", account_tier=User.BASIC)
        self.client.force_authenticate(user=self.user)

    def create_test_image(self):
        img_io = io.BytesIO()
        image = PILImage.new('RGB', (100, 50), color='red')
        image.save(img_io, format='JPEG')
        return SimpleUploadedFile("test_image.jpg", img_io.getvalue(), content_type='image/jpeg')