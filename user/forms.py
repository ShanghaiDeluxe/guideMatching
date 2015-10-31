import re
from django import forms
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.forms.widgets import Textarea
from django.http.response import HttpResponseBadRequest
from rest_framework.status import HTTP_400_BAD_REQUEST
from travel.models import DefaultStation
from user.models import User

options_place = []
options_place.append((0, 'No Guide'))
for station in DefaultStation.objects.all().exclude(line__in=['E', 'G', 'I', 'S', 'SU', 'U']).order_by('station'):
    options_place.append((station.station_code, station))


options_language = []
options_language.append(('0', '한국어'))
options_language.append(('1', 'English'))
options_language.append(('2', '日本語'))
options_language.append(('3', '中国'))


options_gender = []
options_gender.append(('0', 'Man'))
options_gender.append(('1', 'Woman'))


error_message = {
    'min_max': {
        'min_length': '최소 %(limit_value)d자 이상으로 입력해주세요. (현재 %(show_value)d자)',
        'max_length': '최대 %(limit_value)d자 이하로 입력해주세요. (현재 %(show_value)d자)',
    },
    'about_me': {
        'min_length': '최소 %(limit_value)d자 이상으로 입력해주세요. (현재 %(show_value)d자)',
        'max_length': '최대 %(limit_value)d자 이하로 입력해주세요. (현재 %(show_value)d자)',
    },
    'username': {
        'required': 'ID 항목을 입력해주세요.',
        'min_length': '최소 %(limit_value)d자 이상으로 입력해주세요. (현재 %(show_value)d자)',
        'max_length': '최대 %(limit_value)d자 이하로 입력해주세요. (현재 %(show_value)d자)',
    },
    'password': {
        'required': 'Password 항목을 입력해주세요.',
        'min_length': '최소 %(limit_value)d자 이상으로 입력해주세요. (현재 %(show_value)d자)',
    },
    'placeLanguage': {
        'invalid_choice': '올바른 선택이 아닙니다.',
        'invalid_list': '올바른 목록이 아닙니다.'
    },
    'email': {
        'required': 'Email 항목을 입력해주세요.',
    },
    'cert_code': {
        'required': '올바른 인증코드를 입력해주세요.'
    },
    'invalid_login': '정확한 Id \(%(username)s\)와 Password를 입력해주세요.',
}


class Clean:
    @staticmethod
    def _username(username):
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('사용자 이름은 알파벳, 숫자, 밑줄(_)만 가능합니다.')

    @staticmethod
    def exist_username(username):
        Clean._username(username)
        try:
            User.objects.get(username=username)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return username
        raise forms.ValidationError('이미 사용 중인 사용자 정보입니다.')

    @staticmethod
    def not_exist_username(username):
        Clean._username(username)
        try:
            User.objects.get(username=username)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            raise forms.ValidationError('없는 사용자 정보입니다.')
        return username

    @staticmethod
    def not_exist_email(email):
        try:
            User.objects.filter(email=email)
        except ObjectDoesNotExist:
            raise forms.ValidationError('없는 사용자 정보입니다.')
        return email

    @staticmethod
    def password_check(password, password_check):
        if password == password_check:
            return password_check

        raise forms.ValidationError('비밀번호가 일치하지 않습니다.')

    @staticmethod
    def name(name):
        if name != '':
            compiler = re.compile(r'^[A-Za-zㄱ-ㅣ가-힣]+')
            if compiler.findall(name):
                if name != compiler.findall(name)[0]:
                    raise forms.ValidationError('사용자 이름은 알파벳, 한글만 가능합니다.')
            else:
                raise forms.ValidationError('사용자 이름은 알파벳, 한글만 가능합니다.')
        return name

    @staticmethod
    def content(content):
        if content != '':
            compiler = re.compile(r'^[0-9A-Za-zㄱ-ㅣ가-힣]+')
            if compiler.findall(content):
                pass
            else:
                raise forms.ValidationError('내용은 알파벳, 한글, 숫자만 가능합니다.')
        return content


