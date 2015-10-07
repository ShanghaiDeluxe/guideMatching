from smtplib import SMTPException, SMTPAuthenticationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import auth_login
from django.contrib.sites.shortcuts import get_current_site
from django.core.context_processors import csrf
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from travel.forms import SearchForm
from user.forms import JoinForm, LostForm, SendForm
from user.models import User, MyStation, MyUser
from django.contrib.auth.forms import AuthenticationForm


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
        return render_to_response('login.html', context)


def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = JoinForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                User.objects.create_user(username=username, password=password)
                MyUser.objects.create(user=User.objects.get(username=username))

                return HttpResponseRedirect('/')

        else:
            form = JoinForm()

        context = RequestContext(request, {
            'form': form
        })
        context.update(csrf(request))

        return render_to_response("signup.html", context)


def lost(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    else:
        if request.method == 'POST':
            form = LostForm(request.POST)
            if form.is_valid():
                username = User.objects.get(username=form.cleaned_data['username'])
                email = User.objects.get(email=form.cleaned_data['email'])

                if username.id != email.id:
                    form.add_error('username', '없는 사용자 정보입니다.')
                    form.add_error('email', '없는 사용자 정보입니다.')
                    return JsonResponse({"status": 0, "messages": form.errors})

                else:
                    my_user = MyUser.objects.get(user=username)
                    if my_user.cert_code != form.cleaned_data['cert_code']:
                        form.add_error('cert_code', '인증번호가 틀렸습니다.')
                        return JsonResponse({"status": 0, "messages": form.errors})

                    username.set_password(form.cleaned_data['password_check'])
                    username.save()

                    my_user.cert_code = ''
                    my_user.save()

                return JsonResponse({"status": 1})

            return JsonResponse({"status": 0, "messages": form.errors})

        else:
            form = LostForm()

            context = RequestContext(request, {
                'form': form
            })
            context.update(csrf(request))

            return render_to_response("lost.html", context)


def send_code(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    else:
        if request.method == 'POST':
            form = SendForm(request.POST)
            if form.is_valid():
                username = User.objects.get(username=form.cleaned_data['username'])
                email = User.objects.get(email=form.cleaned_data['email'])

                if username.id == email.id:
                    my_user = MyUser.objects.get(user=username)
                    my_user.cert_code = User.objects.make_random_password(20)
                    my_user.save()
                else:
                    form.add_error('username', '없는 사용자 정보입니다.')
                    form.add_error('email', '없는 사용자 정보입니다.')
                    return JsonResponse({"status": 0, "messages": form.errors})

                try:
                    my_user.send()
                except (SMTPException, SMTPAuthenticationError):
                    return JsonResponse({"status": 0, "messages": "메일 전송에 실패하였습니다."})

                return JsonResponse({"status": 1})
            else:
                return JsonResponse({"status": 0, "messages": form.errors})

        else:
            return HttpResponseRedirect('/')


@login_required(login_url='/login/')
def index(request):
    form = SearchForm()
    search_result = []
    show_results = False
    if 'query' in request.GET:
        show_results = True
        query = request.GET['query'].strip()
        if query:
            form = SearchForm({'query': query})
            search_result = MyStation.objects.filter(station__icontains=query)[:10]
    context = RequestContext(request, {
        'form': form,
        'search_result': search_result,
        'show_results': show_results,
        'show_email': True,
    })

    if request.is_ajax():
        return render_to_response('guide_list.html', context)
    else:
        return render_to_response('index.html', context)
