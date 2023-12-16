from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    # Define custom fields to be included in serialization.
    author = serializers.SerializerMethodField()
    author_profile = serializers.SerializerMethodField()
    likes_count = (
        serializers.SerializerMethodField()
    )  # Field to represent the count of likes
    dislikes_count = (
        serializers.SerializerMethodField()
    )  # Field to represent the count of dislikes
    image = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        # Calculate and return the number of likes for a post
        return obj.likes.count()

    def get_dislikes_count(self, obj):
        # Calculate and return the number of dislikes for a post
        return obj.dislikes.count()

    def get_author(self, obj):
        # Retrieve and return the author's nickname if it exists
        return obj.author.nickname if obj.author else None

    def get_author_profile(self, obj):
        # Retrieve and return the author's profile URL if it exists
        return obj.author.profile.url if obj.author else None

    def get_image(self, obj):
        # Retrieve and return the URL of the post's image if it exists
        if obj.image and hasattr(obj.image, "url"):
            return obj.image.url
        return None

    class Meta:
        model = Post  # Specify the model to be serialized
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
