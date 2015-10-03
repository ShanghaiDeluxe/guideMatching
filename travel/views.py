from django.http.response import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
from django.template.loader import get_template
from travel.forms import SearchForm
from user.models import MyStation


def travel_search(request):
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
        return render_to_response('main_page.html', context)


def guide_list(request):
    return HttpResponse("guide_list")


def guide(request):
    return HttpResponse("guide")
