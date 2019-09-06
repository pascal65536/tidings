from django.shortcuts import render
from contactapp.models import Contact
from newsproject.settings_site import sitename


def contact(request):
    contact_list = Contact.objects.all().order_by('name')
    context = {
        'title': 'Контакты | {}'.format(sitename),
        'menu_links': 'menu_links',
        'contact_list': contact_list
    }
    return render(request, 'postapp/post_index.html', context)
