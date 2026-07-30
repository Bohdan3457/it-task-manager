from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Position, Task, TaskType


class PublicViewsTests(TestCase):
    def test_login_required_for_tasks_list(self) -> None:
        response = self.client.get(reverse('task_manager:task-list'))
        self.assertNotEqual(response.status_code, 200)


class PrivateViewsTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name='Developer')
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password123',
            position=self.position,
        )
        self.client.force_login(self.user)

        self.task_type = TaskType.objects.create(name='Bugfix')
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            deadline='2026-12-31',
            priority='Urgent',
            task_type=self.task_type,
        )

    def test_retrieve_index_page(self) -> None:
        response = self.client.get(reverse('task_manager:index'))
        self.assertEqual(response.status_code, 200)

    def test_retrieve_task_list(self) -> None:
        response = self.client.get(reverse('task_manager:task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_task_list_filter_by_name(self) -> None:
        response = self.client.get(
            reverse('task_manager:task-list'),
            {'name': 'Test'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

        response_empty = self.client.get(
            reverse('task_manager:task-list'),
            {'name': 'NonExistingTask'},
        )
        self.assertNotContains(response_empty, self.task.name)

    def test_retrieve_worker_list(self) -> None:
        response = self.client.get(reverse('task_manager:worker-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
