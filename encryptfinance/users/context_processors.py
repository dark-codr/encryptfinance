from django.utils import timezone
from .models import Testimonial

def recent_testimonials(request):
    testimonials = Testimonial.objects.all().filter(modified__lte=timezone.now())[:7]
    return {'recent_testimonials':testimonials}