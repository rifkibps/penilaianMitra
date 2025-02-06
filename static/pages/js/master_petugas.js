let region_code = ''

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