# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from keys.models import Keys
from picardi import run
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.



def index(request):
    latest_question_list = ''
    template = loader.get_template('index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def prof(request):
    profile_user = request.POST.get('uname')
    temp_keys = Keys.objects.filter(user = 'temp')
    for i in temp_keys:
        i.user = profile_user
        i.save()
    template = loader.get_template('prof.html')
    context = {
        'You have submitted your profile':'1'
    }
    return HttpResponse(template.render(context, request))

def listen(request):
    username = 'temp'
    if request.user.is_authenticated():
        username = request.user.username
    request = eval(request.path.split('n/')[-1])

    for e in request:
        b = Keys(user = username, key_name=e['k'], release = e['r'], timestamp = e['t'])
        b.save()
    if request:
        pass
     #print >>file, request

     #file.close()
    return HttpResponse(request)

def listn2(request):
    request = eval(request.path.split('n2/')[-1])
    file = open('data.txt', 'a')
    all_keys = Keys.objects.filter(user = 'jiaju')

    for e in request:

        print >>file, '%s\t%s\t%s' %( e['t'], e['k'],  e['r'])

    print request

    file.close()
    return HttpResponse(request)

def test(request):
    template = loader.get_template('test.html')
    context = {
        'You have submitted your profile':'1'
    }
    return HttpResponse(template.render(context, request))

def result(request):

    attempt_user = request.POST.get('uname')
    all_keys = Keys.objects.filter(user = attempt_user)
    if not all_keys: return HttpResponse('The user name does not exist')
    #r = '\t'.join([str([ i.timestamp, i.key_name, i.release]) for i in all_keys])
    r = sorted([( i.timestamp, i.key_name, i.release) for i in all_keys if i.release==0])
    #r = ', '.join(str(i) for i in r)
    r= run(r)
    #r = '\t'.join([i[1] for i in r if i[2] == 0])
    #r = '\t'.join([i.key_name for i in all_keys if i.release == 0])
    #r = 'You are supposed to get your test result here'
    open('data.txt', 'w')
    if r<=0.4: return HttpResponse('Welcome back, %s. Your distance score is %s<br><a href = "/keys/test">Back to test page</a><br><a href = "/keys/"> Back to Enrollment </a>'%(attempt_user, r))
    #elif r<= 0.45: return HttpResponse('I am not convinced that you are %s, please type some more keys. Your distance score is %s <br><a href = "/keys/test">Back to test page</a><br><a href = "/keys/"> Back to Enrollment </a>'%(attempt_user, r))
    else: return HttpResponse('Your distance score is %s<br><a href = "/keys/test">Back to test page</a><br><a href = "/keys/"> Back to Enrollment </a>'%(  r))

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})