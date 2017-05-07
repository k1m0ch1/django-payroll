# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-07 10:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Absensi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, null=True)),
                ('desc', models.TextField(null=True)),
                ('tanggal', models.DateField()),
                ('hari', models.CharField(max_length=10)),
                ('masuk', models.TimeField()),
                ('keluar', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('delete_date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Agama',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Bagian',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cuti',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('alasan', models.CharField(max_length=255)),
                ('tglmulai', models.DateField()),
                ('tglakhir', models.DateField()),
                ('desc', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Departemen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GajiPokok',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('desc', models.TextField()),
                ('gajipokok', models.DecimalField(decimal_places=0, max_digits=10)),
                ('tmakan', models.DecimalField(decimal_places=0, max_digits=7)),
                ('transportexec', models.DecimalField(decimal_places=0, max_digits=7)),
                ('transportnonexec', models.DecimalField(decimal_places=0, max_digits=7)),
                ('jabatan', models.DecimalField(decimal_places=0, max_digits=7)),
                ('shift', models.DecimalField(decimal_places=0, max_digits=7)),
                ('makanlembur', models.DecimalField(decimal_places=0, max_digits=7)),
                ('translembur', models.DecimalField(decimal_places=0, max_digits=7)),
                ('masakerja', models.DecimalField(decimal_places=0, max_digits=7)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Golongan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HariRaya',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('tanggal', models.DateField()),
                ('sd', models.DateField(null=True)),
                ('desc', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('nomer', models.DecimalField(decimal_places=0, max_digits=20)),
                ('desc', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Jabatan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Karyawan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NIK', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=200)),
                ('shortname', models.CharField(max_length=200, null=True)),
                ('tempatlahir', models.CharField(max_length=200)),
                ('tanggallahir', models.DateField()),
                ('alamat', models.TextField()),
                ('provinsi', models.CharField(max_length=200)),
                ('kota', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=9)),
                ('telepon', models.DecimalField(decimal_places=0, max_digits=12)),
                ('handphone', models.DecimalField(decimal_places=0, max_digits=18)),
                ('ktpid', models.DecimalField(decimal_places=0, max_digits=30)),
                ('atasnama', models.CharField(max_length=200)),
                ('norek', models.CharField(max_length=70)),
                ('fingerid', models.CharField(max_length=30)),
                ('NPWP', models.CharField(max_length=30)),
                ('KPJ', models.CharField(max_length=30)),
                ('statuskaryawan', models.CharField(max_length=30)),
                ('masakaryawan', models.DateField(null=True)),
                ('jumlahhari', models.DecimalField(decimal_places=0, max_digits=1)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('delete_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('agama', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Agama')),
                ('bagian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Bagian')),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Bank')),
                ('departemen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Departemen')),
                ('golongan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Golongan')),
                ('jabatan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Jabatan')),
            ],
        ),
        migrations.CreateModel(
            name='KaryawanShift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75, null=True)),
                ('tglawal', models.DateField()),
                ('tglakhir', models.DateField()),
                ('desc', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('karyawan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='karyawan', to='system.Karyawan')),
            ],
        ),
        migrations.CreateModel(
            name='Lembur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('desc', models.TextField()),
                ('tanggal', models.DateField()),
                ('hari', models.CharField(max_length=10)),
                ('masuk', models.TimeField()),
                ('keluar', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('delete_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('karyawan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Karyawan')),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('tipe', models.CharField(max_length=200)),
                ('log', models.TextField()),
                ('desc', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LokasiPerusahaan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('alamat', models.TextField()),
                ('desc', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Modules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('fungsi', models.CharField(max_length=200)),
                ('menu', models.CharField(max_length=200, null=True)),
                ('icon', models.CharField(max_length=200, null=True)),
                ('url_slug', models.CharField(default='#', max_length=200)),
                ('mode', models.CharField(max_length=200, null=True)),
                ('desc', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Perusahaan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pinjaman',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('tglpinjam', models.DateField(null=True)),
                ('tglkembali', models.DateField(null=True)),
                ('desc', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Inventory')),
                ('karyawan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Karyawan')),
            ],
        ),
        migrations.CreateModel(
            name='PotonganKaryawan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('bpjs', models.DecimalField(decimal_places=0, max_digits=7)),
                ('pph', models.DecimalField(decimal_places=0, max_digits=7)),
                ('potabsensi', models.DecimalField(decimal_places=0, max_digits=7)),
                ('serikat', models.DecimalField(decimal_places=0, max_digits=7)),
                ('pinjlain', models.DecimalField(decimal_places=0, max_digits=7)),
                ('pinjkaryawan', models.DecimalField(decimal_places=0, max_digits=7)),
                ('desc', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('karyawan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Karyawan')),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('desc', models.TextField()),
                ('jammasuk', models.TimeField()),
                ('jamkeluar', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StatusMenikah',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WargaNegara',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='lokasiperusahaan',
            name='perusahaan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Perusahaan'),
        ),
        migrations.AddField(
            model_name='karyawanshift',
            name='shift',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shift', to='system.Shift'),
        ),
        migrations.AddField(
            model_name='karyawan',
            name='perusahaan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Perusahaan'),
        ),
        migrations.AddField(
            model_name='karyawan',
            name='statusmenikah',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.StatusMenikah'),
        ),
        migrations.AddField(
            model_name='karyawan',
            name='warganegara',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.WargaNegara'),
        ),
        migrations.AddField(
            model_name='gajipokok',
            name='karyawan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Karyawan'),
        ),
        migrations.AddField(
            model_name='cuti',
            name='karyawan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Karyawan'),
        ),
        migrations.AddField(
            model_name='absensi',
            name='karyawan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Karyawan'),
        ),
    ]
