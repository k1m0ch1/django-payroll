from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader, Context
import django_tables2 as tables
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from system.models import Perusahaan, Departemen, Bagian, Golongan, Jabatan
from system.models import Bank, Agama, WargaNegara, StatusMenikah, Modules, Konfigurasi
from system.models import LokasiPerusahaan, HariRaya, Shift,KaryawanShift, Karyawan, Inventory
from system.models import GajiPokok, Absensi, Pinjaman, PotonganKaryawan, SuratIzin
from dateutil.parser import parse
from datetime import timedelta
from datetime import datetime
from sys import getsizeof
from zk import ZK, const
import datetime

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

	return render(request, "karyawan/form.html", { 'mode' : 'Tambah', 'module' : getModule(request), 
													   'idpk' : 0, 'dsb' : modules, 'parent' : getParent(request), 'departemen':dep,
													   'bagian': bag, 'golongan':gol, 'jabatan': jab, 'warganegara' : wg,
													   'statusmenikah' : sm, 'bank':bank, 'agama':agama,
													   'perusahaan': per})

@login_required()
def karyawan_save(request):
	nama = request.POST['nama1'] + " " + request.POST['nama2']
	
	# conn = None 
	# zk = ZK('192.168.0.225', port=4370, timeout=5)
	# try:
	# 	conn = zk.connect()
	# 	datausers = conn.get_users()
	# 	userid = 1
	# 	for user in datausers:
	# 		userid = userid + 1
	# 	print request.POST['fingerid']
	# 	conn.set_user(uid=userid, name=nama, privilege=const.USER_DEFAULT, password="", group_id="", user_id=request.POST['fingerid'])
	# 	conn.test_voice()
	# except Exception, e:
	# 	print "Process terminate : {}" . format(e)
	# finally:
	# 	if conn:
	# 		conn.disconnect()

	k = Karyawan(NIK = request.POST['NIK'], name = nama,
					shortname = request.POST['nama1'], tempatlahir = request.POST['tempatlahir'],
					tanggallahir = parse(request.POST['tanggallahir']).strftime("%Y-%m-%d"), gender = request.POST['gender'],
					alamat = request.POST['alamat'], kota = request.POST['kota'],
					provinsi = request.POST['provinsi'], telepon = request.POST['telepon'],
					handphone = request.POST['handphone'], statuskaryawan = request.POST['statuskaryawan'],
					masakaryawan = parse(request.POST['masakaryawan']).strftime("%Y-%m-%d"), ktpid = request.POST['ktp'],
					warganegara_id = request.POST['warganegara'], agama_id = request.POST['agama'],
					statusmenikah_id = request.POST['statusmenikah'], bank_id = request.POST['bank'],
					norek = request.POST['norekening'], atasnama = request.POST['atasnama'],
					fingerid = request.POST['fingerid'], NPWP = request.POST['NPWP'],
					KPJ = request.POST['KPJ'], jumlahhari = request.POST['jumlahhari'],
					departemen_id = request.POST['departemen'], bagian_id = request.POST['bagian'],
					golongan_id = request.POST['golongan'], #jabatan_id = request.POST['jabatan'],
					perusahaan_id= request.POST['perusahaan'])
	k.save()

	g = GajiPokok(karyawan_id=k.id, name="Gaji Pokok " + k.name, gajipokok=request.POST['gajipokok'], 
					jumlahhari = request.POST['jumlahhari'], transportnonexec = request.POST['transportnonexec'], tmakan = request.POST['tmakan'])
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
					masakaryawan = parse(request.POST['masakaryawan']).strftime("%Y-%m-%d"), ktpid = request.POST['ktp'],
					warganegara_id = request.POST['warganegara'], agama_id = request.POST['agama'],
					statusmenikah_id = request.POST['statusmenikah'], bank_id = request.POST['bank'],
					norek = request.POST['norekening'], atasnama = request.POST['atasnama'],
					fingerid = request.POST['fingerid'], NPWP = request.POST['NPWP'],
					KPJ = request.POST['KPJ'], jumlahhari = request.POST['jumlahhari'],
					departemen_id = request.POST['departemen'], bagian_id = request.POST['bagian'],
					golongan_id = request.POST['golongan'], #jabatan_id = request.POST['jabatan'],
					perusahaan_id= request.POST['perusahaan'])
	k.save()

	g = GajiPokok(karyawan_id=k.id, name="Gaji Pokok " + k.name, gajipokok=request.POST['gajipokok'], 
					jumlahhari = request.POST['jumlahhari'], transportnonexec = request.POST['transportnonexec'], tmakan = request.POST['tmakan'])
	g.save()

	return HttpResponse("berhasil-simpan-karyawan")




