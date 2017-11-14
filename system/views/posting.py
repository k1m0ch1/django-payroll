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
from system.models import PostingGaji, MasaTenggangClosing, TunjanganKaryawan
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
			no = 0
			nik = 0
			nama = ""
			departemen = 0
			bagian = 0
			golongan = ""
			norek = 0
			gajipokok = 0
			statusmenikah = ""
			tmakan = 0
			transportnonexec = 0
			tovertime = 0
			tunjangan = 0
			pbpjs_ks = 0
			pbpjs_kt = 0
			ppinjam = 0
			pkoperasi = 0
			pcicil = 0
			pabsen = 0
			pph = 0

			def __init__(self, no, nik, nama, departemen, bagian, 
								golongan, norek, gajipokok, statusmenikah, tmakan, 
								transportnonexec, tovertime, tunjangan, pbpjs_ks, pbpjs_kt, 
								ppinjam, pkoperasi, pabsen, pph):
				self.no = no
				self.nik = nik
				self.nama = nama
				self.departemen = departemen
				self.bagian = bagian
				self.golongan = golongan
				self.norek = norek
				self.gajipokok = gajipokok
				self.statusmenikah = statusmenikah
				self.tmakan = tmakan
				self.transportnonexec = transportnonexec
				self.tovertime = tovertime
				self.tunjangan = tunjangan
				self.pbpjs_ks = pbpjs_ks
				self.pbpjs_kt = pbpjs_kt
				self.ppinjam = ppinjam
				self.pkoperasi = pkoperasi
				self.pabsen = pabsen
				self.pph = pph

	today = datetime.datetime.now()
	idkaryawan = request.POST['idkaryawan']
	masatenggangclosing = request.POST['masatenggangclosing']
	mas = MasaTenggangClosing.objects.get(pk=masatenggangclosing)
	if idkaryawan.find("&") != -1 :
		listid = [x.strip() for x in idkaryawan.split('&')]
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
			k = Karyawan.objects.get(pk=b.id)
			g = GajiPokok.objects.get(karyawan_id=b.id)
			p = PotonganKaryawan.objects.get(karyawan_id=b.id)
			tt = TunjanganKaryawan.objects.get(karyawan_id=b.id)

			gajipokok = g.gajipokok 

			tunjanganmakan = tt.tmakan
			transportnonexec = tt.transportnonexec

			makanlembur = g.makanlembur
			
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

			date_format = "%Y-%m-%d"
			hari = mas.sd - mas.tanggal
			hari = hari.days

			banyak = len(ab)			

			for abi in ab:
				if abi.SPL == 1:
					hari = abi.created_at.strftime("%A")
					if hari == "Minggu" or hari == "Sunday" :
						hitungot = abi.SPL_banyak
						if abi.karyawan.golongan.id == 7 or abi.karyawan.golongan.id == 8 :
							if abi.SPL_banyak <= 7 :
								tovertime = tovertime + int(float((hitungot * 2) * 10000))
							elif abi.SPL_banyak > 7 :
								tovertime = tovertime + int(float((7 * 2) * 10000))
								tovertime = tovertime + ( ( ( abi.SPL_banyak - 7 ) * 3 ) * 10000 )
						elif abi.karyawan.golongan.id < 7 :
							if abi.SPL_banyak <= 7 :
								tovertime = tovertime + int(float((hitungot * 2) * 20000))
							elif abi.SPL_banyak > 7 :
								tovertime = tovertime + int(float((7 * 2) * 10000))
								tovertime = tovertime + ( ( ( abi.SPL_banyak - 7 ) * 3 ) * 20000 )
					else:
						if abi.karyawan.golongan.id == 7 or abi.karyawan.golongan.id == 8 :
							if abi.SPL_banyak <= 1 :
								tovertime = tovertime + int(float(1.5 * 10000))
							elif abi.SPL_banyak > 1 :
								tovertime = tovertime + int(float(1.5 * 10000))
								tovertime = tovertime + ( ( ( abi.SPL_banyak - 1 ) * 2 ) * 10000 )
						elif abi.karyawan.golongan.id < 7 :
							if abi.SPL_banyak >= 1 :
								tovertime = tovertime + int(float(1.5 * 20000))
							elif abi.SPL_banyak > 1 :
								tovertime = tovertime + int(float(1.5 * 20000))
								tovertime = tovertime + ( ( ( abi.SPL_banyak - 1 ) * 2 ) * 20000 )

				if waktu(abi.masuk, abi.karyawanshift.shift.jammasuk, True) > 1:
					pabsen = pabsen + 1

			hari = mas.sd - mas.tanggal
			hari = hari.days

			if k.golongan.id == 7 or k.golongan.id == 8 :
				tunjanganmakan = int( 20000 / hari ) * banyak
			    transportnonexec = int( 20000 / hari ) * banyak
				pabsen = pabsen * 10000
			elif k.golongan.id == 6 or k.golongan.id == 5 :
				tunjanganmakan = int( 40000 / hari ) * banyak
			    transportnonexec = int( 40000 / hari ) * banyak
				pabsen = pabsen * 20000
			elif k.golongan_id < 5:
				tunjanganmakan = int( 60000 / hari ) * banyak
			    transportnonexec = int( 60000 / hari ) * banyak
				pabsen = pabsen * 40000

			# po = PostingGaji(karyawan_id = b.id, masatenggangclosing_id = masatenggangclosing, gajipokok_id = g.id, potongankaryawan_id = p.id, tovertime=tovertime, pabsen=pabsen)
			# po.save()

			wp = 0

			gapok = g.gajipokok
			status = b.statusmenikah.desc
			tunjangan = g.jabatan + tt.kemahalan + tt.tmakan+ tt.transportnonexec
			pph = 0
			bpjs_ks = p.bpjs_ks
			bpjs_kt = p.bpjs_kt

			if gapok <= 50000000 :
			  wp = float(float(5)/100) 
			elif gapok > 50000000 or gapok <= 250000000 :
			  wp = float(float(15)/100) 
			elif gapok > 250000000 or gapok <= 500000000 :
			  wp = float(float(25)/100)
			elif gapok > 500000000 :
			  wp = float(float(30)/100)

			ptkp = 0

			if status == "Lajang Tanpa Tanggungan" :
			  ptkp = 54000000
			elif status == "Lajang 1 Tanggungan" or status == "Menikah Tanpa Tanggungan" :
			  ptkp = 58500000
			elif status ==  "Lajang 2 Tanggungan" or status == "Menikah 1 Tanggungan" :
			  ptkp = 63000000
			elif status == "Menikah 2 Tanggungan" :
			  ptkp = 67500000
			elif status == "Menikah 3 Tanggungan" :
			  ptkp = 72000000

			bpjs_ktg_per_jkk = int(float(float(0.54)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Perusahaan Kecelakaan Kerja 0.54% 
			bpjs_ktg_per_jkm = int(float(float(0.3)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Perusaaan Jaminan Kematian 0.3%
			bpjs_kes_per = int(float(float(4)/100) * int(bpjs_ks)) # BPJS Kesehatan Perusahaan 4%
			bruto = gapok + tunjangan + bpjs_ktg_per_jkk + bpjs_ktg_per_jkm + bpjs_kes_per

			bpjs_ktg_kar_jht = int(float(float(2)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Karyawan Jaminan Hari Tua 2%
			bpjs_ktg_per_jpn = int(float(float(2)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Perusahaan Jaminan Kematian 2%

			ph_netto_sebulan = bruto - ( (int(float(float(5)/100) * int(bruto))) + bpjs_ktg_kar_jht + bpjs_ktg_per_jpn )

			ph_netto_setahun = ph_netto_sebulan * 12

			ph_kena_pajak = ph_netto_setahun - ptkp

			pph_terhutang = int(wp * int(ph_kena_pajak))

			pph = pph_terhutang / 12
			pph = 0 if pph < 0 else pph

			if b.NPWP == 0 or b.NPWP == None :
				pph = int(float(float(120)/100) * int(pph))
			
			objs.append(postgaji(y, b.NIK, b.name, b.departemen.name, b.bagian.name, 
									b.golongan.name, b.norek + " a.n." + b.atasnama + " " + b.bank.name , 
									g.gajipokok, b.statusmenikah.name, tunjanganmakan, transportnonexec, tovertime, 
									g.jabatan, p.bpjs_ks, p.bpjs_kt, cicil, p.koperasi, pabsen, pph))
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
			tt = TunjanganKaryawan.objects.get(karyawan_id=listid[y])

			gajipokok = g.gajipokok 
			tunjanganmakan = tt.tmakan
			makanlembur = g.makanlembur
			transportnonexec = tt.transportnonexec

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
			
			date_format = "%Y-%m-%d"
			hari = mas.sd - mas.tanggal
			hari = hari.days

			banyak = len(ab)

			for abi in ab:
				if abi.SPL == 1:
					hari = abi.created_at.strftime("%A")
					if hari == "Minggu" or hari == "Sunday" :
						hitungot = abi.SPL_banyak
						if abi.karyawan.golongan.id == 7 or abi.karyawan.golongan.id == 8 :
							if abi.SPL_banyak <= 7 :
								tovertime = tovertime + int(float((hitungot * 2) * 10000))
							elif abi.SPL_banyak > 7 :
								tovertime = tovertime + int(float((7 * 2) * 10000))
								tovertime = tovertime + ( ( ( abi.SPL_banyak - 7 ) * 3 ) * 10000 )
						elif abi.karyawan.golongan.id < 7 :
							if abi.SPL_banyak <= 7 :
								tovertime = tovertime + int(float((hitungot * 2) * 20000))
							elif abi.SPL_banyak > 7 :
								tovertime = tovertime + int(float((7 * 2) * 10000))
								tovertime = tovertime + ( ( ( abi.SPL_banyak - 7 ) * 3 ) * 20000 )
					else:
						if abi.karyawan.golongan.id == 7 or abi.karyawan.golongan.id == 8 :
							if abi.SPL_banyak <= 1 :
								tovertime = tovertime + int(float(1.5 * 10000))
							elif abi.SPL_banyak > 1 :
								tovertime = tovertime + int(float(1.5 * 10000))
								tovertime = tovertime + ( ( ( abi.SPL_banyak - 1 ) * 2 ) * 10000 )
						elif abi.karyawan.golongan.id < 7 :
							if abi.SPL_banyak >= 1 :
								tovertime = tovertime + int(float(1.5 * 20000))
							elif abi.SPL_banyak > 1 :
								tovertime = tovertime + int(float(1.5 * 20000))
								tovertime = tovertime + ( ( ( abi.SPL_banyak - 1 ) * 2 ) * 20000 )

				if waktu(abi.masuk, abi.karyawanshift.shift.jammasuk, True) > 1:
					pabsen = pabsen + 1

			hari = mas.sd - mas.tanggal
			hari = hari.days
			
			if k.golongan.id == 7 or k.golongan.id == 8 :
				tunjanganmakan = int( 20000 / hari ) * banyak
			    transportnonexec = int( 20000 / hari ) * banyak
				pabsen = pabsen * 10000
			elif k.golongan.id == 6 or k.golongan.id == 5 :
				tunjanganmakan = int( 40000 / hari ) * banyak
			    transportnonexec = int( 40000 / hari ) * banyak
				pabsen = pabsen * 20000
			elif k.golongan_id < 5:
				tunjanganmakan = int( 60000 / hari ) * banyak
			    transportnonexec = int( 60000 / hari ) * banyak
				pabsen = pabsen * 40000

			# po = PostingGaji(karyawan_id = b.id, masatenggangclosing_id = masatenggangclosing, gajipokok_id = g.id, potongankaryawan_id = p.id,tovertime=tovertime, pabsen=pabsen)
			# po.save()

			gapok = g.gajipokok
			status = k.statusmenikah.desc
			tunjangan = g.jabatan + tt.kemahalan + tt.tmakan+ tt.transportnonexec
			pph = 0
			bpjs_ks = p.bpjs_ks
			bpjs_kt = p.bpjs_kt

			if gapok <= 50000000 :
			  wp = float(float(5)/100) 
			elif gapok > 50000000 or gapok <= 250000000 :
			  wp = float(float(15)/100) 
			elif gapok > 250000000 or gapok <= 500000000 :
			  wp = float(float(25)/100)
			elif gapok > 500000000 :
			  wp = float(float(30)/100)

			ptkp = 0

			if status == "Lajang Tanpa Tanggungan" :
			  ptkp = 54000000
			elif status == "Lajang 1 Tanggungan" or status == "Menikah Tanpa Tanggungan" :
			  ptkp = 58500000
			elif status ==  "Lajang 2 Tanggungan" or status == "Menikah 1 Tanggungan" :
			  ptkp = 63000000
			elif status == "Menikah 2 Tanggungan" :
			  ptkp = 67500000
			elif status == "Menikah 3 Tanggungan" :
			  ptkp = 72000000

			bpjs_ktg_per_jkk = int(float(float(0.54)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Perusahaan Kecelakaan Kerja 0.54% 
			bpjs_ktg_per_jkm = int(float(float(0.3)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Perusaaan Jaminan Kematian 0.3%
			bpjs_kes_per = int(float(float(4)/100) * int(bpjs_ks)) # BPJS Kesehatan Perusahaan 4%
			bruto = ( gapok + tunjangan + tovertime + bpjs_ktg_per_jkk + bpjs_ktg_per_jkm + bpjs_kes_per ) 

			bpjs_ktg_kar_jht = int(float(float(2)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Karyawan Jaminan Hari Tua 2%
			bpjs_ktg_per_jpn = int(float(float(2)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Perusahaan Jaminan Kematian 2%

			ph_netto_sebulan = bruto - ( (int(float(float(5)/100) * int(bruto))) + bpjs_ktg_kar_jht + bpjs_ktg_per_jpn )

			ph_netto_setahun = ph_netto_sebulan * 12

			ph_kena_pajak = ph_netto_setahun - ptkp

			pph_terhutang = int(wp * int(ph_kena_pajak))

			pph = pph_terhutang / 12
			pph = 0 if pph < 0 else pph

			if k.NPWP == 0 or k.NPWP == None :
				pph = int(float(float(120)/100) * int(pph))
			
			objs.append(postgaji(y+1, k.NIK, k.name, k.departemen.name, k.bagian.name, 
									k.golongan.name, k.norek + " a.n." + k.atasnama + " " + k.bank.name ,
									g.gajipokok, k.statusmenikah.name, tunjanganmakan, transportnonexec,tovertime, 
									g.jabatan, p.bpjs_ks, p.bpjs_kt, cicil, p.koperasi, pabsen, pph))

	objs.pop(0)
	return render(request,"postinggaji/print.html", { 'data': mantap, 'posting' : objs , "bruto" : bruto})

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