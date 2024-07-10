from django.conf import settings
from django.shortcuts import redirect
from django.utils import translation


def set_language(request, language_code):
    if language_code in dict(settings.LANGUAGES).keys():
        request.session[settings.LANGUAGE_SESSION_KEY] = language_code
        translation.activate(language_code)
    return redirect(request.META.get('HTTP_REFERER', '/'))
