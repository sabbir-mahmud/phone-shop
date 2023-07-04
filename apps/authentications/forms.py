from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(
        widget=forms.PasswordInput(), label='Confirm Password')

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'gender'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password1 is not None and password1 != password2:
            self.add_error("password2", "Your passwords must match")

        return cleaned_data

    def save(self, commit=True):

        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserAdminCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(
        widget=forms.PasswordInput(), label='Confirm Password')

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password1 is not None and password1 != password2:
            self.add_error("password2", "Your passwords must match")

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'admin']

    def clean_password(self):
        return self.initial["password"]
