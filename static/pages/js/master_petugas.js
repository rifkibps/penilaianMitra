// MASTER PETUGAS

let region_code = ''

let generate_master_petugas = (url, csrf) => {
    return $("#basic-datatable").DataTable({
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
                    "adm_filter": region_code,
                    "jk_filter": $('#jk-select-filter').val(),
                    "agama_filter": $('#agama-select-filter').val(),
                    "pendidikan_filter": $('#pendidikan-select-filter').val(),
                    "bank_filter": $('#bank-select-filter').val(),
                    "status_filter": $('#status-select-filter').val(),
                })
            },
        },
        columns :[
            {"data": 'adm_id__region'},
            {"data": 'adm_id__region'},
            {"data": 'kode_petugas'},
            {"data": 'nama_petugas'},
            {"data": 'nik'},
            {"data" : 'email'},
            {"data" : 'no_telp'},
            {"data" : 'status'},
            {"data" : 'aksi'},
        ],
        lengthMenu: [7, 10, 25, 50, 100],
        columnDefs: [
            {
            'targets': [8], /* column index */
            'orderable': false, /* true or false */
            },
            {
                "targets": 0,
                "data": null,
                "defaultContent": "",
                "render": function (data, type, row, meta) {
                    return meta.row + 1;
                }
            }
        ],
        keys: !0,
        language: {
            paginate: {
            previous: "<i class='mdi mdi-chevron-left'>",
            next: "<i class='mdi mdi-chevron-right'>",
            },
            lengthMenu : "Menampilkan _MENU_",
            search: "Cari Mitra",
        },
        drawCallback: function () {
            $(".dataTables_paginate > .pagination").addClass("pagination-rounded");
        },
    });
}

let edit_petugas_request = (url, csrf, target_url, e) => {
    $('#formMasterPetugas')[0].reset();
    $('#formMasterPetugas').attr('action', target_url)
    $('#submitFormPetugas').html('Update Data')

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
            for (const [key, value] of Object.entries(data.instance)) {
                $('#id_'+key).val(value)
            }
            $('.nav-tabs a[href="#input-tab"]').tab('show');
        },
        error: (error) => {
            console.log(error);
        }
    });
}

$('#jk-select-filter, #agama-select-filter, #pendidikan-select-filter, #bank-select-filter, #status-select-filter').bind("keyup change", () => {
    table.draw()
})

$('#reset-filter').on('click', () => {
    region_code = ''
    $('.region-adm, #jk-select-filter, #agama-select-filter, #pendidikan-select-filter, #bank-select-filter, #status-select-filter').prop('selectedIndex',0);
    reset_administrative(true)
    table.draw();
})

$('#redraw-table').on('click', () => {
    table.draw();
})

// Petugas track record
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
            "data": function (d){
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
    return $("#list-petugas").DataTable({
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
        keys: !0,
        language: {
            paginate: {
            previous: "<i class='mdi mdi-chevron-left'>",
            next: "<i class='mdi mdi-chevron-right'>",
            },
        },
        drawCallback: function () {
            $(".dataTables_paginate > .pagination").addClass("pagination-rounded");
        },
    });
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
        success: function (response) {
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
        error: function (response) {
            var errors = response["responseJSON"]["error"]
            for (const [key, value] of Object.entries(errors)) {
                var msgs = '<ul>'
                value.forEach(function (item, index) {
                
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
                success: function (response) {
                    
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
                error: function (xhr, status, error) {
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
        success: function (response) {
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
        error: function (response) {
            return console.log(response)
        }
    })
}

$("#formMasterPetugas").on("submit", function (e){
    e.preventDefault()
})

$('#UploadExcelPetugas').on('click', function (e){
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