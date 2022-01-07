from django.apps import AppConfig


class BaseUiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_ui'
