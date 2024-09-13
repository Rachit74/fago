from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import PostSerializer
from posts.models import Post

# endpoints

# Get all posts
@api_view(['GET'])
def get_posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
