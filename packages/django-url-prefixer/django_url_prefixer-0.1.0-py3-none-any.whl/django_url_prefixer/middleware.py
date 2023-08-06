"""Attaches a prefix to all relative links."""

import re
from django.conf import settings


class URLPrefixer:
    """Attaches a prefix to all relative links."""

    def __init__(self, getResponse):
        if not hasattr(settings, 'URL_PREFIX'):
            raise Exception('`URL_PREFIX` not defined in settings.')

        self.getResponse = getResponse

    def __call__(self, request):
        response = self.getResponse(request)
        content = response.content.decode('utf-8')
        content = re.sub(
            r'(?<!(\/|<|\w|:))((\/)(\w{0,}))',
            f'{settings.URL_PREFIX}\\2',
            content,
        )
        response.content = content.encode('utf-8')
        return response
