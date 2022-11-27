from django.db import models
from django.contrib.auth.models import  AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True, blank=True)

    avatar = models.ImageField(null=True, default="C:/Users/revel/Desktop/Phyton_git/studbud/studbud/base/static/images/avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['__all__']

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null = True) #user hostnya
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null = True)# 1 topik, tapi bisa have multiple room
    name = models.CharField(max_length=200) # charfield required untuk masukin maxlength
    description = models.TextField(null=True, blank= True) #textfield adalah charfield yang lebih gede
                    #null set to true, artinya boleh blank. defaultnya false yang ga boleh blank
                    #blank set true, artinya klo submit form bisa empty
    participants = models.ManyToManyField(User, related_name= 'participants') #store siapa yang aktif di room
    updated = models.DateTimeField(auto_now=True)
                    #auto_now, stiap save method, save time stamp
    created = models.DateTimeField(auto_now_add= True)
                    #auto_now_add, take timestamp cuman create pertama
    class Meta:
        ordering = [
            "-updated","-created",

                    ]
    def __str__(self):
        return str(self.name)
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)#relationship dengan database sebelumnya dengan model one to many (one room, bisa many message)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = [
            "-updated","-created",]
    def __str__(self):
        return self.body[0:50] #return first 50 character from the message
