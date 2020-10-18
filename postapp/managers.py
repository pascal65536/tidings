from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class PostManager(models.Manager):
    """
    Менеджер новостей.
    """
    def for_user(self, user):

        if isinstance(user, User) and user.is_superuser:
            qs = self.all()
        else:
            qs = self.filter(deleted__isnull=True, date_post__lte=timezone.now())
        return qs
