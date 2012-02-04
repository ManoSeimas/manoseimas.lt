from django.conf import settings
from django.http import HttpResponseForbidden
from django.template import RequestContext, loader

from .models import Profile


def forbidden(request):
    t = loader.get_template('403.html')
    return HttpResponseForbidden(t.render(RequestContext(request)))


def login(request):
    path = request.get_full_path()
    from django.contrib.auth.views import redirect_to_login
    return redirect_to_login(path, settings.LOGIN_URL, 'next')


def karma_required(karma=None):
    """This view decorator restricts access to views.

    If ``karma`` is not specified, only authenticated user can access decorated
    view.

    If ``karma`` is specified, only authenticated users, that have greater than
    karma, than specified by name can access decorated view. All karma names
    are described in ``manoseimas.accounts.modes.KARMA_CHOICES``.

    If authenticated user is superuser, then karma restrictions will be
    ignored.

    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated():
                login(request)

            profile = Profile.objects.get_profile(request.user)
            if (karma is not None and not request.user.is_superuser and
                profile.karma < karma):
                return forbidden(request)

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
