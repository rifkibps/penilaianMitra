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