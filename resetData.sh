#!/bin/bash
python manage.py migrate system zero
echo Y | rm /home/k1m0ch1/payroll/system/migrations/*
python manage.py makemigrations system
python manage.py migrate 
python manage.py loaddata perusahaan departemen bagian golongan jabatan bank warganegara agama statusmenikah modules
python manage.py loaddata lokasiperusahaan karyawan shift karyawanshift pinjaman inventory absensi hariraya settings
python manage.py loaddata gajipokok potongan masatenggangclosing postinggaji