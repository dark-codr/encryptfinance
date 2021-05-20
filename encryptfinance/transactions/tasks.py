# from celery.decorators import task
# from celery.utils import get_task_logger

# from .emails import send_email

# logger = get_task_logger(__name__)

# @task(name="send_transaction_email")
# def send_transaction_email(email, message):
#     logger.info("Sent transactional email")
#     return send_transaction_email(email, message)