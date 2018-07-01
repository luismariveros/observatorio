from backend.models import Enlace


def my_processor(request):
    context = {
        'enlaces': Enlace.objects.all()
    }
    return context

