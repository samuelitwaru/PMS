from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib import messages
from django.template.loader import get_template
from django.http import HttpResponseRedirect, JsonResponse
from models import User, Token
from tasks.tasks import send_auth_mail
from utils import set_user_token
from ..forms import LoginForm, SetPasswordForm, ForgotPasswordForm, AuthenticationForm
from ..guards import *


def index(request):
    if get_user(request).is_authenticated:
        return render(request, 'home/home.html')
    else:
        return redirect('core:login')


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)

        if user:
            login(request, user)
            return redirect("core:index")
        else:
            messages.error(request, f"User not found!", extra_tags="danger")
            return redirect("core:login")
    else:
        if get_user(request).is_authenticated:
            return redirect('core:index')

        form = LoginForm()
        context = {"form": form}
        return render(request, 'auth/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('core:login')


def forgot_password(request):
    forgot_password_form = ForgotPasswordForm()
    if request.method == "POST":
        forgot_password_form = ForgotPasswordForm(request.POST)
        if forgot_password_form.is_valid():
            cleaned_data = forgot_password_form.cleaned_data
            user = cleaned_data.get("email")
            # set auth token
            set_user_token(user)
            # send email
            send_auth_mail(user.username)
            # send_auth_mail.delay(user.email)
            messages.info(request, f"An email with password reset instructions has been sent to '{user.username}'. Login to your this email to continue.")
            return redirect("core:index")

    context = {"forgot_password_form": forgot_password_form}
    return render(request, "auth/forgot-password.html", context)  


def set_password(request, token):
    token = Token.objects.filter(token=token).first()
    if not token or token.is_expired():
        token.delete()
        messages.error(request, "Your token is invalid or has expired", extra_tags="danger")
        return redirect("core:index")

    user = token.user
    set_password_form = SetPasswordForm()
    if request.method == "POST":
        set_password_form = SetPasswordForm(request.POST)
        if set_password_form.is_valid():
            cleaned_data = set_password_form.cleaned_data
            password = cleaned_data.get("password")
            user.set_password(password)
            user.save()
            token.delete()
            messages.info(request, "Password set. Login with your new password.")
            return redirect("core:index")
    
    context = {"target_user":user, "set_password_form": set_password_form}
    return render(request, "auth/set-password.html", context)     


def authentication(request):
    if request.method == "POST":
        authentication_form = AuthenticationForm(request.POST)
        if authentication_form.is_valid():
            current_user = get_user(request)
            redirect_url = authentication_form.cleaned_data.get('redirect_url')
            password = authentication_form.cleaned_data.get('password')
            user = authenticate(username=current_user.username, password=password)
            if user:
                return HttpResponseRedirect(redirect_url)
            else:
                messages.error(request, "Failed to authenticate you!", extra_tags="danger")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', None) or '/')
        messages.warning(request, "Failed!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', None) or '/')
    else:
        redirect_url = request.GET.get("redirect_url")
        authentication_form = AuthenticationForm({"redirect_url": redirect_url})
        context = {"authentication_form": authentication_form}
        authentication_form_container_template = render(request, 'auth/authenticate.html', context)
        data = {
            "form_templates": {
                "#authenticationFormContainer":authentication_form_container_template.content.decode()
            }
        }
        return JsonResponse(data)
