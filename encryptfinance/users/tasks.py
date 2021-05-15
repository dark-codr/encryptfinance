from __future__ import absolute_import

from celery.utils.log import get_task_logger
from celery.task.schedules import crontab
from celery.decorators import periodic_task

from django.contrib.auth import get_user_model
from django.contrib import messages

from datetime import datetime, timedelta

from config import celery_app

User = get_user_model()

logger = get_task_logger(__name__)

@celery_app.task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()

@celery_app.task()
def cal_daily_profit():
    """A Celery task to update balance daily by the profit."""
    user = User.objects.filter(has_deposited=True)
    if user.has_deposited and user.deposit_date < user.withdrawal_date:
        balance = user.balance + user.profit
        user.create_or_update(balance=balance)
        messages.info(f"{user.username} your profit: {user.profit} has \n been added to your balance: {user.balance}")
        logger.info(f"{user.username} your profit: {user.profit} has \n been added to your balance: {user.balance}")
    return cal_daily_profit()

@celery_app.task()
def can_withdraw():
    """A Celery task to send mail if user withdrawal date reaches."""
    user = User.objects.filter(can_withdraw=True)
    if user.can_withdraw and user.is_authenticated:
        messages.info("You are eligible to make withdrawals now")
        logger.info("You are eligible to make withdrawals now")
    return can_withdraw()
