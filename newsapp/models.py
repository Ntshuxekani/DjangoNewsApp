from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='article_images/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)   # aggregate for quick display

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


class Comment(models.Model):
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return f'Comment on {self.article.title} by {self.author_name or "Anon"}'


class Like(models.Model):
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, related_name='likes')
    session_key = models.CharField(max_length=40, blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('article', 'session_key')  # prevent duplicates per session

    def __str__(self):
        return f'Like: {self.article.title}'
