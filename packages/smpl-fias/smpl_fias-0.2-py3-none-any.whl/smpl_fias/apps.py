
from django.apps import AppConfig


class FIAS_Config(AppConfig):

    name = 'smpl_fias'
    verbose_name = 'ФИАС'

    def ready(self):
        pass
