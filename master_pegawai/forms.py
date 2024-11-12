from django import forms
from . import models

class MasterPegawaiForm(forms.ModelForm):
    
    class Meta:

        model = models.MasterPegawaiModel
        fields = [
            'name', 
            'nip',
            'nip_bps',
            'jabatan',
            'pangkat',
            'pendidikan',
        ]

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'name' : forms.TextInput(attrs = attrs_input),
            'nip' : forms.TextInput(attrs = attrs_input),
            'nip_bps' : forms.TextInput(attrs = attrs_input),
            'jabatan' : forms.Select(attrs = attrs_input | {'class' : 'form-select', 'id' : 'id_jabatan_id'} ),
            'pangkat' : forms.Select(attrs = attrs_input | {'class' : 'form-select', 'id' : 'id_pangkat_id'} ),
            'pendidikan' : forms.TextInput(attrs = attrs_input),
        }


class PosisitionForm(forms.ModelForm):
    
    class Meta:

        model = models.JabatanPegawaiModel
        fields = [
            'jabatan', 
        ]

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'jabatan' : forms.TextInput(attrs = attrs_input),
        }


class PangkatGolonganForm(forms.ModelForm):
    
    class Meta:

        model = models.PangkatPegawaiModel
        fields = [
            'pangkat',
            'golongan', 
        ]

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'pangkat' : forms.TextInput(attrs = attrs_input),
            'golongan' : forms.TextInput(attrs = attrs_input),
        }
