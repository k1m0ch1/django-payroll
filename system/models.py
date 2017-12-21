from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Perusahaan(models.Model):
	name = models.CharField(max_length=200)
	desc = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Konfigurasi(models.Model):
	name = models.CharField(max_length=200)
	value = models.CharField(max_length=200)
	desc = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class LokasiPerusahaan(models.Model):
	perusahaan = models.ForeignKey(Perusahaan, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	alamat = desc = models.TextField()
	desc = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Departemen(models.Model):
	#perusahaan = models.ForeignKey(Perusahaan, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	desc = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

# Deprecated table
# class Unit(models.Model):
# 	departemen = models.ForeignKey(departemen, on_delete=models.CASCADE)
# 	name = models.CharField(max_length=200)
# 	desc = models.TextField()
# 	created_at = models.DateTimeField(auto_now=True)
# 	updated_at = models.DateTimeField(auto_now_add=True, null=True)

# 	def __str__(self):              # __unicode__ on Python 2
# 		return self.name

class Bagian(models.Model):
	#departemen = models.ForeignKey(departemen, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	desc = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Golongan(models.Model):
	#bagian = models.ForeignKey(Bagian, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	desc = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Jabatan(models.Model):
	#jabatan = models.ForeignKey(Bagian, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	desc = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Level(models.Model):
	name = models.CharField(max_length=200)
	desc = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Bank(models.Model):
	name = models.CharField(max_length=200)
	desc = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Agama(models.Model):
	name = models.CharField(max_length=200)
	desc = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class WargaNegara(models.Model):
	name = models.CharField(max_length=200)
	desc = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class StatusMenikah(models.Model):
	name = models.CharField(max_length=200)
	desc = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)
	
	def __str__(self):              # __unicode__ on Python 2
		return self.name

#== Database structure by yahya

class Karyawan(models.Model):
	NIK = models.CharField(max_length=20)
	perusahaan = models.ForeignKey(Perusahaan, default=3, on_delete=models.SET_DEFAULT)
	departemen = models.ForeignKey(Departemen, default=7, on_delete=models.SET_DEFAULT)
	jabatan = models.ForeignKey(Jabatan, null=True, on_delete=models.SET_NULL)
	bagian = models.ForeignKey(Bagian, default=14, on_delete=models.SET_DEFAULT)
	golongan = models.ForeignKey(Golongan, default=10,on_delete=models.SET_DEFAULT)
	bank = models.ForeignKey(Bank, default=15, on_delete=models.SET_DEFAULT)
	agama = models.ForeignKey(Agama, default=6, on_delete=models.SET_DEFAULT)
	warganegara = models.ForeignKey(WargaNegara, default=11, on_delete=models.SET_DEFAULT)
	statusmenikah = models.ForeignKey(StatusMenikah, default=1, on_delete=models.SET_DEFAULT)	
	#unit = models.ForeignKey(Jabatan, on_delete=models.CASCADE)
	#level = models.ForeignKey(Level, on_delete=models.CASCADE)
	#linkacc = undefined
	#groupkat = undefined
	name = models.CharField(max_length=200)
	shortname = models.CharField(max_length=200, null=True)
	tempatlahir = models.CharField(max_length=200, null=True)
	tanggallahir = models.DateField(null=True)
	alamat = models.TextField(null=True)
	provinsi = models.CharField(max_length=200, null=True)
	kota = models.CharField(max_length=200, null=True)
	gender = models.CharField(max_length=9)
	telepon = models.DecimalField(max_digits=12, decimal_places=0, null=True)
	handphone = models.DecimalField(max_digits=18, decimal_places=0, null=True)
	ktpid = models.DecimalField(max_digits=30, decimal_places=0, null=True)	
	atasnama = models.CharField(max_length=200, null=True)
	norek = models.CharField(max_length=70, null=True)
	fingerid = models.CharField(max_length=30, null=True)
	lokasimesin = models.CharField(max_length=15, null=True)
	NPWP = models.CharField(max_length=30, null=True)
	KPJ = models.CharField(max_length=30, null=True)
	tanggalmasuk = models.DateField(null=True)
	statuskaryawan = models.CharField(max_length=30, default="Kontrak 1 (PKWT)")
	masakaryawan = models.DateField(null=True)
	jumlahhari = models.DecimalField(max_digits=1, decimal_places=0)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)
	delete_date = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

#== Experimental structure, so I will split this section of table which every semester of the year will be added 
#== because of most people will look up into database up to 3-5 month in the past
#== so this will be better if database is enchanment into splited every semester
#== this will help DBMS to access data without open the first byte of the file
#== probably this will reduce up to 10% of memory and cpu
#==
#== The script will be determine January - Juny is first semester, further more is another semester on every year
#== a year have 2 Semester
#== 
#== around 12 AM, the database will generate this table and then convert it

