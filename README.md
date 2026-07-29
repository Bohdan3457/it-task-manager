# TaskDesk - IT Task Management System

TaskDesk is a full-featured web application designed for IT companies to streamline task management, track team workloads, and oversee project progress. The platform provides intuitive dashboard metrics, flexible filtering options, and custom role assignments.

## Core Features

- Dashboard: Real-time metrics for total tasks, team members, and positions, along with automated completion rate calculations.
- Task Management: Full CRUD functionality to create, edit, view details, and delete tasks, plus one-click status toggling.
- Filtering and Search: Quick lookup by task name or developer username with multi-attribute filtering by Task Type, Priority, Position, and Status.
- Team and Position Tracking: Manage workers with specific position bindings and review individual workloads.
- Authentication and Security: Restricted access for non-authenticated users using LoginRequiredMixin and a custom user model.
- Automated Testing: Integration testing via Django TestCase covering HTTP status codes, authorization restrictions, and GET filters.

## Demo Credentials

You can test all application features using the pre-configured superuser account:

- URL: [http://127.0.0.1:8000/accounts/login/](http://127.0.0.1:8000/accounts/login/)
- Username: adminuser
- Password: Admintest123!

This account has full administrator privileges to create, edit, and manage all records.