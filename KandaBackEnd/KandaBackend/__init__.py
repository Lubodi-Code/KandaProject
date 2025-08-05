# Este archivo inicializa la aplicación Celery

# Importar la función shared_task de celery
from __future__ import absolute_import, unicode_literals

# Asegurar que la aplicación Celery se carga cuando Django inicia
from .celery import app as celery_app

__all__ = ('celery_app',)