from django_cas_ng.backends import CASBackend

class SiaafCASBackend(CASBackend):
    def authenticate(self, request, ticket, service):
        user = super().authenticate(request, ticket, service)
        if user:
            request.session['is_cas_authenticated'] = True
            print('is_cas_authenticated', request.session['is_cas_authenticated'], user.id)
        return user

    def user_can_authenticate(self, user):
        if user.activo:
            if user.correo_electronico.split('@')[1] == 'unl.edu.ec':
                return True
        return False

    def configure_user(self, user):
        user.activo = True
        user.save()
        return user

    def clean_username(self, username):
        return username.strip().lower()