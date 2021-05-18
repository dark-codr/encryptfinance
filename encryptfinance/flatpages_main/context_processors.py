from django.utils import timezone
from .models import FAQ

def recent_faq(request):
    faqs = FAQ.objects.all()[:15]
    return {'recent_faq':faqs}