from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        input_field_style = {
        'class': 'bg-gray-50  border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'}
        image_field_style={
            'class':'block w-full p-2.5 text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400'
        }
        fields =['email','password']
        widgets = {
            'password': forms.PasswordInput(attrs={**input_field_style,"placeholder":"Enter the password"}),  # Optional if you want to control widget type
            'email':forms.EmailInput(attrs={**input_field_style,"placeholder":"Email address"}),
            # 'first_name':forms.TextInput(attrs={**input_field_style}),
            # 'last_name':forms.TextInput(attrs={**input_field_style}),
            'phone_number':forms.NumberInput(attrs={**input_field_style}),
            # 'profile_img':forms.FileInput(attrs={**image_field_style}),
            
        }

    