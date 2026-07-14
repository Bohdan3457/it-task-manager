from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "is_completed", "priority", "task_type", "assignees"]
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}),
        }
