from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    BASIC = 'Basic'
    PREMIUM = 'Premium'
    ENTERPRISE = 'Enterprise'

    ACCOUNT_TIER_CHOICES = [
        (BASIC, 'Basic'),
        (PREMIUM, 'Premium'),
        (ENTERPRISE, 'Enterprise'),
    ]

    account_tier = models.CharField(
        max_length=100,
        choices=ACCOUNT_TIER_CHOICES,
        default=BASIC,
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class AccountTier(models.Model):
    name = models.CharField(max_length=255, unique=True)
    thumbnail_sizes = models.CharField(max_length=255)
    has_original_link = models.BooleanField(default=True)
    can_generate_expiring_links = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Account Tier"
        verbose_name_plural = "Account Tiers"


class Image(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_image = models.ImageField(upload_to='uploads/')
    thumbnail_200 = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    thumbnail_400 = models.ImageField(upload_to='thumbnails/', null=True, blank=True)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
