from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User

# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator

# serializer import
from .serializers import UserSerializer, UserRegistrationSerializer

class UsersView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('User account created', status=status.HTTP_201_CREATED)
        return Response('Failed to created account', status=status.HTTP_400_BAD_REQUEST)
        
    
class UserEndpoint(APIView):
    def get(self, request, id):
        user = User.objects.get(id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)