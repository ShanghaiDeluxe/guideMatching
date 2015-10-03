from django.http.response import HttpResponse
from django.template.loader import get_template


def index(request):
    # if 로그인 안했으면 redirect -> /user/login으로
    # else 했으면 그냥 index template view
    template = get_template('index.html')
    # context = {'user': }
    return HttpResponse(template)
