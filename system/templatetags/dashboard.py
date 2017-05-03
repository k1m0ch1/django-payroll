from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.assignment_tag
def define(val=None):
  return val

@register.simple_tag
def dashboard(module=None, mode=None, idpk=None):
  if module == "Bagian/ Division":
  	return{
  		'indeks' : reverse('bagian-index'),
  		'tambah' : reverse('bagian-create'),
  		'ubah'	 : reverse('bagian-edit', kwargs={'bagian_id': idpk}),
  		'hapus'	 : reverse('bagian-delete', kwargs={'bagian_id': idpk})
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
  return "null"