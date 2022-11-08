from tabnanny import verbose
from time import timezone
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.db.models.signals import post_save                        # without using save() agar datat save krna hai then one can use signals 
from django.dispatch import receiver                                  #signals allow certain senders to notify a set of receivers that some action has taken place.
#essential when many pieces of code are interested in same event. 

# Create your models here.
def upload_path_generator(instance, filename):
    return f'media/{instance.name}/{filename}'
class Post(models.Model):
    caption  = models.CharField(max_length= 512)
    posted_on = models.DateTimeField(default= timezone.now)
    creator = models.ForeignKey(User , on_delete= models.CASCADE)
    likes = models.ManyToManyField(User,blank= True,related_name='likes')
    dislikes = models.ManyToManyField(User,blank=True,related_name='dislikes')

    def __str__(self):
        return f'{self.creator} post {self.pk}'

class Comment(models.Model):
    comment = models.CharField(max_length=512)
    created_on = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True ,verbose_name='user',related_name='profile',on_delete=models.CASCADE)
    name = models.CharField(max_length=64,blank=False,null=False)
    bio = models.TextField(max_length=512,blank=True)
    birthday = models.DateField(null=True,blank=True)
    followers = models.ManyToManyField(User,blank=True,related_name='followers')
    profile_pic = models.ImageField(upload_to = upload_path_generator,blank = True)
    
    def __str__(self):
        return f'{self.user.username}'

@receiver(post_save,sender =User)
def create_profile(sender, instance, created, *args, **kwargs):
    # ignore if this is an existing User
    if not created:
        return
    UserProfile.objects.create(user=instance)
post_save.connect(create_profile, sender=User)

@receiver(post_save,sender = User)
def save_user_profile(sender,instance,**kwargs):
        print("We have reached this point")
        instance.profile.save()
