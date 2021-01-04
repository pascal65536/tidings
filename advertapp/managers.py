from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import datetime, timezone


class AdvertManager(models.Manager):
    """
    Менеджер рекламы.
    """
    def for_show(self):
        today = datetime.now(timezone.utc)
        qs = self.filter(date_start__lte=today, date_stop__gte=today, deleted__isnull=True)
        return qs
