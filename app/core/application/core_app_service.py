class CoreAppService(object):

    @staticmethod
    def get_request_ip_all(request):
        return request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '127.0.0.1'))

    @staticmethod
    def get_request_ip(request):
        REMOTE_ADDR = CoreAppService.get_request_ip_all(request)
        request.META['REMOTE_ADDR'] = REMOTE_ADDR.split(',')[0].strip()
        return request.META.get("REMOTE_ADDR", None)

    @staticmethod
    def es_ip_campus(request, ips=None):
        if ips:
            ip = CoreAppService.get_request_ip(request)
            for srip in ips:
                vip = ip.split('.')
                rip = srip.split('.')
                for i, oct in enumerate(rip):
                    if oct == '*':
                        vip[i] = '*'
                print(vip, rip, vip == rip)
                if vip == rip:
                    return True
            return False
        return None