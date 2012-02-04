from django.conf import settings


def settings_for_context(context):
    ret = {}
    settings_var_names = (
        'JQUERY_VERSION',
        'FACEBOOK_APP_ID',
    )
    for name in settings_var_names:
        if hasattr(settings, name):
            ret[name] = getattr(settings, name)
    return ret
