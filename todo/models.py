from enum import unique
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    
    #When the user is deleted, all of their to-dos will be deleted as well
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title