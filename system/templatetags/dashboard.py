from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.assignment_tag
def define(val=None):
  return val

@register.filter()
def berubah(val=None):
  return val  

@register.filter()
def ubah(val=None):
  if val == "" :
    val = 0
  return int(val)

@register.simple_tag
def dashboard(module=None, mode=None, idpk=None):
  if module == "Bagian/ Division":
  	return{
  		'indeks' : reverse('bagian-index'),
  		'tambah' : reverse('bagian-create'),
  		'ubah'	 : reverse('bagian-edit', kwargs={'bagian_id': idpk}),
  		'hapus'	 : reverse('bagian-delete', kwargs={'bagian_id': idpk})
  	}[mode]
  elif module == 'Perusahaan/ Company':
    return{
      'indeks' : reverse('perusahaan-index'),
      'tambah' : reverse('perusahaan-create'),
      'ubah'   : reverse('perusahaan-edit', kwargs={'perusahaan_id': idpk}),
      'hapus'  : reverse('perusahaan-delete', kwargs={'perusahaan_id': idpk})
    }[mode]
  elif module == 'Departemen/ Department':
    return{
      'indeks' : reverse('departemen-index'),
      'tambah' : reverse('departemen-create'),
      'ubah'   : reverse('departemen-edit', kwargs={'departemen_id': idpk}),
      'hapus'  : reverse('departemen-delete', kwargs={'departemen_id': idpk})
    }[mode]
  elif module == 'Golongan/ Category':
    return{
      'indeks' : reverse('golongan-index'),
      'tambah' : reverse('golongan-create'),
      'ubah'   : reverse('golongan-edit', kwargs={'golongan_id': idpk}),
      'hapus'  : reverse('golongan-delete', kwargs={'golongan_id': idpk})
    }[mode]
  elif module == 'Jabatan/ Occupation':
    return{
      'indeks' : reverse('jabatan-index'),
      'tambah' : reverse('jabatan-create'),
      'ubah'   : reverse('jabatan-edit', kwargs={'jabatan_id': idpk}),
      'hapus'  : reverse('jabatan-delete', kwargs={'jabatan_id': idpk})
    }[mode]
  elif module == 'Bank':
    return{
      'indeks' : reverse('bank-index'),
      'tambah' : reverse('bank-create'),
      'ubah'   : reverse('bank-edit', kwargs={'bank_id': idpk}),
      'hapus'  : reverse('bank-delete', kwargs={'bank_id': idpk})
    }[mode]
  elif module == 'Agama/ Religion':
    return{
      'indeks' : reverse('agama-index'),
      'tambah' : reverse('agama-create'),
      'ubah'   : reverse('agama-edit', kwargs={'agama_id': idpk}),
      'hapus'  : reverse('agama-delete', kwargs={'agama_id': idpk})
    }[mode]
  elif module == 'Warga Negara/ Nationality':
    return{
      'indeks' : reverse('warganegara-index'),
      'tambah' : reverse('warganegara-create'),
      'ubah'   : reverse('warganegara-edit', kwargs={'warganegara_id': idpk}),
      'hapus'  : reverse('warganegara-delete', kwargs={'warganegara_id': idpk})
    }[mode]
  elif module == 'Status Menikah/ Marital Status':
    return{
      'indeks' : reverse('statusmenikah-index'),
      'tambah' : reverse('statusmenikah-create'),
      'ubah'   : reverse('statusmenikah-edit', kwargs={'statusmenikah_id': idpk}),
      'hapus'  : reverse('statusmenikah-delete', kwargs={'statusmenikah_id': idpk})
    }[mode]
  elif module == 'Hari Raya':
    return{
      'indeks' : reverse('hariraya-index'),
      'tambah' : reverse('hariraya-create'),
      'ubah'   : reverse('hariraya-edit', kwargs={'hariraya_id': idpk}),
      'hapus'  : reverse('hariraya-delete', kwargs={'hariraya_id': idpk})
    }[mode]
  elif module == 'Shift':
    return{
      'indeks' : reverse('shift-index'),
      'tambah' : reverse('shift-create'),
      'ubah'   : reverse('shift-edit', kwargs={'shift_id': idpk}),
      'hapus'  : reverse('shift-delete', kwargs={'shift_id': idpk})
    }[mode]
  elif module == 'Inventory':
    return{
      'indeks' : reverse('inventory-index'),
      'tambah' : reverse('inventory-create'),
      'ubah'   : reverse('inventory-edit', kwargs={'inventory_id': idpk}),
      'hapus'  : reverse('inventory-delete', kwargs={'inventory_id': idpk})
    }[mode]
  elif module == 'Pengaturan Aplikasi':
    return{
      'indeks' : reverse('konfigurasi-index'),
      'tambah' : reverse('konfigurasi-create'),
      'ubah'   : reverse('konfigurasi-edit', kwargs={'konfigurasi_id': idpk}),
      'hapus'  : reverse('konfigurasi-delete', kwargs={'konfigurasi_id': idpk})
    }[mode]
  elif module == 'Inventory Pinjaman':
    return{
      'indeks' : reverse('pinjaman-index'),
      'tambah' : reverse('pinjaman-create'),
      # 'ubah'   : reverse('pinjaman-edit', kwargs={'pinjaman_id': idpk}),
      # 'hapus'  : reverse('pinjaman-delete', kwargs={'pinjaman_id': idpk})
    }[mode]
  elif module == 'Masa Tenggang Closing':
    return{
      'indeks' : reverse('masatenggangclosing-index'),
      'tambah' : reverse('masatenggangclosing-create'),
      'ubah'   : reverse('masatenggangclosing-edit', kwargs={'masatenggangclosing_id': idpk}),
      'hapus'  : reverse('masatenggangclosing-delete', kwargs={'masatenggangclosing_id': idpk})
    }[mode]
  elif module == 'Tunjangan Karyawan':
    return{
      'indeks' : reverse('masatenggangclosing-index')
    }[mode]
  elif module == 'Potongan Karyawan':
    return{
      'indeks' : reverse('masatenggangclosing-index')
    }[mode]
  return "null"

