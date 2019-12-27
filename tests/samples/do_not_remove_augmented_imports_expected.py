from django.conf.global_settings import AUTHENTICATION_BACKENDS


AUTHENTICATION_BACKENDS += ("foo.bar.baz.EmailBackend",)
