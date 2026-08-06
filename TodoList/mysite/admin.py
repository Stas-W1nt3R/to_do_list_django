from django.contrib import admin
from .models import Blog, Comment, Profile, Tag

admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Tag)
