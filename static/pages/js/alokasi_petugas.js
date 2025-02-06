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

$('#btn-submit-file').on('click', (e) => {
    $('#nav-item-import').removeClass('d-none')
    $('.nav-tabs a[href="#import-tab"]').tab('show');
    $(this).blur()
    $('#import-modal').modal('toggle')
})