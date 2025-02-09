let global_rank = (url, csrf) => {
    return $('#ranking-global').DataTable({
        processing: true,
        serverSide: true,
        ajax: {
            "url": url,
            "headers": {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": csrf,
            },
            "type": "POST",
            "data": (d) => {
                return $.extend({}, d, {
                    "search_mitra": $('#search-mitra').val(),
                })
            },
        },
        columns :[
            {"data": 'wilayah'},
            {"data" : 'petugas'},
            {"data" : 'rerata'},
            {"data" : 'rank'},
        ],
        columnDefs: [ {
            'targets': [2,3], /* column index */
            'className': "text-center"
        }],
        bLengthChange: false,
        bPaginate: false,
        bFilter: false,
    });
}

let list_nilai_petugas = (url, csrf) => {
    return $("#list-petugas").DataTable(
        {...{
            processing: true,
            serverSide: true,
            ajax: {
                "url": url,
                "headers": {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": csrf,
                },
                "type": "POST",
                "data": (d) => {
                    return $.extend({}, d, {
                        "search_mitra": $('#search-mitra-datatable').val(),
                    })
                },
            },
            columns :[
                {"data": 'kode_petugas'},
                {"data" : 'adm_id__region'},
                {"data": 'nama_petugas'},
                {"data": 'no_telp'},
                {"data" : 'email'},
                {"data" : 'jml_kegiatan'},
                {"data" : 'jml_penilai'},
                {"data" : 'status'},
                {"data" : 'aksi'},
            ],
            lengthMenu: [5, 25, 50, 100,'All'],
            columnDefs: [ {
                'targets': [8], /* column index */
                'orderable': false, /* true or false */
                'className': "text-center"
            },
            {
                'targets': [3, 5,6,7], /* column index */
                'className': "text-center"
            }
            ],
            bLengthChange: false,
            bFilter: false,
        }, ...settingDatatables()
    }
);
}

let resetFormPetugas = (url) => {
    $('#formMasterPetugas')[0].reset();
    $('#formMasterPetugas').attr('action', url)
    $('#submitFormPetugas').html('Kirim Data')
    clearFormValidation('#formMasterPetugas')
}

let checkSubmitPetugas = (csrf) => {
    clearFormValidation('#formMasterPetugas')
    var serializedData = $('#formMasterPetugas').serialize();
    
    $.ajax({
        url: $('#formMasterPetugas').attr('action'),
        type: 'POST',
        data: serializedData,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrf,
        },
        success: (response) =>  {
            $('#messages-content').html(response["message"])
            $('#msgs-upload').removeClass('alert-danger')
            $('#msgs-upload').addClass('alert-success')
            $('#msgs-upload').removeClass('d-none')
            table.ajax.reload();
            $('.nav-tabs a[href="#petugas-preview"]').tab('show');
            $('#formMasterPetugas')[0].reset();
            $('#formMasterPetugas').trigger("reset");
            clearFormValidation('#formMasterPetugas')
        },
        error: (response) =>  {
            var errors = response["responseJSON"]["error"]
            for (const [key, value] of Object.entries(errors)) {
                var msgs = '<ul>'
                value.forEach((item, index) => {
                    msgs += '<li>'+item+'</li>'
                    });
                msgs += '</ul>'
                if (key == 'adm_id'){
                    $('#id_'+ key +'_id').addClass('is-invalid');
                    $('#msg-id_'+key+'_id').html(msgs)
                }else{
                    $('#id_'+ key).addClass('is-invalid');
                    $('#msg-id_'+key).html(msgs)
                }
            }    
        }
    })
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
                success: (response) =>  {
                    
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
                        $('.nav-tabs a[href="#petugas-preview"]').tab('show');
                        table.ajax.reload();

                    }
                },
                error: (xhr, status, error) => {
                    return console.log(xhr.responseText['messages'])
                }
            })
        } else if (result.dismiss === Swal.DismissReason.cancel) {
          swalWithBootstrapButtons.fire(
            'Cancelled',
            'Data successfully cancelled',
            'error'
          )
        }
    }) 
}

let uploadPetugas = (url, csrf, formData) => {
    $.ajax({
        type: 'POST',
        url: url,
        data: formData,
        processData: false,
        contentType: false,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrf,
        },
        success: (response) =>  {
            if (response.status == 'error') {
                var error_list = '<ol>'
                for (let i = 0; i < response.message.length; i++) {
                    error_list += '<li class="p-1">'+ response.message[i].error +'</li>'
                }
                error_list += '</ol>'

                $("#error-upload-files").html(error_list)
                $("#error-upload-files").removeClass('d-none')
            } else{
                $("#ConfirmUploadExcelPetugas").removeClass('d-none')
                return alert('Success')
            }
        },
        error: (response) =>  {
            return console.log(response)
        }
    })
}

$("#formMasterPetugas").on("submit", (e) => {
    e.preventDefault()
})

$('#UploadExcelPetugas').on('click', (e) => {
    $('#upload-petugas-excel').modal('show')
})

$('#get-templates-upload').on('click', () =>{
    var numrows = $('#number_rows').val()
    return window.location.replace("http://127.0.0.1:8000/master-petugas/template/" + numrows);
})

$('#btn-submit-file').on('click', (e) => {
    $('#nav-item-import').removeClass('d-none')
    $('.nav-tabs a[href="#import-tab"]').tab('show');
    $(this).blur()
    $('#import-modal').modal('toggle')
})

// PETUGAS TRACK RECORD
$('#search-mitra').on("keyup", () => {
    table.draw()
})
$('#search-mitra-datatable').on("keyup", () => {
    table2.draw()
})

$('#refresh-rank').on("click", () => {
    table.draw()
})