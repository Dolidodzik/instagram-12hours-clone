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

class PostLikeViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, OwnProfilePermission]
    serializer_class = PostLikeSerializer
    queryset = PostLike.objects.all()

class CommentLikeViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, OwnProfilePermission]
    serializer_class = CommentLikeSerializer
    queryset = CommentLike.objects.all()

class CommentViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, OwnProfilePermission]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
