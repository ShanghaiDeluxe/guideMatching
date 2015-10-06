import re
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from user.models import User

error_message = {
    'username': {
        'required': 'ID 항목을 입력해주세요.',
        'min_length': '최소 %(limit_value)d자 이상으로 입력해주세요. (현재 %(show_value)d자)',
        'max_length': '최대 %(limit_value)d자 이하로 입력해주세요. (현재 %(show_value)d자)',
    },
    'password': {
        'required': 'Password 항목을 입력해주세요.',
        'min_length': '최소 %(limit_value)d자 이상으로 입력해주세요. (현재 %(show_value)d자)',
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
    def _username(self, username):
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('사용자 이름은 알파벳, 숫자, 밑줄(_)만 가능합니다.')

    @staticmethod
    def exist_username(self, username):
        Clean._username(self, username)
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('이미 사용 중인 사용자 정보입니다.')

    @staticmethod
    def not_exist_username(self, username):
        Clean._username(self, username)
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise forms.ValidationError('없는 사용자 정보입니다.')
        return username

    @staticmethod
    def exist_email(self, email):
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('이미 사용 중인 사용자 정보입니다.')

    @staticmethod
    def not_exist_email(self, email):
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise forms.ValidationError('없는 사용자 정보입니다.')
        return email


class SendForm(forms.Form):
    username = forms.CharField(label='ID', min_length=4, max_length=30, required=True,
                               error_messages=error_message['username'])
    email = forms.EmailField(label="Email", required=True,
                             widget=forms.EmailInput, error_messages=error_message['email'])

    def clean_username(self):
        return Clean.not_exist_username(self, self.cleaned_data['username'])

    def clean_email(self):
        return Clean.not_exist_email(self, self.cleaned_data['email'])


class LostForm(forms.Form):
    username = forms.CharField(label='ID', min_length=4, max_length=30, required=True,
                               error_messages=error_message['username'])
    email = forms.EmailField(label="Email", required=True,
                             widget=forms.EmailInput, error_messages=error_message['email'])
    cert_code = forms.CharField(label='Code', max_length=30, required=True,
                                error_messages=error_message['cert_code'])

    def clean_username(self):
        return Clean.not_exist_username(self, self.cleaned_data['username'])

    def clean_email(self):
        return Clean.not_exist_email(self, self.cleaned_data['email'])


class JoinForm(forms.Form):
    username = forms.CharField(label='ID', min_length=4, max_length=30, required=True,
                               error_messages=error_message['username'])
    password = forms.CharField(label="Password", min_length=6, max_length=30, required=True,
                               widget=forms.PasswordInput, error_messages=error_message['password'])
    password_check = forms.CharField(label="Password(again)", min_length=6, max_length=30, required=True,
                                     widget=forms.PasswordInput, error_messages=error_message['password'])

    def clean_password_check(self):
        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            password_check = self.cleaned_data['password_check']
            if password == password_check:
                return password_check

            else:
                raise forms.ValidationError('비밀번호가 일치하지 않습니다.')

        raise forms.ValidationError('비밀번호를 정확히 입력해주세요.')

    def clean_username(self):
        return Clean.exist_username(self, self.cleaned_data['username'])
