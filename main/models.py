from django.contrib.auth.models import User
from django.db import models
from django.core.validators import FileExtensionValidator


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Application(models.Model):
    class Status(models.TextChoices):
        NEW = 'Новая', 'Новая'
        ACCEPT = 'Принято в работу', 'Принято в работу'
        DONE = 'Выполнено', 'Выполнено'

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.NEW)
    image = models.ImageField(
        upload_to='applications/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'bmp'])],
    )
    design_image = models.ImageField(
        upload_to='designs/', null=True, blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'bmp'])],
    )
    admin_comment = models.TextField(blank=True, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title