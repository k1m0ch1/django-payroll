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
from system.models import Inventory, Konfigurasi
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from sys import getsizeof
from django.core import serializers
import json

modules = Modules.objects.all()

@login_required()
def karyawan(request):
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

	kategori = request.GET['kategori']
	keywords = request.GET['keywords']
	pilihan = Selected("selected" ,"", "", "", "", "")

	if kategori=="Departemen":
		karyawan_list = Karyawan.objects.filter(departemen__name__icontains=keywords).order_by('-created_at')
		pilihan = Selected("" ,"", "", "selected", "", "")
	elif kategori=="Kategori":
		karyawan_list = Karyawan.objects.all().order_by('-created_at')
		pilihan = Selected("selected" ,"", "", "", "", "")
	elif kategori=="NIK":
		karyawan_list = Karyawan.objects.filter(NIK__icontains=keywords).order_by('-created_at')
		pilihan = Selected("" ,"selected", "", "", "", "")
	elif kategori=="Nama":
		karyawan_list = Karyawan.objects.filter(name__icontains=keywords).order_by('-created_at')
		pilihan = Selected("" ,"", "selected", "", "", "")
	elif kategori=="Bagian":
		karyawan_list = Karyawan.objects.filter(bagian__name__icontains=keywords).order_by('-created_at')
		pilihan = Selected("" ,"", "", "", "selected", "")
	elif kategori=="Golongan":
		karyawan_list = Karyawan.objects.filter(golongan__name__icontains=keywords).order_by('-created_at')
		pilihan = Selected("" ,"", "", "", "", "selected")

	page = request.GET.get('page', 1)
	paginator = Paginator(karyawan_list, 30)	
    
	try:
 		karyawan = paginator.page(page)
	except PageNotAnInteger:
		karyawan = paginator.page(1)
	except EmptyPage:
   		karyawan = paginator.page(paginator.num_pages)

   	

	return render(request, "karyawan/dashboard.html", { 'karyawan' : karyawan, 'dsb' : modules, 'selected': pilihan, 'keywords' : keywords })