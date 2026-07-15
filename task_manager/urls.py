from django.urls import path

from .views import index, TaskListView, WorkerListView, PositionListView, TaskDetailView, TaskCreateView, \
    PositionCreateView, WorkerCreateView, TaskDeleteView, TaskUpdateView

app_name = "task_manager"

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task"),
    path("task/create/", TaskCreateView.as_view(), name="task-create"),
    path("position/create/", PositionCreateView.as_view(), name="position-create"),
    path("worker/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("task/delete/<int:pk>/", TaskDeleteView.as_view(), name="task-delete"),
    path("task/update/<int:pk>/", TaskUpdateView.as_view(), name="task-update")
]