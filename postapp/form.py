from ckeditor.widgets import CKEditorWidget
from django import forms
from taggit.models import Tag
from postapp.models import Post, Charter



class SearchForm(forms.Form):
    """
    Поисковый запрос
    """
    search = forms.CharField(label=u'Search', required=False)

    def clean(self):
        cd = super(SearchForm, self).clean()
        return cd


class PostForm(forms.ModelForm):
    """
    Форма редактирования поста
    """
    text = forms.CharField(widget=CKEditorWidget())

    def __init__(self, *args, **kwargs):
        images_list = kwargs.pop('images_list', None)
        super().__init__(*args, **kwargs)

        self.fields['photo'].widget.attrs['class'] = 'select2'
        self.fields['photo'].widget.choices = images_list

        self.fields['date_post'].widget.attrs.update({
            'class': 'form_datetime',
            'required': 'required',
            'data-provide': 'datetimepicker',
            'data-date-format': 'dd.mm.yyyy hh:ii:ss',
        })

        self.fields['deleted'].widget.attrs.update({
            'class': 'form_datetime',
            'data-provide': 'datetimepicker',
            'data-date-format': 'dd.mm.yyyy hh:ii:ss',
        })

    class Meta:
        model = Post
        exclude = ['meta_description', 'meta_keywords', 'meta_title', 'changed',
                   'created', 'og_picture', 'picture']


class CharterForm(forms.ModelForm):
    """
    Форма редактирования рубрики
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Charter
        exclude = ['meta_description', 'meta_keywords', 'meta_title', 'og_picture', 'slug']


class TagForm(forms.ModelForm):
    """
    Форма для редактирования тега
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Tag
        exclude = []
