# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-20 09:11
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
            name='Bagian',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField()),
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
            name='Jabatan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('jabatan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Bagian')),
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
                ('agama', models.CharField(max_length=20)),
                ('warganegara', models.CharField(max_length=20)),
                ('statusmenikah', models.CharField(max_length=12)),
                ('bankname', models.CharField(max_length=50)),
                ('atasnama', models.CharField(max_length=200)),
                ('norek', models.CharField(max_length=70)),
                ('fingerid', models.CharField(max_length=30)),
                ('NPWP', models.CharField(max_length=30)),
                ('KPJ', models.CharField(max_length=30)),
                ('jumlahhari', models.DecimalField(decimal_places=0, max_digits=1)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('delete_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Department')),
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
                ('desc', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('log', models.TextField()),
                ('desc', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Perusahaan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField()),
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
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Jabatan')),
            ],
        ),
        migrations.AddField(
            model_name='log',
            name='tipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Unit'),
        ),
        migrations.AddField(
            model_name='level',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Unit'),
        ),
        migrations.AddField(
            model_name='karyawanshift',
            name='shift',
            field=models.ManyToManyField(to='system.Shift'),
        ),
        migrations.AddField(
            model_name='karyawan',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Unit'),
        ),
        migrations.AddField(
            model_name='karyawan',
            name='perusahaan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Perusahaan'),
        ),
        migrations.AddField(
            model_name='karyawan',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Jabatan'),
        ),
        migrations.AddField(
            model_name='gajipokok',
            name='NIK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Karyawan'),
        ),
        migrations.AddField(
            model_name='department',
            name='perusahaan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Perusahaan'),
        ),
        migrations.AddField(
            model_name='bagian',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Department'),
        ),
        migrations.AddField(
            model_name='absensi2017semester1',
            name='NIK',
            field=models.ManyToManyField(to='system.Karyawan'),
        ),
    ]
