from django.conf import settings


def settings_avaliable_to_templates(request):

    return {
        'CIVICUK_ID': settings.CIVICUK_ID,
        'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID
    }
