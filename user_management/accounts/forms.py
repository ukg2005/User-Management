from django import forms
from .models import User

class UserTypeForm(forms.Form):
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, widget=forms.RadioSelect)

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_picture', 'username', 'email', 'password', 'address_line1', 'city', 'state', 'pincode', 'user_type']

    def __init__(self, *args, **kwargs):
        self.user_type_choice = kwargs.pop('user_type', None)
        super().__init__(*args, **kwargs)
        if self.user_type_choice:
            self.fields['user_type'].initial = self.user_type_choice

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match"
            )
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.user_type_choice = kwargs.pop('user_type', None)
        super().__init__(*args, **kwargs)
        if self.user_type_choice:
            self.fields['user_type'].initial = self.user_type_choice