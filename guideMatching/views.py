from smtplib import SMTPException, SMTPAuthenticationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import auth_login
from django.contrib.sites.shortcuts import get_current_site
from django.core.context_processors import csrf
from django.core.exceptions import MultipleObjectsReturned
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
from user.forms import *
from user.models import User, MyUser
from django.contrib.auth.forms import AuthenticationForm


@csrf_exempt
def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                auth_login(request, form.get_user())

                return HttpResponseRedirect('/')
        else:
            form = AuthenticationForm(request)

        current_site = get_current_site(request)
        context = RequestContext(request, {
            'form': form,
            'site': current_site,
            'site_name': current_site.name,
        })
        context.update(csrf(request))
        return render_to_response('login.html', context)


@csrf_exempt
def signup(request):
    status = 0
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                if form.cleaned_data.get('username') and form.cleaned_data.get('password') and form.cleaned_data.get('email'):
                    username = form.cleaned_data.get('username')
                    password = form.cleaned_data.get('password')
                    email = form.cleaned_data.get('email')
                    User.objects.create_user(username=username, password=password, email=email,
                                             first_name='No', last_name='Name')
                    MyUser.objects.create(user=User.objects.get(username=username))
                    status = 1
        else:
            form = SignupForm()

        context = RequestContext(request, {
            'form': form,
            'status': status,
        })
        context.update(csrf(request))

        return render_to_response("signup.html", context)


@csrf_exempt
def lost(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    else:
        if request.method == 'POST':
            form = LostForm(request.POST)
            if form.is_valid():
                try:
                    user = User.objects.get(username=form.cleaned_data.get('username'))

                    if user.email != form.cleaned_data.get('email'):
                        return JsonResponse({'message': "We can't find user information."})

                    else:
                        my_user = MyUser.objects.get(user=user)
                        if form.cleaned_data.get('cert_code'):
                            if my_user.cert_code != form.cleaned_data.get('cert_code'):
                                return JsonResponse({'message': "You've put wrong code. Try again."})
                            else:
                                user.set_password(form.cleaned_data.get('password_check'))
                                user.save()

                                my_user.cert_code = ''
                                my_user.save()
                                return JsonResponse({
                                    'message': "Password has changed. Please login.",
                                    'status': "1",
                                })
                        else:
                            return JsonResponse({'message': "You've put wrong code. Try again."})
                except (ObjectDoesNotExist, MultipleObjectsReturned):
                    raise Http404
            else:
                return JsonResponse({'message': "You've put a wrong form."})
        else:
            form = LostForm()

            context = RequestContext(request, {
                'form': form,
            })
            context.update(csrf(request))

            return render_to_response("lost.html", context)


@csrf_exempt
def send_code(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    else:
        if request.method == 'POST':
            form = SendForm(request.POST)
            if form.is_valid():
                try:
                    user = User.objects.get(username=form.cleaned_data.get('username'))

                    if form.cleaned_data.get('email'):
                        if user.email != form.cleaned_data.get('email'):
                            return JsonResponse({'message': "We can't find user information."})
                        else:
                            my_user = MyUser.objects.get(user=user)
                            my_user.cert_code = User.objects.make_random_password(20)
                            my_user.save()
                    else:
                        return JsonResponse({'message': "You've put a wrong form."})

                except (ObjectDoesNotExist, MultipleObjectsReturned):
                    return JsonResponse({'message': "We can't find user information."})

                try:
                    my_user.send()
                except(SMTPException, SMTPAuthenticationError):
                    return JsonResponse({'message': "You've failed to send a request. Try again."})

                return JsonResponse({'message': "You've successed to send a code via email."})

            return JsonResponse({'message': "You've put a wrong form."})

        else:
            raise Http404


@login_required(login_url='/login/')
def index(request):
    return render_to_response('index.html')
