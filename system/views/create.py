from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader, Context
import django_tables2 as tables
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from system.models import Perusahaan, Departemen, Bagian, Golongan, Jabatan
from system.models import Bank, Agama, WargaNegara, StatusMenikah, Modules, Konfigurasi, Mesin
from system.models import LokasiPerusahaan, HariRaya, Shift,KaryawanShift, Karyawan, Inventory
from system.models import GajiPokok, Absensi, Pinjaman, PotonganKaryawan, IzinCuti, MasaTenggangClosing, Bonusthr, KaryawanMesin
from system.models import TunjanganKaryawan, bpjs as BPJS
from dateutil.parser import parse
from datetime import timedelta
from datetime import datetime
from sys import getsizeof
from zk import ZK, const
import datetime
from django.core.management import call_command

modules = Modules.objects.all()
allmenu = Modules.objects.only('name')

@login_required()
def karyawan(request):
	per = Perusahaan.objects.all()
	dep = Departemen.objects.all()
	bag = Bagian.objects.all()
	gol = Golongan.objects.all()
	jab = Jabatan.objects.all()
	wg = WargaNegara.objects.all()
	sm = StatusMenikah.objects.all()
	bank = Bank.objects.all()
	agama = Agama.objects.all()
	idfinger = int(100) + len(Karyawan.objects.all()) + 1
	#call_command('createuser', '1233', "lapet")

	mesin = Mesin.objects.all()


	return render(request, "karyawan/form.html", { 'mode' : 'Tambah', 'module' : getModule(request), 
													   'idpk' : 0, 'dsb' : modules, 'parent' : getParent(request), 'departemen':dep,
													   'bagian': bag, 'golongan':gol, 'jabatan': jab, 'warganegara' : wg,
													   'statusmenikah' : sm, 'bank':bank, 'agama':agama,
													   'perusahaan': per , "idfinger" : idfinger, 'mesin' : mesin})

def tambah_karyawan_ke_mesin(karyawan_id, nama_karyawan):
	mesin = Mesin.objects.all()

	for m in mesin:
		conn = None
		zk = ZK(m.ip, port=m.port, timeout=5)
		try:
			conn = zk.connect()
			datausers = conn.get_users()
			userid = 1
			for user in datausers:
				userid = userid + 1
			#conn.disable_device()
			conn.set_user(uid=userid, name="" + str(nama_karyawan), privilege=const.USER_DEFAULT, password='12345678', group_id='', user_id="" + str(userid) )
			km = KaryawanMesin(mesin_id=m.id, karyawan_id=karyawan_id, userid=userid)
			km.save()
			#conn.test_voice()
			#conn.enable_device()
		except Exception, e:
		    print "Process terminate : {}".format(e)
		finally:
		    if conn:
		        conn.disconnect()


