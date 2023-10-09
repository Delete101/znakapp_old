from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, NewUserForm
from django.contrib import messages
from .models import UserInfo, UserRequests, ClearPrice, Cart
import subprocess
import os
import zipfile
from datetime import datetime
from .parser_znakapp.main import main as parsers_img




static_dir = '/Users/daniillavrentyev/PycharmProjects/znakapp3.8/znakapp_38/znakapp/znakapp/service/static'
static_parser_dir = '/Users/daniillavrentyev/PycharmProjects/znakapp3.8/znakapp_38/znakapp/znakapp/service/parser_znakapp/images'
static_out_dir = '/Users/daniillavrentyev/PycharmProjects/znakapp3.8/znakapp_38/znakapp/znakapp/service/static/out'
static_out_users_dir = '/Users/daniillavrentyev/PycharmProjects/znakapp3.8/znakapp_38/znakapp/znakapp/service/static/users_out'
mask_path = '/Users/daniillavrentyev/PycharmProjects/znakapp3.8/znakapp_38/znakapp/znakapp/service/lama/prepare_masks.py'
lama_path = '/Users/daniillavrentyev/PycharmProjects/znakapp3.8/znakapp_38/znakapp/znakapp/service/lama/lama/bin/predict.py'
txt_out_dir = '/Users/daniillavrentyev/PycharmProjects/znakapp3.8/znakapp_38/znakapp/znakapp/service/static'


def index(requests):
    if requests.method == 'POST':
        photos = []
        # Clear parser lib
        for f in os.listdir(static_out_dir):
            os.remove(os.path.join(static_out_dir, f))
        for f in os.listdir(static_parser_dir):
            os.remove(os.path.join(static_parser_dir, f))

        # Clear IMG after POST request
        input_value = requests.POST.get('link_input')
        if input_value:
            parsers_img(str(input_value))
            print('PARSER: OK')
            if 'krisha.kz' in input_value:
                subprocess.call([python_path, mask_path])
                print('MASK: OK')
                subprocess.call([python_path, lama_path])
                print('LAMA: OK')

            photos = os.listdir(static_out_dir)
            os.rename(f'{static_out_dir}/{photos[0]}', f'{static_out_dir}/first_img.png')
            photos[0] = 'first_img.png'

            with open(f'{txt_out_dir}/info_list.txt', 'r') as file:
                data = file.read()

            context = data

            return render(requests, 'service/base.html', {'images': photos, 'context': context})
        return render(requests, 'service/base.html', {'error': 'Ошибка: исправьте ссылку на объявления'})

    return render(requests, 'service/base.html')


def how_it_work(requests):
    return render(requests, 'service/how_it_work.html', {})


def price_list(requests):
    return render(requests, 'service/price_list.html', {})


def contacts(requests):
    return render(requests, 'service/contacts.html')


def cabinet(requests, user_id):
    cart = Cart.objects.first()
    if requests.user.is_authenticated and requests.method == 'POST':
        for f in os.listdir(static_out_dir):
            os.remove(os.path.join(static_out_dir, f))
        for f in os.listdir(static_parser_dir):
            os.remove(os.path.join(static_parser_dir, f))

        # Clear IMG after POST request
        input_value = requests.POST.get('link_input')
        if input_value:
            parsers_img(str(input_value))
            if 'krisha.kz' in input_value:
                subprocess.call([python_path, mask_path])
                subprocess.call([python_path, lama_path])

            # Date now
            now = datetime.now()
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d_%m_%Y.%H_%M_%S")
            # Make dir for datetime
            os.mkdir(f'{static_out_users_dir}/{user_id}/{dt_string}')
            # Move files
            for img in os.listdir(static_out_dir):
                os.rename(f'{static_out_dir}/{img}', f'{static_out_users_dir}/{user_id}/{dt_string}/{img}')

            # Sort out images
            photos = os.listdir(f'{static_out_users_dir}/{user_id}/{dt_string}')
            photos.sort()
            with open(f'{txt_out_dir}/info_list.txt', 'r') as file:
                data = file.read()

            context = data
            return render(requests, 'service/cabinet.html',
                          {'images': photos, 'dt': dt_string, 'cart': cart, 'context': context})
        return render(requests, 'service/cabinet.html',
                      {'error': 'Ошибка: исправьте ссылку на объявления', 'cart': cart})

    if requests.user.is_authenticated:
        user_info = UserInfo.objects.filter(user=requests.user)
        user_request = UserRequests.objects.filter(user=requests.user)
        clear_price = ClearPrice.objects.all()
        for elem in clear_price:
            clear_price = elem.clear_price
        balance = 0
        for elem in user_info:
            balance = elem.balance / clear_price
        return render(requests, 'service/cabinet.html',
                      {'user_info': int(balance), 'user_request': user_request, 'cart': cart})
    else:
        return redirect('login')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            print(user)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(f'cabinet/{user}')
                else:
                    error_msg = 'Проверьте логин и пароль и попробуйте еще раз.'
                    return render(request, 'service/login.html', {'form': form, 'error_msg': error_msg})
            else:
                error_msg = 'Проверьте логин и пароль и попробуйте еще раз.'
                return render(request, 'service/login.html', {'form': form, 'error_msg': error_msg})
    else:
        form = LoginForm()
    return render(request, 'service/login.html', {'form': form})


