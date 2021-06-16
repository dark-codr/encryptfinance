from datetime import datetime, timedelta
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail, send_mass_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse
from django.utils import timezone
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from encryptfinance.wallets.models import Wallet

from .forms import DepositForm, RecoverForm, SupportForm, WithdrawalForm
from .models import Deposit, RecoverFunds, Support, Withdrawal

User = get_user_model()

# Create your views here.
class DebitLists(LoginRequiredMixin, ListView):
    model = Deposit
    template_name = "transactions/deposit_list.html"
    queryset = Deposit.objects.all()
    success_message = 'Deposit Verified'
    context_object_name = 'obj'
    allow_empty = True	
    paginate_by = 20

   

class WithdrawalLists(LoginRequiredMixin, ListView):
    model = Withdrawal
    template_name = "transactions/withdrawal_list.html"
    queryset = Withdrawal.objects.all()
    success_message = 'Withdrawal Verified'
    context_object_name = 'obj'
    allow_empty = True	
    paginate_by = 20

class DepositFormView(LoginRequiredMixin, CreateView):
    model = Deposit
    template_name = 'transactions/depositform.html'
    form_class = DepositForm


    def get_success_url(self):
        return reverse("transactions:walletID")

    def form_valid(self, form):
        form.instance.depositor = self.request.user
        user = form.instance.depositor
        email = user.email
        amount = form.instance.amount
        msg = """Your deposit of: ${amount} is pending and will be completed after you complete payment.\n\nPlease be patient while the transaction completes.""".format(amount=amount)
        sender = "noreply@encryptfinance.net"
        admin = "admin@encryptfinance.net"
        msg2="""Deposit request has been made for: ${amount}""".format(amount=amount)
        emails = (
            (
                'DEPOSIT REQUEST',
                msg,
                sender,
                [email]
            ),

            (
                'DEPOSIT REQUEST',
                msg2,
                sender,
                [admin]
            )
        )
        results = send_mass_mail(emails, fail_silently=False)
        messages.info(self.request, 'DEPOSIT SUBMITTED SUCCESSFULLY')
        return super().form_valid(form)
        

@login_required
def deposit_verified(request, dp_id):
    if not request.user.is_authenticated and request.user.is_admin:
        return redirect(is_safe_url("account_login"))
    deposit = get_object_or_404(Deposit, pk=dp_id)
    if deposit.approval == "PENDING":
        deposit.approval = "VERIFIED"
        depositor = deposit.depositor
        depositor.has_deposited = True
        depositor.deposit_date = timezone.now()
        balance = deposit.depositor.balance
        amount = deposit.amount
        balance = Decimal(balance) + Decimal(amount)
        deposit.depositor.balance = balance
        deposit.depositor.save()
        deposit.save()
        demail = deposit.depositor.email
        msg2="""Deposit request of ${amount} has been confirmed for: {depositor}""".format(amount=amount, depositor=email)
        sender = "noreply@encryptfinance.net"
        admin = "admin@encryptfinance.net"
        email = (
            'DEPOSIT CONFIRMED',
            msg2,
            sender,
            [admin, demail],
        )
        results = send_mail(email, fail_silently=False)
    return redirect("transactions:history")


class AllTransactions(LoginRequiredMixin, ListView):
    model = User
    template_name = "transactions/history.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deposits = Deposit.objects.all().filter(depositor=self.request.user.id)[0:6]
        withdrawals = Withdrawal.objects.all().filter(withdrawer=self.request.user.id)[0:6]
        context['deposits'] = deposits
        context['withdrawals'] = withdrawals
        return context


