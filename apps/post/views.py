from datetime import date, datetime

from django.db.models import Count
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.post.mixins import MethodMatchingViewSetMixin
from apps.post.models import Post, PostRating
from apps.post.serializers import PostSerializer, RatePostSerializer
from apps.utils.bot import bot_validation


class PostViewSet(MethodMatchingViewSetMixin, ModelViewSet):
    queryset = Post.objects.all()
    http_method_names = ['post', 'get']
    serializer_class = PostSerializer

    action_serializers = {
        "create": PostSerializer,
        "like": RatePostSerializer,
        "unlike": RatePostSerializer,
    }

    def create(self, request, *args, **kwargs):
        if not bot_validation('Post', Post.objects.filter(user=request.user).count()):
            return Response({'error': 'Maximum number of posts per user'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True)
    def like(self, request, *args, **kwargs):
        if not bot_validation('PostRating', PostRating.objects.filter(user=request.user).count()):
            return Response({'error': 'Maximum number of likes per user'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def unlike(self, request, *args, **kwargs):
        post_rate = PostRating.objects.filter(
            post=self.get_object(),
            user=request.user
        ).first()
        if post_rate:
            post_rate.delete()
        return Response({'status': 'unliked'})

    @extend_schema(parameters=[
        OpenApiParameter(name="date_from", location=OpenApiParameter.QUERY, type=str, description='01.01.2021'),
        OpenApiParameter(name="date_to", location=OpenApiParameter.QUERY, type=str, description='02.02.2021')
    ])
    @action(methods=["get"], detail=False)
    def analytics(self, request, *args, **kwargs):
        date_from = datetime.strptime(request.query_params.get('date_from'), '%d.%m.%Y')
        date_to = datetime.strptime(request.query_params.get('date_to'), '%d.%m.%Y').replace(
            hour=23, minute=59, second=0
        )
        post_likes = PostRating.objects.filter(
            created_at__gte=date_from,
            created_at__lte=date_to
        ).aggregate(total_like=Count('pk'))
        return Response(post_likes)
