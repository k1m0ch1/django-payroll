from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader, Context
import django_tables2 as tables
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from system.models import Perusahaan, Departemen, Bagian, Golongan, Jabatan
from system.models import Bank, Agama, WargaNegara, StatusMenikah, Modules, Absensi
from system.models import LokasiPerusahaan, Karyawan, HariRaya, KaryawanShift, Shift
from system.models import Inventory, Konfigurasi, GajiPokok, PotonganKaryawan, Pinjaman
from system.models import MasaTenggangClosing
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from sys import getsizeof
from django.core import serializers
import json
import os
from pathlib import * 

modules = Modules.objects.all()
allmenu = Modules.objects.only('name')

@login_required
def absensi_index(request):
	a = Absensi.objects.all()
	return render(request, "absen/dashboard.html", { 'absen': a, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request)})

@login_required
def overtime_index(request):
	a = Absensi.objects.all()
	return render(request, "overtime/dashboard.html", { 'absen': a, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request)})

@login_required
def api_karyawan(request):
	
	k = Karyawan.objects.all()
	if request.method == "GET":

		if 'perusahaan' in request.GET:
			perusahaan = "" if request.GET['perusahaan'] == "" else request.GET['perusahaan']
			k = k.filter(perusahaan_id=perusahaan) if perusahaan != "" else k

		if 'departemen' in request.GET:
			departemen = "" if request.GET['departemen'] == "" else request.GET['departemen']
			k = k.filter(departemen_id=departemen) if departemen != "" else k

		if 'bagian' in request.GET:
			bagian = "" if request.GET['bagian'] == "" else request.GET['bagian']
			k = k.filter(bagian_id=bagian) if bagian != "" else k

		if 'golongan' in request.GET:
			golongan = "" if request.GET['golongan'] == "" else request.GET['golongan']
			k = k.filter(golongan_id=golongan) if golongan != "" else k

		# if 'jabatan' in request.GET:
		# 	jabatan = "" if request.GET['jabatan'] == "" else request.GET['jabatan']
		# 	k = k.filter(jabatan_id=jabatan) if jabatan != "" else k

		if 'nik' in request.GET:
			nik = "" if request.GET['nik'] == "" else request.GET['nik']
			k = k.filter(NIK__contains=nik) if nik != "" else k

		if 'name' in request.GET:
			name = request.GET['name'] if request.GET['name'] != "" else ""
			k = k.filter(name__contains=name) if name != "" else k	

	per = Perusahaan.objects.all()
	dep = Departemen.objects.all()
	bag = Bagian.objects.all()
	gol = Golongan.objects.all()
	jab = Jabatan.objects.all()
	ks = KaryawanShift.objects.all()

	page = request.GET.get('page', 1)
	paginator = Paginator(k, 10)	
    
	try:
 		k = paginator.page(page)
	except PageNotAnInteger:
		k = paginator.page(1)
	except EmptyPage:
   		k = paginator.page(paginator.num_pages)

	return render(request, "karyawanshift/modal.html", { 'karyawan': k, 'departemen' : dep, 'bagian': bag,
															 'golongan' : gol, 'jabatan' : jab, 'perusahaan' : per, 'ks': ks})

   	# return HttpResponse(serializers.serialize("json", [q for q in k.object_list]), content_type='application/json')
   	# return HttpResponse(json.dumps([k.get_queryset()]))
   	# return HttpResponse(json.dumps(tai))


