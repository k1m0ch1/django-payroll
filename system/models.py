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
	NIK = models.CharField(max_length=15)
	perusahaan = models.ForeignKey(Perusahaan)
	departemen = models.ForeignKey(Departemen)
	jabatan = models.ForeignKey(Jabatan, null=True)
	bagian = models.ForeignKey(Bagian)
	golongan = models.ForeignKey(Golongan)
	#unit = models.ForeignKey(Jabatan, on_delete=models.CASCADE)
	#level = models.ForeignKey(Level, on_delete=models.CASCADE)
	#linkacc = undefined
	#groupkat = undefined
	name = models.CharField(max_length=200)
	shortname = models.CharField(max_length=200, null=True)
	tempatlahir = models.CharField(max_length=200)
	tanggallahir = models.DateField()
	alamat = models.TextField()
	provinsi = models.CharField(max_length=200)
	kota = models.CharField(max_length=200)
	gender = models.CharField(max_length=9)
	telepon = models.DecimalField(max_digits=12, decimal_places=0)
	handphone = models.DecimalField(max_digits=18, decimal_places=0)
	ktpid = models.DecimalField(max_digits=30, decimal_places=0)
	agama = models.ForeignKey(Agama)
	warganegara = models.ForeignKey(WargaNegara)
	statusmenikah = models.ForeignKey(StatusMenikah)
	bank = models.ForeignKey(Bank)
	atasnama = models.CharField(max_length=200)
	norek = models.CharField(max_length=70)
	fingerid = models.CharField(max_length=30)
	NPWP = models.CharField(max_length=30)
	KPJ = models.CharField(max_length=30)
	statuskaryawan = models.CharField(max_length=30)
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
	name = models.CharField(max_length=25)
	desc = models.TextField()
	jammasuk = models.TimeField()
	jamkeluar = models.TimeField()
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class KaryawanShift(models.Model):
	name = models.CharField(max_length=75, null=True)
	karyawan = models.ForeignKey(Karyawan,related_name="karyawan")
	shift = models.ForeignKey(Shift, related_name="shift")
	tglawal = models.DateField()
	tglakhir = models.DateField()
	desc = models.TextField()
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name
		
class Absensi(models.Model):
	name = models.CharField(max_length=25, null=True)
	desc = models.TextField(null=True)
	karyawan = models.ForeignKey(Karyawan)
	karyawanshift = models.ForeignKey(KaryawanShift)
	tanggal = models.DateField()
	hari = models.CharField(max_length=10)
	masuk = models.TimeField()
	keluar = models.TimeField()
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)
	delete_date = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Lembur(models.Model):
	name = models.CharField(max_length=25)
	desc = models.TextField()
	karyawan = models.ForeignKey(Karyawan)
	tanggal = models.DateField()
	hari = models.CharField(max_length=10)
	masuk = models.TimeField()
	keluar = models.TimeField()
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)
	delete_date = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

#== EOF

class GajiPokok(models.Model):
	karyawan = models.ForeignKey(Karyawan)
	name = models.CharField(max_length=255)
	desc = models.TextField(null=True)
	gajipokok = models.DecimalField(max_digits=20, decimal_places=0)
	tmakan = models.DecimalField(max_digits=7, decimal_places=0, null=True)
	transportexec = models.DecimalField(max_digits=7, decimal_places=0, null=True)
	transportnonexec = models.DecimalField(max_digits=7, decimal_places=0, null=True)
	jabatan = models.DecimalField(max_digits=7, decimal_places=0, null=True)
	shift = models.DecimalField(max_digits=7, decimal_places=0, null=True)
	makanlembur = models.DecimalField(max_digits=7, decimal_places=0, null=True)
	translembur = models.DecimalField(max_digits=7, decimal_places=0, null=True)
	jumlahhari = models.DecimalField(max_digits=7, decimal_places=0)
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
	inventory = models.ForeignKey(Inventory)
	karyawan = models.ForeignKey(Karyawan)
	desc = models.TextField()
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Cuti(models.Model):
	name = models.CharField(max_length=200, null=True)
	karyawan = models.ForeignKey(Karyawan)
	alasan = models.CharField(max_length=255)
	tglmulai = models.DateField()
	tglakhir = models.DateField()
	desc = models.TextField()
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name    

class PotonganKaryawan(models.Model):
	name = models.CharField(max_length=200, null=True)
	bpjs = models.DecimalField(max_digits=7, decimal_places=0)
	pph = models.DecimalField(max_digits=7, decimal_places=0)
	potabsensi = models.DecimalField(max_digits=7, decimal_places=0)
	serikat = models.DecimalField(max_digits=7, decimal_places=0)
	pinjlain = models.DecimalField(max_digits=7, decimal_places=0)
	pinjkaryawan = models.DecimalField(max_digits=7, decimal_places=0)
	karyawan = models.ForeignKey(Karyawan)
	desc = models.TextField()
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

class Log(models.Model):
	name = models.CharField(max_length=200) #short 25 char from log
	tipe = models.CharField(max_length=200)
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