@register.assignment_tag
def bpjs(val=None, per=None):
  return int(float(float(per)/100)) * val

@register.assignment_tag
def bpjs_kes(val=None):
  bpjs_kes_kar = int(float(float(1)/100) * int('0' + val)) # BPJS Kesehatan Karyawan 1%
  bpjs_kes_per = int(float(float(4)/100) * int('0' + val)) # BPJS Kesehatan Perusahaan 4%
  return bpjs_kes_kar + bpjs_kes_per


@register.assignment_tag
def bpjs_ket(val=None):
  bpjs_ktg_kar_jpn = int(float(float(1)/100) * int('0' + val)) # BPJS Ketenagakerjaan Karyawan Jaminan Pensiunan 1%
  bpjs_ktg_kar_jht = int(float(float(2)/100) * int('0' + val)) # BPJS Ketenagakerjaan Karyawan Jaminan Hari Tua 2%
  bpjs_ktg_per_jpn = int(float(float(2)/100) * int('0' + val)) # BPJS Ketenagakerjaan Perusahaan Jaminan Kematian 2%
  bpjs_ktg_per_jkk = int(float(float(0.54)/100) * int('0' + val)) # BPJS Ketenagakerjaan Perusahaan Kecelakaan Kerja 0.54% 
  bpjs_ktg_per_jht = int(float(float(3.7)/100) * int('0' + val)) # BPJS Ketenagakerjaan Perusahaan Jaminan Hari Tua 3.7%
  bpjs_ktg_per_jkm = int(float(float(0.3)/100) * int('0' + val)) # BPJS Ketenagakerjaan Perusaaan Jaminan Kematian 0.3%
  return bpjs_ktg_kar_jpn + bpjs_ktg_kar_jht + bpjs_ktg_per_jpn + bpjs_ktg_per_jkk + bpjs_ktg_per_jht + bpjs_ktg_per_jkm

