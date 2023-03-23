from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, permissions
from users.models import User
from .models import Following
from .serializers import FollowSerializer

# Create your views here.


class FollowingView(APIView):
    permissions_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        followed_user_id = request.data.get("followed_user_id")
        if followed_user_id:
            try:
                followed_user = User.objects.get(id=followed_user_id)
            except User.DoesNotExist:
                return Response(
                    {"error": "User does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            follow = Following(follower=request.user, followed_user=followed_user)
            follow.save()
            serializer = FollowSerializer(follow)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "followed_user_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        followed_user_id = request.data.get("followed_user_id")
        if followed_user_id:
            try:
                follow = Following.objects.get(
                    follower=request.user, followed_user_id=followed_user_id
                )
            except Following.DoesNotExist:
                return Response(
                    {"error": "You are not following this user."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"error": "followed_user_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
