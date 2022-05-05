

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class Recomendasi(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

class Fakultas(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Organisasi(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    fakultas = models.ForeignKey(Fakultas, on_delete=models.SET_NULL, null=True)
    
    name = models.CharField(max_length=50, unique=True)   
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now= True)
    profile_picture = models.ImageField(null=True, blank=True, upload_to='avatar/')
    showcase1 = models.ImageField(null=True, blank=True, upload_to='showcase/')
    showcase2 = models.ImageField(null=True, blank=True, upload_to='showcase/')
    showcase3 = models.ImageField(null=True, blank=True, upload_to='showcase/')

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.name

class Event(models.Model):
    organisasi = models.ForeignKey(Organisasi, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    desciption = models.TextField(null=True, blank=True)
    jadwal = models.DateTimeField(null=True, blank=True)
    lokasi = models.CharField(max_length=50, null=True, blank=True)
    banner = models.ImageField(null=True, blank=True, upload_to='images/')
    active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now = True)
    class Meta:
        ordering = ['-created', '-jadwal']

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    interest = models.ManyToManyField(Topic, blank=True, related_name='interest')
    avatar = models.ImageField(upload_to = 'user/', blank=True, null=True)
    fakultas = models.ForeignKey(Fakultas, on_delete=models.CASCADE, null=True, blank=True)
    
    follow = models.ManyToManyField(Organisasi, blank=True, related_name='follow')
    def __str__(self):
        return self.user.username

class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    body = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body


class Feed(models.Model):
    organisasi = models.ForeignKey(Organisasi, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=50)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now=True)
    banner = models.ImageField(null=True, blank=True, upload_to='images/')

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title

class FeedComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

    body = models.TextField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body



    