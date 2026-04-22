import datetime
from typing import Any

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView, TemplateView

from tasks.models import Task
from tasks.models import TaskList

from .forms import LoginForm, NewPasswordForm, RegistrationForm, ResetPasswordForm


@method_decorator(
    sensitive_post_parameters("password1", "password2"),
    name="dispatch",
)
class RegisterView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.localdate()
        week_start = today - datetime.timedelta(days=today.weekday())

        base_qs = Task.objects.filter(owner=user)
        pending_qs = base_qs.filter(
            status__in=[Task.Status.PENDING, Task.Status.IN_PROGRESS]
        )

        ctx["count_pending"] = pending_qs.count()
        ctx["count_overdue"] = pending_qs.filter(due_date__lt=today).count()
        ctx["count_today"] = pending_qs.filter(
            Q(planned_date=today) | Q(due_date=today)
        ).count()
        ctx["count_completed_week"] = base_qs.filter(
            status=Task.Status.DONE, updated_at__date__gte=week_start
        ).count()

        ctx["task_lists"] = (
            TaskList.objects.filter(user=user)
            .annotate(
                pending_count=Count(
                    "tasks",
                    filter=Q(
                        tasks__status__in=[Task.Status.PENDING, Task.Status.IN_PROGRESS]
                    ),
                )
            )
            .order_by("name")
        )

        overdue = pending_qs.filter(due_date__lt=today).order_by("due_date")
        near_due = pending_qs.filter(
            due_date__gte=today, due_date__lte=today + datetime.timedelta(days=7)
        ).order_by("due_date")
        high_priority = pending_qs.filter(priority=Task.Priority.HIGH).order_by(
            "due_date"
        )

        seen_ids: set[int] = set()
        upcoming: list[Task] = []
        for task in list(overdue) + list(near_due) + list(high_priority):
            if task.pk not in seen_ids:
                seen_ids.add(task.pk)
                upcoming.append(task)

        ctx["upcoming_tasks"] = upcoming[:10]
        ctx["overdue_tasks"] = list(overdue[:5])
        ctx["completed_tasks"] = list(
            base_qs.filter(status=Task.Status.DONE).order_by("-updated_at", "-pk")[:5]
        )
        ctx["today"] = today
        return ctx


register_view = RegisterView.as_view()
home_view = HomeView.as_view()
login_view = LoginView.as_view(
    template_name="registration/login.html",
    authentication_form=LoginForm,
    redirect_authenticated_user=True,
)
logout_view = LogoutView.as_view(next_page=reverse_lazy("users:login"))
password_reset_view = PasswordResetView.as_view(
    template_name="registration/password_reset_form.html",
    form_class=ResetPasswordForm,
    email_template_name="registration/password_reset_email.html",
    subject_template_name="registration/password_reset_subject.txt",
    success_url=reverse_lazy("users:password_reset_done"),
)
password_reset_done_view = PasswordResetDoneView.as_view(
    template_name="registration/password_reset_done.html",
)
password_reset_confirm_view = PasswordResetConfirmView.as_view(
    template_name="registration/password_reset_confirm.html",
    form_class=NewPasswordForm,
    success_url=reverse_lazy("users:password_reset_complete"),
)
password_reset_complete_view = PasswordResetCompleteView.as_view(
    template_name="registration/password_reset_complete.html",
)
