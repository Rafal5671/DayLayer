from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .events import (
    publish_account_deleted,
    publish_password_changed,
    publish_profile_updated,
    publish_user_registered,
)
from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        publish_user_registered(user.email, user.username)


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        old_username = request.user.username
        old_email = request.user.email

        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            changes = []
            if (
                request.data.get("username")
                and request.data["username"] != old_username
            ):
                changes.append(f"Username changed to {request.data['username']}")
            if request.data.get("email") and request.data["email"] != old_email:
                changes.append(f"Email changed to {request.data['email']}")

            if changes:
                publish_profile_updated(
                    request.user.email, request.user.username, changes
                )

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        email = request.user.email
        username = request.user.username
        request.user.delete()
        publish_account_deleted(email, username)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        if not request.user.check_password(current_password):
            return Response(
                {"detail": "Current password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(new_password) < 8:
            return Response(
                {"detail": "Password must be at least 8 characters"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.set_password(new_password)
        request.user.save()
        publish_password_changed(request.user.email, request.user.username)
        return Response({"detail": "Password changed successfully"})
