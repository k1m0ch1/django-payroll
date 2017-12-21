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
from system.models import Inventory, Konfigurasi, GajiPokok, PotonganKaryawan, Pinjaman, Bonusthr
from system.models import MasaTenggangClosing, IzinCuti
from system.models import TunjanganKaryawan, bpjs as BPJS
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from sys import getsizeof
from django.core import serializers
from dateutil.parser import parse
import json
import os, time
from pathlib import * 

modules = Modules.objects.all()
allmenu = Modules.objects.only('name')

@login_required
def absensi_index(request):
	a = Absensi.objects.all().order_by("-created_at")
	return render(request, "absen/dashboard.html", { 'absen': a, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request)})

@login_required
def overtime_index(request):
	a = Absensi.objects.all().order_by("-created_at")
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
	ks = KaryawanShift.objects.all()

	if request.method == "GET":

		if 'search' in request.GET:
			ks = ks.filter(karyawan__NIK__contains=request.GET['value']) if request.GET['search'] == "nik" else ks
			ks = ks.filter(karyawan__name__contains=request.GET['value']) if request.GET['search'] == "name" else ks

	dep = Departemen.objects.all()
	per = Perusahaan.objects.all()
	bag = Bagian.objects.all()
	gol = Golongan.objects.all()
	jab = Jabatan.objects.all()
	shift = Shift.objects.all()
	
	ks = ks.order_by("-created_at")
	
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
def izincuti_index(request):
	k = Karyawan.objects.all()
	dep = Departemen.objects.all()
	per = Perusahaan.objects.all()
	bag = Bagian.objects.all()
	gol = Golongan.objects.all()
	jab = Jabatan.objects.all()
	shift = Shift.objects.all()
	ic = IzinCuti.objects.all().order_by("-created_at")
	
	page = request.GET.get('page', 1)
	paginator = Paginator(ic, 20)
    
	try:
 		ic = paginator.page(page)
	except PageNotAnInteger:
		ic = paginator.page(1)
	except EmptyPage:
   		ic = paginator.page(paginator.num_pages)

	return render(request, "izincuti/dashboard.html", { 'dsb' : modules, 'karyawan': k, 'departemen' : dep, 'bagian': bag,
															 'golongan' : gol, 'jabatan' : jab, 'ic': ic, 'shift' : shift,
															 'module' : getModule(request), 'perusahaan' : per, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def potongankaryawan_index(request):

	pk = PotonganKaryawan.objects.all()

	if request.method == "GET":

		if 'search' in request.GET:
			pk = pk.filter(karyawan__NIK__contains=request.GET['value']) if request.GET['search'] == "nik" else pk
			pk = pk.filter(karyawan__name__contains=request.GET['value']) if request.GET['search'] == "name" else pk

	k = Karyawan.objects.all()
	dep = Departemen.objects.all()
	bag = Bagian.objects.all()
	gol = Golongan.objects.all()
	per = Perusahaan.objects.all()
	jab = Jabatan.objects.all()
	shift = Shift.objects.all()
	mas = MasaTenggangClosing.objects.all()	

	pk = pk.order_by("-updated_at")
	
	page = request.GET.get('page', 1)
	paginator = Paginator(pk, 15)
    
	try:
 		pk = paginator.page(page)
	except PageNotAnInteger:
		pk = paginator.page(1)
	except EmptyPage:
   		pk = paginator.page(paginator.num_pages)

	return render(request, "potongan/dashboard.html", { 'pk': pk,'mas' : mas,'dsb' : modules, 'karyawan': k, 'departemen' : dep, 'bagian': bag,
															 'golongan' : gol, 'jabatan' : jab,
															 'module' : getModule(request), 'perusahaan' : per, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def bpjs_index(request):

	bpjs = PotonganKaryawan.objects.all()

	if request.method == "GET":

		if 'search' in request.GET:
			bpjs = bpjs.filter(karyawan__NIK__contains=request.GET['value']) if request.GET['search'] == "nik" else bpjs
			bpjs = bpjs.filter(karyawan__name__contains=request.GET['value']) if request.GET['search'] == "name" else bpjs

	k = Karyawan.objects.all()
	dep = Departemen.objects.all()
	bag = Bagian.objects.all()
	gol = Golongan.objects.all()
	per = Perusahaan.objects.all()
	jab = Jabatan.objects.all()
	shift = Shift.objects.all()

	bpjs = bpjs.order_by("-updated_at")
	
	page = request.GET.get('page', 1)
	paginator = Paginator(bpjs, 15)
    
	try:
 		bpjs = paginator.page(page)
	except PageNotAnInteger:
		bpjs = paginator.page(1)
	except EmptyPage:
   		bpjs = paginator.page(paginator.num_pages)

	return render(request, "bpjs/dashboard.html", { 'bpjs': bpjs, 'dsb' : modules, 'karyawan': k, 'departemen' : dep, 'bagian': bag,
															 'golongan' : gol, 'jabatan' : jab,
															 'module' : getModule(request), 'perusahaan' : per, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def ptkp_index(request):

	ptkp = Karyawan.objects.all()

	if request.method == "GET":

		if 'search' in request.GET:
			ptkp = ptkp.filter(NIK__contains=request.GET['value']) if request.GET['search'] == "nik" else ptkp
			ptkp = ptkp.filter(name__contains=request.GET['value']) if request.GET['search'] == "name" else ptkp

	k = Karyawan.objects.all()
	dep = Departemen.objects.all()
	bag = Bagian.objects.all()
	gol = Golongan.objects.all()
	per = Perusahaan.objects.all()
	jab = Jabatan.objects.all()
	shift = Shift.objects.all()

	ptkp = ptkp.order_by("-updated_at")
	
	page = request.GET.get('page', 1)
	paginator = Paginator(ptkp, 15)
    
	try:
 		ptkp = paginator.page(page)
	except PageNotAnInteger:
		ptkp = paginator.page(1)
	except EmptyPage:
   		ptkp = paginator.page(paginator.num_pages)

	return render(request, "ptkp/dashboard.html", { 'ptkp': ptkp, 'dsb' : modules, 'karyawan': k, 'departemen' : dep, 'bagian': bag,
															 'golongan' : gol, 'jabatan' : jab,
															 'module' : getModule(request), 'perusahaan' : per, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def tunjangankaryawan_index(request):

	tk = TunjanganKaryawan.objects.all()

	if request.method == "GET":

		if 'search' in request.GET:
			tk = tk.filter(karyawan__NIK__contains=request.GET['value']) if request.GET['search'] == "nik" else tk
			tk = tk.filter(karyawan__name__contains=request.GET['value']) if request.GET['search'] == "name" else tk

	k = Karyawan.objects.all()
	dep = Departemen.objects.all()
	bag = Bagian.objects.all()
	gol = Golongan.objects.all()
	per = Perusahaan.objects.all()
	jab = Jabatan.objects.all()
	shift = Shift.objects.all()
	mas = MasaTenggangClosing.objects.all()	

	tk = tk.order_by("-updated_at")
	
	page = request.GET.get('page', 1)
	paginator = Paginator(tk, 15)
    
	try:
 		tk = paginator.page(page)
	except PageNotAnInteger:
		tk = paginator.page(1)
	except EmptyPage:
   		tk = paginator.page(paginator.num_pages)

	return render(request, "tunjangan/dashboard.html", { 'tk': tk, 'mas' : mas,'dsb' : modules, 'karyawan': k, 'departemen' : dep, 'bagian': bag,
															 'golongan' : gol, 'jabatan' : jab,
															 'module' : getModule(request), 'perusahaan' : per, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def bonusthr_index(request):

	tk = Bonusthr.objects.all()

	if request.method == "GET":

		if 'search' in request.GET:
			tk = tk.filter(karyawan__NIK__contains=request.GET['value']) if request.GET['search'] == "nik" else tk
			tk = tk.filter(karyawan__name__contains=request.GET['value']) if request.GET['search'] == "name" else tk

	k = Karyawan.objects.all()
	dep = Departemen.objects.all()
	bag = Bagian.objects.all()
	gol = Golongan.objects.all()
	per = Perusahaan.objects.all()
	jab = Jabatan.objects.all()
	shift = Shift.objects.all()
	mas = MasaTenggangClosing.objects.all()	

	tk = tk.order_by("-updated_at")
	
	page = request.GET.get('page', 1)
	paginator = Paginator(tk, 15)
    
	try:
 		tk = paginator.page(page)
	except PageNotAnInteger:
		tk = paginator.page(1)
	except EmptyPage:
   		tk = paginator.page(paginator.num_pages)

   	for xx in tk:
   		gp = GajiPokok.objects.get(karyawan_id=xx.karyawan.id)
   		lamakerja = (parse(time.strftime("%d/%m/%Y"))-parse(xx.karyawan.tanggalmasuk.strftime("%d/%m/%Y")))
   		if lamakerja.days > 365 :
   			try:
	   			bti = Bonusthr.objects.get(karyawan_id=xx.karyawan.id)
				bti = Bonusthr.objects.select_for_update().filter(karyawan_id=xx.karyawan.id)
				bti.update(thr=(gp.gajipokok+gp.jabatan))
			except Bonusthr.DoesNotExist:
				bti = Bonusthr(thr=(gp.gajipokok+gp.jabatan))
				bti.save()
		elif lamakerja.days <365 and lamakerja.days >= 31 :
			try:
	   			bti = Bonusthr.objects.get(karyawan_id=xx.karyawan.id)
				bti = Bonusthr.objects.select_for_update().filter(karyawan_id=xx.karyawan.id)
				bti.update(thr=int(int(gp.gajipokok+gp.jabatan)/12)*int(lamakerja.days/30))
			except Bonusthr.DoesNotExist:
				bti = Bonusthr(thr=int(int(gp.gajipokok+gp.jabatan)/12)*int(lamakerja.days/30))
				bti.save()

	tk = Bonusthr.objects.all()

	if request.method == "GET":

		if 'search' in request.GET:
			tk = tk.filter(karyawan__NIK__contains=request.GET['value']) if request.GET['search'] == "nik" else tk
			tk = tk.filter(karyawan__name__contains=request.GET['value']) if request.GET['search'] == "name" else tk

	k = Karyawan.objects.all()
	dep = Departemen.objects.all()
	bag = Bagian.objects.all()
	gol = Golongan.objects.all()
	per = Perusahaan.objects.all()
	jab = Jabatan.objects.all()
	shift = Shift.objects.all()
	mas = MasaTenggangClosing.objects.all()	

	tk = tk.order_by("-updated_at")
	
	page = request.GET.get('page', 1)
	paginator = Paginator(tk, 15)
    
	try:
 		tk = paginator.page(page)
	except PageNotAnInteger:
		tk = paginator.page(1)
	except EmptyPage:
   		tk = paginator.page(paginator.num_pages)

	return render(request, "bonusthr/dashboard.html", { 'tk': tk, 'mas' : mas,'dsb' : modules, 'karyawan': k, 'departemen' : dep, 'bagian': bag,
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
def download(request, dire, path):
    file_path = os.path.join(settings.MEDIA_ROOT, dire + path)
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
	files = []
	if filePath.is_dir():
		#mtime = lambda f: os.stat(os.path.join("./laporan/gaji/", f)).st_mtime
		#file = list(sorted(os.listdir("./laporan/gaji/"), key=mtime))
	    files = list(x for x in filePath.iterdir() if x.is_file())

	return render(request, "laporan-gaji/dashboard.html", { 'files': files, 'mas' : mas, 'dsb' : modules, 'karyawan': k, 'departemen' : dep, 'bagian': bag,
															 'golongan' : gol, 'jabatan' : jab,
															 'module' : getModule(request), 'perusahaan' : per, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def laporanbpjs_index(request):
	k = Karyawan.objects.all()
	dep = Departemen.objects.all()
	bag = Bagian.objects.all()
	gol = Golongan.objects.all()
	per = Perusahaan.objects.all()
	jab = Jabatan.objects.all()
	mas = MasaTenggangClosing.objects.all()

	filePath = Path("./laporan/bpjs/")
	files = []
	if filePath.is_dir():
		#mtime = lambda f: os.stat(os.path.join("./laporan/gaji/", f)).st_mtime
		#file = list(sorted(os.listdir("./laporan/gaji/"), key=mtime))
	    files = list(x for x in filePath.iterdir() if x.is_file())

	return render(request, "laporan-bpjs/dashboard.html", { 'files': files, 'mas' : mas, 'dsb' : modules, 'karyawan': k, 'departemen' : dep, 'bagian': bag,
															 'golongan' : gol, 'jabatan' : jab,
															 'module' : getModule(request), 'perusahaan' : per, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def datakaryawan_index(request):
	k = Karyawan.objects.all()
	dep = Departemen.objects.all()
	bag = Bagian.objects.all()
	gol = Golongan.objects.all()
	per = Perusahaan.objects.all()
	jab = Jabatan.objects.all()
	mas = MasaTenggangClosing.objects.all()

	filePath = Path("./laporan/datakaryawan/")
	files = []
	if filePath.is_dir():
		#mtime = lambda f: os.stat(os.path.join("./laporan/gaji/", f)).st_mtime
		#file = list(sorted(os.listdir("./laporan/gaji/"), key=mtime))
	    files = list(x for x in filePath.iterdir() if x.is_file())

	return render(request, "laporan-datakaryawan/dashboard.html", { 'files': files, 'mas' : mas, 'dsb' : modules, 'karyawan': k, 'departemen' : dep, 'bagian': bag,
															 'golongan' : gol, 'jabatan' : jab,
															 'module' : getModule(request), 'perusahaan' : per, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def laporanabsensi_index(request):
	k = Karyawan.objects.all()
	dep = Departemen.objects.all()
	bag = Bagian.objects.all()
	gol = Golongan.objects.all()
	per = Perusahaan.objects.all()
	jab = Jabatan.objects.all()
	mas = MasaTenggangClosing.objects.all()

	filePath = Path("./laporan/absensi/")
	files = []
	if filePath.is_dir():
	    files = list(x for x in filePath.iterdir() if x.is_file())

	return render(request, "laporan-absensi/dashboard.html", { 'files': files, 'mas' : mas, 'dsb' : modules, 'karyawan': k, 'departemen' : dep, 'bagian': bag,
															 'golongan' : gol, 'jabatan' : jab,
															 'module' : getModule(request), 'perusahaan' : per, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def laporanpinjamankaryawan_index(request):
	k = Karyawan.objects.all()
	dep = Departemen.objects.all()
	bag = Bagian.objects.all()
	gol = Golongan.objects.all()
	per = Perusahaan.objects.all()
	jab = Jabatan.objects.all()
	mas = MasaTenggangClosing.objects.all()

	filePath = Path("./laporan/absensi/")
	files = []
	if filePath.is_dir():
	    files = list(x for x in filePath.iterdir() if x.is_file())

	return render(request, "laporan-absensi/dashboard.html", { 'files': files, 'mas' : mas, 'dsb' : modules, 'karyawan': k, 'departemen' : dep, 'bagian': bag,
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
	try:
		potongan = PotonganKaryawan.objects.get(karyawan_id=karyawan_id)
	except PotonganKaryawan.DoesNotExist:
		potongan = PotonganKaryawan

	return render(request, "karyawan/detail.html", {'karyawan' : karyawan, 'absen': absen, 'gajipokok': gajipokok , 'pinjaman' : pinjaman, 
													'parent' : getParent(request), 'potongan' : potongan, 'dsb': modules})

@login_required()
def perusahaan_index(request):
	perusahaan = Perusahaan.objects.all().order_by("-created_at")
	return render(request, "include/base-dashboard.html", { 'ulang' : perusahaan, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request) })

@login_required()
def shift_index(request):
	data = serializers.serialize( "python", Shift.objects.all().order_by("-created_at"),fields=('name','jammasuk', 'jamkeluar', 'desc'))
	exfield = [{'field': 'Jam Masuk'}, {'field': 'Jam Keluar'}]
	return render(request, "include/base-dyn-dashboard.html", { 'ulang' : data, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request), 'exfield' : exfield})

@login_required()
def masatenggangclosing_index(request):
	data = serializers.serialize( "python", MasaTenggangClosing.objects.all(),fields=('name','tanggal', 'sd', 'desc'))
	exfield = [{'field': 'Tanggal Mulai'}, {'field': 'Tanggal Akhir'}]
	return render(request, "include/base-dyn-dashboard.html", { 'ulang' : data, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request), 'exfield' : exfield})

@login_required()
def hariraya_index(request):
	data = serializers.serialize( "python", HariRaya.objects.all(),fields=('name','tanggal', 'sd', 'desc'))
	exfield = [{'field': 'Tanggal Mulai'}, {'field': 'Tanggal Akhir'}]
	return render(request, "include/base-dyn-dashboard.html", { 'ulang' : data, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request), 'exfield' : exfield})

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
	getmodule = [x.strip() for x in request.get_full_path().split('?')][0]
	getmodule = [x.strip() for x in getmodule.split('/')][2]
	for sb in modules:
		if getmodule.upper() == sb.name:
			return sb.fungsi

def getParent(request):
	getmodule = [x.strip() for x in request.get_full_path().split('?')][0]
	getmodule = [x.strip() for x in getmodule.split('/')][2]
	for sb in modules:
		if getmodule.upper() == sb.name:
			return sb.menu