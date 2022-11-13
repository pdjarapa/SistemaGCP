$(document).ready(function () {
    var next = "?next=" + document.location.pathname;
    //$('#loader').show();

    var oTableCiclos = $('#dt-ciclos').DataTable(options_datatable_ciclos());

    $('#filtro_ciclo_activo').change(function () {
        oTableCiclos.draw();
    });

    init_actions();
});


/**
* Datatable casos de prueba
*/
function options_datatable_ciclos(){
    var url_grupos = $('#dt-ciclos').data('url');
    var url_detalle = $('#dt-ciclos').data('url_detalle');
    var proyecto_id = $('#dt-ciclos').data('id');
    var url_ejecutar = $('#dt-ciclos').data('url_ejecutar');

    return {
        "order": [[0, "desc"]],
        "responsive": true,
        "autoWidth": false,
        "destroy": true,
        "deferRender": true,
        "language": {url: getUrl('static/plugins/datatables/es.txt')},
        "processing": true,
        "serverSide": true,
        ajax: {
            url: url_grupos,
            type: 'POST',
            data: function ( d ) {
                d.proyecto_id = proyecto_id;
                d.filtro_activo = $('#filtro_ciclo_activo').val();
            },
            //dataSrc: "",
            cache: false,
            error: function(err){
                if (err.responseJSON && err.responseJSON.message){
                    var msg = err.responseJSON.message;
                    alert(msg);
                }
                console.log(err);
                if (err.status == 401){
                    window.location = window.location;
                }
            }
        },
        columns: [
            {"data": "nombre"},
            {"data": "descripcion"},
            {"data": "casos"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                orderable: false,
                targets: [2],
                class: '',
            },
            {targets: [0], render: function (data, type, row) {
                return data;
            }},
            {targets: [1], render: function (data, type, row) {
                return data;
            }},
            {targets: [2], render: function (data, type, row) {
                return data;
            }},
            {targets: [3], 'class': "text-right", render: function (data, type, row) {
                var url_edit =  url_detalle + row.id;
                var url_exec = url_ejecutar + row.id;
                var html = '';
                html += $.validator.format('<a href="{0}"><i class="fas fa-pen"></i> {1}</a> | ', url_edit, 'Editar');
                html += $.validator.format('<a href="{0}"><i class="fas fa-running"></i> {1}</a>', url_exec, 'Ejecutar');
                return html;
            }}

        ],
        initComplete: function (settings, json) {
        },
        "stateSave": true,
        fnStateSaveParams: function(oSettings, oData){
            oData.filtro_activo = $('#filtro_ciclo_activo').val();
        },
        fnStateLoadParams: function(oSettings, oData){
            $('#filtro_ciclo_activo').val(oData.filtro_activo);
        }
    };
};

function init_actions(){

}