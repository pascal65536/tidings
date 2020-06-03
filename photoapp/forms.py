from django import forms
from photoapp.models import Photo


class PhotoForm(forms.ModelForm):
    """
    Форма для редактирования фото
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['deleted'].widget.attrs.update({
            'class': 'form_datetime',
            'data-provide': 'datetimepicker',
            'data-date-format': 'dd.mm.yyyy hh:ii:ss',
        })

    class Meta:
        model = Photo
        exclude = ['created', 'changed']