class SendForm(forms.Form):
    username = forms.CharField(label='ID', min_length=4, max_length=30, required=True,
                               error_messages=error_message['username'])
    email = forms.EmailField(label="Email", required=True,
                             widget=forms.EmailInput, error_messages=error_message['email'])

    def clean_username(self):
        return Clean.not_exist_username(self.cleaned_data['username'])

    def clean_email(self):
        return Clean.not_exist_email(self.cleaned_data['email'])


class LostForm(forms.Form):
    username = forms.CharField(label='ID', min_length=4, max_length=30, required=True,
                               error_messages=error_message['username'])
    email = forms.EmailField(label="Email", required=True,
                             widget=forms.EmailInput, error_messages=error_message['email'])
    cert_code = forms.CharField(label='Code', max_length=30, required=True,
                                error_messages=error_message['cert_code'])
    password = forms.CharField(label="Password", min_length=6, max_length=30, required=True,
                               widget=forms.PasswordInput, error_messages=error_message['password'])
    password_check = forms.CharField(label="Password(again)", min_length=6, max_length=30, required=True,
                                     widget=forms.PasswordInput, error_messages=error_message['password'])

    def clean_username(self):
        return Clean.not_exist_username(self.cleaned_data['username'])

    def clean_email(self):
        return Clean.not_exist_email(self.cleaned_data['email'])

    def clean_password_check(self):
        return Clean.password_check(self.cleaned_data['password'], self.cleaned_data['password_check'])


class SignupForm(forms.Form):
    username = forms.CharField(label='ID', min_length=4, max_length=30, required=True,
                               error_messages=error_message['username'])
    email = forms.EmailField(label="Email", required=True,
                             widget=forms.EmailInput, error_messages=error_message['email'])
    password = forms.CharField(label="Password", min_length=6, max_length=30, required=True,
                               widget=forms.PasswordInput, error_messages=error_message['password'])
    password_check = forms.CharField(label="Password(again)", min_length=6, max_length=30, required=True,
                                     widget=forms.PasswordInput, error_messages=error_message['password'])

    def clean_password_check(self):
        return Clean.password_check(self.cleaned_data['password'], self.cleaned_data['password_check'])

    def clean_username(self):
        return Clean.exist_username(self.cleaned_data['username'])


class UserInfoForm(forms.Form):
    profile_picture = forms.ImageField(widget=forms.FileInput, required=False)
    first_name = forms.CharField(label="First_Name", min_length=1, max_length=30, required=False,
                                 error_messages=error_message['min_max'])
    last_name = forms.CharField(label="Last_Name", min_length=1, max_length=30, required=False,
                                error_messages=error_message['min_max'])
    gender = forms.ChoiceField(label='Gender', choices=options_gender, required=False)
    place = forms.MultipleChoiceField(label='Place', widget=forms.SelectMultiple, choices=options_place,
                                      required=False, error_messages=error_message['placeLanguage'])
    language = forms.MultipleChoiceField(label='Language', widget=forms.SelectMultiple, choices=options_language,
                                         required=False, error_messages=error_message['placeLanguage'])
    about_me = forms.CharField(label='About_Me', max_length=300, required=False,
                               widget=Textarea, error_messages=error_message['about_me'])

    email = forms.EmailField(label="Email", required=True,
                             widget=forms.EmailInput, error_messages=error_message['email'])
    password = forms.CharField(label="Password(current)", min_length=6, max_length=30, required=True,
                               widget=forms.PasswordInput, error_messages=error_message['password'])
    change_password = forms.CharField(label="Password(change)", min_length=6, max_length=30, required=False,
                                      widget=forms.PasswordInput, error_messages=error_message['password'])
    change_password_check = forms.CharField(label="Password(change again)", min_length=6, max_length=30,
                                            required=False, widget=forms.PasswordInput,
                                            error_messages=error_message['password'])

    def clean_first_name(self):
        return Clean.name(self.cleaned_data['first_name'])

    def clean_last_name(self):
        return Clean.name(self.cleaned_data['last_name'])

    def clean_change_password_check(self):
        return Clean.password_check(self.cleaned_data['change_password'], self.cleaned_data['change_password_check'])


class ReviewForm(forms.Form):
    content = forms.CharField(label='About_Me', min_length=1, max_length=300, required=True,
                              widget=Textarea, error_messages=error_message['about_me'])

    def clean_content(self):
        return Clean.content(self.cleaned_data['content'])
