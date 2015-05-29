from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

# django-social-auth doesn't actually send this signal
@receiver(user_logged_in)
def login(sender, request, **kwargs):
    request.session.set_expiry(1209600) # 2 weeks

@receiver(user_logged_out)
def logout(sender, request, **kwargs):
    request.session.set_expiry(0) # until browser is closed
