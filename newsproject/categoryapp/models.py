from django.db import models
from ckeditor.fields import RichTextField
import mymodule


def latin_filename(instance, filename):
    f_folder = '{:%Y/%m/%d}'.format(instance.date_start)
    salt = '{:%M%S}'.format(instance.date_start)
    part_of_name = filename.split(".")
    f_name = mymodule.cyr_lat('_'.join(part_of_name[0:-1]))
    f_ext = mymodule.cyr_lat(part_of_name[-1])
    return format('{}/{}/{}-{}.{}'.format('news_picture', f_folder, f_name, salt, f_ext))


class Content(models.Model):
    txt_doc_id = models.IntegerField()
    txt_node_id = models.IntegerField()
    txt_title = models.CharField(max_length=255)
    txt_lead = RichTextField(null=True)
    txt_text = RichTextField(null=True)
    txt_author = models.CharField(max_length=255, blank=True, null=False)
    txt_issue = models.IntegerField()
    txt_clean_url = models.CharField(max_length=255)
    txt_publish_start = models.DateTimeField()
    txt_tags = models.CharField(max_length=1000, blank=True, null=False)

    class Meta:
        db_table = 'content'
        verbose_name = 'txt_title'
        verbose_name_plural = 'txt_title'
        ordering = ['-txt_publish_start']

    def __str__(self):
        return self.txt_title


class Person(models.Model):
    person_name = models.CharField(max_length=200)
    person_last_name = models.CharField(max_length=200, blank=True, null=False)
    person_status = models.CharField(max_length=200)
    person_bio = RichTextField(null=True)
    person_bio_short = RichTextField(null=True)
    person_foto = models.CharField(max_length=200, blank=True, null=False)
    person_clean_url = models.CharField(max_length=200)


    class Meta:
        db_table = 'person'
        verbose_name = 'person_status'
        verbose_name_plural = 'person_status'
        ordering = ['person_last_name']

    def __str__(self):
        return self.person_status

