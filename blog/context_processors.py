from django.conf import settings

from .models import Category


def categories(request):
    categories = Category.objects.all()
    return {'categories': categories, 'languages': settings.LANGUAGES}
