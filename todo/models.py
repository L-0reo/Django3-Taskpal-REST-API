from django.db import models
from django.contrib.auth.models import User #to be able to make the forein relationship between our Todo and User models


class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True) #blank=True means they don't necessarily NEED to fill anything in there
    created = models.DateTimeField(auto_now_add=True) #it will automatically log creation time - it is not editable
    datecompleted = models.DateTimeField(null=True, blank=True) #if this is set then todo is completed
    important = models.BooleanField(default=False)
    #to connect a specific user id to the todo
    user = models.ForeignKey(User, on_delete=models.CASCADE) #to connect todo to a specific user

    def __str__(self): #to see todo title in admin list
        return self.title
