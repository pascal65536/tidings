from django import forms

from advertapp.models import Advert



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
