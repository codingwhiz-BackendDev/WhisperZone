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
    make_private = models.BooleanField(default=False, null=True)
    no_of_likes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.OwnerUsername

 
    
class  Profile(models.Model):
    profile_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    profile_pic = models.FileField(upload_to='ProfileImage', max_length=100,null=True, default='sta.jpg')
    bio = models.TextField(null=True)
    user_link = models.CharField(max_length=255, null=True)
    facebook_link = models.CharField(max_length=255, null=True, default='')
    instagram_link = models.CharField(max_length=255, null=True, default='')
    twitter_link = models.CharField(max_length=255, null=True, default='')
    
    def __str__(self):
        return str(self.profile_user)
    
class Poll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class Option(models.Model):
    poll = models.ForeignKey(Poll, related_name='options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255, null=True)
    votes = models.IntegerField(default=0, null=True)

    def __str__(self):
        return f"{self.option_text} ({self.votes} votes)"
    

class VoteRecord(models.Model):
    ip_address = models.GenericIPAddressField()
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    
class MessagesLike(models.Model):
    ip_address = models.GenericIPAddressField(null=True)
    message = models.CharField(max_length=255, null=True)

    
    def __str__(self):
        return str(self.ip_address)
    