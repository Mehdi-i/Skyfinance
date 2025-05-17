
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import CustomUser
from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError

class CustomSignupform(UserCreationForm):
    username = forms.CharField(widget = forms.TextInput(attrs = {'required': 'required',
                                                                'id': 'username',}))
    
    email = forms.EmailField(widget = forms.EmailInput(attrs = {'placeholder': 'xyz@email.com',
                                                                'required': 'required',
                                                                'id': 'Custom-email-field',}))
    
    password1 = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Must Be More Than 8 Characters',
                                                                'required': 'required',
                                                                'id': 'Custom-password-field-1',}))
    
    password2 = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Re-Enter Your Password',
                                                                'required': 'required',
                                                                'id': 'Custom-password-field-2',}))
    
    date_of_birth = forms.DateField(widget = forms.DateInput(attrs = {'type': 'date',
                                                                      'required': 'required',
                                                                      'id': 'Custom-dob',}))
    
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth > timezone.now().date():
            raise ValidationError('Woah there, time traveler!')
        return date_of_birth
    
    class Meta:
        model = CustomUser
        fields = ['username', 'date_of_birth', 'email', 'password1', 'password2']


class CustomLoginForm(forms.Form):
    email = forms.EmailField(widget = forms.EmailInput(attrs = {'required': 'required',
                                                                'id': 'Custom-email-field',}))
    
    password = forms.CharField(widget = forms.PasswordInput(attrs = {'required': 'required',
                                                                'id': 'Custom-password-field',}))


class CustomPasswordReset(PasswordResetForm):
    def save(self, request):
        return super().save(
            request=request,
            use_https=request.is_secure(),
            email_template_name='skyfinance_app/password_reset_email.html',
            subject_template_name='skyfinance_app/password_reset_subject.txt',
        )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'required': 'required',
            'id': 'email-verification',
        })
    )