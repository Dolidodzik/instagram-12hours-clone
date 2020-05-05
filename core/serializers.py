from core.models import *
from rest_framework import serializers



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


class CommentSerializer(serializers.ModelSerializer):
    is_already_liked = serializers.SerializerMethodField('isAlreadyLiked')
    owner_username = serializers.SerializerMethodField('profileUsername')
    owner_profile_photo = serializers.SerializerMethodField('profilePhoto')

    def profilePhoto(self, instance):
        return instance.owner.profile_image.url

    def profileUsername(self, instance):
        return instance.owner.username

    def isAlreadyLiked(self, instance):
        if CommentLike.objects.filter(comment=instance).first():
            return True
        else:
            return False

    class Meta:
        model = Comment
        fields = ('id', 'owner', 'likesCount', 'text', 'is_already_liked', 'created_date', 'modified_date', 'owner_username', 'owner_profile_photo', 'post')
        read_only_fields =  ('id', 'likes', 'created_date', 'modified_date', 'owner', 'likesCount')

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'content', 'created_date', 'modified_date')

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ('post', 'owner', 'created_date', 'modified_date')
        read_only_fields = ('post', 'owner', 'created_date', 'modified_date')

class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ('comment', 'owner', 'created_date', 'modified_date')
        read_only_fields = ('comment', 'owner', 'created_date', 'modified_date')

class PostSerializer(serializers.ModelSerializer):
    is_already_liked = serializers.SerializerMethodField('isAlreadyLiked')
    owner_username = serializers.SerializerMethodField('profileUsername')
    owner_profile_photo = serializers.SerializerMethodField('profilePhoto')
    comments = serializers.SerializerMethodField('getComments')

    def profilePhoto(self, instance):
        return instance.owner.profile_image.url

    def profileUsername(self, instance):
        return instance.owner.username

    def getComments(self, instance):
        comments = Comment.objects.filter(post=instance)
        return CommentSerializer(comments, many=True).data

    def isAlreadyLiked(self, instance):
        if PostLike.objects.filter(post=instance).first():
            return True
        else:
            return False

    class Meta:
        model = Post
        fields = ('id', 'owner', 'likesCount', 'commentsCount', 'title', 'is_already_liked', 'created_date', 'modified_date', 'description', 'photo', 'owner_username', 'owner_profile_photo', 'comments')
        read_only_fields =  ('id', 'likes', 'created_date', 'modified_date', 'owner')
