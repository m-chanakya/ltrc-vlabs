from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.template import RequestContext
from users.forms import RegistrationForm

def home(request):
	return render(request,'users/home.html',{'user':request.user})

def login(request):
	return render(request,'users/login.html')

def register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')

	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
			username=form.cleaned_data['username'],
			email=form.cleaned_data['email']
			)
			user.set_password(form.cleaned_data['password1'])
			user.profile.institute = form.cleaned_data['institute']
			user.profile.institute = form.cleaned_data['course']
			user.profile.save()
			user.save()
        		return HttpResponseRedirect('/')
	else:
		form = RegistrationForm()
	return render(request,'users/register.html',{'form':form})
