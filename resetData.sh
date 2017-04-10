python manage.py migrate system zero
echo Y | rm /media/k1m0ch1/82EC1E40EC1E2EC3/Document/payroll/system/migrations/*
python manage.py makemigrations system
python manage.py migrate 
python manage.py loaddata perusahaan departemen bagian golongan jabatan bank warganegara agama statusmenikah modules
python manage.py loaddata lokasiperusahaan karyawan shift karyawanshift pinjaman inventory cuti
