import json

from ckeditor.widgets import CKEditorWidget
from django import forms
from django.conf.urls.static import static
from taggit.models import Tag

from advertapp.models import Advert
from postapp.models import Post, Charter
from django.forms import Textarea
from django.utils.safestring import mark_safe


class AdvertForm(forms.ModelForm):
    """
    Форма редактирования рекламы
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['date_start'].widget.attrs.update({
            'class': 'form_datetime',
            'required': 'required',
            'data-provide': 'datetimepicker',
            'data-date-format': 'dd.mm.yyyy hh:ii:ss',
        })

        self.fields['date_stop'].widget.attrs.update({
            'class': 'form_datetime',
            'required': 'required',
            'data-provide': 'datetimepicker',
            'data-date-format': 'dd.mm.yyyy hh:ii:ss',
        })

    class Meta:
        model = Advert
        exclude = ['changed', 'created', 'deleted', 'counter_json']
