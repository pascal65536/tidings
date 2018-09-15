import urllib
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


font_awesome_dict = {
    'vk.com': 'fa fa-vk',
    'ok.ru': 'fa fa-odnoklassniki',
    'facebook.com': 'fa fa-facebook',
    'twitter.com': 'fa fa-twitter',
    'plus.google.com': 'fa fa-google-plus',
    'linkedin.com': 'fa fa-linkedin',
    'youtube.com': 'fa fa-youtube',
    'pinterest.ru': 'fa fa-pinterest'
}


@register.filter()
def font_awesome(value):
    pp = urllib.parse.urlsplit(value).netloc
    ret = ''
    for lnk, fnt in font_awesome_dict.items():
        if pp.find(lnk) >= 0:
            ret = fnt
    return ret


#print(font_awesome('https://plus.google.com/112709900185667455059'))