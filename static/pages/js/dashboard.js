'use strict'

let ExportToExcel = (type, fn, dl) => {
    var elt = document.getElementById('ranking-mitra');
    var wb = XLSX.utils.table_to_book(elt, { sheet: "Ranking Mitra" });
    return dl ?
        XLSX.write(wb, { bookType: type, bookSST: true, type: 'base64' }):
        XLSX.writeFile(wb, fn || ('Data Ranking Mitra.' + (type || 'xlsx')));
    }

let generate_ranked = (url, csrf) => {
    return $("#ranking-mitra").DataTable(
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
                "data": (d) => {
                    return $.extend({}, d, {
                        "kegiatan_filter": $('#kegiatan_filter').val(),
                    })
                },
                "type": "POST"
            },
        
            lengthMenu: [5, 25, 50, 100],
            columns :[
                {"data": 'petugas__petugas__nama_petugas'},
                {"data": 'petugas__role__jabatan'},
                {"data" : 'detail_nilai__indikator_penilaian__kegiatan_penilaian__kegiatan_survey__nama_kegiatan'},
                {"data" : 'rerata'},
                {"data" : 'rerata_final'},
                {"data" : 'ranking'},
                {"data" : 'ranking_final'},
            ], 
        },  ...settingDatatables()
    }
);
}

$('#kegiatan_filter').bind("keyup change", () => {
    table.draw()
})

$('#redraw-table').on('click', () => {
    table.draw();
})
