from django.db import models
from django.contrib.auth.models import User

class JabatanPegawaiModel(models.Model):
    jabatan = models.CharField(max_length=64, null=False, blank=False, verbose_name='Jabatan')

    def __str__(self):
         return f"{self.pk} | {self.jabatan}"

class PangkatPegawaiModel(models.Model):
    golongan = models.CharField(max_length=64, null=False, blank=False, verbose_name='Golongan')
    pangkat = models.CharField(max_length=64, null=False, blank=False, verbose_name='Pangkat')

    def __str__(self):
         return f"{self.pk} | {self.golongan}/{self.pangkat}"


class MasterPegawaiModel(models.Model):

   user = models.OneToOneField(User, on_delete=models.RESTRICT, null=True, blank=True, verbose_name='User Account')
   name = models.CharField(max_length=64, null=False, blank=False, verbose_name='Nama')
   nip = models.CharField(max_length=9, null=False, blank=False, unique=True, verbose_name='NIP')
   nip_bps = models.CharField(max_length=18, null=False, blank=False, unique=True, verbose_name='NIP BPS')
   jabatan = models.ForeignKey(JabatanPegawaiModel, on_delete=models.RESTRICT, null=False, blank=False, verbose_name='Jabatan Pegawai')
   pangkat = models.ForeignKey(PangkatPegawaiModel, on_delete=models.RESTRICT, null=False, blank=False, verbose_name='Pangkat/Golongan Pegawai')
   pendidikan = models.CharField(max_length=64, null=False, blank=False, verbose_name='Pendidikan Terakhir')

   def __str__(self):
         return f"[{self.nip}] {self.name}"