@login_required()
def karyawan_save(request):
	nama = request.POST['nama1'] + " " + request.POST['nama2']

	banyakpegawai = Karyawan.objects.filter(tanggalmasuk__year=parse(request.POST['tanggalmasuk']).strftime("%Y"), tanggalmasuk__month=parse(request.POST['tanggalmasuk']).strftime("%m"))
	banyakpegawai = len(banyakpegawai)+1
	jarak = "000"
	if banyakpegawai > 9 :
		jarak = "00"
	elif banyakpegawai > 99 :
		jarak = "0"
	elif banyakpegawai > 999 :
		jarak = "" 

	NIK = "GC" + str(request.POST['golongan']) + parse(request.POST['tanggalmasuk']).strftime("%Y")[2:] + parse(request.POST['tanggalmasuk']).strftime("%m") + jarak + str(banyakpegawai)
	k = Karyawan(NIK = NIK, name = nama,
					shortname = request.POST['nama1'], tempatlahir = request.POST['tempatlahir'],
					tanggallahir = parse(request.POST['tanggallahir']).strftime("%Y-%m-%d"), gender = request.POST['gender'],
					alamat = request.POST['alamat'], kota = request.POST['kota'],
					provinsi = request.POST['provinsi'], telepon = request.POST['telepon'],
					handphone = request.POST['handphone'], statuskaryawan = request.POST['statuskaryawan'],
					tanggalmasuk = parse(request.POST['tanggalmasuk']).strftime("%Y-%m-%d"),
					masakaryawan = parse(request.POST['masakaryawan']).strftime("%Y-%m-%d"), ktpid = request.POST['ktp'],
					warganegara_id = request.POST['warganegara'], agama_id = request.POST['agama'],
					statusmenikah_id = request.POST['statusmenikah'], bank_id = request.POST['bank'],
					norek = request.POST['norekening'], atasnama = request.POST['atasnama'],
					fingerid = request.POST['fingerid'],
					NPWP = request.POST['NPWP'],
					KPJ = request.POST['KPJ'], jumlahhari = request.POST['jumlahhari'],
					departemen_id = request.POST['departemen'], bagian_id = request.POST['bagian'],
					golongan_id = request.POST['golongan'], #jabatan_id = request.POST['jabatan'],
					perusahaan_id= request.POST['perusahaan'])
	k.save()

	tambah_karyawan_ke_mesin(k.id, k.name)
			
	jabatan = int(request.POST['gajipokok']) * (25/100)
	gajipokok = int(request.POST['gajipokok']) * (75/100)
	g = GajiPokok(karyawan_id=k.id, name="Gaji Pokok " + k.name, gajipokok=gajipokok, 
					jumlahhari = request.POST['jumlahhari'], jabatan = jabatan,
					umut = request.POST['umut'])
	g.save()

	return redirect('karyawan-index')

@login_required()
def karyawan_save_api(request):
	nama = request.POST['nama1'] + " " + request.POST['nama2']

	k = Karyawan(NIK = request.POST['NIK'], name = nama,
					shortname = request.POST['nama1'], tempatlahir = request.POST['tempatlahir'],
					tanggallahir = parse(request.POST['tanggallahir']).strftime("%Y-%m-%d"), gender = request.POST['gender'],
					alamat = request.POST['alamat'], kota = request.POST['kota'],
					provinsi = request.POST['provinsi'], telepon = request.POST['telepon'],
					handphone = request.POST['handphone'], statuskaryawan = request.POST['statuskaryawan'],
					tanggalmasuk = parse(request.POST['tanggalmasuk']).strftime("%Y-%m-%d"),
					masakaryawan = parse(request.POST['masakaryawan']).strftime("%Y-%m-%d"), ktpid = request.POST['ktp'],
					warganegara_id = request.POST['warganegara'], agama_id = request.POST['agama'],
					statusmenikah_id = request.POST['statusmenikah'], bank_id = request.POST['bank'],
					norek = request.POST['norekening'], atasnama = request.POST['atasnama'],
					fingerid = request.POST['fingerid'],
					NPWP = request.POST['NPWP'],
					KPJ = request.POST['KPJ'], jumlahhari = request.POST['jumlahhari'],
					departemen_id = request.POST['departemen'], bagian_id = request.POST['bagian'],
					golongan_id = request.POST['golongan'], #jabatan_id = request.POST['jabatan'],
					perusahaan_id= request.POST['perusahaan'])
	k.save()

	tambah_karyawan_ke_mesin(k.id, k.name)

	jabatan = int(request.POST['gajipokok']) * (25/100)
	gajipokok = int(request.POST['gajipokok']) * (75/100)
	g = GajiPokok(karyawan_id=k.id, name="Gaji Pokok " + k.name, gajipokok=gajipokok, 
					jumlahhari = request.POST['jumlahhari'], jabatan = jabatan,
					umut = request.POST['umut'])
	g.save()

	return HttpResponse("berhasil-simpan-karyawan")




