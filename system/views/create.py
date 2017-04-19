from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader, Context
import django_tables2 as tables
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from system.models import Perusahaan, Departemen, Bagian, Golongan, Jabatan
from system.models import Bank, Agama, WargaNegara, StatusMenikah, Modules
from system.models import LokasiPerusahaan, HariRaya, Shift,KaryawanShift
from dateutil.parser import parse
from sys import getsizeof

modules = Modules.objects.all()
allmenu = Modules.objects.only('name')

@login_required()
def shift_save(request):
	shift = [request.POST['shift1'], request.POST['shift2'], request.POST['shift3'],request.POST['shift4']]
	idkaryawan = request.POST['idkaryawan']
	tanggal = request.POST['tanggal']
	tglawal = parse([x.strip() for x in tanggal.split(' ')][0]).strftime("%Y-%m-%d")
	tglakhir = parse([x.strip() for x in tanggal.split(' ')][2]).strftime("%Y-%m-%d")
	listid = [x.strip() for x in idkaryawan.split(',')]
	for y in range(0, len(listid)):
		for z in range(0, 4):
			s = KaryawanShift(karyawan_id=listid[y], shift_id = shift[z], tglawal=tglawal, tglakhir=tglakhir)
			s.save()

	return HttpResponse("yay berhasil")


@login_required()
def departemen(request):
	return render(request, "include/base-form.html", { 'mode' : 'Tambah', 'module' : getModule(request), 
													   'idpk' : 0, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def departemen_save(request):
	nama = request.POST['name']
	desc = request.POST['desc']
	d = Departemen(name=nama, desc=desc)
	d.save()
	return redirect("departemen-index")

@login_required()
def bagian(request):
	return render(request, "include/base-form.html", { 'mode' : 'Tambah', 'module' : getModule(request), 
													   'idpk' : 0, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def bagian_save(request):
	nama = request.POST['name']
	desc = request.POST['desc']
	b = Bagian(name=nama, desc=desc)
	b.save()
	return redirect("bagian-index")

@login_required()
def golongan(request):
	return render(request, "include/base-form.html", { 'mode' : 'Tambah', 'module' : getModule(request), 
													   'idpk' : 0, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def golongan_save(request):
	nama = request.POST['name']
	desc = request.POST['desc']
	g = Golongan(name=nama, desc=desc)
	g.save()
	return redirect("golongan-index")

@login_required()
def jabatan(request):
	return render(request, "include/base-form.html", { 'mode' : 'Tambah', 'module' : getModule(request), 
													   'idpk' : 0, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def jabatan_save(request):
	nama = request.POST['name']
	desc = request.POST['desc']
	j = Jabatan(name=nama, desc=desc)
	j.save()
	return redirect("jabatan-index")

@login_required()
def bank(request):
	return render(request, "include/base-form.html", { 'mode' : 'Tambah', 'module' : getModule(request), 
													   'idpk' : 0, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def bank_save(request):
	nama = request.POST['name']
	desc = request.POST['desc']
	b = Bank(name=nama, desc=desc)
	b.save()
	return redirect("bank-index")

@login_required()
def agama(request):
	return render(request, "include/base-form.html", { 'mode' : 'Tambah', 'module' : getModule(request), 
													   'idpk' : 0, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def agama_save(request):
	nama = request.POST['name']
	desc = request.POST['desc']
	a = Agama(name=nama, desc=desc)
	a.save()
	return redirect("agama-index")

@login_required()
def warganegara(request):
	return render(request, "include/base-form.html", { 'mode' : 'Tambah', 'module' : getModule(request), 
													   'idpk' : 0, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def warganegara_save(request):
	nama = request.POST['name']
	desc = request.POST['desc']
	w = WargaNegara(name=nama, desc=desc)
	w.save()
	return redirect("warganegara-index")

@login_required()
def statusmenikah(request):
	return render(request, "include/base-form.html", { 'mode' : 'Tambah', 'module' : getModule(request), 
													   'idpk' : 0, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def statusmenikah_save(request):
	nama = request.POST['name']
	desc = request.POST['desc']
	s = StatusMenikah(name=nama, desc=desc)
	s.save()
	return redirect("statusmenikah-index")

@login_required()
def profile_perusahaan(request):
	return render(request, "profile-perusahaan/form.html", { 'mode' : 'Tambah', 'module' : getModule(request), 
													   'idpk' : 0, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def profile_perusahaan_save(request):
	alamat = request.POST['name']
	desc = request.POST['desc']
	pp = LokasiPerusahaan(name=alamat, alamat=alamat, desc=desc, perusahaan_id=1)
	pp.save()
	return redirect("profile-perusahaan-index")

@login_required()
def hariraya(request):
	return render(request, "hariraya/form.html", { 'mode' : 'Tambah', 'module' : getModule(request), 
													   'idpk' : 0, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def hariraya_save(request):
	name = request.POST['name']
	tanggal = request.POST['desc']
	sd = request.POST['desc']
	desc = request.POST['desc']
	pp = HariRaya(name=name, tanggal=tanggal, sd=sd, desc=desc)
	pp.save()
	return redirect("hariraya-index")

def getModule(request):
	getmodule = [x.strip() for x in request.get_full_path().split('/')][2]
	for sb in modules:
		if getmodule.upper() == sb.name:
			return sb.fungsi

def getParent(request):
	getmodule = [x.strip() for x in request.get_full_path().split('/')][2]
	for sb in modules:
		if getmodule.upper() == sb.name:
			return sb.menu