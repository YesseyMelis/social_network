from rest_framework import serializers

from apps.post.models import Post, PostRating


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('name',)

    def create(self, validated_data):
        data = validated_data.copy()
        data['user'] = self.context.get('user')
        return super(PostSerializer, self).create(validated_data=data)


class RatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostRating
        fields = ()

    def create(self, validated_data):
        data = validated_data.copy()
        data['user'] = self.context.get('user')
        return super(RatePostSerializer, self).create(validated_data=data)
