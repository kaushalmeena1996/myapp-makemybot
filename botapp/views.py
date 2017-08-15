from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from botapp.helper.helper import (
    valid_username, valid_email, valid_password, generate_context)
from .models import Bot


def signin(request):
    """CONNECTS the user."""
    if request.user.is_authenticated:
        messages.info(request, 'You have already logged in.')
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
        messages.info(request, 'You have successfully logged out.')
        return redirect('home')
    else:
        messages.info(request, 'You have already logged out.')
        return redirect('home')


def signup(request):
    """CONNECTS the user."""
    if request.user.is_authenticated:
        messages.info(request, 'You have already logged in.')
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

            if len(email) > 0:
                if len(email) > 64:
                    messages.info(
                        request, "lastname must be not be more than 64 characters.")
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
                user = User.objects.create_user(
                    username, email, password, first_name=firstname, last_name=lastname)
                user.save()
                if user is not None:
                    login(request, user)
                    messages.info(request, "You have successfully signuped.")
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
    if request.user.is_authenticated:
        query = request.GET.get('query')
        page = request.GET.get('page')
        context = generate_context(request, 'chatbots')

        if query:
            paginator = Paginator(Bot.objects.filter(name__icontains=query), 1)
            context['botQuery'] = query
        else:
            paginator = Paginator(Bot.objects.all(), 25)
        try:
            bot_list = paginator.page(page)
        except PageNotAnInteger:
            bot_list = paginator.page(1)
        except EmptyPage:
            bot_list = paginator.page(paginator.num_pages)

        bot_item = request.user.bot_set.first()
        context['botList'] = bot_list
        context['botId'] = bot_item.id
        return render(request, 'chatbots00.html', context)

    else:
        messages.info(request, 'You must be logged in first.')
        return redirect('login')


def chatbots01(request, bot_id):
    if request.user.is_authenticated:
        bot_item = Bot.objects.get(pk=bot_id)
        context = generate_context(request, 'chatbots')

        if bot_item:
            context['botItem'] = bot_item
            context['chatPage'] = True
        else:
            messages.info(request, 'Specified bot was not found.')

        return render(request, 'chatbots01.html', context)
    else:
        messages.info(request, 'You must be logged in first.')
        return redirect('login')


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
        bot_item = request.user.bot_set.first()
        context = generate_context(request, 'chat')

        if bot_item:
            context['botItem'] = bot_item
            context['chatPage'] = True
        else:
            messages.info(request, 'Specified bot was not found.')

        return render(request, 'chat.html', context)
    else:
        messages.info(request, 'You must be logged in first.')
        return redirect('login')


def teach00(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            brain_text = request.POST['brainText']
            bot_item = request.user.bot_set.first()
            brain_file = bot_item.brain
            brain_file.open(mode='wb')
            brain_file.write(brain_text)
            brain_file.close()

            messages.info(request, 'brain file edited successfully.')
            return redirect('teach00')
        else:
            bot_item = request.user.bot_set.first()
            brain_file = bot_item.brain
            brain_file.open(mode='rb')
            brain_text = brain_file.read()
            brain_file.close()

            context = generate_context(request, 'teach')
            context['brainText'] = brain_text
            return render(request, 'teach00.html', context)
    else:
        messages.info(request, 'You must be logged in first.')
        return redirect('login')


def teach01(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.FILES['brainfile']:
                bot_item = request.user.bot_set.first()
                bot_item.brain = request.FILES['brainfile']
                bot_item.save()
                messages.info(request, 'brain file uploaded successfully.')
            else:
                messages.info(request, 'brain file was no found.')
            return redirect('teach01')
        else:
            context = generate_context(request, 'teach')
            return render(request, 'teach01.html', context)
    else:
        messages.info(request, 'You must be logged in first.')
        return redirect('login')


def setting00(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.FILES['brainfile']:
                bot_item = request.user.bot_set.first()
                bot_item.brain = request.FILES['brainfile']
                bot_item.save()
                messages.info(request, 'brain file uploaded successfully.')
            else:
                messages.info(request, 'brain file was no found.')
            return redirect('teach01')
        else:
            bot_item = request.user.bot_set.first()
            context = generate_context(request, 'setting')
            context['botItem'] = bot_item
            return render(request, 'setting00.html', context)
    else:
        messages.info(request, 'You must be logged in first.')
        return redirect('login')


def setting01(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.FILES['brainfile']:
                bot_item = request.user.bot_set.first()
                bot_item.brain = request.FILES['brainfile']
                bot_item.save()
                messages.info(request, 'brain file uploaded successfully.')
            else:
                messages.info(request, 'brain file was no found.')
            return redirect('teach01')
        else:
            context = generate_context(request, 'setting')
            return render(request, 'setting01.html', context)
    else:
        messages.info(request, 'You must be logged in first.')
        return redirect('login')


def embed(request):
    if request.user.is_authenticated:
        bot_item = request.user.bot_set.first()
        context = generate_context(request, 'embed')
        context['botId'] = bot_item.pk
        return render(request, 'embed.html', context)
    else:
        messages.info(request, 'You must be logged in first.')
        return redirect('login')
