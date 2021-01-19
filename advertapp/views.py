from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from advertapp.form import AdvertForm
from advertapp.models import Advert


@login_required(login_url='/login/')
@staff_member_required
def advert_view(request):
    message = None
    advert_qs = Advert.objects.all()
    query = request.GET.get('query')
    if query:
        query = query.strip()
        advert_qs = advert_qs.filter(
            Q(name__icontains=query) |
            Q(slug__icontains=query)
        )
        message = f'Вся реклама по поиску "{query}"'

    return render(request, "advertapp/advert_view.html", {
        'advert_qs': advert_qs.order_by('title'),
        'active': 'advert',
        'message': message,
    })


@login_required(login_url='/login/')
@staff_member_required
def advert_edit(request, pk=None):
    """
    Добавить или отредактировать тег
    """
    advert = None
    if pk:
        advert = get_object_or_404(Advert, pk=pk)
    form = AdvertForm(data=request.POST or None, files=request.FILES or None, instance=advert)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(advert_view)

    return render(request, "advertapp/advert_edit.html", {
        'form': form,
        'advert': advert,
        'active': 'advert',
    })
