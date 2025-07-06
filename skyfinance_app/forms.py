
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import CustomUser, Transactions, Balance
from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserChangeForm
from decimal import Decimal

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
            request = request,
            use_https = request.is_secure(),
            email_template_name = 'skyfinance_app/password_reset_email.html',
            subject_template_name = 'skyfinance_app/password_reset_subject.txt',
        )

    email = forms.EmailField(
        widget = forms.EmailInput(attrs = {
            'required': 'required',
            'id': 'email-verification',
        })
    )

class AddTransaction(forms.ModelForm):
    transaction_type = forms.ChoiceField(choices = [('', 'Choose an option'), ('income', 'Income'), ('expense', 'Expense')],
                                         widget = forms.Select(attrs = {'required': 'required',
                                                                        'id': 'transaction_type',
    }))

    category = forms.ChoiceField(required = False, choices = [('', 'Choose an option'), ('rent', 'Rent'), ('utilities', 'Utilities'), ('food', 'Food'), ('groceries', 'Groceries'), 
                                            ('entertainment', 'Entertainment'), ('misc', 'Miscellaneous')],
                                            widget = forms.Select(attrs = {'id': 'transaction_category',
    }))

    amount = forms.DecimalField(widget = forms.NumberInput(attrs = {'required': 'required',
                                                                    'id': 'amount',                                                            
    }))

    transaction_date = forms.DateField(required = False, initial = timezone.now().date(), widget = forms.DateInput(attrs = {'id': 'transaction_date',
                                                                                                                            'type': 'date',
    }))

    memo = forms.CharField(max_length = 50, required = False,
                         widget = forms.Textarea(attrs = {'id': 'memo',}))

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        category = cleaned_data.get('category')

        if transaction_type == 'expense' and (category == '' or category is None):
            self.add_error('category', 'This field is required for expense transactions.')
        elif transaction_type == 'income': 
            cleaned_data['category'] = ''

    class Meta:
        model = Transactions
        fields = ['transaction_type', 'category', 'amount', 'transaction_date', 'memo',]


class UserBalance(forms.ModelForm):
    balance = forms.DecimalField(required = False,
                                widget = forms.NumberInput(attrs = {'id': 'balance',}))
    class Meta:
        model = Balance
        fields = ['balance']


class Settings(UserChangeForm):
    balance = forms.DecimalField(required = False,
                                widget = forms.NumberInput(attrs={'id': 'balance',}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        try:
            self.fields['balance'].initial = self.user.balance.balance
        except Balance.DoesNotExist:
            self.fields['balance'].initial = 0

    def clean_balance(self):
        balance = self.cleaned_data.get('balance')
        min_limit = Decimal('-99999999.99')
        max_limit = Decimal('99999999.99')

        if balance is not None and (balance < min_limit or balance > max_limit):
            raise forms.ValidationError("Ensure that there are no more than 10 digits in total.")
        return balance

    def save(self, commit = True):
        user = super().save(commit = False)

        balance_value = self.cleaned_data.get('balance')
        balance_obj, _ = Balance.objects.get_or_create(user = user)
        balance_obj.balance = balance_value
        balance_obj.save()

        if commit:
            user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ['username', 'profile_picture']
