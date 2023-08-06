from django.utils.module_loading import autodiscover_modules

from .conf import settings


__all__ = 'autodiscover',


def autodiscover():
    autodiscover_modules(settings.AUTOLOAD_MODULE)
