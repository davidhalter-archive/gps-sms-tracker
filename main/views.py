# Create your views here.
from django.shortcuts import render_to_response, redirect
from django import forms
from django.template import RequestContext

from main import models

class UserForm(forms.ModelForm):
    class Meta:
        model = models.User


def index(request, id=None):
    if id is not None:
        id = int(id)

    if request.method == 'POST':
        form = UserForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            form.save()
            return redirect('/')

    form = UserForm()  # An unbound form

    user_list = models.User.objects.all().order_by('name')
    context = {'form': form, 'user_list': user_list, 'id': id}
    return render_to_response('index.html', context,
                              context_instance=RequestContext(request))

def delete(request, id):
    models.User.objects.filter(id=id).delete()
    return redirect('/')
