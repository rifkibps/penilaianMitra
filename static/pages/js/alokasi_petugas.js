let generate_alokasi_petugas = (url, csrf) => {
    return $("#basic-datatable").DataTable(
    {
        ...{
            processing: true,
            serverSide: true,
            ajax: {
                "url": url,
                "headers": {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": csrf,
                },
                "type": "POST",
                "data": function (d){
                    return $.extend({}, d, {
                        "survei_filter": $('#survei-select-filter').val(),
                        "jabatan_filter": $('#jabatan-select-filter').val(),
                    })
                },
            },
            lengthMenu: [5, 25, 50, 100, 250],
            columns :[
                {"data": 'petugas__nama_petugas'},
                {"data": 'petugas__kode_petugas'},
                {"data": 'petugas__nama_petugas'},
                {"data": 'sub_kegiatan__nama_kegiatan'},
                {"data" : 'role__jabatan'},
                {"data" : 'pegawai'},
                {"data" : 'aksi'},
            ],
            columnDefs: [ {
                'targets': [6], /* column index */
                'orderable': false, /* true or false */
            },
            {
                "targets": 0,
                "data": null,
                "defaultContent": "",
                "render": function (data, type, row, meta) {
                    return meta.row + 1;
                }
            }],
        }, ...settingDatatables()
    }
);
}

let form_submit = (csrf) => {
    var serializedData = $('#formAlokPetugas').serialize();
    $('.invalid-feedback').html('')
    $('.is_invalid').removeClass('is_invalid')
    
    $.ajax({
        type: 'POST',
        url: $('#formAlokPetugas').attr('action'),
        data: serializedData,
        "headers": {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrf,
        },
        success: (response) =>  {
            if (response.status == 'success'){
                $('#messages-content').html(response["message"])
                $('#msgs-upload').removeClass('alert-danger')
                $('#msgs-upload').addClass('alert-success')
                $('#msgs-upload').removeClass('d-none')
                table.ajax.reload();
                resetForm()
                $('.nav-tabs a[href="#alokasi-preview"]').tab('show');
            }else{
                Swal.fire(
                    'Terjadi Kesalahan!',
                    response.message,
                    'info'
                )
            }
        },
        error: (response) => {
            var errors = response["responseJSON"]["error"]
            for (const [key, value] of Object.entries(errors)) {
                var msgs = '<ul>'
                value.forEach((item, index) => {
                    msgs += '<li>'+item+'</li>'
                    });
                
                msgs += '</ul>'
                $('#id_'+ key).addClass('is-invalid');
                $('#msg-id_'+key).html(msgs)
            }    
        }
    })
}

let editAlokasiPetugas = (url, csrf, target_url, e) => {
    $('#formAlokPetugas')[0].reset();
    $('#formAlokPetugas').attr('action', target_url)
    $('#submitformAlokPetugas').html('Update Data')

    $.ajax({
        url: url,
        type: "POST",
        dataType: "json",
        data : {
            'id' : e
        },
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrf,
        },
        success: (data) => {

            if (data.status == 'failed'){
                Swal.fire(
                    'Terjadi Kesalahan!',
                     data.message,
                    'info'
                    )
            }else{
                for (const [key, value] of Object.entries(data.instance)) {
                    $('#id_'+key).val(value)
                    console.log(key)
                }
                $('.nav-tabs a[href="#input-tab"]').tab('show');
                table.ajax.reload();
            }
        },
        error: (error) => {
            console.log(error);
        }
    });
}

let confirmSubmitFile = (url, csrf, target_form_data) => {
    swalWithBootstrapButtons.fire({
        title: 'Are you sure?',
        text: "Apakah anda yakin ingin mengupload data mitra?",
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Yes, upload it!',
        cancelButtonText: 'No, cancel!',
        reverseButtons: true
      }).then((result) => {
        if (result.isConfirmed) {

            var data = new FormData();
            data.append("import_file", target_form_data)
         
            $.ajax({
                type: 'POST',
                url: url,
                data: data,
                processData: false,
                contentType: false,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": csrf,
                },
                success: (response) => {
                    
                    if (response.status == 'error'){

                        var content_msgs = '<strong>Terjadi kesalahan</strong> saat import data: <ol class="px-3 font-12">'

                        for (let i = 0; i < response.messages.length; i++) {
                            content_msgs += '<li>'+ response.messages[i] +'</li>'
                        }
                        
                        $('#messages-content').html(content_msgs)
                        $('#msgs-upload').removeClass('alert-success')
                        $('#msgs-upload').addClass('alert-danger')
                        $('#msgs-upload').removeClass('d-none')
                    }else{
                        var content_msgs = response.messages
                        
                        $('#messages-content').html(content_msgs)
                        $('#msgs-upload').removeClass('alert-danger')
                        $('#msgs-upload').addClass('alert-success')
                        $('#msgs-upload').removeClass('d-none')

                        $('#nav-item-import').addClass('d-none')
                        $('.nav-tabs a[href="#alokasi-preview"]').tab('show');

                        table.ajax.reload();
                    }
                },
                error: (xhr, status, error) => {
                    return console.log(xhr.responseText['messages'])
                }
            })
        } else if (
         
          result.dismiss === Swal.DismissReason.cancel
        ) {
          swalWithBootstrapButtons.fire(
            'Cancelled',
            'Data successfully cancelled',
            'error'
          )
        }
    }) 
}

let resetFormAlokasiPetugas = (url) => {
    $('#formAlokPetugas')[0].reset();
    $('.was-validated').removeClass('was-validated')
    $('#submitformAlokPetugas').html('Kirim Data')
    $('#formAlokPetugas').attr('action', url)
}

let input_mitra_tab = () => {
    $('#form_id_petugas_id').removeClass('d-none')
    $('#form_id_pegawai_id').addClass('d-none')
    $('#id_pegawai_id').val('')
    $('#input-mitra').addClass('active')
}

let input_pegawai_tab = () => {
    $('#form_id_petugas_id').addClass('d-none')
    $('#id_petugas_id').val('')
    $('#form_id_pegawai_id').removeClass('d-none')
    $('#input-pegawai').addClass('active')
}

$('#survei-select-filter').bind("keyup change", () => {
    table.draw()
})

$('#jabatan-select-filter').bind("keyup change", () => {
    table.draw()
})

$('#ResetformAlokPetugas').on('click', (e) => {
    resetForm()
})

$('#formAlokPetugas').on('submit', (e) => {
    e.preventDefault()
})

$('#reset-filter').on('click', () => {
    $('#survei-select-filter').prop('selectedIndex',0);
    $('#jabatan-select-filter').prop('selectedIndex',0);
    table.draw();
})

$('#redraw-table').on('click', () => {
    table.draw();
})

$('#get-templates-upload').on('click', () => {
    var numrows = $('#number_rows').val()
    return window.location.replace("http://127.0.0.1:8000/alokasi-petugas/template/" + numrows);
})

$('#btn-submit-file').on('click', (e) => {
    $('#nav-item-import').removeClass('d-none')
    $('.nav-tabs a[href="#import-tab"]').tab('show');
    $(this).blur()
    $('#import-modal').modal('toggle')
})

$('#btn-submit-file').on('click', (e) => {
    $('#nav-item-import').removeClass('d-none')
    $('.nav-tabs a[href="#import-tab"]').tab('show');
    $('#btn-submit-file').blur()
    $('#import-modal').modal('toggle')
})