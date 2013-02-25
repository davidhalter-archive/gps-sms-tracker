# Create your views here.
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext

from main import models

class UserForm(forms.ModelForm):
    class Meta:
        model = models.User


def index(request):
    if request.method == 'POST':
        form = UserForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            form.save()
    elif request.GET.get('action', None) == 'delete':
        models.User.objects.filter(id=request.GET['id']).delete()

    print dir(request), request.raw_post_data
    form = UserForm() # An unbound form

    user_list = models.User.objects.all().order_by('name')
    context = {'form': form, 'user_list': user_list}
    return render_to_response('index.html', context,
                              context_instance=RequestContext(request))