class Shift(models.Model):
	name = models.CharField(max_length=225)
	jammasuk = models.TimeField()
	jamkeluar = models.TimeField()
	desc = models.TextField()
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class KaryawanShift(models.Model):
	name = models.CharField(max_length=75, null=True)
	karyawan = models.ForeignKey(Karyawan,related_name="karyawan", on_delete=models.CASCADE)
	shift = models.ForeignKey(Shift, related_name="shift", on_delete=models.CASCADE)
	tglawal = models.DateField()
	tglakhir = models.DateField()
	tgloffawal = models.DateField(null=True)
	tgloffakhir = models.DateField(null=True)
	desc = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name
		
class Absensi(models.Model):
	name = models.CharField(max_length=25, null=True)
	desc = models.TextField(null=True)
	karyawan = models.ForeignKey(Karyawan, on_delete=models.CASCADE)
	karyawanshift = models.ForeignKey(KaryawanShift, on_delete=models.CASCADE)
	tanggal = models.DateField()
	hari = models.CharField(max_length=10)
	masuk = models.TimeField(null=True)
	keluar = models.TimeField(null=True)
	koreksi = models.DecimalField(max_digits=1, decimal_places=0, null=True, default=0)
	alasan_koreksi = models.TextField(null=True)
	SPL = models.DecimalField(max_digits=1, decimal_places=0, null=True, default=0)
	SPL_banyak = models.DecimalField(max_digits=2, decimal_places=0, null=True, default=0)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)
	delete_date = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class IzinCuti(models.Model):
	karyawan = models.ForeignKey(Karyawan)
	name = models.CharField(max_length=25, null=True)
	desc = models.TextField(null=True)
	alasan = models.TextField(null=True)
	tglmulai = models.DateField()
	tglakhir = models.DateField(null=True)
	lama = models.DecimalField(max_digits=2, decimal_places=0, null=True, default=0)
	jenis = models.CharField(max_length=6, null=True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)
	delete_date = models.DateTimeField(auto_now_add=True, null=True)

class Lembur(models.Model):
	name = models.CharField(max_length=25, null=True)
	desc = models.TextField(null=True)
	karyawan = models.ForeignKey(Karyawan, on_delete=models.CASCADE)
	tanggal = models.DateField()
	hari = models.CharField(max_length=10, null=True)
	masuk = models.TimeField(null=True)
	keluar = models.TimeField(null=True)
	jumlahjam = models.DecimalField( max_digits=2 , decimal_places=0)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)
	delete_date = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

#== EOF

