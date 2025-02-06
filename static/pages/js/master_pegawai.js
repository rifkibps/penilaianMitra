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

$("#formMasterPegawai").on("submit", function (e){
    e.preventDefault()
})

$(document).on('change', '.form-control, .form-select', () => {
    if ($(this).hasClass('is-invalid')){
        $(this).removeClass('is-invalid')
    }
});


// Pangkat dan Golongan
$("#formMasterPangkat").on("submit", function (e){
    e.preventDefault()
})

$("#formMasterPosition").on("submit", function (e){
    e.preventDefault()
})