from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render_to_response
from django.shortcuts import render
from .models import Lot
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def give_lots(request):
    lots = Lot.objects.all()
    paginator = Paginator(lots, 1)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'auction_site/lots.html', {'page': page,
            'posts': posts,})
