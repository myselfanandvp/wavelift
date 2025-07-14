from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        input_field_style = {
            'class': 'bg-gray-50  border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'}
        image_field_style = {
            'class': 'block w-full p-2.5 text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400'
        }
        fields = ['email', 'password']
        widgets = {
            # Optional if you want to control widget type
            'password': forms.PasswordInput(attrs={**input_field_style, "placeholder": "Enter the password"}),
            'email': forms.EmailInput(attrs={**input_field_style, "placeholder": "Email address"}),
            # 'first_name':forms.TextInput(attrs={**input_field_style}),
            # 'last_name':forms.TextInput(attrs={**input_field_style}),
            'phone_number': forms.NumberInput(attrs={**input_field_style}),
            # 'profile_img':forms.FileInput(attrs={**image_field_style}),

        }


class BaseLoginForm(forms.Form):
    input_field_style = {
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'
    }

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={**input_field_style, "placeholder": "Email address"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={**input_field_style, "placeholder": "Enter your password"})
    )


class LoginForm(BaseLoginForm):
    pass


class Admin_Login_Form(BaseLoginForm):
    pass


class Change_Password_Form(forms.Form):
    input_field_style = {
        'class': 'bg-gray-50  border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'}

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={**input_field_style, "placeholder": "New password", "autocomplete": "off"}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={**input_field_style, "placeholder": "Confirm Password", "autocomplete": "off"}))


class OTPVerificationForm(forms.Form):
    otp_1 = forms.CharField(max_length=1, required=True, widget=forms.TextInput(attrs={
        'class': 'w-14 h-14 text-center text-2xl font-extrabold text-slate-900 bg-slate-100 border border-transparent hover:border-slate-200 appearance-none rounded p-4 outline-none focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100',
        'inputmode': 'numeric',
        'autocomplete': 'off',
        "maxlength": "1",
    }))

    otp_2 = forms.CharField(max_length=1, required=True, widget=forms.TextInput(attrs={
        'class': 'w-14 h-14 text-center text-2xl font-extrabold text-slate-900 bg-slate-100 border border-transparent hover:border-slate-200 appearance-none rounded p-4 outline-none focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100',
        'inputmode': 'numeric',
        'autocomplete': 'off',
        "maxlength": "1",
    }))
    otp_3 = forms.CharField(max_length=1, required=True, widget=forms.TextInput(attrs={
        'class': 'w-14 h-14 text-center text-2xl font-extrabold text-slate-900 bg-slate-100 border border-transparent hover:border-slate-200 appearance-none rounded p-4 outline-none focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100',
        'inputmode': 'numeric',
        'autocomplete': 'off',
        "maxlength": "1",
    }))
    otp_4 = forms.CharField(max_length=1, required=True, widget=forms.TextInput(attrs={
        'class': 'w-14 h-14 text-center text-2xl font-extrabold text-slate-900 bg-slate-100 border border-transparent hover:border-slate-200 appearance-none rounded p-4 outline-none focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100',
        'inputmode': 'numeric',
        'autocomplete': 'off',
        "maxlength": "1",
    }))
    otp_5 = forms.CharField(max_length=1, required=True, widget=forms.TextInput(attrs={
        'class': 'w-14 h-14 text-center text-2xl font-extrabold text-slate-900 bg-slate-100 border border-transparent hover:border-slate-200 appearance-none rounded p-4 outline-none focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100',
        'inputmode': 'numeric',
        'autocomplete': 'off',
        "maxlength": "1",
    }))
    otp_6 = forms.CharField(max_length=1, required=True, widget=forms.TextInput(attrs={
        'class': 'w-14 h-14 text-center text-2xl font-extrabold text-slate-900 bg-slate-100 border border-transparent hover:border-slate-200 appearance-none rounded p-4 outline-none focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100',
        'inputmode': 'numeric',
        'autocomplete': 'off',
        "maxlength": "1",
    }))

    def get_otp(self):
        return ''.join([
            self.cleaned_data.get('otp_1', ''),
            self.cleaned_data.get('otp_2', ''),
            self.cleaned_data.get('otp_3', ''),
            self.cleaned_data.get('otp_4', ''),
            self.cleaned_data.get('otp_5', ''),
            self.cleaned_data.get('otp_6', ''),
        ])


class RestPassword(forms.Form):
    input_field_style = {
        'class': 'bg-gray-50  border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'}

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={**input_field_style, "placeholder": "Enter your email id" }))