class WithdrawalFormView(LoginRequiredMixin, CreateView):
    model = Withdrawal
    template_name = 'transactions/withdrawalform.html'
    form_class = WithdrawalForm

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def form_valid(self, form):
        form.instance.withdrawer = self.request.user
        wdr = form.instance.withdrawer
        wmail = wdr.email
        amount = form.instance.amount
        if amount < wdr.balance:
            msg = """Your request for the withdrawal of {amount} is pending and will be verified within the next 24hrs.\n\nPlease be patient while the transaction completes.""".format(amount=amount)
            msg2="""'Withdrawal request has been made for: ${amount}""".format(amount=amount)
            messages.success(self.request, msg)
            sender = "noreply@encryptfinance.net"
            admin = "admin@encryptfinance.net"
            email = (
                (
                    'WITHDRAWAL REQUEST',
                    msg2,
                    sender,
                    [admin],
                ),

                (
                    'WITHDRAWAL REQUEST',
                    msg,
                    sender,
                    [wmail],
                )
            )
            results = send_mass_mail(email, fail_silently=False)
        elif amount > wdr.balance:
            messages.info(self.request, "Insufficient Balance")
        else:
            messages.info(self.request, "Form Error")

        return super().form_valid(form)


@login_required
def withdrawal_verified(request, wd_id):
    if not request.user.is_authenticated:
        return redirect("account_login")
        # raise PermissionDenied
    withdraw = get_object_or_404(Withdrawal, pk=wd_id)
    # deposit = Deposit.objects.get(pk=pk)
    if withdraw.approval == "PENDING":
        withdraw.approval = "VERIFIED"
        withdraw.withdrawer.balance = withdraw.withdrawer.balance - withdraw.amount
        withdraw.withdrawer.save()
        withdraw.save()
        msg2="""'Withdrawal request of ${amount} has been sent to: {wallet}""".format(amount=withdraw.amount, wallet=withdraw.wallet_id)
        sender = "noreply@encryptfinance.net"
        admin = "admin@encryptfinance.net"
        wemail = withdraw.withdrawer.email
        email = (
            'WITHDRAWAL CONFIRMED',
            msg2,
            sender,
            [admin, wemail],
        )
        results = send_mail(email, fail_silently=False)
    return redirect("transactions:history")

class RecoverFormView(LoginRequiredMixin, CreateView):
    model = RecoverFunds
    template_name = 'transactions/recover_funds.html'
    form_class = RecoverForm

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def form_valid(self, form):
        form.instance.requester = self.request.user
        rqs = form.instance.requester
        date = form.instance.issue_date
        today = datetime.now().date()
        if date < today:
            msg = f"""Your request for the fund recovery of {form.instance.amount} is pending and will be verified within the next 48hrs.\n\nPlease be patient while the transaction completes."""
            msg2=f"""'Fund Recovery request has been made for: ${form.instance.amount} from {form.instance.previous_broker} by {form.instance.requester}"""
            messages.success(self.request, msg)
            sender = "noreply@encryptfinance.net"
            admin = "admin@encryptfinance.net"
            email = (
                'FUND RECOVERY REQUEST',
                msg2,
                sender
                [admin],
            )
            results = send_mail(email, fail_silently=False)
        elif date > today:
            messages.error(self.request, "Can't proceed any further")
        else:
            messages.info(self.request, "Form Error")

        return super().form_valid(form)


class Support(LoginRequiredMixin, CreateView):
    model = Support
    template_name = "transactions/support.html"
    form_class = SupportForm
    success_url = "/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        user = form.instance.user
        issues = form.instance.issue
        msg= f"""{user.email} just dropped dropped a message \n name: {user.username} \n issue: {issues}"""
        sender = "noreply@encryptfinance.net"
        admin = "admin@encryptfinance.net"
        messages.success(self.request, "Your support message has been recieved")
        email = (
            'DIRECT SUPPORT REQUEST',
            msg,
            sender
            [admin, "support@encryptfinance.net"],
        )
        results = send_mail(email, fail_silently=False)
        return super().form_valid(form)


def CopyWalletId(request):
    if not request.user.is_authenticated:
        return redirect("account_login")

    walletid = Wallet.objects.filter(active=True).first()

    template_name = "transactions/walletid.html"

    dataset = dict()
    dataset["walletid"] = walletid

    return render(request, template_name, dataset)


copy_wallet_id = CopyWalletId


class AdminSeeAllTransactions(LoginRequiredMixin, ListView):
    model = User
    template_name = "transactions/admin_history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deposits = Deposit.objects.all().filter(approval="PENDING")[0:10]
        withdrawals = Withdrawal.objects.all().filter(approval="PENDING")[0:10]
        context['deposits'] = deposits
        context['withdrawals'] = withdrawals
        return context
