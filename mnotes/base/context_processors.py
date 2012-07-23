from django.conf import settings


def django_compressor_processor(request):
    """Adds settings from django_compressor."""
    return {'COMPRESS_URL': settings.COMPRESS_URL}
