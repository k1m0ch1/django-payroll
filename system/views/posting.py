from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader, Context
import django_tables2 as tables
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from system.models import Perusahaan, Departemen, Bagian, Golongan, Jabatan, Konfigurasi
from system.models import Bank, Agama, WargaNegara, StatusMenikah, Modules, Inventory, Absensi
from system.models import LokasiPerusahaan, Karyawan, HariRaya, KaryawanShift, Shift, GajiPokok
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from sys import getsizeof
from django.core import serializers
import json
from dateutil.parser import parse
import datetime

modules = Modules.objects.all()
allmenu = Modules.objects.only('name')

@login_required()
def postinggaji(request):

	class postgaji(object):
			no = ""
			nik = ""
			nama = ""
			departemen = ""
			bagian = ""
			golongan = ""
			gajipokok = ""
			gajipokok = ""
			tmakan = ""
			transportnonexec = ""

			def __init__(self, no, nik, nama, departemen, bagian, golongan, gajipokok, tmakan, transportnonexec):
				self.no = no
				self.nik = nik
				self.nama = nama
				self.departemen = departemen
				self.bagian = bagian
				self.golongan = golongan
				self.gajipokok = gajipokok
				self.tmakan = tmakan
				self.transportnonexec = transportnonexec

	today = datetime.datetime.now()
	idkaryawan = request.POST['idkaryawan']
	listid = [x.strip() for x in idkaryawan.split(',')]
	a = ""
	mantap = ""
	objs = [range(0, len(listid)-1)]

	for y in range(0, len(listid)-1):
		a = Absensi.objects.filter(karyawan=listid[y]).filter(tanggal__year=today.year).filter(tanggal__month=4)
		k = Karyawan.objects.get(pk=listid[y])
		g = GajiPokok.objects.get(karyawan_id=listid[y])

		gajipokok = g.gajipokok 
		tunjanganmakan = g.tmakan
		makanlembur = g.makanlembur
		transportnonexec = g.transportnonexec

		# for x in a:
		# 	mantap =  waktu(x.keluar, x.karyawanshift.shift.jamkeluar, True)
		
		objs.append(postgaji(y+1, k.NIK, k.name, k.departemen.name, k.bagian.name, k.golongan.name, g.gajipokok, tunjanganmakan, transportnonexec))


	return render(request,"postinggaji/print.html", { 'data': mantap, 'idkaryawan': listid[y], 'posting' : objs})

def waktu(waktu=None, jadwal=None, masuk=None):
	hasil = 0
	akhir = 0

	wj, wm, wd = waktu.strftime("%H:%M:%S").split(':')
	waktu = (int(wj)*3600) + (int(wm)*60) + int(wd)

	jj, jm, jd = jadwal.strftime("%H:%M:%S").split(':')
	jadwal = (int(jj)*3600) + (int(jm)*60) + int(jd)

	nilai = waktu-jadwal

	return nilai
	# jamA = int(nilai)/3600
	# menitA = int(nilai)/60
	# detikA = int(nilai) - int(nilai)
	# jam = 0
	# menit = 0
	# detik = 0
	# jamB= False
	# menitB= False
	# #melakukan lebih awal daripada jam
	# #akhir = "< " if jamA == -1 else ""
	# akhir = 0

	# if jamA < -1 :
	# 	a, jam = str(jamA).split('-')
	# 	#jam = str(jamA+3) + " jam "
	# 	jam = int(jamA+3)
	# 	akhir = akhir + jam
	# elif jamA > 0 :
	# 	akhir = akhir + int(jamA)
	# 	jamB = True

	# if menitA <= -1 :
	# 	a, menit = str(int(menitA%-60)).split('-')
	# 	akhir = akhir + int(menit)
	# elif menitA > 0 :
	# 	hasil = hasil + int(menitA%60)
	# 	akhir = akhir + hasil if jamB == False else akhir + hasil
	# 	menitB = True

	# if detikA <= -1 :
	# 	a, detik = str(detikA).split('-')
	# 	hasil = hasil + int(detik)
	# 	akhir = akhir + hasil
	# elif int(nilai) - int(nilai) >0:
	# 	hasil = hasil + detikA 
	# 	akhir = akhir + hasil


	# return akhir 