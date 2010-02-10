from django.shortcuts import render_to_response

def index(request):
    data = {}
    return render_to_response('reports/index.html', data)
