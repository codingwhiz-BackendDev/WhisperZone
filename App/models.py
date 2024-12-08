from django.db import models

# Create your models here. 

# Create Users model
class Users(models.Model):
    OwnerUsername = models.CharField(max_length=255)
    
    def __str__(self):
        return self.OwnerUsername
    

# Create Models for messages
class AnonymousMessage(models.Model):
    OwnerUsername = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    
    def __str__(self):
        return self.OwnerUsername