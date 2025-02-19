from django.contrib.auth import get_user_model

from rest_framework import serializers

from taggit.serializers import TaggitSerializer, TagListSerializerField

from items.models import Item
from accounts.models import Profile

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):

    flag = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ["country", "flag"]
    
    def get_flag(self, obj):
        request = self.context["request"]
        return request.build_absolute_uri(obj.country.flag)

class UserSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ["username", "email", "profile"]


class ItemSerializer(TaggitSerializer, serializers.ModelSerializer):
    
    user = UserSerializer(read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = Item
        fields = ["user", "name", "description", "price", "image", "tags", "views_count", "updated_at", "created_at"]