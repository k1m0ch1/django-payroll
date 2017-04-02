cd \
D:
cd \
cd Document\payroll
python manage.py migrate --fake system zero
python manage.py migrate system zero
cd system\migrations
del *.*
cd ../../
python manage.py makemigrations system
python manage.py migrate
python manage.py loaddata perusahaan departemen bagian golongan
