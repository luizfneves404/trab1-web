from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView, TemplateView

from .forms import RegistrationForm


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


register_view = RegisterView.as_view()
home_view = HomeView.as_view()
login_view = LoginView.as_view(
    template_name="registration/login.html",
    redirect_authenticated_user=True,
)
logout_view = LogoutView.as_view(next_page=reverse_lazy("users:login"))
