from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import TaskForm, WorkerCreationForm
from .models import Position, Task, Worker


@login_required
def index(request) -> HttpResponse:
    context = {
        "num_task": Task.objects.count(),
        "num_worker": Worker.objects.count(),
        "num_position": Position.objects.count(),
    }
    return render(request, "task_manager/index.html", context=context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "task_manager/task_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = Task.objects.all().select_related("task_type")
        title_search = self.request.GET.get("title")

        if title_search:
            queryset = queryset.filter(name__icontains=title_search)

        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "task_manager/task_detail.html"
    context_object_name = "task"

    def get_queryset(self):
        return Task.objects.all().prefetch_related("assignees")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_manager/task_form.html"
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_manager/task_update.html"
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "task_manager/task_delete.html"
    success_url = reverse_lazy("task_manager:task-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    context_object_name = "worker_list"
    template_name = "task_manager/worker_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = Worker.objects.all().select_related("position")
        title_search = self.request.GET.get("username")

        if title_search:
            queryset = queryset.filter(username__icontains=title_search)

        return queryset

class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    template_name = "task_manager/worker_form.html"
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    fields = ["first_name", "last_name", "email", "position", "username"]
    template_name = "task_manager/worker_update.html"
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    template_name = "task_manager/worker_delete.html"
    success_url = reverse_lazy("task_manager:worker-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    context_object_name = "position_list"
    template_name = "task_manager/position_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = Position.objects.all()
        title_search = self.request.GET.get("name")

        if title_search:
            queryset = queryset.filter(name__icontains=title_search)

        return queryset


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = ["name"]
    template_name = "task_manager/position_form.html"
    success_url = reverse_lazy("task_manager:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = ["name"]
    template_name = "task_manager/position_update.html"
    success_url = reverse_lazy("task_manager:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    template_name = "task_manager/position_delete.html"
    success_url = reverse_lazy("task_manager:position-list")