@login_required()
def karyawan_shift_save(request):
	shift = [request.POST['shift1'], request.POST['shift2'], request.POST['shift3'],request.POST['shift4']]
	idkaryawan = request.POST['idkaryawan']
	offa = request.POST['off1']
	offb = request.POST['off2']
	offc = request.POST['off3']
	offd = request.POST['off4']
	sma = request.POST['sm1']
	smb = request.POST['sm2']
	smc = request.POST['sm3']
	smd = request.POST['sm4']

	# tglawal = parse([x.strip() for x in tanggal.split(' ')][0]).strftime("%Y-%m-%d")
	# tglakhir = parse([x.strip() for x in tanggal.split(' ')][2]).strftime("%Y-%m-%d")

	listid = [x.strip() for x in idkaryawan.split(',')]
	for y in range(0, len(listid)-1):
		k = Karyawan.objects.get(pk=listid[y])
		jumlahhari = int(k.jumlahhari)

		m1awal = parse([x.strip() for x in sma.split(' ')][0]).strftime("%Y-%m-%d")
		m1akhir = parse([x.strip() for x in smb.split(' ')][2]).strftime("%Y-%m-%d")
		m1offawal = parse([x.strip() for x in offa.split(' ')][0]).strftime("%Y-%m-%d")
		m1offakhir = parse([x.strip() for x in offa.split(' ')][2]).strftime("%Y-%m-%d")

		m2awal = parse([x.strip() for x in sma.split(' ')][0]).strftime("%Y-%m-%d")
		m2akhir = parse([x.strip() for x in smb.split(' ')][2]).strftime("%Y-%m-%d")
		m2offawal = parse([x.strip() for x in offa.split(' ')][0]).strftime("%Y-%m-%d")
		m2offakhir = parse([x.strip() for x in offa.split(' ')][2]).strftime("%Y-%m-%d")

		m3awal = parse([x.strip() for x in sma.split(' ')][0]).strftime("%Y-%m-%d")
		m3akhir = parse([x.strip() for x in smb.split(' ')][2]).strftime("%Y-%m-%d")
		m3offawal = parse([x.strip() for x in offa.split(' ')][0]).strftime("%Y-%m-%d")
		m3offakhir = parse([x.strip() for x in offa.split(' ')][2]).strftime("%Y-%m-%d")

		m4awal = parse([x.strip() for x in sma.split(' ')][0]).strftime("%Y-%m-%d")
		m4akhir = parse([x.strip() for x in smb.split(' ')][2]).strftime("%Y-%m-%d")
		m4offawal = parse([x.strip() for x in offa.split(' ')][0]).strftime("%Y-%m-%d")
		m4offakhir = parse([x.strip() for x in offa.split(' ')][2]).strftime("%Y-%m-%d")

		s = KaryawanShift(karyawan_id=listid[y], shift_id = shift[0], tglawal=m1awal, tglakhir=m1akhir, tgloffawal=m1offawal, tgloffakhir=m1offakhir)
		s.save()
		s = KaryawanShift(karyawan_id=listid[y], shift_id = shift[1], tglawal=m2awal, tglakhir=m2akhir, tgloffawal=m2offawal, tgloffakhir=m2offakhir)
		s.save()
		s = KaryawanShift(karyawan_id=listid[y], shift_id = shift[2], tglawal=m3awal, tglakhir=m3akhir, tgloffawal=m3offawal, tgloffakhir=m3offakhir)
		s.save()
		s = KaryawanShift(karyawan_id=listid[y], shift_id = shift[3], tglawal=m4awal, tglakhir=m4akhir, tgloffawal=m4offawal, tgloffakhir=m4offakhir)
		s.save()

	return HttpResponse("yay berhasil")