@login_required()
def karyawan_shift_save(request):
	shift = [request.POST['shift1'], request.POST['shift2'], request.POST['shift3'],request.POST['shift4']]
	idkaryawan = request.POST['idkaryawan']
	tanggal = request.POST['tanggal']
	offa = request.POST['off1']
	offb = request.POST['off2']
	offc = request.POST['off3']
	offd = request.POST['off4']

	tglawal = parse([x.strip() for x in tanggal.split(' ')][0]).strftime("%Y-%m-%d")
	tglakhir = parse([x.strip() for x in tanggal.split(' ')][2]).strftime("%Y-%m-%d")

	listid = [x.strip() for x in idkaryawan.split(',')]
	for y in range(0, len(listid)-1):
		k = Karyawan.objects.get(pk=listid[y])
		jumlahhari = int(k.jumlahhari)
		m1awal = datetime.strptime(tglawal, "%Y-%m-%d")
		m1offawal = parse([x.strip() for x in offa.split(' ')][0]).strftime("%Y-%m-%d")
		m1offakhir = parse([x.strip() for x in offa.split(' ')][2]).strftime("%Y-%m-%d")
		m1offawal = "2017-05-15"
		m1offakhir = "2017-05-16"
		m1jarak = datetime.strptime(m1offakhir, "%Y-%m-%d") - datetime.strptime(m1offawal, "%Y-%m-%d")
		m1jarak = int(m1jarak.days)
		s = KaryawanShift(karyawan_id=listid[y], shift_id = shift[z], tglawal=tglawal, tglakhir=tglakhir, tgloff=tgloff)
		s.save()

	return HttpResponse("yay berhasil")

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
	for y in range(0, len(listid)-1):
		a = SuratIzin(izintgl = parse(request.POST['izin']).strftime("%Y-%m-%d"), izinlama=request.POST['izinlama'], karyawan_id=listid[y])
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
	listid = [x.strip() for x in idkaryawan.split(',')]
	bpjs = request.POST['bpjs']
	pajakbulanan = request.POST['pajakbulanan']
	pinjaman = request.POST['pinjaman']
	for y in range(0, len(listid)-1):
		p = PotonganKaryawan.objects.filter(karyawan_id=listid[y])
		g = GajiPokok.objects.get(karyawan_id=listid[y])
		gajipokok = g.gajipokok
		if bpjs.find("%") != -1 :
			pisah = [x.strip() for x in bpjs.split('%')]
			bpjs = int(float(float(pisah[0])/100) * int(gajipokok))

		if pajakbulanan.find("%") != -1 :
			pisah = [x.strip() for x in pajakbulanan.split('%')]
			pajakbulanan = int(float(float(pisah[0])/100) * int(gajipokok))

		if pinjaman.find("%") != -1 :
			pisah = [x.strip() for x in pinjaman.split('%')]
			pinjaman = int(float(float(pisah[0])/100) * int(gajipokok))

		if bpjs == "":
			bpjs = p[0].bpjs

		if pajakbulanan == "":
			pajakbulanan = p[0].pph

		if pinjaman == "":
			pinjaman = p[0].pinjkaryawan

		if len(p)>0:
			p.update(bpjs=bpjs, pph=pajakbulanan, pinjkaryawan=pinjaman)
		else:
			p = PotonganKaryawan(bpjs=bpjs, pph=pajakbulanan, pinjkaryawan=pinjaman, karyawan_id=listid[y])	
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
	d = Inventory(name=nama, value=value, desc=desc)
	d.save()
	return redirect("konfigurasi-index")

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