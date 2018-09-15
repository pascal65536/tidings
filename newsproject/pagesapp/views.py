from django.shortcuts import render

# Create your views here.

def contacts(request):
    context = {
        'title': 'sitename',
        'menu_links': 'menu_links'
    }
    return render(request, 'pagesapp/contacts.html', context)
