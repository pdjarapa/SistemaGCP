var Toast = null;

$(function(){
    Toast = Swal.mixin({
      toast: true,
      position: 'top-end',
      showConfirmButton: false,
      timer: 3000
    });

    //is-invalid
    //invalid-feedback
    $.validator.setDefaults({
        errorElement: "span",
        errorClass: "invalid-feedback",
        highlight: function (element, errorClass, validClass) {
            $(element).addClass('is-invalid');
        },
        unhighlight: function (element, errorClass, validClass) {
            $(element).removeClass('is-invalid');
        }
    });

});



function getUrl(url){
    return BASE_PATH + url;
};

function mensaje_error(mensaje) {
    Toast.fire({
        icon: 'error',
        title: mensaje ? mensaje : 'Ocurrió un error al procesar la petición'
    });
};

function mensaje_exito(mensaje){
  Toast.fire({
    icon: 'success',
    title: mensaje ? mensaje : '¡La petición se procesó con éxito!'
  });
};

function mensaje_info(){
    Toast.fire({
        icon: 'info',
        title: mensaje ? mensaje : '¡Mensaje informativo!'
      });
};

// sweetalert
function alert_confirm(title, text, icon, confirm_txt='Si, estoy de acuerdo', target=null) {
    var opciones = {
        target: document.getElementById(target),
        title: title,
        text: text,
        icon: icon,
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        cancelButtonText: 'Cancelar',
        confirmButtonText: confirm_txt
    };

    return Swal.fire(opciones)
};

function alert_notificacion(title, text, icon, target=null) {
    return Swal.fire({
        target: document.getElementById(target),
        title: title,
        text: text,
        icon: icon,
    });
};

