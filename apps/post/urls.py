from django.urls import path
from rest_framework import routers

from apps.post.views import PostViewSet

urlpatterns = []

app_name = 'post'

router = routers.DefaultRouter()
router.register('', PostViewSet)

urlpatterns += router.urls
