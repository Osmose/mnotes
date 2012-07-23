import iso8601
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from mnotes.base.util import JSONPResponse, JSONResponse
from mnotes.tasks.models import Task
from mnotes.users.models import APIKey


def task_list(request):
    return render(request, 'tasks/task_list.html')


@require_POST
@csrf_exempt
@login_required
def tasks(request):
    """Sync a task list to the database."""
    tasks = request.POST.get('tasks')
    if tasks:
        tasks = json.loads(tasks)
        user = request.user
        for task in tasks:
            server_task = None
            try:
                server_task = Task.objects.get(id=task['id'])
            except (Task.DoesNotExist, KeyError):
                user.task_set.create(title=task['title'],
                                     is_done=task['is_done'])

            if server_task:
                task_updated = iso8601.parse_date(task['updated'])
                if task_updated > server_task.updated:
                    if task['_delete']:
                        server_task.delete()
                    else:
                        server_task.title = task['title']
                        server_task.is_done = task['is_done']
                        server_task.save()
    return JSONResponse({'tasks': list(request.user.task_set.values())})


def create_task(request):
    key = request.GET.get('key')
    if key:
        try:
            api_key = APIKey.objects.get(key=key)
        except APIKey.DoesNotExist:
            return JSONPResponse({'error': 'Invalid API Key!'}, status=401)
        user = api_key.user
        title = request.GET.get('title')
        if title:
            user.task_set.create(title=title, is_done=False)
            return JSONPResponse({'msg': 'Task created successfully!'})
        else:
            return JSONPResponse({'error': 'No title specified!'}, status=400)
    else:
        return JSONPResponse({'error': 'No API key provided!'}, status=401)
