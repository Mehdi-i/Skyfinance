from django.shortcuts import render, redirect
from .forms import CustomSignupform, CustomLoginForm, CustomPasswordReset
from .models import CustomUser
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = CustomSignupform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'skyfinance_app/signup.html', {'form': form})
    else:
        if request.user.is_authenticated:
            return redirect('overview')
        else:
            form = CustomSignupform()
            return render(request, 'skyfinance_app/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                form.add_error("email", "Email is incorrect")
                return render(request, 'skyfinance_app/login.html', {'form': form})

            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('overview')

            else:
                form.add_error("password", "Password is incorrect")
                return render(request, 'skyfinance_app/login.html', {'form': form})

        else:
            return render(request, 'skyfinance_app/login.html', {'form': form})

    else:
        if request.user.is_authenticated:
            return redirect('overview')
        else:
            form = CustomLoginForm()
            return render(request, 'skyfinance_app/login.html', {'form': form})
    

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordReset
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'skyfinance_app/email_verification.html', {'form': form})
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                CustomUser.objects.get(email = email)
                form.save(request = request)
                return redirect('login')
            except CustomUser.DoesNotExist:
                form.add_error("email", "Email Does Not Exist!")
                return render(request, 'skyfinance_app/email_verification.html', {'form': form})   
        else:
            form = self.form_class()
            return render(request, 'skyfinance_app/email_verification.html', {'form': form})


def overview_view(request):
    return render(request, 'skyfinance_app/overview.html')