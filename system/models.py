from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Perusahaan(models.Model):
	name = models.CharField(max_length=200)
	desc = models.TextField()
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Department(models.Model):
	perusahaan = models.ForeignKey(Perusahaan, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	desc = models.TextField()
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Bagian(models.Model):
	department = models.ForeignKey(Department, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	desc = models.TextField()
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Jabatan(models.Model):
	jabatan = models.ForeignKey(Bagian, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	desc = models.TextField()
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Unit(models.Model):
	unit = models.ForeignKey(Jabatan, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	desc = models.TextField()
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Level(models.Model):
	level = models.ForeignKey(Unit, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	desc = models.TextField()
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

#== Database structure by yahya

class Karyawan(models.Model):
	NIK = models.CharField(max_length=15)
	perusahaan = models.ForeignKey(Perusahaan, on_delete=models.CASCADE)
	department = models.ForeignKey(Department, on_delete=models.CASCADE)
	jabatan = models.ForeignKey(Bagian, on_delete=models.CASCADE)
	unit = models.ForeignKey(Jabatan, on_delete=models.CASCADE)
	level = models.ForeignKey(Unit, on_delete=models.CASCADE)
	#linkacc = undefined
	#groupkat = undefined
	name = models.CharField(max_length=200)
	shortname = models.CharField(max_length=200)
	tempatlahir = models.CharField(max_length=200)
	tanggallahir = models.DateField()
	alamat = models.TextField()
	provinsi = models.CharField(max_length=200)
	kota = models.CharField(max_length=200)
	gender = models.CharField(max_length=8)
	telepon = models.DecimalField(max_digits=12, decimal_places=0)
	handphone = models.DecimalField(max_digits=18, decimal_places=0)
	ktpid = models.DecimalField(max_digits=30, decimal_places=0)
	agama = models.CharField(max_length=20)
	warganegara = models.CharField(max_length=20)
	statusmenikah = models.CharField(max_length=12)
	bankname = models.CharField(max_length=50)
	atasnama = models.CharField(max_length=200)
	norek = models.CharField(max_length=70)
	fingerid = models.CharField(max_length=30)
	NPWP = models.CharField(max_length=30)
	KPJ = models.CharField(max_length=30)
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

class Absensi2017Semester1(models.Model):
	name = models.CharField(max_length=25)
	desc = models.TextField()
	NIK = models.ManyToManyField(Karyawan)
	tanggal = models.DateField()
	hari = models.CharField(max_length=10)
	masuk = models.TimeField()
	keluar = models.TimeField()
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)
	delete_date = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Lembur2017Semester1(models.Model):
	name = models.CharField(max_length=25)
	desc = models.TextField()
	NIK = models.ManyToManyField(Karyawan)
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
	NIK = models.ForeignKey(Karyawan, on_delete=models.CASCADE)
	name = models.CharField(max_length=25)
	desc = models.TextField()
	gajipokok = models.DecimalField(max_digits=10, decimal_places=0)
	tunjanganmakan = models.DecimalField(max_digits=7, decimal_places=0)
	tunjangantransport = models.DecimalField(max_digits=7, decimal_places=0)
	tunjanganjabatan = models.DecimalField(max_digits=7, decimal_places=0)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Shift(models.Model):
	name = models.CharField(max_length=25)
	desc = models.TextField()
	jadwalmasuk = models.TimeField()
	jadwalkeluar = models.TimeField()
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class KaryawanShift(models.Model):
	NIK = models.ManyToManyField(Karyawan)
	shift = models.ManyToManyField(Shift)
	tglawal = models.DateField()
	tglakhir = models.DateField()
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Log(models.Model):
	name = models.CharField(max_length=200) #short 25 char from log
	tipe = models.ForeignKey(Unit, on_delete=models.CASCADE)
	log = models.TextField()
	desc = models.TextField()
	created_at = models.DateTimeField(auto_now=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name