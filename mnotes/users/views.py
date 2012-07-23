from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django_browserid import get_audience

from mnotes.base.util import JSONResponse
from mnotes.users.models import APIKey


def get_user(request):
    """Returns a JSON representation of the current user, or a 404."""
    if request.user.is_authenticated():
        user = {
            'id': request.user.id,
            'email': request.user.email,
            'key': APIKey.objects.get(user=request.user).key
        }
        return JSONResponse({'user': user})
    else:
        return JSONResponse({'error': 'No user logged in.'}, status=404)


@require_POST
@csrf_exempt
def login(request):
    assertion = request.POST.get('assertion')
    if assertion is not None:
        audience = get_audience(request)
        user = auth.authenticate(assertion=assertion, audience=audience)
        if user and user.is_active:
            auth.login(request, user)
    return get_user(request)


@require_POST
@csrf_exempt
def logout(request):
    auth.logout(request)
    return JSONResponse({'msg': 'User logged out'})
