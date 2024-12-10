from django.db import models
from master_survey.models import SurveyModel, SubKegiatanSurvei
from .validators import int_validators
from master_honor.models import HonorModel
from master_pegawai.models import MasterPegawaiModel
# Create your models here.

class AdministrativeModel(models.Model):
   
   code = models.CharField(max_length=10, null=False, blank=False, unique=True, verbose_name='Kode Wilayah')
   region = models.CharField(max_length=128, null=False, blank=False, verbose_name='Nama Wilayah')
   def __str__(self):
         return f"{self.region} [{self.code}]"

class MasterPetugas(models.Model):

   status_choices = (
      ('0', 'Aktif'), ('1', 'Non Aktif'), ('2', 'Organik'), ('3', 'Blacklist')
   )

   pendidikan = (
      ('0', 'SD/MI Sederajat'), 
      ('1', 'SMP/SLTP Sederajat'),
      ('2', 'SMA/SLTA Sederajat'),
      ('3', 'DI-DIII'),
      ('4', 'DV/S1'),
      ('5', 'S2'),
      ('6', 'S3')
   )


   agama = (
      ('0', 'Islam'), 
      ('1', 'Kristen'),
      ('2', 'Hindu'),
      ('3', 'Budha'),
   )

   jk = (
       ('0', 'Laki-laki'), 
       ('1', 'Perempuan')
   )

   bank = (
      ('1', 'BRI'),
      ('2', 'BNI'),
      ('3', 'BSI'),
      ('4', 'BCA'),
      ('5', 'Mandiri'),
      ('6', 'Bank Sultra'),
   )

   adm_id = models.ForeignKey(AdministrativeModel, on_delete=models.RESTRICT, null=False, blank=False, related_name='region_code', verbose_name='Kode Desa')
   kode_petugas = models.CharField(max_length=12, null=False, blank=False, unique=True, verbose_name='Kode Petugas')
   nama_petugas = models.CharField(max_length=64, null=False, blank=False,  verbose_name='Nama Petugas')
   jk = models.CharField(max_length=1, null=False, blank=False, choices=jk,  verbose_name='Jenis Kelamin')
   nik = models.CharField(max_length=16, null=False, blank=False, validators=[int_validators], unique=True, verbose_name='NIK')
   npwp = models.CharField(max_length=15, null=True, blank=True, validators=[int_validators], unique=True, verbose_name='NPWP')
   tgl_lahir = models.DateField(auto_now=False, auto_now_add=False, null=False, blank=False, verbose_name='Tanggal Lahir')
   pendidikan = models.CharField(max_length=1, choices=pendidikan, null=False, blank=False, verbose_name='Pendidikan Terakhir')
   pekerjaan = models.CharField(max_length=128, null=False, blank=False, verbose_name='Pekerjaan')
   agama = models.CharField(max_length=1, choices=agama, null=False, blank=False, verbose_name='Agama')
   email = models.EmailField(max_length=128, null=False, blank=False,unique=True, verbose_name='Email')
   no_telp = models.CharField(max_length=13, null=True, blank=True, validators=[int_validators], verbose_name='No. Telp (Ex: 6285712345678)')
   alamat = models.CharField(max_length=256, null=False, blank=False, verbose_name='Alamat Domisili')
   status = models.CharField(max_length=1, choices=status_choices, blank=False, verbose_name='Status Mitra')
   
   bank = models.CharField(max_length=1, choices=bank, null=True, blank=True, verbose_name='Jenis Bank')
   rekening = models.CharField(max_length=16, null=True, blank=True, verbose_name='Nomor Rekening')
   pemilik_rek = models.CharField(max_length=64, null=True, blank=True, verbose_name='Pemilik Rekening')

   def __str__(self):
      return f"{self.nama_petugas} [{self.kode_petugas}]"

class RoleMitra(models.Model):
   jabatan = models.CharField(max_length=128, null=False, blank=False, verbose_name='Jabatan/Peran')
   def __str__(self):
         return f"{self.jabatan}"


class AlokasiPetugas(models.Model):
   pegawai = models.ForeignKey(MasterPegawaiModel, null=True, blank=True, on_delete=models.CASCADE, related_name='master_alokasi_pegawai', verbose_name='Pegawai')
   petugas = models.ForeignKey(MasterPetugas, null=True, blank=True, on_delete=models.CASCADE, related_name='master_alokasi_petugas', verbose_name='Kode Petugas')
   role = models.ForeignKey(RoleMitra, on_delete=models.RESTRICT, related_name='master_alokasi_role', verbose_name='Jabatan Petugas')
   sub_kegiatan = models.ForeignKey(SubKegiatanSurvei, null=False, blank=False, on_delete=models.RESTRICT, related_name='subkegiatan_survei', verbose_name='Kegiatan Survei')

   def __str__(self):
      return (f"{self.pk}. [{self.pegawai.nip}] {self.pegawai.name}" if self.pegawai else f"{self.pk}. [{self.petugas.kode_petugas}] {self.petugas.nama_petugas}") + ' | ' +  f'{self.sub_kegiatan.survey.nama}_{self.role.jabatan}'
   

class AlokasiPenugasan(models.Model):

   pengawas = models.ForeignKey(AlokasiPetugas, on_delete=models.CASCADE, related_name='alokasi_penugasan', verbose_name='Pengawas')
   pendata = models.ManyToManyField(AlokasiPetugas)

   def __str__(self):
      return f"{self.pengawas}"
   