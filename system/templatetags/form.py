from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def form(module=None, mode=None, idpk=None):
	if module == "Bagian/ Division":
		return{
			'Tambah' : reverse('bagian-create-save'),
			'Ubah'   : reverse('bagian-edit-save', kwargs={'bagian_id': idpk})
		}[mode]
	elif module == "Perusahaan/ Company":
	    return{
			'Tambah' : reverse('perusahaan-create-save'),
			'Ubah'   : reverse('perusahaan-edit-save', kwargs={'perusahaan_id': idpk})
		}[mode]
	elif module == "Departemen/ Department":
	    return{
			'Tambah' : reverse('departemen-create-save'),
			'Ubah'   : reverse('departemen-edit-save', kwargs={'departemen_id': idpk})
		}[mode]
	elif module == 'Golongan/ Category':
	    return{
			'Tambah' : reverse('golongan-create-save'),
			'Ubah'   : reverse('golongan-edit-save', kwargs={'golongan_id': idpk})
		}[mode]
	elif module == 'Jabatan/ Occupation':
	    return{
			'Tambah' : reverse('jabatan-create-save'),
			'Ubah'   : reverse('jabatan-edit-save', kwargs={'jabatan_id': idpk})
		}[mode]
	elif module == 'Bank':
	    return{
			'Tambah' : reverse('bank-create-save'),
			'Ubah'   : reverse('bank-edit-save', kwargs={'bank_id': idpk})
		}[mode]
	elif module == 'Agama/ Religion':
	    return{
			'Tambah' : reverse('agama-create-save'),
			'Ubah'   : reverse('agama-edit-save', kwargs={'agama_id': idpk})
		}[mode]
	elif module == 'Warga Negara/ Nationality':
	    return{
			'Tambah' : reverse('warganegara-create-save'),
			'Ubah'   : reverse('warganegara-edit-save', kwargs={'warganegara_id': idpk})
		}[mode]
	elif module == 'Status Menikah/ Marital Status':
	    return{
			'Tambah' : reverse('statusmenikah-create-save'),
			'Ubah'   : reverse('statusmenikah-edit-save', kwargs={'statusmenikah_id': idpk})
		}[mode]
	elif module == 'Lokasi Perusahaan':
	    return{
			'Tambah' : reverse('profile-perusahaan-create-save'),
			'Ubah'   : reverse('profile-perusahaan-edit-save', kwargs={'lokasiperusahaan_id': idpk})
		}[mode]
	elif module == 'Profile Perusahaan':
	    return{
			'Ubah'   : reverse('profile-edit-save')
		}[mode]
	elif module == 'Hari Raya':
	    return{
			'Tambah' : reverse('hariraya-create-save'),
			'Ubah'   : reverse('hariraya-edit-save', kwargs={'hariraya_id': idpk})
		}[mode]
	elif module == 'Inventory':
	    return{
			'Tambah' : reverse('inventory-create-save'),
			'Ubah'   : reverse('inventory-edit-save', kwargs={'inventory_id': idpk})
		}[mode]
	elif module == 'Pengaturan Aplikasi':
	    return{
			'Tambah' : reverse('konfigurasi-create-save'),
			'Ubah'   : reverse('konfigurasi-edit-save', kwargs={'konfigurasi_id': idpk})
		}[mode]
	elif module == 'Inventory Pinjaman':
	    return{
			'Tambah' : reverse('pinjaman-create-save'),
			'Ubah'   : reverse('pinjaman-edit-save', kwargs={'pinjaman_id': idpk})
		}[mode]
	return "null"