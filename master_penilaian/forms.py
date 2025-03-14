from django import forms
from . import models
from master_petugas.models import AlokasiPetugas
from django.core.validators import FileExtensionValidator
from master_petugas import utils
import pandas as pd
from pprint import pprint
from io import BytesIO
import numpy as np

from django.db.models import Q

class IndikatorPenilaianForm(forms.ModelForm):
    
    class Meta:

        model = models.IndikatorPenilaian
        fields = [
            'nama_indikator', 
            'deskripsi_penilaian'
        ]

        labels = {
            'nama_indikator' : 'Nama Indikator', 
            'deskripsi_penilaian'  : 'Deskripsi Penilaian'
        }

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'nama_indikator': forms.TextInput(
                attrs = attrs_input
            ),
            'deskripsi_penilaian': forms.Textarea(
                attrs = attrs_input
            )            
        }

class KegiatanPenilaianForm(forms.ModelForm):
    
    class Meta:

        model = models.KegiatanPenilaianModel
        fields = [
            'kegiatan_survey', 
            'tgl_penilaian',
            'status',
            'role_permitted',
            'role_penilai_permitted',
        ]

        labels = {
            'nama_kegiatan' : 'Nama Kegiatan', 
            'survey'  : 'Nama Survei',
            'tgl_penilaian' : 'Tanggal Penilaian',
            'status' : 'Status Penilaian'
        }

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'kegiatan_survey': forms.Select(
                attrs = attrs_input | {'class' : 'form-select'}
            ),
            'tgl_penilaian': forms.DateInput(
                attrs = attrs_input  | {'type' : 'date'}
            ),
            'role_permitted': forms.SelectMultiple(
                 attrs = attrs_input | {'size' : '10', 'style' : "height: 100%;"}
            ),
             'role_penilai_permitted': forms.SelectMultiple(
                 attrs = attrs_input | {'size' : '10', 'style' : "height: 100%;"}
            ),
                  'status': forms.Select(
                attrs = attrs_input | {'class' : 'form-select'}
            ),
        }


class IndikatorKegiatanPenilaianForm(forms.ModelForm):
    
    class Meta:

        model = models.IndikatorKegiatanPenilaian
        fields = [
            'kegiatan_penilaian', 
            'indikator_penilaian',
            'scale',
            'n_min',
            'n_max'
        ]

        labels = {
            'kegiatan_penilaian' : 'Kegiatan Penilaian', 
            'indikator_penilaian'  : 'Indikator Penilaian',
        }

        attrs_input = {
            'class' : 'form-control form-control-sm',
            'placeholder': '...'
        }

        widgets = {
            'kegiatan_penilaian': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id' : 'id_kegiatan_penilaian_id'}
            ),
            'indikator_penilaian': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id' : 'id_indikator_penilaian_id'}
            ),
            'scale': forms.Select(
                attrs = attrs_input | {'class' : 'form-select'}
            ),
            'n_min': forms.NumberInput(
                attrs = attrs_input
            ),
            'n_max': forms.NumberInput(
                attrs = attrs_input
            ),
        }


class PenilaianMitraForm(forms.Form):

    def clean(self):
        df = []
        base_errors = []
        for key, value in self.data.items():
            if 'nilai_indikator_' in key:
                indikator_penilaian = key.replace('nilai_indikator_', '')
                indikator_penilaian_model = models.IndikatorKegiatanPenilaian.objects.filter(pk = indikator_penilaian)
                if indikator_penilaian_model.exists():
                    n_min = indikator_penilaian_model.first().n_min
                    n_max = indikator_penilaian_model.first().n_max

                    if value.isnumeric() == False or len(value) == 0:
                        base_errors.append('Nilai petugas tidak boleh kosong.') # Sesuaikan sama threshold nilainya yaaaaaaa
                    else:
                        nilai = int(value)
                        if nilai > n_max or nilai < n_min:
                            base_errors.append(f'Nilai petugas harus berkisar [{n_min} - {n_max}]') # Sesuaikan sama threshold nilainya yaaaaaaa

                    df.append({
                        'petugas' : self.data['field_mitra'], #ID ALOKASI
                        'penilai' : self.data['field_id_penilai'], #ID ALOKASI
                        'penilaian' : indikator_penilaian,
                        'nilai': value
                    })
                else:
                    base_errors.append('Terdapat indikator penilaian yang tidak relevan.')
                    continue

            if 'catatan_indikator_' in key:
                check_exist = [index for (index, d) in enumerate(df) if d["penilaian"] == key.replace('catatan_indikator_', '')]
                if len(check_exist) > 0:
                    df[check_exist[0]]['catatan'] = value

        if len(base_errors) > 0:
            self._errors['nilai_petugas'] = self.error_class(base_errors)
            return self._errors['nilai_petugas'] 
        
        self.cleaned_data = df
        return self.cleaned_data    


