from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.base import ContentFile, File
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.clickjacking import xframe_options_exempt

from botapp.helper.helper import (
    valid_username, valid_email, valid_password, generate_context, generate_filepath, basename)
from .models import Bot

# pylint: disable=E1101

def signin(request):
    """CONNECTS the user."""
    if request.user.is_authenticated:
        messages.info(request, 'you have already logged in.')
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            signin_err = False
            if len(username) < 4 or len(username) > 32:
                messages.info(
                    request, "username must be between 4 to 32 characters.")
                signin_err = True

            elif not valid_username(username):
                messages.info(
                    request, "username must only contain alphanumeric characters and special characters.")
                signin_err = True

            if len(password) < 4 or len(password) > 32:
                messages.info(
                    request, "password must be between 4 to 32 characters.")
                signin_err = True

            elif not valid_password(password):
                messages.info(
                    request, "password must only contain alphanumeric characters and special characters.")
                signin_err = True

            if signin_err:
                context = generate_context(request, 'login')
                context['formUsername'] = username
                context['formPassword'] = password
                return render(request, 'signin.html', context)
            else:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, "You have successfully logged in.")
                    return redirect('home')
                else:
                    messages.info(
                        request, "Either username or password is incorrect.")
                    context = generate_context(request, 'login')
                    context['formUsername'] = username
                    context['formPassword'] = password
                    return render(request, 'signin.html', context)
        else:
            context = generate_context(request, 'login')

            return render(request, 'signin.html', context)


def signout(request):
    """DISCONNECTS the user."""
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'you have successfully logged out.')
        return redirect('home')
    else:
        messages.info(request, 'you have already logged out.')
        return redirect('home')


def signup(request):
    """CONNECTS the user."""
    if request.user.is_authenticated:
        messages.info(request, 'you have already logged in.')
        return redirect('home')
    else:
        if request.method == 'POST':
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password']
            confirm = request.POST['password']

            signup_err = False
            if len(firstname) > 32:
                messages.info(
                    request, "firstname must be not be more than 32 characters.")
                signup_err = True

            if len(lastname) > 32:
                messages.info(
                    request, "lastname must be not be more than 32 characters.")
                signup_err = True

            if len(email) > 128:
                messages.info(
                    request, "lastname must be not be more than 128 characters.")
                signup_err = True
            elif User.objects.filter(email=email).exists():
                messages.info(
                    request, 'specified e-mail has been already taken.')
                signup_err = True
            elif not valid_email(email):
                messages.info(
                    request, "email must be valid.")
                signup_err = True

            if len(username) < 4 or len(username) > 32:
                messages.info(
                    request, "username must be between 4 to 32 characters.")
                signup_err = True
            elif not valid_username(username):
                messages.info(
                    request, "username must only contain alphanumeric characters and special characters.")
                signup_err = True

            if len(password) < 4 or len(password) > 32:
                messages.info(
                    request, "password must be between 4 to 32 characters.")
                signup_err = True
            elif not valid_password(password):
                messages.info(
                    request, "password must only contain alphanumeric characters and special characters.")
                signup_err = True
            elif not password == confirm:
                messages.info(
                    request, "password and confirm don't match.")
                signup_err = True

            if signup_err:
                context = generate_context(request, 'register')
                context['formFirstname'] = firstname
                context['formLastname'] = lastname
                context['formEmail'] = email
                context['formUsername'] = username
                context['formPassword'] = password
                context['formConfirm'] = confirm
                return render(request, 'signup.html', context)
            else:
                user_item = User.objects.create_user(
                    username, email, password, first_name=firstname, last_name=lastname)
                user_item.save()
                bot_item = Bot(user=user_item)
                bot_item.save()
                if user_item is not None:
                    login(request, user_item)
                    messages.info(request, "You have successfully registered.")
                    messages.info(request, "You have successfully logged in.")
                    return redirect('home')
                else:
                    messages.info(
                        request, "Some problem occured while signuping.")
                    context = generate_context(request, 'register')
                    context['formFirstname'] = firstname
                    context['formLastname'] = lastname
                    context['formEmail'] = email
                    context['formUsername'] = username
                    context['formPassword'] = password
                    context['formConfirm'] = confirm
                    return render(request, 'signup.html', context)
        else:
            context = generate_context(request, 'register')
            return render(request, 'signup.html', context)


def home(request):
    context = generate_context(request, 'home')
    return render(request, 'home.html', context)