@login_required()
def koreksi(request, absensi_id):
	a = Absensi.objects.get(pk=absensi_id)
	return render(request, "koreksi/form.html", { "absen" : a, 'mode' : 'Tambah', 'module' : getModule(request), 
													   'idpk' : absensi_id, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def koreksi_save(request, absensi_id):
	koreksi = request.POST['koreksi']
	alasan = request.POST['alasan'] if koreksi == "1" else ""
	a = Absensi.objects.select_for_update().filter(id=absensi_id)
	a.update(koreksi = koreksi, alasan_koreksi=alasan)

	return redirect("absensi-index")

@login_required()
def overtime(request, absensi_id):
	a = Absensi.objects.get(pk=absensi_id)
	return render(request, "overtime/form.html", { "absen" : a, 'mode' : 'Tambah', 'module' : getModule(request), 
													   'idpk' : absensi_id, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def karyawan_lembur_save(request, absensi_id):
	SPL = request.POST['SPL']
	banyakjam = request.POST['banyakjam'] if SPL == "1" else 0
	a = Absensi.objects.select_for_update().filter(id=absensi_id)
	a.update(SPL = SPL, SPL_banyak=banyakjam)

	return redirect("overtime-index")

@login_required()
def karyawan_lembur_save_api(request):
	idkaryawan = request.POST['idkaryawan']
	listid = [x.strip() for x in idkaryawan.split(',')]
	for y in range(0, len(listid)-1):
		a = Absensi.objects.select_for_update().filter(karyawan_id=listid[y]).filter(tanggal=datetime.datetime.now().strftime("%Y-%m-%d"))
		a.update(SPL = 1, SPL_banyak=request.POST['lamalembur'])

	return HttpResponse("berhasil-simpan-lembur")

@login_required()
def karyawan_izin_save_api(request):
	idkaryawan = request.POST['idkaryawan']
	listid = [x.strip() for x in idkaryawan.split(',')]
	tanggal = request.POST['tanggal']
	tglmulai = parse([x.strip() for x in tanggal.split(' ')][0]).strftime("%Y-%m-%d")
	tglakhir = parse([x.strip() for x in tanggal.split(' ')][2]).strftime("%Y-%m-%d")
	for y in range(0, len(listid)-1):
		a = IzinCuti(tglmulai = tglmulai, tglakhir=tglakhir, karyawan_id=listid[y], alasan=request.POST['alasan'], jenis=request.POST["jenis"])
		a.save()

	return HttpResponse("berhasil-simpan-lembur")

@login_required()
def pinjaman(request):
	i = Inventory.objects.all()
	return render(request, "pinjaman/form.html", { 'mode' : 'Tambah', 'module' : getModule(request), 
													   'idpk' : 0, 'dsb' : modules, 'parent' : getParent(request), 'inventory' : i})

@login_required()
def pinjaman_save(request):
	idkaryawan = request.POST['idkaryawan']
	listid = [x.strip() for x in idkaryawan.split(',')]
	for y in range(0, len(listid)-1):
		p = Pinjaman(name="", desc="", karyawan_id=listid[y], inventory_id=request.POST['idbarang'], tglpinjam=parse(request.POST['tanggalpinjam']).strftime("%Y-%m-%d"))	
		p.save()

	return redirect("pinjaman-index")

@login_required()
def potongan_save(request):
	idkaryawan = request.POST['idkaryawan']
	#idmas = request.POST['idmas']
	listid = [x.strip() for x in idkaryawan.split(',')]
	#bpjs = request.POST['bpjs']
	#pajakbulanan = request.POST['pajakbulanan']
	pinjaman = request.POST['pinjaman']
	koperasi = request.POST['koperasi']
	cicil_pinjaman = request.POST['cicil_pinjaman']
	cicil_koperasi = request.POST['cicil_koperasi']
	for y in range(0, len(listid)-1):
		# p = PotonganKaryawan.objects.filter(karyawan_id=listid[y])
		# g = GajiPokok.objects.get(karyawan_id=listid[y])
		# gajipokok = g.gajipokok
		# # if bpjs.find("%") != -1 :
		# # 	pisah = [x.strip() for x in bpjs.split('%')]
		# # 	bpjs = int(float(float(pisah[0])/100) * int(gajipokok))

		# # if pajakbulanan.find("%") != -1 :
		# # 	pisah = [x.strip() for x in pajakbulanan.split('%')]
		# # 	pajakbulanan = int(float(float(pisah[0])/100) * int(gajipokok))

		# if pinjaman.find("%") != -1 :
		# 	pisah = [x.strip() for x in pinjaman.split('%')]
		# 	pinjaman = int(float(float(pisah[0])/100) * int(gajipokok))

		# # if bpjs == "":
		# # 	bpjs = 0 if p[0].bpjs == 0 else p[0].bpjs

		# # if pajakbulanan == "":
		# # 	pajakbulanan = p[0].pph

		# if pinjaman == "" or pinjaman == None:
		# 	pinjaman = 0 if p[0].pinjkaryawan == 0 else p[0].pinjkaryawan

		# if cicil_pinjaman == "":
		# 	cicil_pinjaman = 0 if p[0].cicil_pinjkaryawan == 0 else p[0].cicil_pinjkaryawan
		try:
			p = PotonganKaryawan.objects.get(karyawan_id=listid[y])
			p = PotonganKaryawan.objects.select_for_update().filter(karyawan_id=listid[y])
			p.update(koperasi=koperasi, pinjkaryawan=pinjaman, karyawan_id=listid[y], cicil_pinjkaryawan=cicil_pinjaman, cicil_koperasi=cicil_koperasi)
		except PotonganKaryawan.DoesNotExist:
			p = PotonganKaryawan(koperasi=koperasi, pinjkaryawan=pinjaman, karyawan_id=listid[y], cicil_pinjkaryawan=cicil_pinjaman, cicil_koperasi=cicil_koperasi)	
			p.save()

	return HttpResponse("Berhasil Simpan")

@login_required()
def tunjangan_save(request):
	idkaryawan = request.POST['idkaryawan']
	idmas = request.POST['idmas']
	listid = [x.strip() for x in idkaryawan.split(',')]
	#pajakbulanan = request.POST['pajakbulanan']
	kemahalan = request.POST['kemahalan']
	for y in range(0, len(listid)-1):
		try:
			b = TunjanganKaryawan.objects.get(karyawan_id=listid[y])
			b = TunjanganKaryawan.objects.select_for_update().filter(karyawan_id=listid[y])
			b.update(masatenggangclosing_id=idmas, kemahalan=kemahalan, karyawan_id=listid[y],
									transportnonexec=request.POST['transportnonexec'], ttelepon = request.POST['ttelepon'], 
									tmakan = request.POST['tmakan'])
		except TunjanganKaryawan.DoesNotExist:
			p = TunjanganKaryawan(masatenggangclosing_id=idmas, kemahalan=kemahalan, karyawan_id=listid[y],
									transportnonexec=request.POST['transportnonexec'], ttelepon = request.POST['ttelepon'], 
									tmakan = request.POST['tmakan'])	
			p.save()
			

	return HttpResponse("Berhasil Simpan")

@login_required()
def bonus_save(request):
	idkaryawan = request.POST['idkaryawan']
	listid = [x.strip() for x in idkaryawan.split(',')]

	for y in range(0, len(listid)-1):
		try:
			b = Bonusthr.objects.get(karyawan_id=listid[y])
			b = Bonusthr.objects.select_for_update().filter(karyawan_id=listid[y])
			b.update(bonus = request.POST['bonus'])
		except Bonusthr.DoesNotExist:
			b = Bonusthr(karyawan_id=listid[y],bonus = request.POST['bonus'])	
			b.save()			

	return HttpResponse("Berhasil Simpan")

@login_required()
def bpjs_save(request):
	idkaryawan = request.POST['idkaryawan']
	listid = [x.strip() for x in idkaryawan.split(',')]
	bpjsks = request.POST['bpjsks']
	bpjskt = request.POST['bpjskt']
	for y in range(0, len(listid)-1):
		x = PotonganKaryawan.objects.filter(karyawan_id=listid[y])
		if len(x) > 0 :
			x = PotonganKaryawan.objects.select_for_update().filter(karyawan_id=listid[y])
			x.update(bpjs_ks = bpjsks , bpjs_kt = bpjskt)
		else:
			p = PotonganKaryawan(bpjs_ks = bpjsks, bpjs_kt = bpjskt, karyawan_id=listid[y])	
			p.save()			

	return HttpResponse("Berhasil Simpan")

@login_required()
def perusahaan(request):
	return render(request, "include/base-form.html", { 'mode' : 'Tambah', 'module' : getModule(request), 
													   'idpk' : 0, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def perusahaan_save(request):
	nama = request.POST['name']
	desc = request.POST['desc']
	d = Perusahaan(name=nama, desc=desc)
	d.save()
	return redirect("perusahaan-index")


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
def shift(request):
	return render(request, "shift/form.html", { 'mode' : 'Tambah', 'module' : getModule(request), 
													   'idpk' : 0, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def shift_save(request):
	nama = request.POST['name']
	desc = request.POST['desc']
	masuk = request.POST['masuk']
	keluar = request.POST['keluar']
	d = Shift(name=nama, desc=desc, jammasuk=masuk, jamkeluar=keluar)
	d.save()
	return redirect("shift-index")

@login_required()
def inventory(request):
	exfield = [{"name": "nomer","type":"text", "placeholder":"Nomer Barang", "label":"Nomer Barang", "data": ""}]
	return render(request, "include/base-dyn-form.html", { 'mode' : 'Tambah', 'module' : getModule(request), 
													   'idpk' : 0, 'dsb' : modules, 'parent' : getParent(request),
													   'exfield' : exfield
													  })

@login_required()
def inventory_save(request):
	nama = request.POST['name']
	nomer = request.POST['nomer']
	desc = request.POST['desc']
	d = Inventory(name=nama, nomer=nomer, desc=desc)
	d.save()
	return redirect("inventory-index")

@login_required()
def konfigurasi(request):
	exfield = [{"name": "value","type":"text", "placeholder":"Value", "label":"Value", "data": ""}]
	return render(request, "include/base-dyn-form.html", { 'mode' : 'Tambah', 'module' : getModule(request), 
													   'idpk' : 0, 'dsb' : modules, 'parent' : getParent(request),
													   'exfield' : exfield
													  })

@login_required()
def konfigurasi_save(request):
	nama = request.POST['name']
	value = request.POST['value']
	desc = request.POST['desc']
	d = Konfigurasi(name=nama, value=value, desc=desc)
	d.save()
	return redirect("konfigurasi")

@login_required()
def mesin(request):
	exfield = [{"name": "ip","type":"text", "placeholder":"Value", "label":"IP Address", "data": ""}, {"name": "port","type":"text", "placeholder":"Value", "label":"Port", "data": ""}]
	return render(request, "include/base-dyn-form.html", { 'mode' : 'Tambah', 'module' : getModule(request), 
													   'idpk' : 0, 'dsb' : modules, 'parent' : getParent(request),
													   'exfield' : exfield
													  })

@login_required()
def mesin_save(request):
	nama = request.POST['name']
	ip = request.POST['ip']
	port = request.POST['port']
	d = Mesin(name=nama, ip=ip, port=port)
	d.save()
	return redirect("mesin")

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
def masatenggangclosing(request):
	return render(request, "masatenggangclosing/form.html", { 'mode' : 'Tambah', 'module' : getModule(request), 
													   'idpk' : 0, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def masatenggangclosing_save(request):
	name = request.POST['name']
	tanggal = parse(request.POST['tanggal']).strftime("%Y-%m-%d")
	sd = parse(request.POST['sd']).strftime("%Y-%m-%d")
	desc = request.POST['desc']
	pp = MasaTenggangClosing(name=name, tanggal=tanggal, sd=sd, desc=desc)
	pp.save()
	return redirect("masatenggangclosing-index")

@login_required()
def hariraya(request):
	return render(request, "hariraya/form.html", { 'mode' : 'Tambah', 'module' : getModule(request), 
													   'idpk' : 0, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def hariraya_save(request):
	name = request.POST['name']
	tanggal = parse(request.POST['tanggal']).strftime("%Y-%m-%d")
	sd = parse(request.POST['sd']).strftime("%Y-%m-%d")
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