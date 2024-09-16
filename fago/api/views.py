from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import PostSerializer
from posts.models import Post
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated

# endpoints

# Get all posts
@api_view(['GET'])
def get_posts(request):
    if request.user.is_authenticated:
        print(f"User Authenticated {request.user}")
    print('Not Authenticated')
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


class LoginView(APIView):

    # handle post request
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if not user is None:
            login(request, user)
            return Response({"detail": "Successfully logged in."}, status=status.HTTP_200_OK)
        
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

# api only authentication users can hit
class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            post = Post.objects.get(id=id)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except post.DoesNotExist:
            return Response({'Not Found': 'post not found'}, status=status.HTTP_404_NOT_FOUND)