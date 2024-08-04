from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=60)
    summary = models.TextField()
    category = models.CharField(max_length=60)
    image = models.ImageField(upload_to="books/")  # app name.
    book_url = models.URLField(blank=True)

    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    text = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    will_recommend = models.BooleanField()

    def __str__(self) -> str:
        return self.text