class NilaiFormUpload(forms.Form):
    import_penilaian = forms.FileField(allow_empty_file=False, validators=[FileExtensionValidator(allowed_extensions=['xlsx'])], label="Import Alokasi Petugas", widget=forms.FileInput(
                              attrs={'class': "form-control"}))
    
    def clean(self):
        try:
            data = self.cleaned_data.get('import_file').read()
            df = pd.read_excel(BytesIO(data), skiprows=1, dtype='str')
        except:
            self._errors['import_file'] = self.error_class(['Format template tidak sesuai. Silahkan gunakan template yang telah disediakan.'])
            return self._errors['import_file']
        
        df.dropna(axis=0, how='all', inplace=True)
        base_errors = []

       ### PENGECEKAN FORMAT TEMPLATE ###
        headers = ['No', 'ID Alokasi Mitra', 'ID Kegiatan Penilaian', 'ID Penilai', 'Kode Petugas', 'Nama Petugas', 'Survei', 'Jabatan', 'Kegiatan Penilaian', 'Nama Penilai (Organik)']  
        for header in headers:
            if header not in df.columns:
                self._errors['import_file'] = self.error_class(['Format template tidak sesuai. Silahkan gunakan template yang telah disediakan.'])
                return self._errors['import_file']
        
        ### VALIDASI NULL UNTUK COMMOM HEADER
        df_id = df[['ID Alokasi Mitra', 'ID Kegiatan Penilaian', 'ID Penilai']]
        df_null = df_id[df_id.isna().any(axis=1)]
        for idx, i in df_null.iterrows():
            self._errors['import_file'] = self.error_class([f'Nilai kosong pada <b>Baris {idx+1}</b> ditemukan. Periksa kolom <b>ID Alokasi Mitra (Kol. B)</b> atau <b>ID Kegiatan Penilaian (Kol. C)</b>'])
            return self._errors['import_file']
        
        # CHECK HANYA ADA SATU KEGIATAN PENILAIAN DALAM FILE UPLOAD
        df_kegiatan_ = df['ID Kegiatan Penilaian'].unique()
        if len(df_kegiatan_) > 1 :
            self._errors['import_file'] = self.error_class([f'Satu file upload hanya digunakan untuk satu jenis kegiatan penilaian penilaian. Periksa kolom <b>ID Kegiatan Penilaian (Kol.C) </b>'])
            return self._errors['import_file']

        # CHECK HANYA ADA SATU Penilai DALAM FILE UPLOAD
        df_kegiatan_ = df['ID Penilai'].unique()
        if len(df_kegiatan_) > 1 :
            self._errors['import_file'] = self.error_class([f'Satu file upload hanya digunakan untuk satu orang penilai. Periksa kolom <b>ID Penilai (Kol.D) </b>'])
            return self._errors['import_file']

        for idx, dt in df['ID Kegiatan Penilaian'].items():
            check_db = models.KegiatanPenilaianModel.objects.filter(pk = dt)
            if not check_db.exists():
                self._errors['import_file'] = self.error_class([f'Kegiatan penilaian [{dt}] tidak tersedia pada database. Periksa kolom <b>ID Kegiatan Penilaian [KOLOM C] Baris {idx+1}</b>.'])
                return self._errors['import_file']
            
        for idx, dt in df['ID Penilai'].items():
            check_db = AlokasiPetugas.objects.filter(pk = dt)
            if not check_db.exists():
                self._errors['import_file'] = self.error_class([f'Penilai [{dt}] tidak tersedia pada database. Periksa kolom <b>ID Penilai [KOLOM D] Baris {idx+1}</b>.'])
                return self._errors['import_file']

        kegiatan_penilaian = models.KegiatanPenilaianModel.objects.filter(pk = df['ID Kegiatan Penilaian'][0]).first()
        role_permitted = list(kegiatan_penilaian.role_permitted.values_list('id', flat=True))

        check_indikator = list(models.IndikatorKegiatanPenilaian.objects.filter(kegiatan_penilaian = kegiatan_penilaian.id).values_list('indikator_penilaian__nama_indikator', flat=True))
        data_indikator = check_indikator
        check_catatan_personal = [f'Catatan Personal {indikator}' for indikator in check_indikator]
        check_indikator = [f'Penilaian Indikator {indikator}' for indikator in check_indikator]
    
        for check in check_indikator:
            if check not in df.columns:
                self._errors['import_file'] = self.error_class([f'Format template tidak sesuai (Indikator Penilaian [{check}] tidak match / tidak tersedia pada file upload). Silahkan gunakan template yang telah disediakan.'])
                return self._errors['import_file']
            
        for check in check_catatan_personal:
            if check not in df.columns:
                self._errors['import_file'] = self.error_class([f'Format template tidak sesuai (Catatan Personal [{check}] tidak match / tidak tersedia pada file upload). Silahkan gunakan template yang telah disediakan.'])
                return self._errors['import_file']

        df.drop(columns=df.columns[0], axis=1, inplace=True)
        
        ### PENGECEKAN ISIAN ###
        df_null = df[df.isna().any(axis=1)]
        for idx, i in df_null.iterrows():
            null_cols = []
            for e in i[i.isna()].index:
                if 'Catatan Personal' not in e:
                    null_cols.append(str(e).capitalize())

            if len(null_cols) > 0:
                base_errors.append(f'Nilai kosong pada <b>Baris {idx+1}</b> ditemukan. Periksa kolom <b>({", ".join(null_cols)})</b>')
        
        for idx, dt in df.iterrows():
            id_penilai = dt['ID Penilai']
            nama_penilai = dt['Nama Penilai (Organik)']
            db_check = AlokasiPetugas.objects.filter(
                pk = id_penilai,
                pegawai__name = nama_penilai,
            )
            if not db_check.exists():
                base_errors.append(f'Data penilai: <b>{nama_penilai}</b> tidak sesuai dengan ID Penilai. Harap periksa baris <b>{idx+1}</b>')

        # Cek ID Alokasi Mitra dengan data file upload sesuai atau tidak
        for idx, dt in df.iterrows():
            id_alokasi = dt['ID Alokasi Mitra']
            kode_petugas = dt['Kode Petugas']
            nama_petugas = dt['Nama Petugas']
            jabatan = dt['Jabatan']

            db_check = AlokasiPetugas.objects.filter(
                petugas__kode_petugas = kode_petugas,
                petugas__nama_petugas = nama_petugas,
                role__jabatan = jabatan,
                sub_kegiatan = kegiatan_penilaian.kegiatan_survey.pk,
            )
            
            if not db_check.exists():
                base_errors.append(f'Data alokasi petugas: <b>[{kode_petugas}] {nama_petugas} - {kegiatan_penilaian.kegiatan_survey.nama_kegiatan} - {jabatan}</b> tidak tersedia pada Database. Harap periksa baris <b>{idx+1}</b>')
                continue
            else:
                db_check_data = db_check.first()
                if db_check_data.role.id not in role_permitted:
                    base_errors.append(f'Role petugas <b>[{kode_petugas}] {nama_petugas} - {jabatan}</b> tidak sesuai dengan <b>role permitted</b> untuk kegiatan penilaian {kegiatan_penilaian.kegiatan_survey.nama_kegiatan} <b>(Role yang diizinkan hanya {", ".join(role_permitted)})</b>. Harap periksa baris <b>{idx+1}</b>')
                    continue
            
            if str(db_check.first().id) != str(id_alokasi) :
                base_errors.append(f'Data alokasi petugas: <b>[{kode_petugas}] {nama_petugas} - {kegiatan_penilaian.kegiatan_survey.nama_kegiatan} - {jabatan}</b> tidak sesuai dengan ID Alokasi Petugas. Harap periksa baris <b>{idx+1}</b>')
            

        # Cek ID Kegiatan Penilaian Mitra dengan data file upload sesuai atau tidak
        for idx, dt in df.iterrows():
            id_alokasi = dt['ID Kegiatan Penilaian']
            dt_kegiatan = dt['Kegiatan Penilaian']

            db_check = models.KegiatanPenilaianModel.objects.filter(
                            pk = id_alokasi,
                            kegiatan_survey__nama_kegiatan = dt_kegiatan
                        )
            if db_check.exists() == False :
                base_errors.append(f'Data Kegiatan Penilaian: <b>[{dt_kegiatan}]</b> tidak tersedia pada Database. Harap periksa baris <b>{idx+1}</b>')
                continue
        
        # Cek duplikasi Data pada master file
        df_data_mitra = df[headers[2:]]
        duplicated_petugas = df_data_mitra[df_data_mitra.duplicated()]['Nama Petugas']
        for idx, row in duplicated_petugas.items():
            base_errors.append(f'Duplikasi data petugas: <b>{row}</b> dengan beban tugas yang sama ditemukan. Harap periksa baris <b>{idx+1}</b>')
        
        pprint(base_errors)
        if len(base_errors) > 0:
            self._errors['import_file'] = self.error_class(base_errors)
            return self._errors['import_file'] 
        
        for idx, data in df[check_indikator].iterrows():
            for idx2, row in data.items():
                if not row.isnumeric():
                    base_errors.append(f'Indikator penilaian <b>{idx2}</b> untuk petugas <b> [{df["Kode Petugas"][idx]}] {df["Nama Petugas"][idx]} </b> hanya dapat diisikan digit numerik. Harap periksa baris <b>{idx+1} kolom {idx2}</b>')
                else:
                    check_requirement = models.IndikatorKegiatanPenilaian.objects.filter(kegiatan_penilaian = kegiatan_penilaian.pk, indikator_penilaian__nama_indikator = idx2.replace("Penilaian Indikator ", "")).first()
                    n_max = check_requirement.n_max
                    n_min = check_requirement.n_min
                    if (int(row) > n_max) or (int(row) < n_min):
                        base_errors.append(f'Indikator penilaian <b>{idx2}</b> untuk petugas <b> [{df["Kode Petugas"][idx]}] {df["Nama Petugas"][idx]} </b> hanya dapat diisikan <b>nilai {n_min}-{n_max}</b>. Harap periksa baris <b>{idx+1} kolom {idx2}</b>')

        if len(base_errors) > 0:
            self._errors['import_file'] = self.error_class(base_errors)
            return self._errors['import_file'] 

        # FORMATING DICTIONARY
        id_indikator = []
        for col_new, col_old in zip(data_indikator, check_indikator):
            db_query = models.IndikatorPenilaian.objects.filter(nama_indikator = col_new ).first()
            id_indikator.append(db_query.id)
            df.rename(columns = {col_old:db_query.id}, inplace = True)
            df.rename(columns = {f"Catatan Personal {col_new}": f"catatan_{db_query.id}"}, inplace = True)

        df_dict = []
        for idx, data in df.iterrows():
            for id in id_indikator:
                row_db =  {}
                penilaian = models.IndikatorKegiatanPenilaian.objects.filter(kegiatan_penilaian = kegiatan_penilaian.id, indikator_penilaian = id).first()
                petugas = AlokasiPetugas.objects
                row_db['petugas'] = petugas.filter(pk = data['ID Alokasi Mitra']).first()
                row_db['penilai'] = petugas.filter(pk = data['ID Penilai']).first()
                row_db['penilaian'] = penilaian
                row_db['nilai'] = data[id]

                if not type(data[f'catatan_{id}']) is str:
                    row_db['catatan'] = ''
                else:
                    row_db['catatan'] = data[f'catatan_{id}']
                df_dict.append(row_db)

        pprint(df_dict)
        self.cleaned_data = df_dict
        return self.cleaned_data
    