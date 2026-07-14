from django import forms
from .models import Task, Worker
from django.contrib.auth.forms import UserCreationForm

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "is_completed", "priority", "task_type", "assignees"]
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}),
        }


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "position")
