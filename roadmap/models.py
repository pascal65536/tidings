from django.db import models


class Distance(models.Model):
    src = models.CharField(max_length=200)
    dst = models.CharField(max_length=200)
    distance = models.IntegerField()

    def __str__(self):
        return '{} {} {}'.format(self.src, self.dst, self.distance)

    class Meta:
        verbose_name = 'Расстояние'
        verbose_name_plural = 'Расстояние'
        ordering = ['distance']
        unique_together = [['src', 'dst']]

