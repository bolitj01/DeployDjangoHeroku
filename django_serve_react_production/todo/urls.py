from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"todos", views.TodoViewSet, basename="todo")

# URL Configuration
urlpatterns = [
    # Django REST Framework URLs
    # Using APIView
    path("create_todo/", views.CreateTodo.as_view(), name="create_todo"),
    path("toggle_completed/", views.ToggleCompleted.as_view(), name="toggle_complete"),
    path("<str:title>/", views.TodoByTitle.as_view(), name="todo_by_title"),
    # Using ModelViewSet
    path("mv/", include(router.urls)),
    
]

