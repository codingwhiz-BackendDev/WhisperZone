from django.db import models
from django.contrib.auth import get_user_model
 
User = get_user_model()
# Create Users model

class Users(models.Model):
    OwnerUsername = models.CharField(max_length=255)
    
    def __str__(self):
        return self.OwnerUsername
    

# Create Models for messages
class AnonymousMessage(models.Model):
    OwnerUsername = models.CharField(max_length=255, null=True)
    message = models.CharField(max_length=255, null=True)
    time = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.OwnerUsername
    
class  Profile(models.Model):
    profile_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    profile_pic = models.FileField(upload_to='ProfileImage', max_length=100,null=True)
    bio = models.TextField(null=True)
    user_link = models.CharField(max_length=255, null=True)
    facebook_link = models.CharField(max_length=255, null=True, default='')
    instagram_link = models.CharField(max_length=255, null=True, default='')
    twitter_link = models.CharField(max_length=255, null=True, default='')
    
    def __str__(self):
        return str(self.profile_user)