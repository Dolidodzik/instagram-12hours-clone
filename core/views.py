from django.shortcuts import render
from rest_framework import viewsets
from core.serializers import *
from core.permissions import *
from rest_framework import permissions
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from django.core import serializers
from django.db.models import Q
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from rest_framework.views import APIView
from django.db import IntegrityError
import json
import datetime


class PostViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, OwnProfilePermission]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def list(self, request, *args, **kwargs):
        follow_number = request.query_params.get('feed_number') # number of days that posts are posted between
        if not follow_number:
            follow_number = 1
        followed = Followship.objects.filter(follower=request.user)
        followed_users = []
        for follow in followed:
            followed_users.append(follow.followed)

        today = datetime.date.today()
        startdate = today + datetime.timedelta(days=follow_number-1)
        enddate = today + datetime.timedelta(days=follow_number)

        posts = Post.objects.filter(Q(owner__in=followed_users) & Q(Q(created_date__range=[startdate, enddate]) | Q(id__range=[follow_number, follow_number+30]))).order_by("created_date")[:50]
        return Response(PostSerializer(posts, many=True).data)

class CustomUserViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, OwnProfilePermission]
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

class FollowshipViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, OwnProfilePermission]
    serializer_class = FollowshipSerializer
    queryset = Followship.objects.all()

    def list(self, request, *args, **kwargs):
        follow = request.query_params.get('follow')
        user_id = request.query_params.get('user_id')
        user = CustomUser.objects.filter(pk=user_id).first()

        if request.user == user:
            return Response("you cant follow your own profile")
        if not user_id:
            return Response("you need to provide data in get parameter like this: /?user_id=123&follow=yes")
        if not user:
            return Response("user not found")

        request_user = request.user

        if follow == "yes":
            if not Followship.objects.filter(follower=request_user, followed=user).first():
                followship = Followship.objects.create(follower=request_user, followed=user)
                user.followersCount+=1
                request_user.followedCount+=1
        elif follow == "no":
            if Followship.objects.filter(follower=request_user, followed=user).first():
                followship = Followship.objects.filter(follower=request_user, followed=user).first().delete()
                user.followersCount-=1
                request_user.followedCount-=1
        request_user.save()
        user.save()
        return Response({"followers_count": user.followersCount, "followed": follow})

class PostLikeViewset(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, OwnProfilePermission]
    serializer_class = PostLikeSerializer
    queryset = PostLike.objects.all()

    def list(self, request, *args, **kwargs):
        like = request.query_params.get('like')
        post_id = request.query_params.get('post_id')
        post = Post.objects.filter(pk=post_id).first()
        if not post_id:
            return Response("you need to provide data in get parameter like this: /?post_id=123&like=yes")
        if not comment:
            return Response("post not found")

        if like == "yes":
            if not PostLike.objects.filter(post=post, owner=request.user).first():
                post_like = PostLike.objects.create(post=post, owner=request.user)
                post.likesCount+=1
        elif like == "no":
            if PostLike.objects.filter(post=post, owner=request.user).first():
                post_like = PostLike.objects.filter(post=post, owner=request.user).first().delete()
                post.likesCount-=1
        post.save()
        return Response({"likes": post.likesCount, "liked": like})


class CommentLikeViewset(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, OwnProfilePermission]
    serializer_class = CommentLikeSerializer
    queryset = CommentLike.objects.all()

    def list(self, request, *args, **kwargs):
        like = request.query_params.get('like')
        comment_id = request.query_params.get('comment_id')
        comment = Comment.objects.filter(pk=comment_id).first()
        if not comment_id:
            return Response("you need to provide data in get parameter like this: /?comment_id=123&like=yes")
        if not comment:
            return Response("comment not found")

        if like == "yes":
            if not CommentLike.objects.filter(comment=comment, owner=request.user).first():
                comment_like = CommentLike.objects.create(comment=comment, owner=request.user)
                comment.likesCount+=1
        elif like == "no":
            if CommentLike.objects.filter(comment=comment, owner=request.user).first():
                comment_like = CommentLike.objects.filter(comment=comment, owner=request.user).first().delete()
                comment.likesCount-=1
        comment.save()
        return Response({"likes": comment.likesCount, "liked": like})

class CommentViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, OwnProfilePermission]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

class MessageViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, OwnProfilePermission]
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def list(self, request, *args, **kwargs):
        chatted_with = request.user.chatted_with
        conversations = []

        for other_user_id in chatted_with:
            other_user_id = int(other_user_id)
            other_user = CustomUser.objects.filter(pk=other_user_id).first()
            if other_user:
                last_msg = Message.objects.filter(Q(sender=other_user, receiver=request.user) | Q(receiver=other_user, sender=request.user)).order_by("created_date").first()
                conversations.append({"username": other_user.username, "profile_image": other_user.profile_image.url, "last_msg": last_msg.content, "who_sent_last_message": last_msg.sender.username, "user_id": other_user.pk})

        return Response(conversations)

    def retrieve(self, request, pk=None): # IN THIS CASE "pk" IS ID OF OTHER USER, THAT USER WANTS TO SEE CONVERSATION WITH
        other_user = CustomUser.objects.filter(pk=pk).first()

        if not other_user:
            return Response("given user does not exist")

        messages = Message.objects.filter(Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)).order_by("created_date")

        if not messages.first():
            return Response("messages are empty")

        return Response(self.get_serializer(messages, many=True).data)

    def create(self, request):
        request_user = request.user
        other_user = CustomUser.objects.filter(pk=request.data["receiver"]).first()

        if not other_user:
            return Response("given user does not exist")
        if other_user == request_user:
            return Response("you cannot message yourself")

        if not Message.objects.filter(sender=request_user, receiver=other_user):
            request_user.chatted_with.append(other_user.pk)
            other_user.chatted_with.append(request_user.pk)
            request_user.save()
            other_user.save()

        message = Message.objects.create(sender=request_user, receiver=other_user)

        return Response(self.get_serializer(message).data)
