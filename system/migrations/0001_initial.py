# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-08 17:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Absensi2017Semester1',
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
                ('tunjanganmakan', models.DecimalField(decimal_places=0, max_digits=7)),
                ('tunjangantransport', models.DecimalField(decimal_places=0, max_digits=7)),
                ('tunjanganjabatan', models.DecimalField(decimal_places=0, max_digits=7)),
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
                ('shortname', models.CharField(max_length=200)),
                ('tempatlahir', models.CharField(max_length=200)),
                ('tanggallahir', models.DateField()),
                ('alamat', models.TextField()),
                ('provinsi', models.CharField(max_length=200)),
                ('kota', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=8)),
                ('telepon', models.DecimalField(decimal_places=0, max_digits=12)),
                ('handphone', models.DecimalField(decimal_places=0, max_digits=18)),
                ('ktpid', models.DecimalField(decimal_places=0, max_digits=30)),
                ('atasnama', models.CharField(max_length=200)),
                ('norek', models.CharField(max_length=70)),
                ('fingerid', models.CharField(max_length=30)),
                ('NPWP', models.CharField(max_length=30)),
                ('KPJ', models.CharField(max_length=30)),
                ('jumlahhari', models.DecimalField(decimal_places=0, max_digits=1)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('delete_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('agama', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Agama')),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Bank')),
                ('departemen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Departemen')),
                ('jabatan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Bagian')),
            ],
        ),
        migrations.CreateModel(
            name='KaryawanShift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tglawal', models.DateField()),
                ('tglakhir', models.DateField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('NIK', models.ManyToManyField(to='system.Karyawan')),
            ],
        ),
        migrations.CreateModel(
            name='Lembur2017Semester1',
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
                ('NIK', models.ManyToManyField(to='system.Karyawan')),
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
            name='Shift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('desc', models.TextField()),
                ('jadwalmasuk', models.TimeField()),
                ('jadwalkeluar', models.TimeField()),
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
            field=models.ManyToManyField(to='system.Shift'),
        ),
        migrations.AddField(
            model_name='karyawan',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Level'),
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
            name='NIK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Karyawan'),
        ),
        migrations.AddField(
            model_name='absensi2017semester1',
            name='NIK',
            field=models.ManyToManyField(to='system.Karyawan'),
        ),
    ]