def chatbots00(request):
    query = request.GET.get('query')
    page = request.GET.get('page')
    context = generate_context(request, 'chatbots')

    if query:
        paginator = Paginator(Bot.objects.filter(
            name__icontains=query, visible=True).order_by('views'), 1)
        context['botQuery'] = query
    else:
        paginator = Paginator(Bot.objects.filter(
            visible=True).order_by('views'), 25)
    try:
        bot_list = paginator.page(page)
    except PageNotAnInteger:
        bot_list = paginator.page(1)
    except EmptyPage:
        bot_list = paginator.page(paginator.num_pages)

    context['botList'] = bot_list

    bot_item = request.user.bot_set.first()
    if bot_item is None:
        messages.info(request, 'specified bot was not found in database.')
    else:
        context['botId'] = bot_item.pk

    return render(request, 'chatbots00.html', context)


def chatbots01(request, bot_id):
    bot_item = Bot.objects.get(pk=bot_id)

    context = generate_context(request, 'chatbots')
    if bot_item:
        if bot_item.visible:
            context['botItem'] = bot_item
            context['chatPage'] = True
        else:
            context['alertText'] = 'specified bot is not available for viewing.'
    else:
        messages.info(request, 'specified bot was not found.')

    return render(request, 'chatbots01.html', context)


def guide(request):
    context = generate_context(request, 'guide')
    return render(request, 'guide.html', context)


def faqs(request):
    context = generate_context(request, 'faqs')
    return render(request, 'faqs.html', context)


def contact(request):
    context = generate_context(request, 'contact')
    return render(request, 'contact.html', context)


def chat(request):
    if request.user.is_authenticated:
        context = generate_context(request, 'chat')

        bot_item = request.user.bot_set.first()
        if bot_item:
            context['botItem'] = bot_item
            context['chatPage'] = True
        else:
            messages.info(request, 'specified bot was not found in database.')

        return render(request, 'chat.html', context)
    else:
        messages.info(request, 'you must be logged in first.')
        return redirect('login')


