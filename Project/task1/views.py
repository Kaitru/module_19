from django.shortcuts import render
from task1.models import *
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    title = 'Главная страница'
    context = {
        'title': title,
    }
    return render(request, 'index.html', context)

def shop(request):
    title = 'Магазин'
    products = Game.objects.all()
    context = {
        'title': title,
        'products': products,
    }
    return render(request, 'shop.html', context)

def cart(request):
    title = 'Корзина'
    context = {
        'title': title,
    }
    return render(request, 'cart.html', context)

def register(request):
    users = Buyer.objects.all()
    info = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = request.POST.get('age')

        if password != repeat_password:
            info['error'] = 'Пароли не совпадают'
        elif username in users:
            info['error'] = 'Пользователь уже существует'
        elif int(age) < 18:
            info['error'] = 'Вы должны быть старше 18'
        else:
            for user in users:
                if user.name == username:
                    info['error'] = 'Пользователь уже существует'
                    break
            else:
                Buyer.objects.create(name=username, balance=0, age=age)
                info['success'] = f'Приветствуем, {username}'

    return render(request, 'registration_page.html', info)

def news(request):
    news = News.objects.all().order_by('-date')
    paginator = Paginator(news, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news.html', {'news': page_obj})