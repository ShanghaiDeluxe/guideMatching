from django import forms
from django.contrib.auth.models import User


error_message = {
    'email': {
        'required': 'E-Mail 항목을 입력해주세요.',
        'min_length': '최소 %(limit_value)d자 이상으로 입력해주세요. (현재 %(show_value)d자)',
        'max_length': '최대 %(limit_value)d자 이하로 입력해주세요. (현재 %(show_value)d자)'
    },
    'password': {
        'required': 'Password 항목을 입력해주세요.',
        'min_length': '최소 %(limit_value)d자 이상으로 입력해주세요. (현재 %(show_value)d자)'
    },
    'auth_code': {
        'required': 'Cert Code 항목을 입력해주세요.',
        'max_length': '%(limit_value)d자를 입력해주세요. (현재 %(show_value)d자)'
    }
}


class LoginForm(forms.Form):
    email = forms.EmailField(label="E-Mail", min_length=4, max_length=50, required=True,
                             error_messages=error_message['email'])
    password = forms.CharField(label="Password", min_length=6, max_length=12, required=True,
                               widget=forms.PasswordInput, error_messages=error_message['password'])


class JoinForm(forms.Form):
    email = forms.EmailField(label="E-Mail", min_length=4, max_length=50, required=True,
                             error_messages=error_message['email'])
    auth_code = forms.EmailField(label="Cert Code", max_length=20, required=True,
                                 error_messages=error_message['auth_code'])
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

        raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
