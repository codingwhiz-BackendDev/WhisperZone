from django.contrib import admin
from .models import AnonymousMessage, Users, Profile

# Register your models here.

admin.site.register(AnonymousMessage)
admin.site.register(Users)
admin.site.register(Profile)