@login_required()
def karyawan_shift_index(request):
	k = Karyawan.objects.all()
	dep = Departemen.objects.all()
	per = Perusahaan.objects.all()
	bag = Bagian.objects.all()
	gol = Golongan.objects.all()
	jab = Jabatan.objects.all()
	shift = Shift.objects.all()
	ks = KaryawanShift.objects.all()
	
	page = request.GET.get('page', 1)
	paginator = Paginator(ks, 20)
    
	try:
 		ks = paginator.page(page)
	except PageNotAnInteger:
		ks = paginator.page(1)
	except EmptyPage:
   		ks = paginator.page(paginator.num_pages)

	return render(request, "karyawanshift/dashboard.html", { 'dsb' : modules, 'karyawan': k, 'departemen' : dep, 'bagian': bag,
															 'golongan' : gol, 'jabatan' : jab, 'ks': ks, 'shift' : shift,
															 'module' : getModule(request), 'perusahaan' : per, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def potongankaryawan_index(request):
	k = Karyawan.objects.all()
	dep = Departemen.objects.all()
	bag = Bagian.objects.all()
	gol = Golongan.objects.all()
	per = Perusahaan.objects.all()
	jab = Jabatan.objects.all()
	shift = Shift.objects.all()

	return render(request, "potongan/dashboard.html", { 'dsb' : modules, 'karyawan': k, 'departemen' : dep, 'bagian': bag,
															 'golongan' : gol, 'jabatan' : jab,
															 'module' : getModule(request), 'perusahaan' : per, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def postinggaji_index(request):
	k = Karyawan.objects.all()
	dep = Departemen.objects.all()
	bag = Bagian.objects.all()
	gol = Golongan.objects.all()
	per = Perusahaan.objects.all()
	jab = Jabatan.objects.all()
	mas = MasaTenggangClosing.objects.all()

	return render(request, "postinggaji/dashboard.html", { 'mas' : mas, 'dsb' : modules, 'karyawan': k, 'departemen' : dep, 'bagian': bag,
															 'golongan' : gol, 'jabatan' : jab,
															 'module' : getModule(request), 'perusahaan' : per, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, 'laporan/gaji/' + path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

@login_required()
def laporangaji_index(request):
	k = Karyawan.objects.all()
	dep = Departemen.objects.all()
	bag = Bagian.objects.all()
	gol = Golongan.objects.all()
	per = Perusahaan.objects.all()
	jab = Jabatan.objects.all()
	mas = MasaTenggangClosing.objects.all()

	filePath = Path("./laporan/gaji/")
	if filePath.is_dir():
	    files = list(x for x in filePath.iterdir() if x.is_file())

	return render(request, "laporan-gaji/dashboard.html", { 'files': files, 'mas' : mas, 'dsb' : modules, 'karyawan': k, 'departemen' : dep, 'bagian': bag,
															 'golongan' : gol, 'jabatan' : jab,
															 'module' : getModule(request), 'perusahaan' : per, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def pinjaman_index(request):
	i = Pinjaman.objects.all()

	return render(request, "pinjaman/dashboard.html", {'ulang' : i, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def karyawan_index(request):

   	class Selected(object):
			kategori = ""
			nik = ""
			nama = ""
			departemen = ""
			bagian = ""
			golongan = ""

			def __init__(self, kategori, nik, nama, departemen, bagian, golongan):
				self.kategori = kategori
				self.nik = nik
				self.nama = nama
				self.departemen = departemen
				self.bagian = bagian
				self.golongan = golongan

	karyawan_list = Karyawan.objects.all().order_by('-created_at')
	page = request.GET.get('page', 1)
	paginator = Paginator(karyawan_list, 30)	
    
	try:
 		karyawan = paginator.page(page)
	except PageNotAnInteger:
		karyawan = paginator.page(1)
	except EmptyPage:
   		karyawan = paginator.page(paginator.num_pages)


   	ilihan = Selected("selected" ,"", "", "", "", "")

	return render(request, "karyawan/dashboard.html", { 'karyawan' : karyawan, 'dsb' : modules, 'selected': "Kategori",'parent' : getParent(request)})

@login_required()
def karyawan_detail(request, karyawan_id):
	karyawan = Karyawan.objects.get(pk=karyawan_id)
	absen = Absensi.objects.filter(karyawan_id=karyawan_id)
	gajipokok = GajiPokok.objects.get(karyawan_id=karyawan_id)
	pinjaman = Pinjaman.objects.filter(karyawan_id=karyawan_id)
	potongan = PotonganKaryawan.objects.get(karyawan_id=karyawan_id)
	return render(request, "karyawan/detail.html", {'karyawan' : karyawan, 'absen': absen, 'gajipokok': gajipokok , 'pinjaman' : pinjaman, 
													'parent' : getParent(request), 'potongan' : potongan, 'dsb': modules})

@login_required()
def perusahaan_index(request):
	perusahaan = Perusahaan.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : perusahaan, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request) })

@login_required()
def shift_index(request):
	data = serializers.serialize( "python", Shift.objects.all(),fields=('name','jammasuk', 'jamkeluar', 'desc'))
	exfield = [{'field': 'Jam Masuk'}, {'field': 'Jam Keluar'}]
	return render(request, "include/base-dyn-dashboard.html", { 'ulang' : data, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request), 'exfield' : exfield})

@login_required()
def masatenggangclosing_index(request):
	data = serializers.serialize( "python", MasaTenggangClosing.objects.all(),fields=('name','tanggal', 'sd', 'desc'))
	exfield = [{'field': 'Tanggal Mulai'}, {'field': 'Tanggal Akhir'}]
	return render(request, "include/base-dyn-dashboard.html", { 'ulang' : data, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request), 'exfield' : exfield})

@login_required()
def hariraya_index(request):
	hariraya = HariRaya.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : hariraya, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def inventory_index(request):
	data = serializers.serialize( "python", Inventory.objects.all(),fields=('name','nomer', 'desc'))
	exfield = [{'field': 'Nomer'}]
	return render(request, "include/base-dyn-dashboard.html", { 'ulang' : data, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request), 'exfield' : exfield})

@login_required()
def departemen_index(request):
	departemen = Departemen.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : departemen, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request) })

@login_required()
def departemen_index(request):
	departemen = Departemen.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : departemen, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request) })

@login_required()
def bagian_index(request):
	bagian = Bagian.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : bagian, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def golongan_index(request):
	golongan = Golongan.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : golongan, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def jabatan_index(request):
	jabatan = Jabatan.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : jabatan, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def bank_index(request):
	bank = Bank.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : bank, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def agama_index(request):
	agama = Agama.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : agama, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def warganegara_index(request):
	warganegara = WargaNegara.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : warganegara, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def statusmenikah_index(request):
	statusmenikah = StatusMenikah.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : statusmenikah, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def konfigurasi_index(request):
	data = serializers.serialize( "python", Konfigurasi.objects.all(),fields=('name', 'value', 'desc'))
	exfield = [{'field': 'Value'}]
	return render(request, "include/base-dyn-dashboard.html", { 'ulang' : data, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request), 'exfield' : exfield})

@login_required()
def profile_perusahaan_index(request):
	lokasi = LokasiPerusahaan.objects.all()
	perusahaan = Perusahaan.objects.get(id=1)
	#return render(request, "profile-perusahaan/dashboard.html", { 'ulang' : lokasi, 'module' : PROFILEPERUSAHAAN})
	return render(request, "profile-perusahaan/dashboard.html", {'ulang': lokasi, 'perusahaan' : perusahaan, 'module' : getModule(request), 
																 'dsb' : modules, 'parent' : getParent(request)})

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