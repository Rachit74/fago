from rest_framework import serializers
from posts.models import Post

class PostSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'  # Keep using all fields

    def get_image_url(self, obj):
        if obj.image:  # Check if image exists
            return obj.image.url  # Return the URL of the image
        return None  # Return None if there's no image
