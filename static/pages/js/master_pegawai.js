// Master Pegawai
let generate_master_pegawai = (url, csrf) => {
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
                    "data": (d) => {
                        return $.extend({}, d, {
                            "pangkat_filter": $('#pangkat-filter').val(),
                            "jabatan_filter": $('#jabatan-filter').val()
                        })
                    },
                },
                columns :[
                    {"data": 'nip'},
                    {"data": 'nip'},
                    {"data": 'nip_bps'},
                    {"data": 'name'},
                    {"data" : 'pangkat__golongan'},
                    {"data" : 'jabatan__jabatan'},
                    {"data" : 'user'},
                    {"data" : 'aksi'},
                ],
                lengthMenu: [10, 25, 50, 100],
                columnDefs: [ {
                    'targets': [7], /* column index */
                    'orderable': false, /* true or false */
                },
                {
                    "targets": 0,
                    "data": null,
                    "className": "text-center",
                    "defaultContent": "",
                    "render": (data, type, row, meta) => {
                        return meta.row + 1;
                    }
                }
                ],
            }, ...settingDatatables()
        }
);
}

let edit_pegawai_request = (url, csrf, target_url, e) => {
    $('#formMasterPegawai')[0].reset();
    $('#formMasterPegawai').attr('action', target_url)
    $('#submitFormPegawai').html('Update Data')

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

let resetFormPegawai = (url) => {
    $('#formMasterPegawai')[0].reset();
    $('#formMasterPegawai').attr('action', url)
    $('#submitFormPegawai').html('Kirim Data')
    clearFormValidation('#formMasterPegawai')
}

let checkSubmitPegawai = (csrf) => {
    var serializedData = $('#formMasterPegawai').serialize();
    clearFormValidation('#formMasterPegawai')
    
    $.ajax({
        type: 'POST',
        url: $('#formMasterPegawai').attr('action'),
        data: serializedData,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrf,
        },
        success: (response) =>  {
            $('#messages-content').html(response["message"])
            $('#msgs-feedback').removeClass('alert-danger')
            $('#msgs-feedback').addClass('alert-success')
            $('#msgs-feedback').removeClass('d-none')
            table.ajax.reload();
            $('.nav-tabs a[href="#pegawai-preview"]').tab('show');
            $('#formMasterPegawai')[0].reset();
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

$('#jabatan-filter, #pangkat-filter').bind("change", () => {
    table.draw()
})

$('#redraw-table').on('click', () => {
    table.draw();
})

$('#reset-filter').on('click', () => {
    $('#jabatan-filter, #pangkat-filter').prop('selectedIndex',0);
    table.draw();
})

$("#formMasterPegawai").on("submit", (e) => {
    e.preventDefault()
})

// Pangkat dan Golongan
let generate_pangkat = (url, csrf) => {
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
        },
        columns :[
            {"data": 'golongan'},
            {"data": 'golongan'},
            {"data": 'pangkat'},
            {"data" : 'aksi'},
        ],
        lengthMenu: [5, 10, 25, 50, 100],
        columnDefs: [{
            'targets': [3], /* column index */
            'orderable': false, /* true or false */
            'className' : 'text-center'
        },
        {
            "targets": 0,
            "data": null,
            "defaultContent": "",
            "render": (data, type, row, meta) => {
                return meta.row + 1;
            }
        }],
        keys: !0,
        language: {
            paginate: {
            previous: "<i class='mdi mdi-chevron-left'>",
            next: "<i class='mdi mdi-chevron-right'>",
            },
            lengthMenu : "Menampilkan _MENU_",
            search: "Cari Pangkat/Gol.",
        },
        drawCallback: () =>  {
            $(".dataTables_paginate > .pagination").addClass("pagination-rounded");
        },
    });
}

let edit_pangkat_request = (url, csrf, target_url, e) => {
    $('#formMasterPangkat')[0].reset();
    $('#formMasterPangkat').attr('action', target_url)
    $('#submitFormPegawai').html('Update Data')
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

let checkSubmitPangkat = (csrf) => {
    var serializedData = $('#formMasterPangkat').serialize();
    clearFormValidation('#formMasterPangkat')
    
    $.ajax({
        type: 'POST',
        url: $('#formMasterPangkat').attr('action'),
        data: serializedData,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrf,
        },
        success: (response) =>  {
            $('#messages-content').html(response["message"])
            $('#msgs-feedback').removeClass('alert-danger')
            $('#msgs-feedback').addClass('alert-success')
            $('#msgs-feedback').removeClass('d-none')
            table.ajax.reload();
            $('.nav-tabs a[href="#position-preview"]').tab('show');
            $('#formMasterPangkat')[0].reset();
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

let resetFormPangkat = (url) => {
    $('#formMasterPangkat')[0].reset();
    $('#formMasterPangkat').attr('action', url)
    $('#submitFormPegawai').html('Kirim Data')
    clearFormValidation('#formMasterPangkat')
}

$("#formMasterPangkat").on("submit", (e) => {
    e.preventDefault()
})

// Jabatan

let generate_position = (url, csrf) => {
    return $("#basic-datatable").DataTable({
        processing: true,
        serverSide: true,
        ajax: {
            "url":  url,
            "headers": {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": csrf,
            },
            "type": "POST",
        },
        columns :[
            {"data": 'jabatan'},
            {"data": 'jabatan'},
            {"data" : 'aksi'},
        ],
        lengthMenu: [5, 10, 25, 50, 100],
        columnDefs: [
        {
            'targets': [2], 
            'orderable': false,
            'className': "text-center"
        },
        {
            "targets": 0,
            "data": null,
            "defaultContent": "",
            "render": (data, type, row, meta) => {
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
            search: "Cari Jabatan",
        },
        drawCallback: () =>  {
            $(".dataTables_paginate > .pagination").addClass("pagination-rounded");
        },
    });
}

let edit_position_request = (url, csrf, target_url, e) => {
    $('#formMasterPosition')[0].reset();
    $('#formMasterPosition').attr('action', target_url)
    $('#submitFormPegawai').html('Update Data')

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

let checkSubmitPosition = (csrf) => {
    var serializedData = $('#formMasterPosition').serialize();
    clearFormValidation('#formMasterPosition')
    
    $.ajax({
        type: 'POST',
        url: $('#formMasterPosition').attr('action'),
        data: serializedData,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrf,
        },
        success: (response) =>  {
            $('#messages-content').html(response["message"])
            $('#msgs-feedback').removeClass('alert-danger')
            $('#msgs-feedback').addClass('alert-success')
            $('#msgs-feedback').removeClass('d-none')
            table.ajax.reload();
            $('.nav-tabs a[href="#position-preview"]').tab('show');
            $('#formMasterPosition')[0].reset();
        },
        error: (response) =>  {
            var errors = response["responseJSON"]["error"]
            console.log(errors)
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

let resetFormPosition = (url) => {
    $('#formMasterPosition')[0].reset();
    $('#formMasterPosition').attr('action', url)
    $('#submitFormPegawai').html('Kirim Data')
    clearFormValidation('#formMasterPosition')
}

$("#formMasterPosition").on("submit", (e) => {
    e.preventDefault()
})