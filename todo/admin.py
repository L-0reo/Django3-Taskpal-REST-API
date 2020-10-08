from django.contrib import admin
from .models import Todo

class TodoAdmin(admin.ModelAdmin):   #this is how you customize your admin page in this case we're only making the otherwise invisible
    readonly_fields = ('created',)   # 'created' field show up (for date created)

admin.site.register(Todo, TodoAdmin)