@register.assignment_tag
def bpjs_bayar(val=None):
  bpjs_kes_kar = int(float(float(1)/100) * int('0' + val)) # BPJS Kesehatan Karyawan 1%
  bpjs_kes_per = int(float(float(4)/100) * int('0' + val)) # BPJS Kesehatan Perusahaan 4%
  bpjs_ktg_kar_jpn = int(float(float(1)/100) * int('0' + val)) # BPJS Ketenagakerjaan Karyawan Jaminan Pensiunan 1%
  bpjs_ktg_kar_jht = int(float(float(2)/100) * int('0' + val)) # BPJS Ketenagakerjaan Karyawan Jaminan Hari Tua 2%
  bpjs_ktg_per_jpn = int(float(float(2)/100) * int('0' + val)) # BPJS Ketenagakerjaan Perusahaan Jaminan Kematian 2%
  bpjs_ktg_per_jkk = int(float(float(0.54)/100) * int('0' + val)) # BPJS Ketenagakerjaan Perusahaan Kecelakaan Kerja 0.54% 
  bpjs_ktg_per_jht = int(float(float(3.7)/100) * int('0' + val)) # BPJS Ketenagakerjaan Perusahaan Jaminan Hari Tua 3.7%
  bpjs_ktg_per_jkm = int(float(float(0.3)/100) * int('0' + val)) # BPJS Ketenagakerjaan Perusaaan Jaminan Kematian 0.3%
  return bpjs_ktg_kar_jpn + bpjs_ktg_kar_jht + bpjs_ktg_per_jpn + bpjs_ktg_per_jkk + bpjs_ktg_per_jht + bpjs_kes_kar + bpjs_kes_per + bpjs_ktg_per_jkm

@register.assignment_tag
def penghasilan_bruto(gapok=None, tunjangan=None):
  bpjs_ktg_per_jkk = int(float(float(0.54)/100) * int('0' + gapok)) # BPJS Ketenagakerjaan Perusahaan Kecelakaan Kerja 0.54% 
  bpjs_ktg_per_jkm = int(float(float(0.3)/100) * int('0' + gapok)) # BPJS Ketenagakerjaan Perusaaan Jaminan Kematian 0.3%
  bpjs_kes_per = int(float(float(4)/100) * int('0' + gapok)) # BPJS Kesehatan Perusahaan 4%
  return gapok + tunjangan + bpjs_ktg_per_jkk + bpjs_ktg_per_jkm + bpjs_kes_per

@register.assignment_tag
def ph_netto_sebulan(gapok=None, tunjangan=None):
  bpjs_ktg_per_jkk = int(float(float(0.54)/100) * int('0' + gapok)) # BPJS Ketenagakerjaan Perusahaan Kecelakaan Kerja 0.54% 
  bpjs_ktg_per_jkm = int(float(float(0.3)/100) * int('0' + gapok)) # BPJS Ketenagakerjaan Perusaaan Jaminan Kematian 0.3%
  bpjs_kes_per = int(float(float(4)/100) * int('0' + gapok)) # BPJS Kesehatan Perusahaan 4%
  bruto = gapok + tunjangan + bpjs_ktg_per_jkk + bpjs_ktg_per_jkm + bpjs_kes_per

  bpjs_ktg_kar_jht = int(float(float(2)/100) * int('0' + gapok)) # BPJS Ketenagakerjaan Karyawan Jaminan Hari Tua 2%
  bpjs_ktg_per_jpn = int(float(float(2)/100) * int('0' + gapok)) # BPJS Ketenagakerjaan Perusahaan Jaminan Kematian 2%

  return bruto - ( (int(float(float(5)/100) * bruto)) + bpjs_ktg_kar_jht + bpjs_ktg_per_jpn )

