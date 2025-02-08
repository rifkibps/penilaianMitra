
let pushValuePenilaian = (id) => {
    $('#kegiatan_penilaian').val(id)
    table2.draw()
}

$('#search-mitra').on("keyup", () => {
    table3.draw()
})

$('#search-mitra-datatable').on("keyup", () => {
    table2.draw()
})

$('#refresh-rank').on("click", () => {
    table3.draw()
})

$('#formPenilaianPetugas').on('submit', function(e){
    e.preventDefault()
    var serializedData = $(this).serialize();
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: serializedData,
        success: function (response) {
            if (response.status == 'success'){
                
                Swal.fire(
                        'Data berhasil disimpan',
                        response.messages,
                        'success'
                )

                table2.ajax.reload();
            }
        },
        error: function (response) {
            console.log(response)
        }
    })
})

$('#close-card-form').on('click', () => {
    $('.form-select').val('')
    $('#table_form_penilaian tbody').html('')
    $('#card-form-penilaian').addClass('d-none')
})