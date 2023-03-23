from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from django.db.models import Q

# Create your views here.


class UserView(APIView):
    permission_classes = {permissions.IsAuthenticatedOrReadOnly}
    model = User
    queryset = User.objects.all()
    def get(self, request, *args, **kwargs):
        id = int(kwargs["pk"])
        is_exist = User.objects.filter(id=id).exists()
        if is_exist == True:
            serializer = UserSerializer(User.objects.get(id=id))
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)


class AllUsers(APIView):
    permission_classes = {permissions.IsAuthenticatedOrReadOnly}
    model = User
    
    def get(self, request, *args, **kwargs):
        users_list = User.objects.all()
        serializer = UserSerializer(users_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowersUsers(APIView):
    permission_classes = {permissions.IsAuthenticated}
    def post(self, request):
        if request.user.is_authentcated:
            followers_list = User.objects.filter(follower__following=request.user)
            serializer = UserSerializer(followers_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)


class FollowingUsers(APIView):
    permission_classes = {permissions.IsAuthenticated}
    def post(self, request):
        if request.user.is_authenticated:
            following_list = User.objects.filter(following__follower=request.user)
            serializer = UserSerializer(following_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)
