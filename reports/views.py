from django.shortcuts import render_to_response

def index(request):
    return render_to_response('reports/index.html')

def weekly_report(request, user_id, year, week_num):
    return render_to_response('reports/weekly_report.html')