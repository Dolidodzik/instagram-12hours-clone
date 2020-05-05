from core.models import *
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    is_already_liked = serializers.SerializerMethodField('isAlreadyLiked')

    def isAlreadyLiked(self, instance):
        if PostLike.objects.filter(post=instance).first():
            return True
        else:
            return False

    class Meta:
        model = Post
        fields = ('id', 'owner', 'likesCount', 'commentsCount', 'title', 'is_already_liked', 'created_date', 'modified_date', 'description', 'photo')
        read_only_fields =  ('id', 'likes', 'created_date', 'modified_date', 'owner')

class CustomUserSerializer(serializers.ModelSerializer):
    is_already_followed = serializers.SerializerMethodField('isAlreadyFollowed')

    def isAlreadyFollowed(self, instance):
        user =  self.context['request'].user
        if Followship.objects.filter(follower=user, followed=instance).first():
            return True
        else:
            return False

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'followersCount', 'followedCount', 'is_already_followed', 'created_date', 'modified_date', 'description', 'profile_image', 'username')
        read_only_fields =  ('id', 'followersCount', 'followedCount', 'modified_date', 'created_date')

class FollowshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followship
        fields = ('follower', 'followed', 'created_date', 'modified_date')
        read_only_fields = ('follower', 'followed', 'created_date', 'modified_date')

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ('post', 'owner', 'created_date', 'modified_date')
        read_only_fields = ('post', 'owner', 'created_date', 'modified_date')
