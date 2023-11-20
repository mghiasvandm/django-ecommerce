from django.apps import AppConfig
from django.utils.translation import ugettext as _

class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
    verbose_name = "فروشگاه"
