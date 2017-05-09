from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.loginpage,  name="loginpage"),
    url(r'^loginrequest$', views.loginrequest, name='loginrequest'),
    url(r'^logout$', views.logout_view,  name="logout"),

    url(r'^perusahaan$', views.dashboard.perusahaan_index,  name="perusahaan-index"),
    url(r'^departemen$', views.dashboard.departemen_index,  name="departemen-index"),
    #url(r'^unit$', views.dashboard.unit_index, name="unit-index"),
  	url(r'^bagian$', views.dashboard.bagian_index, name="bagian-index"),
  	url(r'^golongan$', views.dashboard.golongan_index, name="golongan-index"),
  	url(r'^jabatan$', views.dashboard.jabatan_index, name="jabatan-index"),
  	url(r'^bank$', views.dashboard.bank_index, name="bank-index"),
  	url(r'^agama$', views.dashboard.agama_index, name="agama-index"),
  	url(r'^warganegara$', views.dashboard.warganegara_index, name="warganegara-index"),
  	url(r'^statusmenikah$', views.dashboard.statusmenikah_index, name="statusmenikah-index"),
    url(r'^profile-perusahaan$', views.dashboard.profile_perusahaan_index, name="profile-perusahaan-index"),
    url(r'^karaywan$', views.dashboard.karyawan_index, name="karyawan-index"),
    url(r'^karaywan/(?P<karyawan_id>[0-9]+)/detail/$', views.dashboard.karyawan_detail, name="karyawan-detail"),
    url(r'^karyawan-shift$', views.dashboard.karyawan_shift_index, name="karyawan-shift-index"),
    url(r'^shift$', views.dashboard.shift_index, name="shift-index"),
    url(r'^hariraya$', views.dashboard.hariraya_index, name="hariraya-index"),
    url(r'^absensi$', views.dashboard.absensi_index, name="absensi-index"),
    url(r'^inventory$', views.dashboard.inventory_index, name="inventory-index"),
    url(r'^konfigurasi$', views.dashboard.konfigurasi_index, name="konfigurasi-index"),
  	#url(r'^notif-system$', views.dashboard.notif_system, name="notif-system-index"),
  	#url(r'^notif-login$', views.dashboard.notif_login, name="notif-login-index"),
  	#url(r'^notif-aplikasi$', views.dashboard.notif_aplikasi, name="notif-aplikasi-index"),
  	#url(r'^notif-karyawan$', views.dashboard.notif_karyawan, name="notif-karyawans-index"),
  	#url(r'^notif-system$', views.dashboard.notif_system, name="notif-system-index"),

  	#url(r'^perusahaan$', views.dashboard.perusahaan_index,  name="perusahaan-index"),

    #==create

    url(r'^departemen/create$', views.create.departemen,  name="departemen-create"),
    url(r'^departemen/create/save$', views.create.departemen_save,  name="departemen-create-save"),
    url(r'^bagian/create$', views.create.bagian,  name="bagian-create"),
    url(r'^bagian/create/save$', views.create.bagian_save,  name="bagian-create-save"),
  	url(r'^golongan/create$', views.create.golongan, name="golongan-create"),
  	url(r'^golongan/create/save$', views.create.golongan_save, name="golongan-create-save"),
  	url(r'^jabatan/create$', views.create.jabatan, name="jabatan-create"),
  	url(r'^jabatan/create/save$', views.create.jabatan_save, name="jabatan-create-save"),
  	url(r'^bank/create$', views.create.bank, name="bank-create"),
  	url(r'^bank/create/save$', views.create.bank_save, name="bank-create-save"),
    url(r'^karyawan-shift/save$', views.create.karyawan_shift_save, name="karyawan-shift-create-save"),
    url(r'^shift/create$', views.create.shift, name="shift-create"),
    url(r'^shift/create/save$', views.create.shift_save, name="shift-create-save"),
    url(r'^hariraya/create$', views.create.hariraya, name="hariraya-create"),
    url(r'^hariraya/create/save$', views.create.hariraya_save, name="hariraya-create-save"),

  	url(r'^agama/create$', views.create.agama, name="agama-create"),
  	url(r'^agama/create/save$', views.create.agama_save, name="agama-create-save"),
  	url(r'^warganegara/create$', views.create.warganegara, name="warganegara-create"),
  	url(r'^warganegara/create/save$', views.create.warganegara_save, name="warganegara-create-save"),
    url(r'^statusmenikah/create$', views.create.statusmenikah, name="statusmenikah-create"),
    url(r'^statusmenikah/create/save$', views.create.statusmenikah_save, name="statusmenikah-create-save"),
    url(r'^profile-perusahaan/create$', views.create.profile_perusahaan, name="profile-perusahaan-create"),
    url(r'^profile-perusahaan/create/save$', views.create.profile_perusahaan_save, name="profile-perusahaan-create-save"),
    url(r'^karyawan/create$', views.create.karyawan, name="karyawan-create"),
    url(r'^karyawan/create/save$', views.create.karyawan_save, name="karyawan-create-save"),
    url(r'^inventory/create$', views.create.inventory, name="inventory-create"),
    url(r'^inventory/create/save$', views.create.inventory_save, name="inventory-create-save"),
    url(r'^konfigurasi/create$', views.create.konfigurasi, name="konfigurasi-create"),
    url(r'^konfigurasi/create/save$', views.create.konfigurasi_save, name="konfigurasi-create-save"),

    #==eof-create
    #==edit

  	url(r'^departemen/(?P<departemen_id>[0-9]+)/edit/$', views.edit.departemen, name="departemen-edit"),
  	url(r'^departemen/(?P<departemen_id>[0-9]+)/edit/save$', views.edit.departemen_save, name="departemen-edit-save"),
  	url(r'^bagian/(?P<bagian_id>[0-9]+)/edit/$', views.edit.bagian, name="bagian-edit"),
  	url(r'^bagian/(?P<bagian_id>[0-9]+)/edit/save$', views.edit.bagian_save, name="bagian-edit-save"),
  	url(r'^golongan/(?P<golongan_id>[0-9]+)/edit/$', views.edit.golongan, name="golongan-edit"),
  	url(r'^golongan/(?P<golongan_id>[0-9]+)/edit/save$', views.edit.golongan_save, name="golongan-edit-save"),
  	url(r'^jabatan/(?P<jabatan_id>[0-9]+)/edit/$', views.edit.jabatan, name="jabatan-edit"),
  	url(r'^jabatan/(?P<jabatan_id>[0-9]+)/edit/save$', views.edit.jabatan_save, name="jabatan-edit-save"),
  	url(r'^bank/(?P<bank_id>[0-9]+)/edit/$', views.edit.bank, name="bank-edit"),
  	url(r'^bank/(?P<bank_id>[0-9]+)/edit/save$', views.edit.bank_save, name="bank-edit-save"),

  	url(r'^agama/(?P<agama_id>[0-9]+)/edit/$', views.edit.agama, name="agama-edit"),
  	url(r'^agama/(?P<agama_id>[0-9]+)/edit/save$', views.edit.agama_save, name="agama-edit-save"),
  	url(r'^warganegara/(?P<warganegara_id>[0-9]+)/edit/$', views.edit.warganegara, name="warganegara-edit"),
  	url(r'^warganegara/(?P<warganegara_id>[0-9]+)/edit/save$', views.edit.warganegara_save, name="warganegara-edit-save"),
    url(r'^statusmenikah/(?P<statusmenikah_id>[0-9]+)/edit/$', views.edit.statusmenikah, name="statusmenikah-edit"),
    url(r'^statusmenikah/(?P<statusmenikah_id>[0-9]+)/edit/save$', views.edit.statusmenikah_save, name="statusmenikah-edit-save"),
    url(r'^profile-perusahaan/(?P<lokasiperusahaan_id>[0-9]+)/edit/$', views.edit.profile_perusahaan, name="profile-perusahaan-edit"),
    url(r'^profile-perusahaan/(?P<lokasiperusahaan_id>[0-9]+)/edit/save$', views.edit.profile_perusahaan_save, name="profile-perusahaan-edit-save"),
    url(r'^profile-perusahaan/profile-edit/$', views.edit.profile_edit, name="profile-edit"),
    url(r'^profile-perusahaan/profile-edit/edit/save$', views.edit.profile_edit_save, name="profile-edit-save"),
    url(r'^shift/(?P<shift_id>[0-9]+)/edit/$', views.edit.shift, name="shift-edit"),
    url(r'^shift/(?P<shift_id>[0-9]+)/edit/save$', views.edit.shift_save, name="shift-edit-save"),

    url(r'^hariraya/(?P<hariraya_id>[0-9]+)/edit/$', views.edit.hariraya, name="hariraya-edit"),
    url(r'^hariraya/(?P<hariraya_id>[0-9]+)/edit/save$', views.edit.hariraya_save, name="hariraya-edit-save"),
    url(r'^inventory/(?P<inventory_id>[0-9]+)/edit/$', views.edit.inventory, name="inventory-edit"),
    url(r'^inventory/(?P<inventory_id>[0-9]+)/edit/save$', views.edit.inventory_save, name="inventory-edit-save"),
    url(r'^konfigurasi/(?P<konfigurasi_id>[0-9]+)/edit/$', views.edit.konfigurasi, name="konfigurasi-edit"),
    url(r'^konfigurasi/(?P<konfigurasi_id>[0-9]+)/edit/save$', views.edit.konfigurasi_save, name="konfigurasi-edit-save"),

    #==eofedit

    url(r'^perusahaan/(?P<perusahaan_id>[0-9]+)/delete/$', views.perusahaan_delete, name="perusahaan-delete"),
    url(r'^departemen/(?P<departemen_id>[0-9]+)/delete/$', views.delete.departemen, name="departemen-delete"),
    url(r'^bagian/(?P<bagian_id>[0-9]+)/delete/$', views.delete.bagian, name="bagian-delete"),
    url(r'^golongan/(?P<golongan_id>[0-9]+)/delete/$', views.delete.golongan, name="golongan-delete"),
    url(r'^jabatan/(?P<jabatan_id>[0-9]+)/delete/$', views.delete.jabatan, name="jabatan-delete"),
    url(r'^bank/(?P<bank_id>[0-9]+)/delete/$', views.delete.bank, name="bank-delete"),
    url(r'^agama/(?P<agama_id>[0-9]+)/delete/$', views.delete.agama, name="agama-delete"),
    url(r'^warganegara/(?P<warganegara_id>[0-9]+)/delete/$', views.delete.warganegara, name="warganegara-delete"),
    url(r'^statusmenikah/(?P<statusmenikah_id>[0-9]+)/delete/$', views.delete.statusmenikah, name="statusmenikah-delete"),
    url(r'^profile-perusahaan/(?P<lokasiperusahaan_id>[0-9]+)/delete/$', views.delete.profile_perusahaan, name="profile-perusahaan-delete"),
    url(r'^shift/(?P<shift_id>[0-9]+)/delete/$', views.delete.shift, name="shift-delete"),

    url(r'^hariraya/(?P<hariraya_id>[0-9]+)/delete/$', views.delete.hariraya, name="hariraya-delete"),
    url(r'^inventory/(?P<inventory_id>[0-9]+)/delete/$', views.delete.inventory, name="inventory-delete"),

    url(r'^api/karyawan$', views.dashboard.api_karyawan, name="karyawan-api"),
    url(r'^karyawan-shift/edit/save$', views.edit.karyawan_shift, name="karyawan-shift-simpan-api"),

]