from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader, Context
import django_tables2 as tables
from django.template import RequestContext
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from system.models import Perusahaan, Departemen, Modules, Karyawan, Konfigurasi, IzinCuti, Absensi
from datetime import datetime, timedelta

modules = Modules.objects.all()

def waktu(waktu=None, jadwal=None, masuk=None):
	hasil = 0
	akhir = 0

	wj, wm, wd = waktu.strftime("%H:%M:%S").split(':')
	waktu = (int(wj)*3600) + (int(wm)*60) + int(wd)

	jj, jm, jd = jadwal.strftime("%H:%M:%S").split(':')
	jadwal = (int(jj)*3600) + (int(jm)*60) + int(jd)

	nilai = waktu-jadwal

	return nilai

@login_required()
def index(request):
	banyak = Karyawan.objects.all().count()
	banyakcuti = IzinCuti.objects.filter(tglmulai__month = datetime.now().month ).count()
	banyakabsenkemaren = Absensi.objects.filter(tanggal__day = datetime.now().day - 1).count()
	hariiniabsen = Absensi.objects.filter(tanggal__day = datetime.now().day).count()
	banyaktelat = 0
	banyakmasuk = 0
	bulanabsen = ""
	for x in range(0,12):
		bulanabsen = str(Absensi.objects.filter(tanggal__month = x).count()) + ", " + str(bulanabsen)

	bulancuti = ""
	for x in range(0, 12):
		bulancuti = "["+ str(int(x+2)) + ", " + str(IzinCuti.objects.filter(tglmulai__month = x+1 ).count()) + "], " + str(bulancuti)

	mauabis = Karyawan.objects.filter(masakaryawan__range = [ datetime.now(), ( datetime.now() + timedelta(days=7))])

	absenkemaren = Absensi.objects.filter(tanggal__day = datetime.now().day - 1)
	for y in absenkemaren :
		if waktu(y.masuk, y.karyawanshift.shift.jammasuk, True) > 300:
			banyaktelat = banyaktelat + 1
		else:
			banyakmasuk = banyakmasuk + 1

	dataPayroll = { 'dsb' : modules, 'banyakKaryawan' :  banyak , 'banyakCuti' : banyakcuti, 
					'banyakabsenkemaren' : banyakabsenkemaren, 'hariiniabsen' : hariiniabsen,
					'bulanabsen' : bulanabsen, 'bulancuti': bulancuti,
					'mauabis' : mauabis, 'banyaktelat' : banyaktelat,
					'banyakmasuk' : banyakmasuk}
	return render(request, "dashboard.html", dataPayroll)

def loginpage(request):
	informasi = Konfigurasi.objects.filter(name="isi-informasi").all()
	logo = Konfigurasi.objects.filter(name="logo").all()
	judul = Konfigurasi.objects.filter(name="judul-informasi").all()
	settings = {'informasi': informasi, 'logo' : logo, 'judul': judul}
	return render(request, "login.html", { 'settings': settings, 'login' : "firsttime"})

def loginrequest(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		auth_login(request, user)
		return render(request, "login.html", { 'login' : "berhasil"})
	else:
		return render(request, "login.html", { 'login' : "gagal"})

@login_required()
def logout_view(request):
	logout(request)
	return render(request, "login.html", { 'login' : "logout"})

@login_required()
def perusahaan_edit(request):
	return HttpResponse("edit")

@login_required()
def departemen_edit(request):
	return HttpResponse("edit")

@login_required()
def perusahaan_delete(request):
	return HttpResponse("Delete")

@login_required()
def departemen_delete(request):
	return HttpResponse("Delete")