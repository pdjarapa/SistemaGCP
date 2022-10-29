$(function () {
    // $('#id_numero_documento').change(function (){
    //     obtener_persona();
    // });

    $('#id_correo_electronico').change(function (){
        $('#btnEnviarToken').prop('disabled', false);
    });
    enviar_token();
    verificar_token();
    verificar_persona()
    // login_solicitante();
    // enviar_token('#form_registro_solicitante', url_enviar_token);
});

function verificar_persona(){
       $('#id_numero_documento').focusout(function (e){
           var url = url_verificar_persona;
           e.preventDefault();
           var numero_documento = $(this).val();
           $.ajax({
               url: url,
               type: 'GET',
               data: {"numero_documento": numero_documento},
               success: function (response){

                   // if not valid user, alert the user
                   if(!response["valido"]){
                       Swal.fire({
                          title: '',
                          text: "El usuario ya se encuentra registrado. Se lo redirigirá a la pantalla de Iniciar Sesión.",
                          icon: 'warning',
                          showCancelButton: false,
                          confirmButtonColor: '#1ee245',
                          cancelButtonColor: '#d33',
                          confirmButtonText: 'Ok'
                        }).then((result) => {
                          if (result.isConfirmed) {
                            //
                              location.href = 'iniciar-sesion/solicitante'
                          }
                        })
                        // alert("You cannot create a friend with same nick name");
                        // var nickName = $("#id_numero_documento");
                        // nickName.val("")
                        // nickName.focus()
                   }else {
                       obtener_persona();
                   }
               },
               error: function (response){
                   console.log(response)
               },
           });
    });
}

function verificar_correo(){
       $('#id_numero_documento').focusout(function (e){
           var url = url_verificar_persona;
           e.preventDefault();
           var numero_documento = $(this).val();
           $.ajax({
               url: url,
               type: 'GET',
               data: {"numero_documento": numero_documento},
               success: function (response){

                   // if not valid user, alert the user
                   if(!response["valido"]){
                       Swal.fire({
                          title: '',
                          text: "El usuario ya se encuentra registrado. Se lo redirigirá a la pantalla de Iniciar Sesión.",
                          icon: 'warning',
                          showCancelButton: false,
                          confirmButtonColor: '#1ee245',
                          cancelButtonColor: '#d33',
                          confirmButtonText: 'Ok'
                        }).then((result) => {
                          if (result.isConfirmed) {
                            //
                              location.href = 'iniciar-sesion/solicitante'
                          }
                        })
                        // alert("You cannot create a friend with same nick name");
                        // var nickName = $("#id_numero_documento");
                        // nickName.val("")
                        // nickName.focus()
                   }else {
                       obtener_persona();
                   }
               },
               error: function (response){
                   console.log(response)
               },
           });
    });
}

function enviar_token() {
    $('#btnEnviarToken').on('click', function(e) {
        var url = url_enviar_token;
        e.preventDefault();
        var frm = this.closest("form");
        let correo_electronico = $("#id_correo_electronico");
        if(correo_electronico.val().indexOf('@', 0) === -1 || correo_electronico.val().indexOf('.', 0) === -1) {
            correo_electronico.addClass('is-invalid');
            $('#m-error').text("El correo electrónico introducido no es correcto.").removeClass('d-none').addClass("has-error");
            return false;
        }else {
            $.ajax({
                url: url,
                type: 'POST',
                data: $('#'+frm.id).serialize(),
                success: function (response) {
                    if (response['usuario_nuevo']){
                        $("#m-error").text("El correo electrónico no se encuentra registrado.").removeClass('d-none').addClass('has-error');
                        return false;
                    }else{
                        $('#mensaje_correo').css("display","block");
                        if($('#m-error').hasClass('has-error')){
                            correo_electronico.removeClass('is-invalid');
                            $('#m-error').hide();
                    }
                    $('#btnEnviarToken').prop('disabled', true);
                    $('#btnValidarToken').prop('disabled', false);
                    }

                },
                error: function (response) {
                    let correo_electronico = $("#id_correo_electronico");
                    correo_electronico.val("").addClass('is-invalid').focus();
                    $('#m-error').val(response.error).removeClass('d-none').addClass('has-error');
                    alertify.error("Error al intentar iniciar sesión.", "notificación", "2");
                },
        });
        }


  });
}

function verificar_token(){
    $('#btnValidarToken').on('click', function (e){
        var url = url_verificar_token;
        e.preventDefault();
        var frm = this.closest("form");
        let token = $('#id_token');
        let token_valor = token.val();
        let correo_electronico = $('#id_correo_electronico')
        let valor_correo_electronico = correo_electronico.val();

        $.ajax({
            url: url,
            type: 'POST',
            data: $('#'+frm.id).serialize(),//$(id_form).serialize(),
            success: function (response){
                if(!response["valido"]){
                    $('#mensaje_verifica_token').css("display","block");
                    if ($('#t-error').hasClass('has-error')){
                        token.removeClass('is-invalid');
                        $('#t-error').hide();
                    }
                    $('#bloque-preguntas').css("display","block");
                    $('#btnValidarToken').prop('disabled', true);
                }else{
                    let token = $('#id_token');
                    token.addClass('is-invalid').focus();
                    $('#t-error').removeClass('d-none').addClass('has-error');
                }
            },
            error: function (response){
                alertify.error("Error al validar token.", "notificación", "2");
            },
        });
    });
}

function login_solicitante(){
    var uri = $('#form_login_solicitante').attr('action');
    console.log(uri)
    $.ajax({
        data: $('#form_login_solicitante').serialize(),
        url: $('#form_login_solicitante').attr('action'),
        type: $('#form_login_solicitante').attr('method'),
        success: function (response) {
            // console.log(response)
            // console.log(getUrl('proceso/lista'))
            location.href = url_proceso_lista;
        },
        error: function (error){
            mostrar_errores_login(error);
            console.log(error)
        }
    });
}

function mostrar_errores_login(errores){
    $('#errores').html("");
    let error = "";
    for(let item in errores.responseJSON.error){
        error += '<div class = "alert alert-danger" <strong>' + errores.responseJSON.error[item] + '</strong></div>';
    }
    $('#errores').append(error);
}

function obtener_persona() {
    var identificacion = $('#id_numero_documento').val();
    var api_bsg = BSG_API_URL + '/consultar-cedula/' + identificacion;
    $.get(api_bsg, {}, function (result) {
        console.log(result.data);
        var res = result.data.Nombre.split(" ");
        console.log(res)
        $('#id_fecha_nacimiento, #id_profesion, #id_primer_nombre, #id_segundo_nombre, #id_primer_apellido, #id_segundo_apellido').prop('readonly', true);
        $('#id_fecha_nacimiento').val(result.data.FechaNacimiento);
        $('#id_profesion').val(result.data.Profesion);
        $('#id_primer_nombre').val(res[2]);
        $('#id_segundo_nombre').val(res[3]);
        $('#id_primer_apellido').val(res[0]);
        $('#id_segundo_apellido').val(res[1]);
    })
}

function alerta() {
    var mensaje;
    var opcion = alert("El código ha sido verficiado correctamente");
    if (opcion === true) {
        mensaje = "Has clickado OK";
	} else {
	    mensaje = "Has clickado Cancelar";
	}
	// document.getElementById("ejemplo").innerHTML = mensaje;
}

