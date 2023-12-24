from django.contrib import admin

# Register your models here.
from .models import Post, Message, Topic

admin.site.register(Post)
admin.site.register(Message)
admin.site.register(Topic)

