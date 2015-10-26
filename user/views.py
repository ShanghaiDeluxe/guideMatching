from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.db.backends.mysql.base import DatabaseError
from django.http.response import HttpResponse, Http404, JsonResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from rest_framework.status import HTTP_400_BAD_REQUEST
from travel.models import DefaultStation, MatchTravel, Comment
from user.forms import UserInfoForm, ReviewForm
from user.models import MyUser, MyStation, Language


@login_required(login_url='/login/')
def user_info(request):
    comment_list = []
    if request.method == "POST":
        form = UserInfoForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                my_user = MyUser.objects.get(id=request.user.id)
            except ObjectDoesNotExist:
                raise Http404

            if not request.user.check_password(request.POST['password']):
                return HttpResponse("비밀번호가 틀립니다.")

            modified_place(request, form)
            modified_language(request, form)
            my_user = modified_my_user(request, form, my_user)
            request = modified_request_user(request, form)

            if 'profile_picture' in request.FILES:
                handle_uploaded_file(request.FILES['profile_picture'], my_user.profile_picture.name)

        else:
            return HttpResponse(form.errors)
    else:
        try:
            my_user = MyUser.objects.get(user=request.user)
            matches = MatchTravel.objects.filter(to_user=request.user, is_active=0)
            if len(matches) > 0:
                for match in matches:
                    if Comment.objects.get(when=match):
                        comment_list.append([Comment.objects.get(when=match), match.from_user,
                                             MyUser.objects.get(user=match.from_user)])
        except ObjectDoesNotExist:
            raise Http404

        form = UserInfoForm()

    my_stations = []
    for station in MyStation.objects.filter(user=request.user):
        my_stations.append(station)

    my_languages = []
    for language in Language.objects.filter(user=request.user):
        my_languages.append(language)

    user_list = (request.user, my_user)

    context = RequestContext(request, {
        'form': form,
        'default_picture': 'static/profile/default_picture.jpg',
        'user_list': user_list,
        'comment_list': comment_list,
        'places': my_stations,
        'languages': my_languages,
    })
    context.update(csrf(request))

    return render_to_response('user/user.html', context)


def modified_place(request, form):
    if 'place' in request.POST and request.POST['place'] != '':
        MyStation.objects.filter(user=request.user).delete()
        if '0' not in form.cleaned_data['place']:
            try:
                for station_temp in form.cleaned_data.get('place'):
                    station = DefaultStation.objects.get(station_code=station_temp)
                    MyStation.objects.create(station=station, user=request.user)
            except ObjectDoesNotExist:
                raise Http404


def modified_language(request, form):
    if 'language' in request.POST and request.POST['language'] != '':
        Language.objects.filter(user=request.user).delete()
        try:
            for language_temp in form.cleaned_data.get('language'):
                Language.objects.create(language=language_temp, user=request.user)
        except ObjectDoesNotExist:
            raise Http404


def modified_my_user(request, form, my_user):
    if 'picture_delete' in request.POST and request.POST['picture_delete'] == '1':
        my_user.profile_picture.delete()
    if 'profile_picture' in request.FILES:
        if my_user.profile_picture:
            my_user.profile_picture.delete()
        my_user.profile_picture = form.cleaned_data['profile_picture']
    if 'gender' in request.POST:
        my_user.gender = form.cleaned_data['gender'].strip()
    if 'about_me' in request.POST:
        my_user.about_me = form.cleaned_data['about_me'].strip()

    my_user.save()
    return my_user


def modified_request_user(request, form):
    if 'first_name' in request.POST:
        request.user.first_name = form.cleaned_data['first_name'].strip()
    if 'last_name' in request.POST:
        request.user.last_name = form.cleaned_data['last_name'].strip()
    if 'email' in request.POST:
        request.user.email = form.cleaned_data['email'].strip()

    if 'change_password_check' in request.POST and request.POST['change_password_check'] != '':
        try:
            request.user.set_password(form.cleaned_data['change_password_check'])
            request.user.save()
            update_session_auth_hash(request, request.user)
            return request
        except ObjectDoesNotExist:
            raise Http404

    request.user.save()
    return request


