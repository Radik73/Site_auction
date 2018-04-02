from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib import auth
from .models import Lot, Rate, UserProfile
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
    lot_object = get_object_or_404(Lot, pk=pk)
    rate_object = Rate.objects.filter(lot__pk=pk)
    form = RateForm(request.POST or None)
    if form.is_valid():
        sum_rate = request.POST.get('sum_rate', '')
        if max_rate(rate_object, sum_rate):
            if chek_rate_time(rate_object, request.user) and lot_object == get_object_or_404(Lot, pk=pk):
                rate = form.save(commit=False)
                rate.time_rate = timezone.now()
                rate.user = request.user
                rate.lot = lot_object
                that_user = get_object_or_404(UserProfile, user = request.user)
                if that_user.bank_book >= int(sum_rate):
                    that_user.bank_book = that_user.bank_book - int(sum_rate)
                    print(that_user.bank_book)
                    that_user.save()
                    rate.save()
                    return redirect('/lots')
                else:
                    return HttpResponse('У вас недостаточно средств на счёте.')
            else:
                return HttpResponse('Прошло слишком мало времени с момента вашей последней ставки.'
                                    ' Попробуйте сделать ставку позднее')
        else:
            return HttpResponse('Ваша ставка ниже уже существующей!')
    else:
        form = RateForm()
        return render(request, 'auction_site/make_rate.html', {'form': form})


def chek_rate_time(rate, user):
    time_rate_list = []
    timeout = 30.0
    for i in rate:
        if i.user == user:
            result_time = timezone.now() - i.time_rate
            time_rate_list.append(float(result_time.total_seconds()))
    print(time_rate_list)
    if time_rate_list != []:
        index = len(time_rate_list) - 1
        if time_rate_list[index] > timeout:
            return True
        else:
            return False
    else:
        return True



def max_rate(rate, new_rate):
    max = int()
    for i in rate:
        if int(i.sum_rate) > int(new_rate):
            max = int(i.sum_rate)
        elif int(new_rate) > int(i.sum_rate):
            max = int(new_rate)
        elif int(i.sum_rate) == int(new_rate):
            max = 0
    if max != int(new_rate):
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
            return render( request, 'auction_site/login.html', args)
    else:
        return render( request, 'auction_site/login.html', args)


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