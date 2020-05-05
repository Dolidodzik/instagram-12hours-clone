from django.contrib import admin
from django.urls import path
from django.urls import include, path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from core import views

router = routers.DefaultRouter()
router.register(r'posts', views.CommentViewset)
router.register(r'users', views.CustomUserViewset)
router.register(r'followships', views.FollowshipViewset)
router.register(r'postLikes', views.PostLikeViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
