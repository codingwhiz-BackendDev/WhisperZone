from django.contrib import admin
from .models import AnonymousMessage, Users, Profile,Poll,Option,VoteRecord,MessagesLike

# Register your models here.

admin.site.register(AnonymousMessage)
admin.site.register(Users)
admin.site.register(Profile)
admin.site.register(Poll)
admin.site.register(Option) 
admin.site.register(VoteRecord)
admin.site.register(MessagesLike)