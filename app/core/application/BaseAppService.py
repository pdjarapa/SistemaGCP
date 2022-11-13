
class BaseAppService(object):
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def get_choice_display(choices, key, default=None):
        d = dict(choices)
        return d.get(key, default)

