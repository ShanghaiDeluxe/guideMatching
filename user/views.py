from django.conf import settings
from django.contrib import auth
from django.contrib.auth import logout
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import Context
from django.template.loader import get_template
from user.forms import LoginForm, JoinForm
from user.models import User


def login(request):
    pass
    # if request.method == 'POST':
    #     form_data = LoginForm(request.POST)
    #
    #     if form_data.is_valid():
    #         username = form_data.cleaned_data['id']
    #         password = form_data.cleaned_data['password']
    #         user = auth.authenticate(username=username, password=password)
    #
    #         if user is not None:
    #             if user.is_active:
    #                 auth.login(request, user)
    #
    #                 return HttpResponseRedirect('/board/')
    #
    # else:
    #     form_data = LoginForm()
    #
    # context = Context({'login_form': form_data})
    # context.update(csrf(request))
    #
    # return render_to_response('login.html', context)


def logout(request):
    logout(request)
    return HttpResponseRedirect("/user/login/")


def signup(request):
    pass
    # if request.method == 'POST':
    #     form = JoinForm(request.POST)
    #
    #     if form.is_valid():
    #         email = form.cleaned_data['email']
    #         password = form.cleaned_data['password']
    #         User.objects.create(
    #             email=form.cleaned_data['username'],
    #             password=form.cleaned_data['password'],
    #         )
    #         # if user is not None:
    #         #     if user.is_active:
    #         #         auth.login(request, user)
    #         #
    #         #         return HttpResponseRedirect('/board/')
    #
    # else:
    #     form = JoinForm()
    #
    # context = Context({'login_form': form})
    # context.update(csrf(request))
    # return render_to_response("signup.html")


# def send_auth_mail(request):
#     if 'auth_code' in self.cleaned_data:
#         auth_code = self.cleaned_data['auth_code']
#         auth_code2 = User.objects.make_random_password(20)
#         if auth_code == auth_code2:
#             return True
#
#     raise forms.ValidationError('인증코드가 일치하지 않습니다.')

# def send_auth_mail(request):
#     subject = 'Guide Matching Application 인증 번호 입니다.'
#     template = get_template('auth.txt')
#     context = Context({
#         'name': request.POST.,
#         'sender': self.sender.username,
#     })
#     message = template.render(context)
#     send_mail(
#         subject, message, settings.EMAIL_HOST_USER, [self.email]
#     )


def user_info(request):
    return HttpResponse("user_info")


def lost(request):
    return HttpResponse("lost")


def status(request):
    return HttpResponse("status")


def post(request):
    return HttpResponse("post")
