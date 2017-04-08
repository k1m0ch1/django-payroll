cd \
D:
cd \
cd Document\payroll
python manage.py migrate system zero
cd system\migrations
echo Y | del *.*
cd ../../
python manage.py makemigrations system
python manage.py migrate
python manage.py loaddata perusahaan departemen bagian golongan jabatan 
python manage.py loaddata bank warganegara agama statusmenikah modules
python manage.py loaddata lokasiperusahaan
