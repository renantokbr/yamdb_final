from django.db import models
from django.contrib.auth.models import AbstractUser


class UserRoles:
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    choices = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    )


class YamUser(AbstractUser):
    email = models.EmailField(verbose_name='email', unique=True)
    bio = models.TextField(verbose_name='bio', blank=True)
    role = models.CharField(
        max_length=9,
        choices=UserRoles.choices,
        default=UserRoles.USER,
        verbose_name='role'
    )

    class Meta:
        ordering = ['id']
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    @property
    def is_admin(self):
        return self.is_superuser or self.role == UserRoles.ADMIN
