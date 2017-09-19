from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader, Context
import django_tables2 as tables
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from system.models import Perusahaan, Departemen, Bagian, Golongan, Jabatan, Konfigurasi
from system.models import Bank, Agama, WargaNegara, StatusMenikah, Modules, Inventory, Absensi
from system.models import LokasiPerusahaan, Karyawan, HariRaya, KaryawanShift, Shift, GajiPokok, PotonganKaryawan
from system.models import PostingGaji, MasaTenggangClosing
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
			norek = ""
			gajipokok = ""
			tmakan = ""
			transportnonexec = ""
			tovertime = ""
			pbpjs = ""
			ppinjam = ""
			pabsen = ""

			def __init__(self, no, nik, nama, departemen, bagian, 
								golongan, norek, gajipokok, tmakan, 
								transportnonexec, tovertime, pbpjs, 
								ppinjam, pabsen):
				self.no = no
				self.nik = nik
				self.nama = nama
				self.departemen = departemen
				self.bagian = bagian
				self.golongan = golongan
				self.norek = norek
				self.gajipokok = gajipokok
				self.tmakan = tmakan
				self.transportnonexec = transportnonexec
				self.tovertime = tovertime
				self.pbpjs = pbpjs
				self.ppinjam = ppinjam
				self.pabsen = pabsen

	today = datetime.datetime.now()
	idkaryawan = request.POST['idkaryawan']
	masatenggangclosing = request.POST['masatenggangclosing']
	mas = MasaTenggangClosing.objects.get(pk=masatenggangclosing)
	if idkaryawan.find("&") != -1 :
		listid = [x.strip() for x in idkaryawan.split('&')]
		a= ""
		mantap = ""
	
		a = Karyawan.objects
		if listid[0] != "":
			a = a.filter(perusahaan=listid[0])

		if listid[1] != "":
			a = a.filter(departemen=listid[1])

		if listid[2] != "":
			a = a.filter(bagian=listid[2])

		if listid[3] != "":
			a = a.filter(golongan=listid[3])

		#a = a.filter(tanggal__year=today.year).filter(tanggal__month=4)

		y = 0

		objs = [range(len(a))]

		for b in a:
			y = y + 1
			#k = Karyawan.objects.get(pk=b.karyawan.id)
			g = GajiPokok.objects.get(karyawan_id=b.id)
			p = PotonganKaryawan.objects.get(karyawan_id=b.id)

			gajipokok = g.gajipokok 
			tunjanganmakan = g.tmakan
			makanlembur = g.makanlembur
			transportnonexec = g.transportnonexec
			cicil = 0
			tovertime = 0
			pabsen = 0

			if p.cicil_pinjkaryawan > 0 :
				cicil = (p.pinjkaryawan/p.cicil_pinjkaryawan)
				pe = PotonganKaryawan.objects.select_for_update().filter(id=p.id)
				pe.update(cicil_pinjkaryawan=p.cicil_pinjkaryawan-1)

			# for x in a:
			# 	mantap =  waktu(x.keluar, x.karyawanshift.shift.jamkeluar, True)

			ab = Absensi.objects.filter(karyawan_id=b.id).filter(tanggal__range = [mas.tanggal, mas.sd])

			for abi in ab:
				if abi.SPL == 1:
					tovertime = tovertime + (abi.SPL_banyak * 20000)

				if waktu(abi.masuk, abi.karyawanshift.shift.jammasuk, True) > 1:
					pabsen = pabsen + 1

			pabsen = pabsen * 10000

			po = PostingGaji(karyawan_id = b.id, masatenggangclosing_id = masatenggangclosing, gajipokok_id = g.id, potongankaryawan_id = p.id, tovertime=tovertime, pabsen=pabsen)
			po.save()

			# bpjs_kes_kar = int(float(float(1)/100)) * p.bpjs # BPJS Kesehatan Karyawan 1%
			# bpjs_kes_per = int(float(float(4)/100)) * p.bpjs # BPJS Kesehatan Perusahaan 4%
			# bpjs_ktg_kar_jpn = int(float(float(1)/100)) * p.bpjs # BPJS Ketenagakerjaan Karyawan Jaminan Pensiunan 1%
			# bpjs_ktg_kar_jht = int(float(float(2)/100)) * p.bpjs # BPJS Ketenagakerjaan Karyawan Jaminan Hari Tua 2%
			# bpjs_ktg_per_jpn = int(float(float(2)/100)) * p.bpjs # BPJS Ketenagakerjaan Perusahaan Jaminan Kematian 2%
			# bpjs_ktg_per_jkk = int(float(float(0.54)/100)) * p.bpjs # BPJS Ketenagakerjaan Perusahaan Kecelakaan Kerja 0.54% 
			# bpjs_ktg_per_jht = int(float(float(3.7)/100)) * p.bpjs # BPJS Ketenagakerjaan Perusahaan Jaminan Hari Tua 3.7%
			# bpjs_ktg_per_jkn = int(float(float(0.3)/100)) * p.bpjs # BPJS Ketenagakerjaan Perusaaan Jaminan Kematian 0.3%
			
			objs.append(postgaji(y, b.NIK, b.name, b.departemen.name, b.bagian.name, b.golongan.name, b.norek + " a.n." + b.atasnama + " " + b.bank.name , g.gajipokok, tunjanganmakan, transportnonexec, tovertime, p.bpjs, cicil, pabsen))
	else:
		listid = [x.strip() for x in idkaryawan.split(',')]
		a = ""
		mantap = ""
		objs = [range(0, len(listid)-1)]

		for y in range(0, len(listid)-1):
			a = Absensi.objects.filter(karyawan=listid[y]).filter(tanggal__year=today.year).filter(tanggal__month=4)
			k = Karyawan.objects.get(pk=listid[y])
			g = GajiPokok.objects.get(karyawan_id=listid[y])
			p = PotonganKaryawan.objects.get(karyawan_id=listid[y])

			gajipokok = g.gajipokok 
			tunjanganmakan = g.tmakan
			makanlembur = g.makanlembur
			transportnonexec = g.transportnonexec

			cicil = 0
			tovertime = 0
			pabsen = 0

			if p.cicil_pinjkaryawan > 0 :
				cicil = (p.pinjkaryawan/p.cicil_pinjkaryawan)
				pe = PotonganKaryawan.objects.select_for_update().filter(id=p.id)
				pe.update(cicil_pinjkaryawan=p.cicil_pinjkaryawan-1)

			# for x in a:
			# 	mantap =  waktu(x.keluar, x.karyawanshift.shift.jamkeluar, True)

			ab = Absensi.objects.filter(karyawan_id=b.id).filter(tanggal__range[mas.tanggal, mas.sd])
			
			for abi in ab:
				if abi.SPL == 1:
					tovertime = tovertime + (abi.SPL_banyak * 20000)

				if waktu(abi.masuk, abi.karyawanshift.shift.jammasuk, True) > 1:
					pabsen = pabsen + 1

			pabsen = pabsen * 10000

			po = PostingGaji(karyawan_id = b.id, masatenggangclosing_id = masatenggangclosing, gajipokok_id = g.id, potongankaryawan_id = p.id,tovertime=tovertime, pabsen=pabsen)
			po.save()
			
			objs.append(postgaji(y+1, k.NIK, k.name, k.departemen.name, k.bagian.name, k.golongan.name, k.norek + " a.n." + k.atasnama + " " + k.bank.name , g.gajipokok, tunjanganmakan, transportnonexec,tovertime, p.bpjs, cicil, pabsen))


	return render(request,"postinggaji/print.html", { 'data': mantap, 'posting' : objs})

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