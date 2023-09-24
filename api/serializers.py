from rest_framework import serializers
from .models import User, AccountTier, Image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'account_tier')


class AccountTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountTier
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Image
        fields = ['id', 'uploaded_image', 'thumbnail_200', 'thumbnail_400', 'owner']
        read_only_fields = ['id', 'thumbnail_200', 'thumbnail_400']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request_user = self.context['request'].user
        rep.pop('owner', None)

        if request_user.account_tier == User.BASIC:
            rep.pop('uploaded_image', None)

        return rep
