from django.conf import settings
from logzero import logger

from proofdock.rp.contrib.django.config import DjangoConfig
from proofdock.rp.core import chaos


class DjangoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        try:
            if settings.CHAOS_MIDDLEWARE:
                config = DjangoConfig(settings.CHAOS_MIDDLEWARE)
                chaos.register(config, ["python.django.request"])

        except Exception as ex:
            logger.error("Unable to configure chaos middleware. Error: %s", ex, stack_info=True)

    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.

        response = self.get_response(request)
        attack_ctx = {"type": "python.django.request", "params": {"route": request.path}}
        chaos.attack(attack_ctx)

        return response
