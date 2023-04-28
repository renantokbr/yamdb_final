from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import year_validator

User = get_user_model()


class Category(models.Model):
    name = models.CharField(verbose_name='name', max_length=50)
    slug = models.SlugField(verbose_name='slug', unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(verbose_name='name', max_length=50)
    slug = models.SlugField(verbose_name='slug', unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(verbose_name='name', max_length=200)
    year = models.PositiveSmallIntegerField(
        verbose_name='year',
        validators=[year_validator]
    )
    description = models.CharField(
        verbose_name='description',
        max_length=200,
        blank=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles', blank=True,
        null=True, verbose_name='category',
    )
    genre = models.ManyToManyField(
        Genre, related_name='titles', blank=True, verbose_name='genre',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'title'
        verbose_name_plural = 'titles'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='title',
        db_index=True
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='reviews',
        db_index=True
    )
    score = models.PositiveSmallIntegerField(
        help_text='Оценка от 1 до 10',
        validators=[
            MaxValueValidator(10, 'Оценка от 1 до 10'),
            MinValueValidator(1, 'Оценка от 1 до 10')
        ],
        verbose_name='score'
    )
    pub_date = models.DateTimeField(
        verbose_name='review date',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_author'
            ),
        ]
        verbose_name = 'review',
        verbose_name_plural = 'reviews'

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        'Review', on_delete=models.CASCADE, related_name='comments',
        verbose_name='review'
    )
    text = models.TextField(verbose_name='text')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='author'
    )
    pub_date = models.DateTimeField(
        verbose_name='comment date',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self):
        return self.text