def register_request(request):
    error_msg = ''
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            os.mkdir(f'{static_dir}users_out/{user}')
            return redirect(user_login)
        error_msg = 'Проверьте логин и пароль и попробуйте еще раз.'
    form = NewUserForm()
    return render(request, "service/register.html", {"register_form": form, 'error_msg': error_msg})


def user_logout(request):
    logout(request)
    return redirect("homepage")


def download_images(requests, user_id):
    if requests.user.is_authenticated:
        # Получение списка файлов из папки static
        user_id = str(requests.user)
        static_out_users_dir = static_dir + 'users_out/'

        # Получаем список элементов в директории
        entries = os.scandir(static_out_users_dir + user_id)

        # Сортируем список по времени создания
        entries = sorted(entries, key=lambda entry: entry.stat().st_ctime)

        # Получаем последний элемент в списке
        latest_entry = entries[-1]

        # Получаем путь к последней директории
        latest_dir_path = latest_entry.path

        # Получаем список файлов в последней директории
        files = os.listdir(latest_dir_path)

        # Создаем архив
        temp_zip_path = static_dir + 'images.zip'  # Замените на путь, куда вы хотите сохранить архив
        with zipfile.ZipFile(temp_zip_path, 'w') as zipf:
            for file in files:
                file_path = os.path.join(latest_dir_path, file)
                zipf.write(file_path, arcname=file)

        # Отправляем архив в ответе
        with open(temp_zip_path, 'rb') as zipf:
            response = HttpResponse(zipf.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="images.zip"'
            return response


def pol_sogl(requests):
    return render(requests, 'service/pol_sogl.html', {})


def pol_obr(requests):
    return render(requests, 'service/pol_obr.html', {})


def sposob_opl(requests):
    return render(requests, 'service/sposob_opl.html', {})


def checkout_view(request, item):
    selected_items = []

    if item == 'beginner':
        selected_items = Cart.objects.filter(beginner_quantity__gt=0)
        for elem in selected_items:
            quantity = elem.beginner_quantity
            bonus = elem.beginner_bonus
            access = elem.beginner_access
            price = elem.beginner_price
    elif item == 'advanced':
        selected_items = Cart.objects.filter(advanced_quantity__gt=0)
        for elem in selected_items:
            quantity = elem.advanced_quantity
            bonus = elem.advanced_bonus
            access = elem.advanced_access
            price = elem.advanced_price
    elif item == 'expert':
        selected_items = Cart.objects.filter(expert_quantity__gt=0)
        for elem in selected_items:
            quantity = elem.expert_quantity
            bonus = elem.expert_bonus
            access = elem.expert_access
            price = elem.expert_price
    return render(request, 'service/checkout.html',
                  {'quantity': quantity, 'bonus': bonus, 'access': access, 'price': price})


def oferta(request):
    return render(request, 'service/oferta.html')