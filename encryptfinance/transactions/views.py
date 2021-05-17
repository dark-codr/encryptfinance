from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, ListView
from django.utils.http import is_safe_url

from django.core.mail import send_mail

from .forms import DepositForm, WithdrawalForm, RecoverForm, SupportForm
from .models import Deposit, Withdrawal, RecoverFunds, Support

from encryptfinance.wallets.models import Wallet

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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["date"] = timezone.now() - timedelta(minutes=2)
    #     return context
    

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
    # success_message = 'Deposit is PENDING'
    form_class = DepositForm


    def get_success_url(self):
        return reverse("transactions:walletID")

    def form_valid(self, form):
        form.instance.depositor = self.request.user
        user = form.instance.depositor
        amount = form.instance.amount
        msg = """Your deposit of: ${amount} is pending and will be verified within the next 24hrs.\n\nPlease be patient while the transaction completes.""".format(amount=amount)
        messages.info(self.request, 'DEPOSIT SUBMITTED SUCCESSFULLY')
        msg2="""Deposit request has been made for: ${amount}""".format(amount=amount)
        send_mail(
            'DEPOSIT REQUEST',
            msg2,
            'noreply@encryptfinance.net',
            ['admin@encryptfinance.net'],
            fail_silently=False,
        )
        return super().form_valid(form)
        

@login_required
def deposit_verified(request, dp_id):
    if not request.user.is_authenticated and request.user.is_admin:
        return redirect(is_safe_url("account_login"))
        # raise PermissionDenied
    deposit = get_object_or_404(Deposit, pk=dp_id)
    # deposit = Deposit.objects.all().get(pk=dp_id)
    if deposit.approval == "PENDING":
        deposit.approval = "VERIFIED"
        deposit.depositor.balance += deposit.amount
        deposit.depositor.save()
        deposit.save()
        msg2="""'Deposit request of ${amount} has been confirmed for: {depositor}""".format(amount=deposit.amount, depositor=deposit.depositor.email)
        email = deposit.depositor.email
        send_mail(
            'DEPOSIT CONFIRMED',
            msg2,
            'noreply@encryptfinance.net',
            ['admin@encryptfinance.net', email],
            fail_silently=False,
        )
    return redirect("transactions:history")


class AllTransactions(LoginRequiredMixin, ListView):
    model = User
    template_name = "transactions/history.html"
    # context_object_name = "investors"

    # def get_queryset(self):
    #     queryset = {
    #         'all_deposits': Deposit.objects.all().filter(depositor=self.request.user.username), 
    #         'all_deposits': Withdrawal.objects.all().filter(withdrawer=self.request.user.username)
    #         }
    #     return queryset

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
        amount = form.instance.amount
        if amount < wdr.balance:
            msg = """Your request for the withdrawal of {amount} is pending and will be verified within the next 24hrs.\n\nPlease be patient while the transaction completes.""".format(amount=amount)
            msg2="""'Withdrawal request has been made for: ${amount}""".format(amount=amount)
            messages.success(self.request, msg)
            admin = settings.ADMINS
            send_mail(
                'WITHDRAWAL REQUEST',
                msg2,
                settings.DEFAULT_FROM_EMAIL,
                admin,
                fail_silently=False,
            )
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
        email = withdraw.withdrawer.email
        send_mail(
            'WITHDRAWAL CONFIRMED',
            msg2,
            'noreply@encryptfinance.net',
            ['admin@encryptfinance.net', email],
            fail_silently=False,
        )
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
            sender = settings.EMAIL_HOST_USER
            admin = settings.ADMINS
            send_mail(
                'FUND RECOVERY REQUEST',
                msg2,
                sender,
                admin,
                fail_silently=False,
            )
        elif date > today:
            messages.error(self.request, "Can't proceed any further")
        else:
            messages.info(self.request, "Form Error")

        return super().form_valid(form)


class Support(LoginRequiredMixin, CreateView):
    model = Support
    template_name = "transactions/support.html"
    form_class = SupportForm
    success_url = "home"

    def form_valid(self, form):
        form.instance.user = self.request.user
        user = form.instance.user

        messages.success(self.request, "Your message has been recieved")
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
    # context_object_name = "investors"

    # def get_queryset(self):
    #     queryset = {
    #         'all_deposits': Deposit.objects.all().filter(depositor=self.request.user.username), 
    #         'all_deposits': Withdrawal.objects.all().filter(withdrawer=self.request.user.username)
    #         }
    #     return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deposits = Deposit.objects.all().filter(approval="PENDING")[0:10]
        withdrawals = Withdrawal.objects.all().filter(approval="PENDING")[0:10]
        context['deposits'] = deposits
        context['withdrawals'] = withdrawals
        return context
