from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='article_images/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class BreakingAlert(models.Model):
    message = models.CharField(max_length=300)
    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email