class GajiPokok(models.Model):
	karyawan = models.ForeignKey(Karyawan, on_delete=models.CASCADE)
	name = models.CharField(max_length=255, null=True)
	desc = models.TextField(null=True)
	gajipokok = models.DecimalField(max_digits=20, decimal_places=0)
	jabatan = models.DecimalField(max_digits=9, decimal_places=0, null=True)
	shift = models.DecimalField(max_digits=9, decimal_places=0, null=True)
	makanlembur = models.DecimalField(max_digits=9, decimal_places=0, null=True)
	translembur = models.DecimalField(max_digits=9, decimal_places=0, null=True)
	jumlahhari = models.DecimalField(max_digits=9, decimal_places=0)
	umut = models.DecimalField(max_digits=9, decimal_places=0, null=True)
	ttelepon = models.DecimalField(max_digits=9, decimal_places=0, null=True)
	tmakan = models.DecimalField(max_digits=9, decimal_places=0, null=True)
	ttransport = models.DecimalField(max_digits=9, decimal_places=0, null=True)
	thr = models.DecimalField(max_digits=9, decimal_places=0, null=True)
	bonus = models.DecimalField(max_digits=9, decimal_places=0, null=True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Inventory(models.Model):
	name = models.CharField(max_length=200, null=True)
	nomer = models.DecimalField(max_digits=20, decimal_places=0)
	desc = models.TextField()
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Pinjaman(models.Model):
	name = models.CharField(max_length=200, null=True)
	tglpinjam = models.DateField(null=True)
	tglkembali = models.DateField(null=True)
	inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
	karyawan = models.ForeignKey(Karyawan, on_delete=models.CASCADE)
	desc = models.TextField()
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Bonusthr(models.Model):
	karyawan = models.ForeignKey(Karyawan, on_delete=models.CASCADE)
	bonus = models.DecimalField(max_digits=7, decimal_places=0,null=True, default=0)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Cuti(models.Model):
	name = models.CharField(max_length=200, null=True)
	karyawan = models.ForeignKey(Karyawan, on_delete=models.CASCADE)
	alasan = models.CharField(max_length=255)
	tglmulai = models.DateField()
	tglakhir = models.DateField()
	desc = models.TextField()
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name    

class MasaTenggangClosing(models.Model):
	name = models.CharField(max_length=200, null=True)
	tanggal = models.DateField()
	sd = models.DateField()
	desc = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class PotonganKaryawan(models.Model):
	name = models.CharField(max_length=200, null=True)
	bpjs_ks = models.DecimalField(max_digits=7, decimal_places=0,null=True, default=0)
	bpjs_kt = models.DecimalField(max_digits=7, decimal_places=0,null=True, default=0)
	pph = models.DecimalField(max_digits=7, decimal_places=0,null=True, default=0)
	koperasi = models.DecimalField(max_digits=7, decimal_places=0,null=True, default=0)
	potabsensi = models.DecimalField(max_digits=7, decimal_places=0,null=True, default=0)
	serikat = models.DecimalField(max_digits=7, decimal_places=0,null=True, default=0)
	pinjlain = models.DecimalField(max_digits=7, decimal_places=0,null=True, default=0)
	cicil_pinjlain = models.DecimalField(max_digits=2, decimal_places=0,null=True, default=0)
	pinjkaryawan = models.DecimalField(max_digits=8, decimal_places=0,null=True, default=0)
	cicil_pinjkaryawan = models.DecimalField(max_digits=2, decimal_places=0,null=True, default=0)
	masatenggangclosing = models.ForeignKey(MasaTenggangClosing, default=3, null=True, on_delete=models.SET_DEFAULT)
	karyawan = models.ForeignKey(Karyawan, on_delete=models.CASCADE)
	desc = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class TunjanganKaryawan(models.Model):
	name = models.CharField(max_length=200, null=True)
	kemahalan = models.DecimalField(max_digits=7, decimal_places=0,null=True, default=0)
	umut = models.DecimalField(max_digits=9, decimal_places=0, null=True, default=0)
	ttelepon = models.DecimalField(max_digits=9, decimal_places=0, null=True, default=0)
	tmakan = models.DecimalField(max_digits=9, decimal_places=0, null=True, default=0)
	masatenggangclosing = models.ForeignKey(MasaTenggangClosing, default=3, null=True, on_delete=models.SET_DEFAULT)
	transportexec = models.DecimalField(max_digits=7, decimal_places=0, null=True, default=0)
	transportnonexec = models.DecimalField(max_digits=7, decimal_places=0, null=True, default=0)
	karyawan = models.ForeignKey(Karyawan, on_delete=models.CASCADE)
	desc = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class HariRaya(models.Model):
	name = models.CharField(max_length=200)
	tanggal = models.DateField()
	sd = models.DateField(null=True)
	desc = models.TextField()
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class PostingGaji(models.Model):
	name = models.CharField(max_length=200, null=True)
	karyawan = models.ForeignKey(Karyawan, on_delete=models.CASCADE)
	masatenggangclosing = models.ForeignKey(MasaTenggangClosing,default=3, null=True, on_delete=models.SET_DEFAULT)	
	gajipokok = models.ForeignKey(GajiPokok, on_delete=models.PROTECT)
	potongankaryawan = models.ForeignKey(PotonganKaryawan, default=3, null=True, on_delete=models.SET_DEFAULT)
	tovertime = models.DecimalField(max_digits=7, decimal_places=0,null=True, default=0)
	pabsen = models.DecimalField(max_digits=7, decimal_places=0,null=True, default=0)
	desc = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Log(models.Model):
	name = models.CharField(max_length=200) #short 25 char from log
	tipe = models.CharField(max_length=200) # auth, app, sys
	log = models.TextField()
	desc = models.TextField()
	created_at = models.DateTimeField(auto_now=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Modules(models.Model):
	isi = "#"
	name = models.CharField(max_length=200)
	fungsi = models.CharField(max_length=200)
	menu = models.CharField(max_length=200, null=True)
	icon = models.CharField(max_length=200, null=True)
	url_slug = models.CharField(max_length=200, default=isi)
	mode = models.CharField(max_length=200, null=True)
	desc = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name

class bpjs(models.Model):
	name = models.CharField(max_length=200, null=True)
	karyawan = models.ForeignKey(Karyawan, on_delete=models.CASCADE)
	biaya = models.DecimalField(max_digits=7, decimal_places=0,null=True, default=0)
	desc = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name