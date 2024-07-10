from django.conf import settings
from django.utils import translation


class CustomLocaleMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.get(settings.LANGUAGE_SESSION_KEY):
            request.session[settings.LANGUAGE_SESSION_KEY] = settings.LANGUAGE_CODE
        language = request.session.get(settings.LANGUAGE_SESSION_KEY)
        translation.activate(language)
        request.LANGUAGE_CODE = language
        response = self.get_response(request)
        translation.deactivate()
        return response
