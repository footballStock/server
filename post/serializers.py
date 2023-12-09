from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    author_profile = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_dislikes_count(self, obj):
        return obj.dislikes.count()

    def get_author(self, obj):
        return obj.author.nickname if obj.author else None

    def get_author_profile(self, obj):
        return obj.author.profile.url if obj.author else None

    def get_image(self, obj):
        if obj.image and hasattr(obj.image, "url"):
            return obj.image.url
        return None

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "image",
            "author",
            "author_profile",
            "created_at",
            "likes_count",
            "dislikes_count",
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
