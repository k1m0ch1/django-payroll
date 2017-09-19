SET basenya=E:\Document\payroll
cd %basenya%
python manage.py migrate system zero
cd %basenya%\system\migrations
echo Y | del *.*
cd %basenya%
python manage.py makemigrations system
python manage.py migrate 
python manage.py loaddata perusahaan departemen bagian golongan jabatan bank warganegara agama statusmenikah modules
python manage.py loaddata lokasiperusahaan karyawan shift karyawanshift pinjaman inventory absensi hariraya settings
python manage.py loaddata gajipokok potongan masatenggangclosing postinggaji izindancuti tunjangankaryawan bpjs
