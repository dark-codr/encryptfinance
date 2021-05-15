from __future__ import absolute_import

from django.urls import path

from encryptfinance.transactions.views import (
    DebitLists,
    WithdrawalLists,
    DepositFormView,
    WithdrawalFormView,
    AllTransactions,
    RecoverFormView,
    Support,
    AdminSeeAllTransactions,
    # user_profile_view,
    deposit_verified,
    copy_wallet_id,
    withdrawal_verified,
    deposit_verified,
    withdrawal_verified
)

app_name = "transactions"
urlpatterns = [
    path("~deposit/", view=DepositFormView.as_view(), name="deposit"),
    path("~withdrawal/", view=WithdrawalFormView.as_view(), name="withdraw"),
    path("~recover-funds/", view=RecoverFormView.as_view(), name="recover"),
    path("~transaction-support/", view=Support.as_view(), name="support"),
    path("deposit/", view=DebitLists.as_view(), name="deposits"),
    path("withdrawals/", view=WithdrawalLists.as_view(), name="withdrawals"),
    # path("<str:username>/profile/", view=user_profile_view, name="profile"),
    path("transactions/", view=AllTransactions.as_view(), name="history"),
    path("transactions/admin-verify/", view=AdminSeeAllTransactions.as_view(), name="verify"),
    path("copy-wallet/", view=copy_wallet_id, name="walletID"),
    path("verify-deposit/<int:dp_id>", view=deposit_verified, name="verify-deposit"),
    path("verify-withdrawal/<int:wd_id>>", view=withdrawal_verified, name="verify-withdrawal"),
]