def handle_uploaded_file(f, name):
    with open(name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required(login_url='/login/')
def match_list(request):
    calls_list = []
    receives_list = []
    before_travels1_list = []
    before_travels2_list = []

    try:
        calls = MatchTravel.objects.filter(from_user=request.user, is_active=1).order_by('created')
        receives = MatchTravel.objects.filter(to_user=request.user, is_active=1).order_by('created')
        before_travels1 = MatchTravel.objects.filter(from_user=request.user, is_active=0).order_by('created')
        before_travels2 = MatchTravel.objects.filter(to_user=request.user, is_active=0).order_by('created')

        for call in calls:
            calls_list.append([call, MyUser.objects.get(user=call.to_user)])

        for receive in receives:
            receives_list.append([receive, MyUser.objects.get(user=receive.from_user)])

        for before_travel in before_travels1:
            before_travels1_list.append([before_travel, MyUser.objects.get(user=before_travel.to_user)])

        for before_travel in before_travels2:
            before_travels2_list.append([before_travel, MyUser.objects.get(user=before_travel.from_user)])

    except ObjectDoesNotExist:
        raise Http404

    context = RequestContext(request, {
        'calls': calls_list,
        'receives': receives_list,
        'before_travels1': before_travels1_list,
        'before_travels2': before_travels2_list,
    })

    return render_to_response('user/match_list.html', context)


def ask_status(request, match_id):

    try:
        match = MatchTravel.objects.get(id=match_id)

        if request.user == match.from_user:
            user = match.to_user
            my_user = MyUser.objects.get(user=user)
            my_stations = MyStation.objects.filter(user=user)
            my_languages = Language.objects.filter(user=user)

            if match.is_active == 1:
                if match.to_status == 'invite' and match.from_status == 'receive':
                    stat = 'invite'
                elif match.to_status == 'confirm' and match.from_status == 'confirm':
                    stat = 'confirm'
                else:
                    raise Exception(HTTP_400_BAD_REQUEST)

            elif match.is_active == 0:
                stat = 'complete'

            else:
                raise Exception(HTTP_400_BAD_REQUEST)

        elif request.user == match.to_user:
            user = match.from_user
            my_user = MyUser.objects.get(user=user)
            my_stations = MyStation.objects.filter(user=user)
            my_languages = Language.objects.filter(user=user)

            if match.is_active == 1:
                if match.to_status == 'invite' and match.from_status == 'receive':
                    stat = 'receive'
                elif match.to_status == 'confirm' and match.from_status == 'confirm':
                    stat = 'confirm'
                else:
                    raise Exception(HTTP_400_BAD_REQUEST)

            elif match.is_active == 0:
                stat = 'complete'

            else:
                raise Exception(HTTP_400_BAD_REQUEST)

        else:
            raise Exception(HTTP_400_BAD_REQUEST)

    except ObjectDoesNotExist:
        raise Http404

    user_list = (user, my_user)

    context = RequestContext(request, {
        'status': stat,
        'default_picture': 'static/profile/default_picture.jpg',
        'user_list': user_list,
        'places': my_stations,
        'languages': my_languages,
    })

    return context


@login_required(login_url='/login/')
def status(request, match_id):
    context = ask_status(request, match_id)
    context.update(csrf(request))
    try:
        match = MatchTravel.objects.get(id=match_id)
    except ObjectDoesNotExist:
        raise Http404

    if match.is_active == 0:
        if Comment.objects.get(when=match):
            context.update({'comment': Comment.objects.get(when=match)})
        context.update({'form': ReviewForm()})
    return render_to_response('user/match.html', context)


def cancel_guide(request, match_id):
    if request.method == "POST":
        try:
            match = MatchTravel.objects.get(id=match_id)
            match.delete()
            return JsonResponse({'result': '1'})
        except ObjectDoesNotExist:
            raise Http404


def accept_guide(request, match_id):
    if request.method == "POST":
        try:
            match = MatchTravel.objects.get(id=match_id)
            match.to_status = 'confirm'
            match.from_status = 'confirm'
            match.save()
            return JsonResponse({'result': '2'})
        except ObjectDoesNotExist:
            raise Http404


def complete_guide(request, match_id):

    if request.method == "POST":
        try:
            match = MatchTravel.objects.get(id=match_id)
            match.to_status = 'complete'
            match.from_status = 'complete'
            match.is_active = 0
            match.save()
            return JsonResponse({'result': '3'})
        except ObjectDoesNotExist:
            raise Http404


def review(request, match_id):
    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            try:
                match = MatchTravel.objects.get(id=match_id)
                if Comment.objects.get(when=match):
                    comment = Comment.objects.get(when=match)
                    comment.content = form.cleaned_data['content']
                    comment.save()
                else:
                    Comment.objects.create(when=match, content=form.cleaned_data['content'])

                return JsonResponse({'result': '1'})
            except ObjectDoesNotExist:
                raise Http404

        else:
            return JsonResponse({'result': '0'})
