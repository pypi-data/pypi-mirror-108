from dataclasses import dataclass
from px_settings.contrib.django import settings as s


__all__ = 'Settings', 'settings'


@s('PX_ACCESS_TOKENS')
@dataclass
class Settings:
    AUTOLOAD_MODULE: str = 'access_scopes'


settings = Settings()
