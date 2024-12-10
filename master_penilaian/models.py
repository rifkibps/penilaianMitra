from django.db import models
from master_survey.models import SurveyModel
from master_petugas.models import AlokasiPetugas, RoleMitra, SubKegiatanSurvei
from master_pegawai.models import MasterPegawaiModel

class IndikatorPenilaian(models.Model):
   nama_indikator = models.CharField(max_length=128, null=False, blank=False, verbose_name='Indikator Penilaian' )
   deskripsi_penilaian = models.TextField(null=True, blank=True, verbose_name='Deskripsi Penilaian')

   def __str__(self):
      return f"{self.nama_indikator}"

class KegiatanPenilaianModel(models.Model):
   
    status = (
       ('0', 'Tidak Aktif'),
       ('1', 'Berlangsung'),
       ('2', 'Selesai'),
    )

   #  survey = models.ForeignKey(SurveyModel, on_delete=models.RESTRICT, blank=False, null=False, related_name='penilaian_survei') # Harus dihapus ini, diganti ke alokasi
   #  nama_kegiatan = models.CharField(max_length=256, null=False, blank=False, verbose_name='Nama Kegiatan Penilaian' )# Harus dihapus ini, diganti ke alokasiPetugas

    kegiatan_survey = models.ForeignKey(SubKegiatanSurvei, on_delete=models.RESTRICT, blank=False, null=False, related_name='penilaian_survei', verbose_name='Kegiatan Survei')
    tgl_penilaian = models.DateField( null=False, blank=False,  verbose_name='Tanggal Penilaian')
    role_permitted = models.ManyToManyField(RoleMitra, verbose_name='Role Petugas', related_name='role_permitted_petugas')
    role_penilai_permitted = models.ManyToManyField(RoleMitra, verbose_name='Role Penilai', related_name='role_permitted_penilai')
    status = models.CharField(max_length=1, choices=status, default=0, null=False, blank=False, verbose_name='Status Penilaian')
    
    def __str__(self):
        return f"{self.id}. {self.kegiatan_survey.nama_kegiatan}"
   
class IndikatorKegiatanPenilaian(models.Model):
   kegiatan_penilaian = models.ForeignKey(KegiatanPenilaianModel, on_delete=models.CASCADE, related_name='kegiatan_penilaian_petugas')
   indikator_penilaian = models.ForeignKey(IndikatorPenilaian, on_delete=models.RESTRICT, related_name='indikator_penilaian_petugas')

   scale = (
       ('0', 'Ordinal'),
       ('1', 'Numerik'),
   )
   
   scale = models.CharField(max_length=1, choices=scale, default=0, null=False, blank=False, verbose_name='Skala Penilaian')
   n_min = models.IntegerField(null=False, blank=False, default=1, verbose_name='Batas Minimum')
   n_max = models.IntegerField(null=False, blank=False, default=5, verbose_name='Batas Maksimal')
   
   def __str__(self):
      return f"{self.kegiatan_penilaian.kegiatan_survey.nama_kegiatan} [{self.indikator_penilaian}]"

class MasterNilaiPetugas(models.Model):

   penilai = models.ForeignKey(MasterPegawaiModel, on_delete=models.CASCADE,  related_name='penilai')
   petugas = models.ForeignKey(AlokasiPetugas, on_delete=models.CASCADE,  related_name='nilai_petugas')
   penilaian = models.ForeignKey(IndikatorKegiatanPenilaian, on_delete=models.RESTRICT, related_name='indikator_kegiatan_penilaian')
   nilai = models.SmallIntegerField(null=True, blank=True, verbose_name='Nilai Kegiatan Petugas')
   catatan = models.TextField(null=True, blank=True, verbose_name='Catatan Personal')

   def __str__(self):
      return f"{self.petugas.petugas.nama_petugas} [{self.penilaian.kegiatan_penilaian}]"
      