def teach00(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            brain_text = request.POST['brainText']

            bot_item = request.user.bot_set.first()
            if bot_item is None:
                messages.info(
                    request, 'specified bot was not found in database.')
                return redirect('teach00')

            brain_file = bot_item.brain
            if not basename(brain_file.name) == 'bot_default.rive':
                brain_file.delete()
            brain_file.save('bot_brain.rive', ContentFile(brain_text))
            messages.info(request, 'brain file edited successfully.')
            return redirect('teach00')
        else:
            bot_item = request.user.bot_set.first()

            context = generate_context(request, 'teach')
            if bot_item is None:
                messages.info(
                    request, 'specified bot was not found in database.')
            else:
                brain_file = bot_item.brain
                brain_file.open(mode='rb')
                brain_text = brain_file.read()
                brain_file.close()
                context['brainText'] = brain_text

            return render(request, 'teach00.html', context)
    else:
        messages.info(request, 'you must be logged in first.')
        return redirect('login')


def teach01(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if 'brainFile' in request.FILES:
                bot_item = request.user.bot_set.first()
                if bot_item is None:
                    messages.info(
                        request, 'specified bot was not found in database.')
                    return redirect('teach01')

                if not basename(bot_item.brain.name) == 'bot_default.rive':
                    bot_item.brain.delete()
                bot_item.brain = request.FILES['brainFile']
                bot_item.save()
                messages.info(request, 'brain file uploaded successfully.')
            else:
                messages.info(request, 'brain file was no found.')
            return redirect('teach01')
        else:
            context = generate_context(request, 'teach')
            return render(request, 'teach01.html', context)
    else:
        messages.info(request, 'you must be logged in first.')
        return redirect('login')


def teach02(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            bot_item = request.user.bot_set.first()
            if bot_item is None:
                messages.info(
                    request, 'couldn\'t log conversation as bot was not found.')
                return redirect('home')
            log_file = bot_item.chatlog

            if 'logText' in request.POST:
                log_file.open(mode='rb')
                log_text = log_file.read()
                log_file.close()
                if not basename(bot_item.brain.name) == 'bot_default.rive':
                    log_file.delete()
                file_text = log_text + request.POST['logText']
                log_file.save('bot_log.txt', ContentFile(file_text))
                return {'success': True}

            if 'clearText' in request.POST:
                log_file.delete()
                log_file.save('bot_log.txt', ContentFile(''))

                messages.info(request, 'log successfully cleared.')
                return redirect('teach02')
        else:
            bot_item = request.user.bot_set.first()

            context = generate_context(request, 'teach')
            if bot_item is None:
                messages.info(
                    request, 'specified bot was not found in database.')
            else:
                log_file = bot_item.chatlog
                if log_file.name:
                    log_file.open(mode='rb')
                    log_text = log_file.read()
                    log_file.close()
                    context['logText'] = log_text
                else:
                    log_file.save('bot_log.txt', ContentFile(''))
                    context['logText'] = ''

            return render(request, 'teach02.html', context)
    else:
        messages.info(request, 'you must be logged in first.')
        return redirect('login')


def setting00(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            bot_item = request.user.bot_set.first()
            if bot_item is None:
                messages.info(
                    request, 'specified bot was not found in database.')
                return redirect('setting00')

            if 'avtaarFile' in request.FILES:
                if not basename(bot_item.avtaar.name) == 'avtaar_default.png':
                    bot_item.avtaar.delete()
                bot_item.avtaar = request.FILES['avtaarFile']
            if 'defaultFile' in request.POST:
                if request.POST['defaultFile']:
                    bot_item.avtaar.delete()
                    filepath = generate_filepath('avtaar\\avtaar_default.png')
                    f = open(filepath, 'rb')
                    bot_item.avtaar.save('bot_avtaar.png', File(f))

            if len(request.POST['name']) < 4 or len(request.POST['name']) > 32:
                messages.info(
                    request, "name must be between 4 to 32 characters.")
            else:
                bot_item.name = request.POST['name']

            if len(request.POST['description']) > 128:
                messages.info(
                    request, "description must be less than 128 characters.")
            else:
                bot_item.description = request.POST['description']

            bot_item.visible = request.POST.get('visible', False)
            bot_item.greet = request.POST.get('greet', False)
            if 'message' in request.POST:
                bot_item.message = request.POST['message']
            bot_item.save()
            messages.info(request, 'bot settings successfully updated.')
            return redirect('setting00')
        else:
            context = generate_context(request, 'settings')

            bot_item = request.user.bot_set.first()
            if bot_item is None:
                messages.info(
                    request, 'specified bot was not found in database.')
            else:
                context['botItem'] = bot_item

            return render(request, 'setting00.html', context)
    else:
        messages.info(request, 'you must be logged in first.')
        return redirect('login')


def setting01(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_item = request.user
            if user_item is None:
                messages.info(
                    request, 'specified user was not found in database.')
                return redirect('setting01')

            if 'delete' in request.POST:
                user_item.delete()
                logout(request)
                messages.info(
                    request, 'account has been successfully deleted.')
                return redirect('home')

            if 'oldpass' in request.POST:
                if user_item.check_password(request.POST['oldpass']):
                    user_item.set_password(request.POST['newpass'])
                    messages.info(
                        request, 'password has been successfully changed.')
                else:
                    messages.info(
                        request, 'password didn\'t matched with current password.')
                return redirect('setting01')

            if 'firstname' in request.POST:
                if not user_item.first_name == request.POST['firstname']:
                    user_item.first_name = request.POST['firstname']
            if 'lastname' in request.POST:
                if not user_item.last_name == request.POST['lastname']:
                    user_item.last_name = request.POST['lastname']
            if 'email' in request.POST:
                if not user_item.email == request.POST['email']:
                    if User.objects.filter(email=request.POST['email']).exists():
                        messages.info(
                            request, 'specified e-mail has been already taken.')
                    else:
                        user_item.email = request.POST['email']

            user_item.save()
            messages.info(request, 'user settings successfully updated.')
            return redirect('setting01')
        else:
            context = generate_context(request, 'settings')
            context['userItem'] = request.user
            return render(request, 'setting01.html', context)
    else:
        messages.info(request, 'you must be logged in first.')
        return redirect('login')


def embed(request):
    if request.user.is_authenticated:
        context = generate_context(request, 'embed')

        bot_item = request.user.bot_set.first()
        if bot_item is None:
            messages.info(request, 'specified bot was not found in database.')
        else:
            context['botId'] = bot_item.pk

        return render(request, 'embed.html', context)
    else:
        messages.info(request, 'you must be logged in first.')
        return redirect('login')


@xframe_options_exempt
def window(request, bot_id):
    bot_item = Bot.objects.get(pk=bot_id)
    if bot_item.visible:
        return render(request, 'window.html', {'botItem': bot_item})
    else:
        return render(request, 'window.html', {'alertText': 'specified bot is not available for viewing.'})
