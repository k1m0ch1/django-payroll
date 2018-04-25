from django import template
from django.core.urlresolvers import reverse
import time, datetime
from dateutil.relativedelta import relativedelta, MO

register = template.Library()

@register.simple_tag
def hari(day=None):
	if day=="Sun":
		return "Minggu"
	elif day=="Mon":
		return "Senin"
	elif day=="Tue":
		return "Selasa"
	elif day=="Wed":
		return "Rabu"
	elif day=="Thu":
		return "Kamis"
	elif day=="Fri":
		return "Jumat"
	elif day=="Sat":
		return "Sabtu"

@register.simple_tag
def waktu(waktu=None, jadwal=None, masuk=None):

	if waktu is None:
		waktu = datetime.time(0)
		return ""
	else:
		waktu = waktu

		hasil = ""
		akhir = ""
		wj, wm, wd = waktu.strftime("%H:%M:%S").split(':')
		waktu = (int(wj)*3600) + (int(wm)*60) + int(wd)
		jj, jm, jd = jadwal.strftime("%H:%M:%S").split(':')
		jadwal = (int(jj)*3600) + (int(jm)*60) + int(jd)
		nilai = waktu-jadwal
		jamA = int(nilai)/3600
		menitA = int(nilai)/60
		detikA = int(nilai) - int(nilai)
		jam = "" 
		menit = ""
		detik = ""
		jamB= False
		menitB= False
		#melakukan lebih awal daripada jam
		akhir = "<label style='color:red;'> < " if jamA == -1 else "<label style='color:red;'>"

		if jamA < -1 :
			a, jam = str(jamA).split('-')
			jam = str(jamA+3) + " jam "
			akhir = akhir + " < " + jam
		elif jamA > 0 :
			akhir = akhir + " > " + str(jamA)  + " jam "
			jamB = True

		if menitA <= -1 :
			a, menit = str(int(menitA%-60)).split('-')
			akhir = akhir + menit + " menit "
		elif menitA > 0 :
			hasil = hasil + str(int(menitA%60)) + " menit "
			akhir = akhir + ">" + hasil if jamB == False else akhir + hasil
			menitB = True

		if detikA <= -1 :
			a, detik = str(detikA).split('-')
			hasil = hasil + detik + " detik "
			akhir = akhir +  " < " + hasil
		elif int(nilai) - int(nilai) >0:
			hasil = hasil + str(detikA) + " detik "
			akhir = akhir + " > " + hasil


		return akhir + "</label>"
	#return str(int(nilai)/3600) + " jam " + str(int(nilai)/60) + " menit " + str(int(nilai)-int(nilai)) + " detik "
	#return (datetime.datetime.strptime(waktu.strftime("%H:%M:%S"), "%H:%M:%S")-datetime.datetime.strptime(jadwal.strftime("%H:%M:%S"), "%H:%M:%S"))

@register.simple_tag
def plainwaktu(waktu=None):
	if waktu is None:
		return "<label style='color:blue;'>Belum Keluar</label>"
	else:
		return waktu

@register.simple_tag
def getSenin(date=None):
	kurangi = 0
	if date.strftime('%a')=="Sun":	
		kurangi = 6
	elif date.strftime('%a')=="Mon":
		kurangi = 0
	elif date.strftime('%a')=="Tue":
		kurangi = 1
	elif date.strftime('%a')=="Wed":
		kurangi = 2
	elif date.strftime('%a')=="Thu":
		kurangi = 3
	elif date.strftime('%a')=="Fri":
		kurangi = 4
	elif date.strftime('%a')=="Sat":
		kurangi = 5

	return datetime.datetime.fromordinal(date.toordinal()-kurangi).strftime("%Y-%m-%d")