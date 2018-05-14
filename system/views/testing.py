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
from datetime import timedelta
from django.http import JsonResponse

modules = Modules.objects.all()
allmenu = Modules.objects.only('name')

@login_required()
def postinggaji(request):
	today = datetime.datetime.now()
	idkaryawan = request.POST['idkaryawan']
	masatenggangclosing = request.POST['masatenggangclosing']
	mas = MasaTenggangClosing.objects.get(pk=masatenggangclosing)
	listkaryawan = getlistkaryawan(idkaryawan)

	hasil = serializers.serialize("json", listkaryawan)

	return JsonResponse(hasil, safe=False)

def getlistkaryawan(idkaryawan):
	if idkaryawan.find(",") != -1 :
		listid = [x.strip() for x in idkaryawan.split(',')]
		a = listid
	else:		
		listid = [x.strip() for x in idkaryawan.split('&')]
		a = Karyawan.objects
		if listid[0] != "":
			a = a.filter(perusahaan=listid[0])

		if listid[1] != "":
			a = a.filter(departemen=listid[1])

		if listid[2] != "":
			a = a.filter(bagian=listid[2])

		if listid[3] != "":
			a = a.filter(golongan=listid[3])

	print a

	return a