@register.assignment_tag
def ph_netto_setahun(gapok=None, tunjangan=None):
  bpjs_ktg_per_jkk = int(float(float(0.54)/100) * int('0' + gapok)) # BPJS Ketenagakerjaan Perusahaan Kecelakaan Kerja 0.54% 
  bpjs_ktg_per_jkm = int(float(float(0.3)/100) * int('0' + gapok)) # BPJS Ketenagakerjaan Perusaaan Jaminan Kematian 0.3%
  bpjs_kes_per = int(float(float(4)/100) * int('0' + gapok)) # BPJS Kesehatan Perusahaan 4%
  bruto = gapok + tunjangan + bpjs_ktg_per_jkk + bpjs_ktg_per_jkm + bpjs_kes_per

  bpjs_ktg_kar_jht = int(float(float(2)/100) * int('0' + gapok)) # BPJS Ketenagakerjaan Karyawan Jaminan Hari Tua 2%
  bpjs_ktg_per_jpn = int(float(float(2)/100) * int('0' + gapok)) # BPJS Ketenagakerjaan Perusahaan Jaminan Kematian 2%

  ph_netto_sebulan = bruto - ( (int(float(float(5)/100) * bruto)) + bpjs_ktg_kar_jht + bpjs_ktg_per_jpn )

  return ph_netto_sebulan * 12

@register.assignment_tag
def ph_kena_pajak(gapok=None, tunjangan=None, status=None):
  ptkp = 0
  if status == "Lajang Tanpa Tanggungan" :
    ptkp = 54000000
  elif status == "Lajang 1 Tanggungan" or status == "Menikah Tanpa Tanggungan" :
    ptkp = 58500000
  elif status ==  "Lajang 2 Tanggungan" or status == "Menikah 1 Tanggungan" :
    ptkp = 63000000
  elif status == "Menikah 2 Tanggungan" :
    ptkp = 67500000
  elif status == "Menikah 3 Tanggungan" :
    ptkp = 72000000

  bpjs_ktg_per_jkk = int(float(float(0.54)/100) * int('0' + gapok)) # BPJS Ketenagakerjaan Perusahaan Kecelakaan Kerja 0.54% 
  bpjs_ktg_per_jkm = int(float(float(0.3)/100) * int('0' + gapok)) # BPJS Ketenagakerjaan Perusaaan Jaminan Kematian 0.3%
  bpjs_kes_per = int(float(float(4)/100) * int('0' + gapok)) # BPJS Kesehatan Perusahaan 4%
  bruto = gapok + tunjangan + bpjs_ktg_per_jkk + bpjs_ktg_per_jkm + bpjs_kes_per

  bpjs_ktg_kar_jht = int(float(float(2)/100) * int('0' + gapok)) # BPJS Ketenagakerjaan Karyawan Jaminan Hari Tua 2%
  bpjs_ktg_per_jpn = int(float(float(2)/100) * int('0' + gapok)) # BPJS Ketenagakerjaan Perusahaan Jaminan Kematian 2%

  ph_netto_sebulan = bruto - ( (int(float(float(5)/100) * bruto)) + bpjs_ktg_kar_jht + bpjs_ktg_per_jpn )

  ph_netto_setahun = ph_netto_sebulan * 12

  return ph_netto_setahun - ptkp

@register.assignment_tag
def pph_terhutang(gapok=None, tunjangan=None, status=None):
  wp = 0

  if gapok <= 50000000 :
    wp = float(float(5)/100) 
  elif gapok > 50000000 or gapok <= 250000000 :
    wp = float(float(15)/100) 
  elif gapok > 250000000 or gapok <= 500000000 :
    wp = float(float(25)/100)
  elif gapok > 500000000 :
    wp = float(float(30)/100)

  ptkp = 0

  if status == "Lajang Tanpa Tanggungan" :
    ptkp = 54000000
  elif status == "Lajang 1 Tanggungan" or status == "Menikah Tanpa Tanggungan" :
    ptkp = 58500000
  elif status ==  "Lajang 2 Tanggungan" or status == "Menikah 1 Tanggungan" :
    ptkp = 63000000
  elif status == "Menikah 2 Tanggungan" :
    ptkp = 67500000
  elif status == "Menikah 3 Tanggungan" :
    ptkp = 72000000

  bpjs_ktg_per_jkk = int(float(float(0.54)/100) * int('0' + gapok)) # BPJS Ketenagakerjaan Perusahaan Kecelakaan Kerja 0.54% 
  bpjs_ktg_per_jkm = int(float(float(0.3)/100) * int('0' + gapok)) # BPJS Ketenagakerjaan Perusaaan Jaminan Kematian 0.3%
  bpjs_kes_per = int(float(float(4)/100) * int('0' + gapok)) # BPJS Kesehatan Perusahaan 4%
  bruto = gapok + tunjangan + bpjs_ktg_per_jkk + bpjs_ktg_per_jkm + bpjs_kes_per

  bpjs_ktg_kar_jht = int(float(float(2)/100) * int('0' + gapok)) # BPJS Ketenagakerjaan Karyawan Jaminan Hari Tua 2%
  bpjs_ktg_per_jpn = int(float(float(2)/100) * int('0' + gapok)) # BPJS Ketenagakerjaan Perusahaan Jaminan Kematian 2%

  ph_netto_sebulan = bruto - ( (int(float(float(5)/100) * bruto)) + bpjs_ktg_kar_jht + bpjs_ktg_per_jpn )

  ph_netto_setahun = ph_netto_sebulan * 12

  ph_kena_pajak = ph_netto_setahun - ptkp

  return int(wp * int(ph_kena_pajak))

