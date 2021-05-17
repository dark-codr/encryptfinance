import datetime
from .models import Testimonial

def recent_testimonials(request):
    testimonials = Testimonial.objects.all().filter(modified__lte=datetime.now())
    return {'testimonials':testimonials}