from django.http import HttpResponse
from django.shortcuts import render
from .models import Worker, Position, Task


def index(request) -> HttpResponse:
    num_task = Task.objects.count()
    num_worker = Worker.objects.count()
    num_position = Position.objects.count()

    context = {
        "num_task": num_task,
        "num_worker": num_worker,
        "num_position": num_position,
    }

    return render(request, "task_manager/index.html", context=context)
