from django import forms
from postapp.models import Post
# from ckeditor.fields import RichTextFormField


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
    Форма редактирования
    """
    class Meta:
        model = Post
        exclude = []
