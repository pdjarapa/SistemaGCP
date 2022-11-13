import time
from importlib import import_module

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.backends.base import UpdateError
from django.core.exceptions import SuspiciousOperation
from django.utils.cache import patch_vary_headers
from django.utils.deprecation import MiddlewareMixin
from django.utils.http import http_date

from threading import current_thread
from django.middleware.common import CommonMiddleware

from app.seguridad.domain.models import LogActivity

_requests = {}


def get_username():
    t = current_thread()
    if t not in _requests:
        return None
    return _requests[t]


class RequestMiddleware(CommonMiddleware):
    def process_request(self, request):
        _requests[current_thread()] = request

        #Log
        user_agent = request.META.get("HTTP_USER_AGENT")
        print('META: ', request.META)

        #TODO: https://allwin-raju-12.medium.com/django-get-browser-and-os-info-from-the-http-requests-ae32147a9519

        #request.user_agent.browser.family  # returns 'Safari'
        #request.user_agent.browser.version  # returns (14, 0)
        #request.user_agent.browser.version_string  # returns '14.0'

        #version = (10, 15, 6), version_string = '10.15.6')request.user_agent.os.family  # returns 'Mac OS X'
        #request.user_agent.os.version  # returns (10, 15, 6)
        #request.user_agent.os.version_string  # returns '10.15.6'

        oagent = request.user_agent

        print('browser', oagent.browser)
        print('so', oagent.os)
        print('device', oagent.device)
        stype = LogActivity.TIPO_OTHER
        if oagent.is_mobile:
            stype = LogActivity.TIPO_MOBILE
        if oagent.is_tablet:
            stype = LogActivity.TIPO_TABLET
        if oagent.is_pc:
            stype = LogActivity.TIPO_PC



        log = LogActivity(
            user=request.user if request.user.is_authenticated else None,
            user_agent=user_agent,
            path=request.get_full_path(),
            ip_address=request.META.get('REMOTE_ADDR'),
            referer=request.META.get('HTTP_REFERER'),
            content_type=request.META.get('CONTENT_TYPE'),
            method=request.META.get('REQUEST_METHOD'),
            is_ajax=request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest',
            browser=oagent.browser.family,
            system=oagent.os.family,
            type=stype
        )
        log.save()



class RemoteUserMiddleware(CommonMiddleware):
    def process_response(self, request, response):
        if request.user.is_authenticated:
            response['X-Remote-User-Name'] = request.user.correo_electronico
        return response

class SessionMiddleware(MiddlewareMixin):
    """
    Personalización de SessionMiddleware, para adaptar a necesidades puntuales
    1. Aplica request.session.get('NOT_SESSION_SAVE', False) para no guardar la sesión (Evitar guardar expire_date en la sesión)
    """
    def __init__(self, get_response=None):
        self.get_response = get_response
        engine = import_module(settings.SESSION_ENGINE)
        self.SessionStore = engine.SessionStore

    def process_request(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        request.session = self.SessionStore(session_key)

    def process_response(self, request, response):
        """
        If request.session was modified, or if the configuration is to save the
        session every time, save the changes and set a session cookie or delete
        the session cookie if the session has been emptied.
        """
        try:
            accessed = request.session.accessed
            modified = request.session.modified
            empty = request.session.is_empty()
        except AttributeError:
            pass
        else:
            # First check if we need to delete this cookie.
            # The session should be deleted only if the session is entirely empty
            if settings.SESSION_COOKIE_NAME in request.COOKIES and empty:
                response.delete_cookie(
                    settings.SESSION_COOKIE_NAME,
                    path=settings.SESSION_COOKIE_PATH,
                    domain=settings.SESSION_COOKIE_DOMAIN,
                )
            else:
                if accessed:
                    patch_vary_headers(response, ('Cookie',))
                if (modified or settings.SESSION_SAVE_EVERY_REQUEST) and not empty:
                    if request.session.get_expire_at_browser_close():
                        max_age = None
                        expires = None
                    else:
                        max_age = request.session.get_expiry_age()
                        expires_time = time.time() + max_age
                        expires = http_date(expires_time)
                    # Save the session data and refresh the client cookie.
                    # Skip session save for 500 responses, refs #3881.
                    # dmunoz: Skip when request.session["NOT_SESSION_SAVE"] is set to True
                    if response.status_code != 500 and request.session.get('NOT_SESSION_SAVE', False) == False:
                        try:
                            request.session.save()
                        except UpdateError:
                            raise SuspiciousOperation(
                                "The request's session was deleted before the "
                                "request completed. The user may have logged "
                                "out in a concurrent request, for example."
                            )
                        response.set_cookie(
                            settings.SESSION_COOKIE_NAME,
                            request.session.session_key, max_age=max_age,
                            expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                            path=settings.SESSION_COOKIE_PATH,
                            secure=settings.SESSION_COOKIE_SECURE or None,
                            httponly=settings.SESSION_COOKIE_HTTPONLY or None,
                            samesite=settings.SESSION_COOKIE_SAMESITE,
                        )
        return response