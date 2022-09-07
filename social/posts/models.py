from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.


User = get_user_model()


class Posts(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, blank=True, null=True,
                              related_name='posts')
    image = models.ImageField(upload_to='posts/media', blank=True, null=True)

    def __str__(self):
        return self.text


class Group(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE,  # blank=True, null=True,
                             related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_user')
    text = models.CharField(max_length=200)
    created = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='follower',
                             blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='following',
                               blank=True, null=True)

