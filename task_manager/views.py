from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View, generic

from task_manager.models import Position, Task, TaskType, Worker


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()
    num_positions = Position.objects.count()

    num_completed_tasks = Task.objects.filter(is_completed=True).count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_workers': num_workers,
        'num_tasks': num_tasks,
        'num_positions': num_positions,
        'num_completed_tasks': num_completed_tasks,
        'num_visits': num_visits + 1,
    }

    return render(request, 'task_manager/index.html', context=context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = 'task_manager/task_list.html'
    context_object_name = 'task_list'
    paginate_by = 10

    def get_queryset(self) -> QuerySet:
        queryset = (
            Task.objects.select_related('task_type').prefetch_related(
                'assignees__position'
            )
        )

        name = self.request.GET.get('name')
        task_type = self.request.GET.get('task_type')
        priority = self.request.GET.get('priority')
        status = self.request.GET.get('status')
        position = self.request.GET.get('position')

        if name:
            queryset = queryset.filter(name__icontains=name)

        if task_type:
            queryset = queryset.filter(task_type_id=task_type)

        if priority:
            queryset = queryset.filter(priority=priority)

        if status == 'completed':
            queryset = queryset.filter(is_completed=True)
        elif status == 'in_progress':
            queryset = queryset.filter(is_completed=False)

        if position:
            queryset = queryset.filter(
                assignees__position__id=position
            ).distinct()

        return queryset

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['task_types'] = TaskType.objects.all()
        context['positions'] = Position.objects.all()
        return context


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = 'task_manager/task_detail.html'


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = '__all__'
    template_name = 'task_manager/task_form.html'
    success_url = reverse_lazy('task_manager:task-list')


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'task_manager/task_form.html'
    success_url = reverse_lazy('task_manager:task-list')


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = 'task_manager/task_confirm_delete.html'
    success_url = reverse_lazy('task_manager:task-list')


class TaskToggleStatusView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        task = get_object_or_404(Task, pk=pk)
        task.is_completed = not task.is_completed
        task.save()
        return redirect(
            request.META.get('HTTP_REFERER', 'task_manager:task-list')
        )


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    template_name = 'task_manager/worker_list.html'
    context_object_name = 'worker_list'
    paginate_by = 10

    def get_queryset(self) -> QuerySet:
        queryset = Worker.objects.select_related('position')

        username = self.request.GET.get('username')
        position = self.request.GET.get('position')

        if username:
            queryset = queryset.filter(
                Q(username__icontains=username)
                | Q(first_name__icontains=username)
                | Q(last_name__icontains=username)
            )

        if position:
            queryset = queryset.filter(position_id=position)

        return queryset

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['positions'] = Position.objects.all()
        return context


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    template_name = 'task_manager/worker_detail.html'


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = UserCreationForm
    template_name = 'task_manager/worker_form.html'
    success_url = reverse_lazy('task_manager:worker-list')


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    fields = ['username', 'first_name', 'last_name', 'email', 'position']
    template_name = 'task_manager/worker_form.html'
    success_url = reverse_lazy('task_manager:worker-list')


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    template_name = 'task_manager/worker_confirm_delete.html'
    success_url = reverse_lazy('task_manager:worker-list')


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    template_name = 'task_manager/position_list.html'
    context_object_name = 'position_list'
    paginate_by = 10

    def get_queryset(self) -> QuerySet:
        queryset = Position.objects.all()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position
    template_name = 'task_manager/position_detail.html'


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = '__all__'
    template_name = 'task_manager/position_form.html'
    success_url = reverse_lazy('task_manager:position-list')


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = '__all__'
    template_name = 'task_manager/position_form.html'
    success_url = reverse_lazy('task_manager:position-list')


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    template_name = 'task_manager/position_confirm_delete.html'
    success_url = reverse_lazy('task_manager:position-list')
