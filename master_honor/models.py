from django.db import models
from munapps.helpers import currency_formatting as cf

# Create your models here.
class HonorModel(models.Model):
   
   status = (
       ('0', 'Aktif'),
       ('1', 'Non Aktif')
   )
   
   nama = models.CharField(max_length=128, null=False, blank=False, verbose_name='Nama' )
   tgl_ref_awal = models.DateField( null=False, blank=False, verbose_name='Tanggal Referensi Awal')
   tgl_ref_akhir = models.DateField( null=False, blank=False, verbose_name='Tanggal Referensi Akhir')
   honor_maks = models.FloatField(null=False, blank=False, verbose_name='Nominal Batasan Honor Mitra')
   status = models.CharField(max_length=1, choices=status, default=0, null=False, blank=False, verbose_name='Status Aktif')

   def __str__(self):
      return f"{self.nama} | Rp{cf(self.honor_maks, True)} [{self.tgl_ref_awal.strftime('%d-%m-%Y')} s.d. { self.tgl_ref_akhir.strftime('%d-%m-%Y')}]"