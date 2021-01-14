from rest_framework import serializers
from todo.models import Todo

class TodoSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField() #so user can't set these himself
    datecompleted = serializers.ReadOnlyField()

    class Meta:
        model = Todo
        fields = ['id','title','memo','created','datecompleted','important'] #we don't include 'user' from Todo model because we only want logged in
                                                                             # users to be able to access completed todos via the API anyway
