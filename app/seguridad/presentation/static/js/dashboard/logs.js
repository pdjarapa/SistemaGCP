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
            {"data": "date"},
            {"data": "user__correo_electronico"},
            {"data": "ip_address"},
            {"data": "user_agent"},
            {"data": "type"},
            {"data": "browser"},
            {"data": "system"},
        ],
        columnDefs: [
            {
                orderable: true,
                targets: [0, 3],
                class: '',
            },
            {targets: [4], render: function (data, type, row) {
                var txt = '<b>Agent:</b> ' + data +
                    '</br><b>' + row.method + ':</b> ' + row.path +
                    '</br><b> Content type:</b> ' + row.content_type;

                //if(row.referer && row.referer.indexOf(window.location.host) == -1){
                    txt = txt + '</br><b> Referer:</b> ' + row.referer;
                //}

                return txt;
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