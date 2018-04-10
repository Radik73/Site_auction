from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib import auth
from .models import Lot, Rate, UserProfile
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import RateForm
from django.contrib.auth.forms import UserCreationForm



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



def register(request):
    args = {}
    # args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.method == "POST":
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                       password = newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)
            return redirect('/lots')
        else:
            args['form'] = newuser_form
    return render(request, 'auction_site/register.html', args)


def chek_date():
    lots = Lot.objects.all()
    for lot_object in lots:
        lot_finish_date = lot_object.finish_date
        now_date = timezone.now()
        if (lot_finish_date >= now_date) is False:
            lot_object.status = 'Finished'
            lot_object.save()


def my_rates(request, pk):
    list_of_rates = []
    rate_object = Rate.objects.filter(lot__pk=pk, user=request.user)
    for rate in rate_object:
        print(list_of_rates.append(str(rate.sum_rate)))
    return HttpResponse(str(list_of_rates))


def profile(request):
    list_of_lots = []
    that_user = get_object_or_404(UserProfile, user=request.user)
    rate_object = Rate.objects.filter(user=request.user)
    for i in rate_object:
        if str(i.lot) not in list_of_lots:
            list_of_lots.append(str(i.lot))
    return HttpResponse(str(that_user.user) + ' ' + str(that_user.bank_book) + ' ' + str(list_of_lots))


def make_rate(request, pk):
    lot_object = get_object_or_404(Lot, pk=pk)
    rate_object = Rate.objects.filter(lot__pk=pk, user=request.user)
    form = RateForm(request.POST or None)
    if form.is_valid():
        sum_rate = request.POST.get('sum_rate', '')
        if lot_object.status != 'Finished':
            print(lot_object.status)
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
            return HttpResponse('Лот закрыт')
    else:
        form = RateForm()
        return render(request, 'auction_site/make_rate.html', {'form': form})


def chek_rate_time(rate, user):
    time_rate_list = []
    timeout = 30.0
    for i in rate:
        result_time = timezone.now() - i.time_rate
        time_rate_list.append(float(result_time.total_seconds()))
    if time_rate_list != []:
        index = len(time_rate_list) - 1
        if time_rate_list[index] > timeout:
            return True
        else:
            return False
    else:
        return True


def max_rate(rate, new_rate):
    print(rate)
    max = int()
    if len(rate) != 0:
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
    else:
        return True





def give_lots(request):
    lots = Lot.objects.all()
    chek_date()
    paginator = Paginator(lots, 3)
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
    chek_date()
    rate = Rate.objects.filter(lot__pk=pk)
    return render_to_response('auction_site/lot_detail.html', {'lot': lot,
			'rate': rate, 'username': auth.get_user(request).username})


def logout(request):
    auth.logout(request)
    return redirect('/lots')