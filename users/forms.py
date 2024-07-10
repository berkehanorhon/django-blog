from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.utils.translation import gettext_lazy as _


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = widgets.EmailInput(
            attrs={'placeholder': _("Write your email here.."), "class": "form-control"})
        self.fields['password'].widget = widgets.PasswordInput(
            attrs={'placeholder': _("Write your password here.."), "class": "form-control"})


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget = widgets.TextInput(
            attrs={'placeholder': _("First Name"), "class": "form-control"})
        self.fields['sur_name'].widget = widgets.TextInput(
            attrs={'placeholder': _("Surname"), "class": "form-control"})
        self.fields['email'].widget = widgets.EmailInput(
            attrs={'placeholder': _("Write your email here.."), "class": "form-control"})
        self.fields['password1'].widget = widgets.PasswordInput(
            attrs={'placeholder': _("Write your password here.."), "class": "form-control"})
        self.fields['password2'].widget = widgets.PasswordInput(
            attrs={'placeholder': _("Write your password again.."), "class": "form-control"})
        self.fields['description'].widget = widgets.Textarea(
            attrs={'placeholder': _(
                "Write something about yourself.. It will be shown in your author profile page. Maximum 500 characters."),
                "class": "form-control"})
        self.fields['avatar'].widget = widgets.FileInput(
            attrs={'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError(_("Email address already in use."))
        return email

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) > 500:
            raise ValidationError(_("Description cannot be longer than 500 characters."))
        return description

    class Meta:
        model = get_user_model()
        fields = ("first_name", "sur_name", "email", "password1", "password2", "description", "avatar")
