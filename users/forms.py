from collections.abc import Mapping
from typing import cast

from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.contrib.auth.models import User


CONTROL_CLASS = "input input-bordered w-full"


def _daisy_style_fields(fields: Mapping[str, forms.Field]) -> None:
    for field in fields.values():
        widget = field.widget
        if isinstance(widget, forms.CheckboxInput):
            widget.attrs.setdefault("class", "checkbox")
        elif isinstance(widget, forms.Textarea):
            widget.attrs.setdefault("class", "textarea textarea-bordered w-full")
        else:
            cast(forms.Widget, widget).attrs.setdefault("class", CONTROL_CLASS)


class DaisyFormMixin:
    def _style_fields(self: forms.BaseForm) -> None:
        _daisy_style_fields(self.fields)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-mail")

    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _daisy_style_fields(self.fields)


class LoginForm(DaisyFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class ResetPasswordForm(DaisyFormMixin, PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class NewPasswordForm(DaisyFormMixin, SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()
