from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from .validators import year_validator


class Role(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class Profile(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=200, blank=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
    )

    def __str__(self) -> str:
        return self.email

    @property
    def is_moder(self) -> bool:
        return self.role == Role.MODERATOR

    @property
    def is_admin(self) -> bool:
        return self.role == Role.ADMIN or self.is_staff or self.is_superuser

    @property
    def is_staff_user(self) -> bool:
        return self.is_admin or self.is_moder

    class Meta:
        ordering = ('id', )


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True,
                            verbose_name='Наименование')
    slug = models.SlugField(unique=True, max_length=200,
                            verbose_name='Ссылка')

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Наименование')
    slug = models.SlugField(
        unique=True, max_length=100, blank=True,
        null=True, verbose_name='Ссылка')

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование')
    year = models.IntegerField(
        validators=[year_validator],
        blank=True, null=True,
        verbose_name='Год')
    description = models.TextField(verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre, related_name='genre', blank=True, verbose_name='Жанр')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='category',
        verbose_name='Категория')

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = 'Название'
        verbose_name_plural = 'Названия'


class Review(models.Model):
    text = models.TextField()
    score = models.IntegerField(
        validators=[
            MinValueValidator(1, message='Введите число не меньше 1'),
            MaxValueValidator(10, message='Введите число не больше 10')],
        blank=True, null=True)
    pub_date = models.DateField(auto_now_add=True, db_index=True)

    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE,
        related_name="reviews")
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name="reviews")

    def __str__(self) -> str:
        return f'{self.author} написал {self.text} на {self.title}.'\
               f'{self.author} оценил {self.title} на {self.score}.'\
               f'{self.pub_date}.'

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    text = models.TextField()
    pub_date = models.DateField(
        'Дата публикации', auto_now_add=True, db_index=True)

    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE,
        related_name="comments")
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name="comments")
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name="comments")

    def __str__(self) -> str:
        return f'{self.author} написал {self.text} на {self.review}.'\
               f'{self.pub_date}.'

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментариев'
