from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator
from core.validators import *


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    class Meta:
        abstract = True

class CustomUser(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    followersCount = models.IntegerField(default=0, validators=[MaxValueValidator(99999999), MinValueValidator(0)]) # users that follow this user
    followedCount = models.IntegerField(default=0, validators=[MaxValueValidator(99999999), MinValueValidator(0)]) # users that are followed by this user
    description = models.TextField(default="")
    profile_image = models.ImageField(upload_to="profile_images/", default="defaults/profile_image.png", validators=[validate_image])

    def save(self, *args, **kwargs):
        if not self.pk:
            self.followersCount = 0
            self.followedCount = 0
        super(CustomUser, self).save(*args, **kwargs)


class Post(BaseModel):
    description = models.TextField(default="")
    photo = models.ImageField(upload_to="postsFiles/", default="defaults/profile_image.png")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    likesCount = models.IntegerField(default=0, validators=[MaxValueValidator(99999999), MinValueValidator(0)])
    commentsCount = models.IntegerField(default=0)

class Followship(BaseModel):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="follower")
    followed = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="followed_user")
    class Meta:
        unique_together = ('follower', 'followed')

class Comment(BaseModel):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="commented_post", blank=True, null=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name="reply_to_comment", blank=True, null=True)
    text = models.CharField(max_length=500)
    likesCount = models.IntegerField(default=0, validators=[MaxValueValidator(99999999), MinValueValidator(0)])

class PostLike(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post", blank=True, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="photo_liker")
    class Meta:
        unique_together = ('post', 'owner')

class CommentLike(BaseModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="liked_comment", blank=True, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comment_liker")
    class Meta:
        unique_together = ('comment', 'owner')
