from django.http import HttpResponse
from django.shortcuts import render
from .models import Worker, Position, Task


def index(request) -> HttpResponse:
    num_task = Task.objects.count()

    context = {
        "num_task": num_task,
    }

    return render(request, "task_manager/index.html", context=context)