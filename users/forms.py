from django import forms
from .models import User


class UserForm(forms.ModelForm):
    confirm_pass = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password','class': 'bg-gray-50  border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'}),
        label="Confirm Password"
    )
    class Meta:
        model = User
        input_field_style = {
            'class': 'bg-gray-50  border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'}
        image_field_style = {
            'class': 'block w-full p-2.5 text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400'
        }
        fields = ['email', 'password','confirm_pass']
        widgets = {
            # Optional if you want to control widget type
            'password': forms.PasswordInput(attrs={**input_field_style, "placeholder": "Enter the password"}),
            'email': forms.EmailInput(attrs={**input_field_style, "placeholder": "Email address"}),
            # 'first_name':forms.TextInput(attrs={**input_field_style}),
            # 'last_name':forms.TextInput(attrs={**input_field_style}),
            'phone_number': forms.NumberInput(attrs={**input_field_style}),
            # 'profile_img':forms.FileInput(attrs={**image_field_style}),

        }
        
    def clean(self):
        cleaned_data= super().clean()
        password= cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_pass')
        if password and confirm_password and confirm_password!=password:
            self.add_error("confirm_pass","Password is not match.")
            
    def save(self, commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()        
            return user
        


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
    field_style={
        'class': 'w-10 h-10 sm:w-12 sm:h-12 md:w-14 md:h-14 text-center text-xl sm:text-2xl font-extrabold text-slate-900 bg-slate-100 border border-transparent hover:border-slate-200 appearance-none rounded p-2 sm:p-3 md:p-4 outline-none focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100',
        'inputmode': 'numeric',
        'autocomplete': 'off',
        "maxlength": "1",
    }
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        for i in range(1, 7):  # otp_1 to otp_6
            self.fields[f'otp_{i}'] = forms.CharField(
                max_length=1,
                required=True,
                widget=forms.TextInput(attrs=self.field_style)
            )
        
    def get_otp(self):
         return int(''.join([
            self.cleaned_data.get(f'otp_{i}', '') for i in range(1, 7)
        ]))


class RestPassword(forms.Form):
    input_field_style = {
        'class': 'bg-gray-50  border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'}

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={**input_field_style, "placeholder": "Enter your email id" }))
