$(document).ready(function () {
    var oTable = $('#lista').DataTable(default_options_datatable());
});

function default_options_datatable(){
    var url = $('#lista').data('url');
    return {
        "order": [[0, "desc"]],
        "responsive": true,
        "autoWidth": false,
        "destroy": true,
        "deferRender": true,
        "language": {url: getUrl('static/plugins/datatables/es.js')},
        "processing": true,
        "serverSide": true,
        ajax: {
            url: url,
            type: 'POST',
            data: function (d) {
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
            {"data": "id"},
            {"data": "login_at"},
            {"data": "logout_at"},
            {"data": "user__correo_electronico"},
            {"data": "user__descripcion"},
            {"data": "ip_address"},
            {"data": "user_agent"},
        ],
        columnDefs: [
            {
                orderable: false,
                targets: [2, 3],
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
            {targets: [3], render: function (data, type, row) {
                return data;
            }},
            {targets: [4], render: function (data, type, row) {
                return data;
            }},
            {targets: [5], render: function (data, type, row) {
                return data;
            }},
            {targets: [6], render: function (data, type, row) {
                return data;
            }}

        ],
        "stateSave": true,
        fnStateSaveParams: function(oSettings, oData){
            oData.filtro_activo = $('#filtro_activo').val();
        },
        fnStateLoadParams: function(oSettings, oData){
            $('#filtro_activo').val(oData.filtro_activo);
        }
    };
};