from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(
        null = True,
        blank = True,
    )
    email = models.EmailField(
        unique = True
    )

    profile_picture = models.ImageField(
        null = True,
        blank = True,
        upload_to = 'images/',
    )

class Transactions(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        choices = [('income', 'Income'), ('expense', 'Expense')],
        max_length = 255,
    )

    category = models.CharField(
        choices = [('rent', 'Rent'), ('utilities', 'Utilities'), ('food', 'Food'), ('groceries', 'Groceries'), ('entertainment', 'Entertainment'), ('misc', 'Miscellaneous')],
        max_length = 255,
        null = True,
        blank = True,
    )

    amount = models.DecimalField(
        max_digits = 30,
        decimal_places = 2,
    )
    transaction_date = models.DateField(
        default = timezone.now
    )
    memo = models.CharField(
        blank = True,
        max_length = 50,
    )

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} on {self.transaction_date}"

class Balance(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(
        max_digits = 30,
        decimal_places = 2,
        default = 0,
    )
    last_update = models.DateTimeField(
        auto_now = True
    )