@register.assignment_tag
def pph_bayar(gapok=None, tunjangan=None, status=None, bpjs=None):

  if gapok == "" and  tunjangan == "" and status == "" and  bpjs == "" :
    return 0
  else:
    wp = 0

    if gapok <= 50000000 :
      wp = float(float(5)/100) 
    elif gapok > 50000000 or gapok <= 250000000 :
      wp = float(float(15)/100) 
    elif gapok > 250000000 or gapok <= 500000000 :
      wp = float(float(25)/100)
    elif gapok > 500000000 :
      wp = float(float(30)/100)

    ptkp = 0

    if status == "Lajang Tanpa Tanggungan" :
      ptkp = 54000000
    elif status == "Lajang 1 Tanggungan" or status == "Menikah Tanpa Tanggungan" :
      ptkp = 58500000
    elif status ==  "Lajang 2 Tanggungan" or status == "Menikah 1 Tanggungan" :
      ptkp = 63000000
    elif status == "Menikah 2 Tanggungan" :
      ptkp = 67500000
    elif status == "Menikah 3 Tanggungan" :
      ptkp = 72000000

    bpjs_ktg_per_jkk = int(float(float(0.54)/100) * int('0' + bpjs)) # BPJS Ketenagakerjaan Perusahaan Kecelakaan Kerja 0.54% 
    bpjs_ktg_per_jkm = int(float(float(0.3)/100) * int('0' + bpjs)) # BPJS Ketenagakerjaan Perusaaan Jaminan Kematian 0.3%
    bpjs_kes_per = int(float(float(4)/100) * int('0' + bpjs)) # BPJS Kesehatan Perusahaan 4%
    bruto = gapok + tunjangan + bpjs_ktg_per_jkk + bpjs_ktg_per_jkm + bpjs_kes_per

    bpjs_ktg_kar_jht = int(float(float(2)/100) * int('0' + bpjs)) # BPJS Ketenagakerjaan Karyawan Jaminan Hari Tua 2%
    bpjs_ktg_per_jpn = int(float(float(2)/100) * int('0' + bpjs)) # BPJS Ketenagakerjaan Perusahaan Jaminan Kematian 2%

    ph_netto_sebulan = bruto - ( (int(float(float(5)/100) * int('0' +bruto))) + bpjs_ktg_kar_jht + bpjs_ktg_per_jpn )

    ph_netto_setahun = ph_netto_sebulan * 12

    ph_kena_pajak = ph_netto_setahun - ptkp

    pph_terhutang = int(wp * int(ph_kena_pajak))

    return pph_terhutang / 12

@register.filter()
def sptkp(val=None):
  ptkp = 0
  status = val
  if status == "Lajang Tanpa Tanggungan" :
    ptkp = 54000000
  elif status == "Lajang 1 Tanggungan" or status == "Menikah Tanpa Tanggungan" :
    ptkp = 58500000
  elif status ==  "Lajang 2 Tanggungan" or status == "Menikah 1 Tanggungan" :
    ptkp = 63000000
  elif status == "Menikah 2 Tanggungan" :
    ptkp = 67500000
  elif status == "Menikah 3 Tanggungan" :
    ptkp = 72000000

  return ptkp
