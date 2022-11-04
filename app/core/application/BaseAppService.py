
class BaseAppService(object):

    @staticmethod
    def get_choice_display(choices, key, default=None):
        d = dict(choices)
        return d.get(key, default)

