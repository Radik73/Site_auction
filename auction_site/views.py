from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib import auth
# from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from .models import Lot, Rate, User
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import RateForm








# def register(request):
#     args = {}
#     args['form'] = UserCreationForm()
#     if request.POST:
#         newuser_form = UserCreationForm(request.POST)
#         if newuser_form.is_valid():
#             newuser_form.save()
#             newuser_form.save()
#             newuser = auth.autheticate(username=newuser_form.cleaned_data['username'],
#                                        password = newuser_form.cleaned_data['password2'])
#             auth.login(request, newuser)
#             return redirect('/')
#         else:
#             args['form'] = newuser_form
#     return render_to_response('register.html', args)




def make_rate(request, pk):
    if request.method == "POST" and ("pause {}".format(str(pk)) not in request.session):
        lot_object = get_object_or_404(Lot, pk=pk)
        form = RateForm(request.POST or None)
        if form.is_valid():
            sum_rate = request.POST.get('sum_rate', '')
            if max_rate(pk, sum_rate):
                rate = form.save(commit=False)
                rate.time_rate = timezone.now()
                #rate.user = auth.get_user(request).username
                rate.lot = lot_object
                rate.save()
                request.session.set_expiry(30)
                request.session["pause {}".format(str(pk))] = True
                return redirect('/lots')
            else:
                return HttpResponse('Ваша ставка ниже уже существующей!')
    else:
        form = RateForm()
    return render(request, 'auction_site/make_rate.html', {'form': form})


def max_rate(pk, sum_rate):
    rate = Rate.objects.filter(lot__pk=pk)
    for i in rate:
        if int(i.sum_rate) >= int(sum_rate):
            return False
        else:
            return True

def login(request):
    args = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/lots')
    else:
        args['login_error'] = "Пользователь не найден"
        return render_to_response('auction_site/login.html', args)


def give_lots(request):
    lots = Lot.objects.all()
    paginator = Paginator(lots, 2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'auction_site/lots.html', {'page': page,
            'posts': posts, 'username': auth.get_user(request).username})


def lot_detail(request, pk):
    lot = get_object_or_404(Lot, pk=pk)
    rate = Rate.objects.filter(lot__pk=pk)
    return render_to_response('auction_site/lot_detail.html', {'lot': lot,
			'rate': rate, 'username': auth.get_user(request).username})



def logout(request):
    auth.logout(request)
    return redirect('/lots')