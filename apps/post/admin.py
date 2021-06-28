from django.contrib import admin

from apps.post.models import Post, PostRating

admin.site.register(Post)
admin.site.register(PostRating)
