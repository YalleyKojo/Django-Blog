from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to='post_photos',blank=True,null=True)
    content=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User,on_delete=CASCADE)

    def __str__(self) :
        return self.title
    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})      

        
class Comment(models.Model):
    post=models.ForeignKey(Post,related_name="comments",on_delete=models.CASCADE)
    author=models.ForeignKey(User,default='unknown',on_delete=CASCADE)
    body=models.TextField()
    date_posted=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.post.title} - {self.author.username}'