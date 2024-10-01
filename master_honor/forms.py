from django import forms
from . import models


from django.core.exceptions import ValidationError

from django.core.validators import FileExtensionValidator

class HonorForm(forms.ModelForm):

    class Meta:
        model = models.HonorModel

        fields = [
            'nama',
            'tgl_ref_awal',
            'tgl_ref_akhir',
            'honor_maks',
            'status',

        ]

        labels = {
            'nama' : 'Nama Batasan Honor Mitra',
            'tgl_ref_awal' : 'Tanggal Referensi Awal',
            'tgl_ref_akhir' : 'Tanggal Referensi Akhir',
            'honor_maks': 'Nominal Honor Maksimal Mitra',
            'status': 'Status Aktif'
        }

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'nama': forms.TextInput(
                attrs = attrs_input
            ),
            'tgl_ref_awal': forms.DateInput(
                attrs = attrs_input | {'type': 'date'}
            ),
            'tgl_ref_akhir': forms.DateInput(
                attrs = attrs_input | {'type': 'date'}
            ),
            'honor_maks': forms.TextInput(
                attrs = attrs_input
            ),
            'status': forms.Select(
                attrs = attrs_input |  {'class' : 'form-select'}
            )
        }