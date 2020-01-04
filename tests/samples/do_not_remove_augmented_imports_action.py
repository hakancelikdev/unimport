from django.conf.global_settings import AUTHENTICATION_BACKENDS, TEMPLATE_CONTEXT_PROCESSORS


AUTHENTICATION_BACKENDS += ("foo.bar.baz.EmailBackend",)
