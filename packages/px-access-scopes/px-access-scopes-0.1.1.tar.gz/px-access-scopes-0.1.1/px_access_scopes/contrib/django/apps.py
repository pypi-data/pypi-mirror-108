from django.apps import AppConfig
from django.utils.translation import pgettext_lazy
from django.db.models.signals import post_migrate

from .discover import autodiscover


__all__ = ('AccessScopesConfig',)


class AccessScopesConfig(AppConfig):
    name = 'px_access_scopes.contrib.django'
    label = 'pxd_access_scopes'
    verbose_name = pgettext_lazy('pxd_access_scopes', 'Access scopes')

    def ready(self):
        # post_migrate.connect(
        #     generate_database,
        #     dispatch_uid="px_access_scopes.contrib.django.cases.db.generate_database"
        # )

        autodiscover()
