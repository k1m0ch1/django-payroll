from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader, Context
import django_tables2 as tables
from django.template import RequestContext
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required()
def index(request):
	return HttpResponse('kamseupay')

def loginpage(request):
	return render(request, "login.html", { 'login' : "ah"})

def loginrequest(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		auth_login(request, user)
		return redirect('index')
	else:
		return render('request', "login.html", { 'login' : "gagal"})
