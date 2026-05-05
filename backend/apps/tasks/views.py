from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user tasks.

    Provides CRUD operations for tasks with optional filtering
    by status and priority. Each user can only access their own tasks.
    """

    serializer_class = TaskSerializer

    def get_queryset(self):
        """
        Return tasks belonging to the authenticated user.

        Supports optional filtering via query parameters:
        - status: filter by task status (todo, in_progress, done)
        - priority: filter by task priority (low, medium, high)
        """
        queryset = Task.objects.filter(user=self.request.user)
        status = self.request.query_params.get("status")
        priority = self.request.query_params.get("priority")

        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)

        return queryset

    def perform_create(self, serializer):
        """Assign the authenticated user as the task owner on creation."""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["patch"])
    def complete(self, request, pk=None):
        """Mark a task as done."""
        task = self.get_object()
        task.status = Task.Status.DONE
        task.save()
        return Response(TaskSerializer(task).data)
