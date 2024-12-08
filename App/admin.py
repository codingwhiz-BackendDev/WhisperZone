from django.contrib import admin
from .models import AnonymousMessage, Users

# Register your models here.

admin.site.register(AnonymousMessage)
admin.site.register(Users)