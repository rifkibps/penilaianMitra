// MASTER PETUGAS

let region_code = ''

let generate_master_petugas = (url, csrf) => {
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
                    "render": (data, type, row, meta) => {
                        return meta.row + 1;
                    }
                }
            ],
            }, ...settingDatatables()    
        }
);
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
