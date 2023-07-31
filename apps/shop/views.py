from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from .models import Phone

# Create your views here.


class Home(View):
    def get(self, request):
        phones = Phone.objects.all().order_by("-id")
        paginator = Paginator(phones, 25)
        page_number = request.GET.get('paginator')
        phones = paginator.get_page(page_number)

        context = {
            "phones": phones
        }

        return render(request, 'shop/home.html', context)
