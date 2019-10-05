from django import forms

from postapp.models import Post


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
        fields = [
            'title', 'lead', 'text', 'charter', 'date_post', 'picture', 'og_picture',
            'tags', 'deleted',  'meta_title', 'meta_keywords', 'meta_description',
                  ]
