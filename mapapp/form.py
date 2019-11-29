from django import forms


class SearchForm(forms.Form):
    """
    Поисковый запрос
    """
    search = forms.CharField(label=u'Search', required=False)

    def clean(self):
        cd = super(SearchForm, self).clean()
        return cd
