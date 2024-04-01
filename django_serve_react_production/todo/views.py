from ast import Is
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import TodoSerializer
from .models import Todo
from rest_framework.permissions import IsAuthenticated
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrAdmin

# Todo interaction via a ModelViewSet
class TodoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = TodoSerializer
    lookup_field = 'title' # Use the title field to look up todos
    
    #Only get the todos of the user who is currently logged in
    #Unless the user is a superuser, then they can see all todos
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Todo.objects.all()
        else:
            return Todo.objects.filter(user=self.request.user)
    
    #Only create a todo for the user who is currently logged in
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Todo interaction via an APIView
class TodoByTitle(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    
    def get(self, request, title,):
        todo = Todo.objects.filter(title=title).first()
        if todo:
            serializer = TodoSerializer(todo)
            return Response(serializer.data)
        return Response({"message": "Todo not found"}, 
                        status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, title, format=None):
        todo = Todo.objects.filter(title=title).first()
        if todo:
            serializer = TodoSerializer(todo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Todo not found"}, 
                        status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, title, format=None):
        todo = Todo.objects.filter(title=title).first()
        if todo:
            todo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Todo not found"}, 
                        status=status.HTTP_404_NOT_FOUND)

# Create a todo via an APIView
class CreateTodo(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    
    def post(self, request, format=None):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ToggleCompleted(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    
    def put(self, request, format=None):
        title = request.data["title"]
        todo = Todo.objects.filter(title=title).first()
        if todo:
            todo.completed = not todo.completed
            todo.save()
            serializer = TodoSerializer(todo)
            return Response(serializer.data)
        return Response({"message": "Todo not found"}, 
                        status=status.HTTP_404_NOT_FOUND)