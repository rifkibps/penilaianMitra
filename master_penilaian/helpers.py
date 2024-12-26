from master_petugas import models as model_petugas
from master_pegawai import models as model_pegawai
from master_petugas.models import AlokasiPetugas
from . import models
from django.db.models import Q

def get_summarize_penilaian(user_id):
    data_pegawai= model_pegawai.MasterPegawaiModel.objects.filter(user=user_id)
        
    jml_kegiatan = 0
    jml_penilaian_aktif = 0
    jml_mitra_belum_dinilai = 0
    jml_mitra_dinilai = 0

    if data_pegawai.exists():
        alokasi_pegawai = AlokasiPetugas.objects.filter(pegawai = data_pegawai.first().id).values('sub_kegiatan', 'role', 'id').distinct()
        jml_kegiatan = alokasi_pegawai.count()
        
        if jml_kegiatan != 0:
            for dt_kegiatan in alokasi_pegawai:
                penilaian_aktif = models.KegiatanPenilaianModel.objects.filter(~Q(status = '0') & Q(kegiatan_survey = dt_kegiatan['sub_kegiatan']))

                if penilaian_aktif.exists():
                    for dt_ in  penilaian_aktif:
                        for role_mitra in dt_.role_permitted.values_list('pk', flat=True).all():
                            alokasi_mitra = AlokasiPetugas.objects.filter(role = role_mitra, sub_kegiatan = dt_.kegiatan_survey.id, pegawai = None)
                            
                            if alokasi_mitra.exists():
                                jml_mitra_belum_dinilai += alokasi_mitra.count()
                                
                                for dt__ in alokasi_mitra:
                                    nilai_mitra = models.MasterPenilaianPetugas.objects.filter(penilai = dt_kegiatan['id'], petugas = dt__.pk)
                                    if nilai_mitra.exists():
                                        jml_mitra_dinilai += 1 

                        if dt_kegiatan['role'] in dt_.role_penilai_permitted.values_list('pk', flat=True).all():
                            jml_penilaian_aktif += 1

    return {
        'jml_kegiatan' : jml_kegiatan,
        'jml_penilaian_aktif' : jml_penilaian_aktif,
        'jml_mitra_belum_dinilai' : jml_mitra_belum_dinilai,
        'jml_mitra_dinilai' : jml_mitra_dinilai,
    }