from django.contrib import admin
from .models import User, AccountTier, Image


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'account_tier')
    search_fields = ('username',)
    list_filter = ('account_tier',)


@admin.register(AccountTier)
class AccountTierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'thumbnail_sizes', 'has_original_link', 'can_generate_expiring_links')
    search_fields = ('name',)
    list_filter = ('has_original_link', 'can_generate_expiring_links')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'uploaded_image')
    search_fields = ('owner__username',)
