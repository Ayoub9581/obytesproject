from django import forms
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import messages


User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
	"""A form for creating new users. Includes all the required
	fields, plus a repeated password."""
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(
		label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('full_name', 'email',)  # 'full_name',)

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(UserAdminCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user


class UserAdminChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.
	"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = ('full_name', 'email', 'password', 'is_active', 'admin')

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control mb-4', 'placeholder': 'E-mail'}),
         			'password': forms.PasswordInput(attrs={'class': 'form-control mb-4', 'placeholder': 'Password'}),
        }

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get('email')
        password = data.get('password')
        qs = User.objects.filter(email=email)
        if qs.exists():
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                raise forms.ValidationError('this user is inactive')
        user = authenticate(request, username=email, password=password)
        if user is None:
            messages.warning(request, "Invalid credentials")
            raise forms.ValidationError('Invalid Credentials')
        login(request, user)
        self.user = user
        return data
