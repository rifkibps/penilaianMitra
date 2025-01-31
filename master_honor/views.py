import json
from django.core.serializers.json import DjangoJSONEncoder

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render
from django.views import View
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from . import forms
from . import models

from master_petugas.models import AlokasiPetugas

from munapps.helpers import currency_formatting as cf
from munapps.mixins import RestrictionsAccess, RestrictionsHttpRequestAccess

class MasterHonorClassView(LoginRequiredMixin, RestrictionsAccess, View):

    def get(self, request):

        context = {
            'title' : 'Manajemen Honor Mitra'
        }
        
        return render(request, 'master_honor/index.html', context)

class MasterHonorSettingClassView(LoginRequiredMixin, RestrictionsAccess, View):

    def get(self, request):

        context = {
            'title' : 'Manajemen Honor Mitra',
            'form' : forms.HonorForm()
        }
        
        return render(request, 'master_honor/honor.html', context)

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:

            form = forms.HonorForm(request.POST)

            if form.is_valid():
                instance = form.save()
                ser_instance = serializers.serialize('json', [ instance, ])
                
                # send to client side.
                return JsonResponse({"instance": ser_instance, 'message': 'Data berhasil ditambahkan'}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": ""}, status=400)

class MasterConstHonorSettingUpdateView(LoginRequiredMixin, RestrictionsAccess, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:

            data = get_object_or_404(models.HonorModel, pk=request.POST.get('id'))

            form = forms.HonorForm(request.POST, instance=data)

            if form.is_valid():
                instance = form.save()
                ser_instance = serializers.serialize('json', [ instance, ])
                
                # send to client side.
                return JsonResponse({"instance": ser_instance, 'message': 'Data berhasil diubah'}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": ""}, status=400)

class MasterHonorJsonResponseClassView(LoginRequiredMixin, RestrictionsAccess, View):

    def post(self, request):
        
        data_wilayah = self._datatables(request)
        return HttpResponse(json.dumps(data_wilayah, cls=DjangoJSONEncoder), content_type='application/json')
		
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

        constraint_salary = models.HonorModel.objects
        if datatables.get('status_filter'):
            constraint_salary = constraint_salary.filter(status = datatables.get('status_filter'))
        
        constraint_salary = constraint_salary.exclude(Q(nama=None)|Q(tgl_ref_awal=None)|Q(tgl_ref_akhir=None)|Q(honor_maks=None)|Q(status=None))

        records_total = constraint_salary.count()
        records_filtered = records_total
        
        if search:
            constraint_salary = models.HonorModel.objects
            if datatables.get('status_filter'):
                constraint_salary = constraint_salary.filter(status = datatables.get('status_filter'))

            constraint_salary = constraint_salary.filter(
                Q(nama__icontains=search)|Q(tgl_ref_awal__icontains=search)|Q(tgl_ref_akhir__icontains=search)|Q(honor_maks__icontains=search)
            ).exclude(Q(nama=None)|Q(tgl_ref_awal=None)|Q(tgl_ref_akhir=None)|Q(honor_maks=None)|Q(status=None))

            records_total = constraint_salary.count()
            records_filtered = records_total
        
        constraint_salary = constraint_salary.order_by(order_col_name)
        # Conf Paginator
        paginator = Paginator(constraint_salary, length)

        try:
            object_list = paginator.page(page_number).object_list
        except PageNotAnInteger:
            object_list = paginator.page(1).object_list
        except EmptyPage:
            object_list = paginator.page(1).object_list

        
        data = []

        for obj in object_list:

            if obj.status == '0':
                class_status = 'badge-primary-lighten'
            elif obj.status == '1':
                class_status = 'badge-danger-lighten'
            else:
                class_status = 'badge-success-lighten'

            data.append(
            {
                'nama': obj.nama,
                'tgl_ref_awal': obj.tgl_ref_awal.strftime('%d-%m-%Y'),
                'tgl_ref_akhir': obj.tgl_ref_akhir.strftime('%d-%m-%Y'),
                'honor_maks': cf(obj.honor_maks, True),
                'status' : f'<span class="badge {class_status}"> {obj.get_status_display()} </span>',
                'aksi': f'<a href="javascript:void(0);" onclick="editConstSalary({obj.id})" class="action-icon"><i class="mdi mdi-square-edit-outline"></i></a> <a href="javascript:void(0);" onclick="deleteConstSalary({obj.id});" class="action-icon"> <i class="mdi mdi-delete"></i></a>'
    
            })

        return {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }


class MasterConstSalarytGetClassView(LoginRequiredMixin, RestrictionsAccess, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                
                id = request.POST.get('id')
                data = models.HonorModel.objects.filter(pk=id)
                if data.exists():
                    return JsonResponse({'status' : 'success', 'instance': list(data.values())[0]}, status=200)
                else:
                    return JsonResponse({'status': 'failed', 'message': 'Data tidak tersedia'}, status=200)
                
        return JsonResponse({'status': 'Invalid request'}, status=400) 
    


class MasterConstSalaryDeleteView(LoginRequiredMixin, RestrictionsAccess, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                
                id = request.POST.get('id')

                data = models.HonorModel.objects.filter(pk = id)
                if data.exists():

                    check_nilai_mitra = AlokasiPetugas.objects.filter(const_salary = id)
                    if check_nilai_mitra.exists():
                        return JsonResponse({'status' : 'failed', 'message': 'Data survei telah digunakan pada alokasi petugas.'}, status=200)
        
                    data.delete()
                    return JsonResponse({'status' : 'success', 'message': 'Data berhasil dihapus'}, status=200)
                else:
                    return JsonResponse({'status': 'failed', 'message': 'Data tidak tersedia'}, status=200)
                
        return JsonResponse({'status': 'Invalid request'}, status=400)
