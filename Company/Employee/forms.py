from django import forms
from django.contrib.auth.models import User
from Employee.models import Employee
from Departments.models import Department

class EmployeeSignupForm(forms.ModelForm):
    username = forms.CharField(max_length=150, help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.")
    password = forms.CharField(widget=forms.PasswordInput(), min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    class Meta:
        model = Employee
        fields = [
            'employee_name',
            'employee_age',
            'employee_address',
            'employee_department',
            'employee_reporting_manager',
            'employee_email',
        ]
        labels = {
            'employee_name': 'Full Name',
            'employee_age': 'Age',
            'employee_address': 'Address',
            'employee_department': 'Department',
            'employee_reporting_manager': 'Reporting Manager',
            'employee_email': 'Email Address',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to all fields for consistent styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'
            label_text = field.label or field_name.replace('_', ' ').title()
            field.widget.attrs['placeholder'] = f"Enter your {label_text.lower()}"

        # Customize password fields placeholders
        self.fields['password'].widget.attrs['placeholder'] = '••••••••'
        self.fields['confirm_password'].widget.attrs['placeholder'] = '••••••••'
        self.fields['username'].widget.attrs['placeholder'] = 'Choose a username'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data
