import json
from django.core.serializers.json import DjangoJSONEncoder

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from . import models, forms
from master_petugas.models import AlokasiPetugas
import numpy as np
from openpyxl import Workbook
from django.contrib.auth.models import User
from pprint import pprint

# Create your views here.

class MasterPegawaiJsonResponseClassView(LoginRequiredMixin, View):

    def post(self, request):
        data = self._datatables(request)
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
		
    def _datatables(self, request):
        datatables = request.POST

        # Get Draw
        draw = int(datatables.get('draw'))
        start = int(datatables.get('start'))
        length = int(datatables.get('length'))
        page_number = int(start / length + 1)

        search = datatables.get('search[value]')

        order_idx = int(datatables.get('order[0][column]')) # Default 1st index for
        order_dir = datatables.get('order[0][dir]') # Descending or Ascending
        order_col = 'columns[' + str(order_idx) + '][data]'
        order_col_name = datatables.get(order_col)

        if (order_dir == "desc"):
            order_col_name =  str('-' + order_col_name)

        data = models.MasterPegawaiModel.objects

        if datatables.get('jabatan_filter'):
            data = data.filter(jabatan = datatables.get('jabatan_filter'))
        if datatables.get('pangkat_filter'):
            data = data.filter(pangkat = datatables.get('pangkat_filter'))
        
        if search:
            data = data.filter(
                Q(user__first_name__icontains=search)|
                Q(user__last_name__icontains=search)|
                Q(nip__icontains=search)|
                Q(nip_bps__icontains=search)|
                Q(jabatan__jabatan__icontains=search)|
                Q(pangkat__golongan__icontains=search)|
                Q(pangkat__pangkat__icontains=search)|
                Q(pendidikan__icontains=search)
            )

        data = data.exclude(Q(nip=None)|Q(nip_bps=None)|Q(jabatan=None)|Q(pangkat=None)|Q(pendidikan=None))
        records_total = data.count()
        records_filtered = records_total
        
        data = data.order_by(order_col_name)
        paginator = Paginator(data, length)

        try:
            object_list = paginator.page(page_number).object_list
        except PageNotAnInteger:
            object_list = paginator.page(1).object_list
        except EmptyPage:
            object_list = paginator.page(1).object_list

        data = []

        for obj in object_list:
            data.append({
                        'nip': f'{obj.nip}',
                        'nip_bps': obj.nip_bps,
                        'name': obj.name,
                        'jabatan__jabatan': obj.jabatan.jabatan,
                        'pangkat__golongan': f'{obj.pangkat.golongan}/ {obj.pangkat.pangkat}',
                        'pendidikan': obj.pendidikan,
                        'user': '<span class="badge badge-primary-lighten font-12"> Created </span>' if obj.user else '-',
                        'aksi': f'<a href="javascript:void(0);" onclick="editPegawai({obj.id})" class="action-icon"><i class="mdi mdi-square-edit-outline font-15"></i></a> <a href="javascript:void(0);" onclick="hapusPegawai({obj.id});" class="action-icon"> <i class="mdi mdi-delete font-15"></i></a>'
                })
            
        return {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }


class MasterPegawaiClassView(LoginRequiredMixin, View):

    def get(self, request):
        context = {
            'title' : 'Master Pegawai',
            'jabatan' : models.JabatanPegawaiModel.objects.values(),
            'pangkat' : models.PangkatPegawaiModel.objects.values(),
            'form' : forms.MasterPegawaiForm
        }
        return render(request, 'master_pegawai/index.html', context)

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            form = forms.MasterPegawaiForm(request.POST)
            if form.is_valid():
                instance = form.save()
                return JsonResponse({'message': 'Data berhasil ditambahkan'}, status=200)
            else:
                pprint(form.errors)
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": ""}, status=400)
    

class MasterPegawaiDetailClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                id = request.POST.get('id')
                data = models.MasterPegawaiModel.objects.filter(pk=id)
                pprint(data)
                if data.exists():
                    return JsonResponse({'status' : 'success', 'instance': list(data.values())[0]}, status=200)
                else:
                    return JsonResponse({'status': 'failed', 'message': 'Data tidak tersedia'}, status=200)
                
        return JsonResponse({'status': 'Invalid request'}, status=400)
    

class MasterPegawaiUpdateClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            
            data = get_object_or_404(models.MasterPegawaiModel, pk=request.POST.get('id'))

            form = forms.MasterPegawaiForm(request.POST, instance=data)

            if form.is_valid():
                instance = form.save()
                ser_instance = serializers.serialize('json', [ instance, ])
                
                # send to client side.
                return JsonResponse({"instance": ser_instance, 'message': 'Data berhasil diubah'}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": ""}, status=400)

class MasterPegawaiDeleteClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                data = models.MasterPegawaiModel.objects.filter(pk = request.POST.get('id'))
                if data.exists():
                    safe_check = AlokasiPetugas.objects.filter(pegawai = data.first().pk)
                    if safe_check.exists():
                        return JsonResponse({'status': 'failed', 'message': 'Data pegawai saat ini telah terdaftar pada alokasi kegiatan'}, status=200)

                    # data.delete()
                    return JsonResponse({'status' : 'success', 'message': 'Data berhasil dihapus'}, status=200)
                else:
                    return JsonResponse({'status': 'failed', 'message': 'Data tidak tersedia'}, status=200)
                
        return JsonResponse({'status': 'Invalid request'}, status=400)


class PositionsClassView(LoginRequiredMixin, View):

    def get(self, request):
        context = {
            'title' : 'Master Jabatan',
            'form' : forms.PosisitionForm
        }
        return render(request, 'master_pegawai/position.html', context)

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            form = forms.PosisitionForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Data berhasil ditambahkan'}, status=200)
            else:
                pprint(form.errors)
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": ""}, status=400)

class MasterPositionJsonResponseClassView(LoginRequiredMixin, View):

    def post(self, request):
        data = self._datatables(request)
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
		
    def _datatables(self, request):
        datatables = request.POST

        # Get Draw
        draw = int(datatables.get('draw'))
        start = int(datatables.get('start'))
        length = int(datatables.get('length'))
        page_number = int(start / length + 1)

        search = datatables.get('search[value]')

        order_idx = int(datatables.get('order[0][column]')) # Default 1st index for
        order_dir = datatables.get('order[0][dir]') # Descending or Ascending
        order_col = 'columns[' + str(order_idx) + '][data]'
        order_col_name = datatables.get(order_col)

        if (order_dir == "desc"):
            order_col_name =  str('-' + order_col_name)

        data = models.JabatanPegawaiModel.objects
        if search:
            data = data.filter(
                Q(jabatan__icontains=search)
            )

        data = data.exclude(Q(jabatan=None))
        records_total = data.count()
        records_filtered = records_total
        
        data = data.order_by(order_col_name)
        # Conf Paginator
        paginator = Paginator(data, length)

        try:
            object_list = paginator.page(page_number).object_list
        except PageNotAnInteger:
            object_list = paginator.page(1).object_list
        except EmptyPage:
            object_list = paginator.page(1).object_list

        data = []

        for obj in object_list:
            data.append({
                        'jabatan': f'{obj.jabatan}',
                        'aksi': f'<a href="javascript:void(0);" onclick="editJabatan({obj.id})" class="action-icon"><i class="mdi mdi-square-edit-outline font-15"></i></a> <a href="javascript:void(0);" onclick="hapusJabatan({obj.id});" class="action-icon"> <i class="mdi mdi-delete font-15"></i></a>'
                })
        return {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }


class MasterPositionDetailClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                id = request.POST.get('id')
                data = models.JabatanPegawaiModel.objects.filter(pk=id)
                if data.exists():
                    return JsonResponse({'status' : 'success', 'instance': list(data.values())[0]}, status=200)
                else:
                    return JsonResponse({'status': 'failed', 'message': 'Data tidak tersedia'}, status=200)
                
        return JsonResponse({'status': 'Invalid request'}, status=400)


class MasterPositionDeleteClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            if request.method == 'POST':
                data = models.JabatanPegawaiModel.objects.filter(pk = request.POST.get('id'))
                if data.exists():
                    safe_check = models.MasterPegawaiModel.objects.filter(jabatan=data.first().pk)
                    if safe_check.exists():
                        return JsonResponse({'status': 'failed', 'message': f'Data Jabatan "{data.first().jabatan}" telah digunakan pada master data pegawai.'}, status=200)

                    data.delete()
                    return JsonResponse({'status' : 'success', 'message': 'Data berhasil dihapus'}, status=200)
                else:
                    return JsonResponse({'status': 'failed', 'message': 'Data tidak tersedia'}, status=200)
                
        return JsonResponse({'status': 'Invalid request'}, status=400)


class MasterPositionUpdateClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            
            data = get_object_or_404(models.JabatanPegawaiModel, pk=request.POST.get('id'))

            form = forms.PosisitionForm(request.POST, instance=data)

            if form.is_valid():
                instance = form.save()
                ser_instance = serializers.serialize('json', [ instance, ])
                
                # send to client side.
                return JsonResponse({"instance": ser_instance, 'message': 'Data berhasil diubah'}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": ""}, status=400)


class PangkatClassView(LoginRequiredMixin, View):

    def get(self, request):
        context = {
            'title' : 'Master Pangkat/Golongan',
            'form' : forms.PangkatGolonganForm
        }
        return render(request, 'master_pegawai/pangkat.html', context)

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            form = forms.PangkatGolonganForm(request.POST)
            if form.is_valid():
                instance = form.save()
                return JsonResponse({'message': 'Data berhasil ditambahkan'}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": ""}, status=400)


class MasterPangkatJsonResponseClassView(LoginRequiredMixin, View):

    def post(self, request):
        data = self._datatables(request)
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
		
    def _datatables(self, request):
        datatables = request.POST

        # Get Draw
        draw = int(datatables.get('draw'))
        start = int(datatables.get('start'))
        length = int(datatables.get('length'))
        page_number = int(start / length + 1)

        search = datatables.get('search[value]')

        order_idx = int(datatables.get('order[0][column]')) # Default 1st index for
        order_dir = datatables.get('order[0][dir]') # Descending or Ascending
        order_col = 'columns[' + str(order_idx) + '][data]'
        order_col_name = datatables.get(order_col)

        if (order_dir == "desc"):
            order_col_name =  str('-' + order_col_name)

        data = models.PangkatPegawaiModel.objects
        
        if search:
            data = data.filter(
                Q(pangkat__icontains=search)|
                Q(golongan__icontains=search)
            )

        data = data.exclude(Q(pangkat=None) | Q(golongan=None))
        records_total = data.count()
        records_filtered = records_total
        
        data = data.order_by(order_col_name)
        # Conf Paginator
        paginator = Paginator(data, length)

        try:
            object_list = paginator.page(page_number).object_list
        except PageNotAnInteger:
            object_list = paginator.page(1).object_list
        except EmptyPage:
            object_list = paginator.page(1).object_list

        data = []

        for obj in object_list:
            data.append({
                    'pangkat': f'{obj.pangkat}',
                    'golongan': f'{obj.golongan}',
                    'aksi': f'<a href="javascript:void(0);" onclick="editPangkat({obj.id})" class="action-icon"><i class="mdi mdi-square-edit-outline font-15"></i></a> <a href="javascript:void(0);" onclick="hapusPangkat({obj.id});" class="action-icon"> <i class="mdi mdi-delete font-15"></i></a>'
                })
            
        return {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }


class MasterPangkatDetailClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                id = request.POST.get('id')
                data = models.PangkatPegawaiModel.objects.filter(pk=id)
                if data.exists():
                    return JsonResponse({'status' : 'success', 'instance': list(data.values())[0]}, status=200)
                else:
                    return JsonResponse({'status': 'failed', 'message': 'Data tidak tersedia'}, status=200)
                
        return JsonResponse({'status': 'Invalid request'}, status=400)


class MasterPangkatUpdateClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            
            data = get_object_or_404(models.PangkatPegawaiModel, pk=request.POST.get('id'))

            form = forms.PangkatGolonganForm(request.POST, instance=data)

            if form.is_valid():
                instance = form.save()
                ser_instance = serializers.serialize('json', [ instance, ])
                
                # send to client side.
                return JsonResponse({"instance": ser_instance, 'message': 'Data berhasil diubah'}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": ""}, status=400)


class MasterPangkatDeleteClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            if request.method == 'POST':
                data = models.PangkatPegawaiModel.objects.filter(pk = request.POST.get('id'))
                if data.exists():
                    safe_check = models.MasterPegawaiModel.objects.filter(pangkat=data.first().pk)
                    if safe_check.exists():
                        return JsonResponse({'status': 'failed', 'message': f'Data Pangkat/Gol. "{data.first().pangkat}/{data.first().golongan}" telah digunakan pada master data pegawai.'}, status=200)
                    data.delete()
                    return JsonResponse({'status' : 'success', 'message': 'Data berhasil dihapus'}, status=200)
                else:
                    return JsonResponse({'status': 'failed', 'message': 'Data tidak tersedia'}, status=200)
                
        return JsonResponse({'status': 'Invalid request'}, status=400)

