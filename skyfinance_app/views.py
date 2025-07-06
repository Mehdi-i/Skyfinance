from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomSignupform, CustomLoginForm, CustomPasswordReset, UserBalance, AddTransaction, Settings
from .models import CustomUser, Transactions, Balance
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum

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
                user = CustomUser.objects.get(email = email)
            except CustomUser.DoesNotExist:
                form.add_error("email", "Email is incorrect")
                return render(request, 'skyfinance_app/login.html', {'form': form})

            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')

            else:
                form.add_error("password", "Password is incorrect")
                return render(request, 'skyfinance_app/login.html', {'form': form})

        else:
            return render(request, 'skyfinance_app/login.html', {'form': form})

    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
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


@login_required
def dashboard_view(request):
    query_transactions = Transactions.objects.filter(user = request.user).order_by('-transaction_date')
    query_balance, _ = Balance.objects.get_or_create(user = request.user)
    income_total = Transactions.objects.filter(user = request.user, transaction_type = 'income').aggregate(Sum('amount'))['amount__sum'] or "{:.2f}".format(0.00)
    expense_total = Transactions.objects.filter(user = request.user, transaction_type = 'expense').aggregate(Sum('amount'))['amount__sum'] or "{:.2f}".format(0.00)
    form = AddTransaction()
    choices = form.fields['transaction_type'].choices
    categories = form.fields['category'].choices

    transaction_type = request.GET.get('type')
    category = request.GET.get('category')
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')
    filter_applied = False 

    if transaction_type:
        query_transactions = query_transactions.filter(transaction_type = transaction_type)
        filter_applied = True
    if category:
        query_transactions = query_transactions.filter(category = category)
        filter_applied = True
    if start and end:
        query_transactions = query_transactions.filter(transaction_date__range = [start, end])
        filter_applied = True
    elif start:
        query_transactions = query_transactions.filter(transaction_date__gte = start)
        filter_applied = True
    elif end:
        query_transactions = query_transactions.filter(transaction_date__lte = end)
        filter_applied = True
    no_result = not query_transactions.exists()

    paginator = Paginator(query_transactions, 5)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    visible_page_count = 5
    current_page = page_object.number
    total_pages = paginator.num_pages

    start_index = max(current_page - visible_page_count // 2, 1)
    end_index = min(start_index + visible_page_count - 1, total_pages)

    if end_index - start_index < visible_page_count - 1:
        start_index = max(end_index - visible_page_count + 1, 1)
    
    custom_page_range = range(start_index, end_index + 1)
    return render(request, 'skyfinance_app/dashboard.html', {'page_object': page_object, 'custom_page_range': custom_page_range, 
                                                                'transaction_type_choices': choices, 'transaction_categories': categories,
                                                                'no_result': no_result, 'filter': filter_applied, 'balance': query_balance.balance,
                                                                'income': income_total, 'expense': expense_total})


@login_required
def add_transaction_view(request):
    add_transaction_form = AddTransaction()

    if request.method == 'POST':
        add_transaction_form = AddTransaction(request.POST)
        if add_transaction_form.is_valid():
            transaction = add_transaction_form.save(commit = False)
            transaction.user = request.user
            add_transaction_form.save()
            current_balance = Balance.objects.get(user = request.user)
            
            if transaction.transaction_type == 'income':
                current_balance.balance += transaction.amount
            else:
                current_balance.balance -= transaction.amount
            current_balance.save()
            return redirect('dashboard')

    context = {
        'add_transaction_form': add_transaction_form,
    }
    return render(request, 'skyfinance_app/add_transaction.html', context)

@login_required
def edit_transaction_view(request, pk):
    transaction = get_object_or_404(Transactions, pk = pk)
    old_amount = transaction.amount
    old_type = transaction.transaction_type
    if request.method == 'POST':
        form = AddTransaction(request.POST, instance = transaction)
        if form.is_valid():
            edit_transaction = form.save(commit = False)
            new_amount = form.cleaned_data['amount']
            new_type = form.cleaned_data['transaction_type']
            current_balance = Balance.objects.get(user = request.user)

            if old_amount != new_amount or old_type != new_type:
                if old_type == 'income':
                    current_balance.balance -= old_amount
                else:
                    current_balance.balance += old_amount
                if new_type == 'income':
                    current_balance.balance += new_amount
                else:
                    current_balance.balance -= new_amount

                current_balance.save()

            edit_transaction.user = request.user
            edit_transaction.save()

            return redirect('dashboard')
        else:
            return render(request, 'skyfinance_app/edit_transaction.html', {'form': form, 'transaction': transaction})

    else:
        form = AddTransaction(instance = transaction)
        return render(request, 'skyfinance_app/edit_transaction.html', {'form': form, 'transaction': transaction})


@login_required
def delete_transaction_view(request, pk):
    transaction = get_object_or_404(Transactions, pk = pk, user = request.user)
    if request.method == 'POST':
        transaction.delete()
        current_balance = Balance.objects.get(user = request.user)
            
        if transaction.transaction_type == 'income':
            current_balance.balance -= transaction.amount
        else:
            current_balance.balance += transaction.amount
        current_balance.save()
        return redirect('dashboard')
    else:
        return render(request, 'skyfinance_app/transaction_delete_confirm.html', {'transaction': transaction})


@login_required
def settings_view(request):
    user = request.user
    if request.method == 'POST':
        form = Settings(request.POST, request.FILES, instance=user)

        if request.POST.get('remove_profile_picture'):
            user.profile_picture.delete(save = False)
            user.profile_picture = None

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    else:
        form = Settings(instance = user)

    return render(request, 'skyfinance_app/edit_profile.html', {'form': form})
