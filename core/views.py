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


class PostViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, OwnProfilePermission]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

class CustomUserViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, OwnProfilePermission]
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

class FollowshipViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, OwnProfilePermission]
    serializer_class = FollowshipSerializer
    queryset = Followship.objects.all()

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
