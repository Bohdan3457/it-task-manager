from django.http import HttpResponse
from django.shortcuts import render
from .models import Worker, Position, Task
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

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

class TaskListView(LoginRequiredMixin,generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "task_manager/task_list.html"
    
