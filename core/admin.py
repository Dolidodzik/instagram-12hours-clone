from django.contrib import admin
from core.models import *

admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(Followship)
admin.site.register(PostLike)
admin.site.register(Comment)
admin.site.register(CommentLike)
