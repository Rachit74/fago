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

# Get one particular post
@api_view(['GET'])
def get_post(request, id:int):
    post = Post.objects.get(id=id)
    serializer = PostSerializer(post)
    return Response(serializer.data)