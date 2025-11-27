from django.shortcuts import render
from django.http import HttpResponse
from .logic import fetch_page, analyze_page

def index(request):
    return render(request, 'analyzer_app/index.html')

def analyze(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if not url:
            return render(request, 'analyzer_app/index.html', {'error': 'Please provide a URL.'})
        
        try:
            analysis_data = analyze_page(url)
            return render(request, 'analyzer_app/result.html', {'data': analysis_data, 'url': url})
        except ValueError as e:
            return render(request, 'analyzer_app/index.html', {'error': str(e)})
    
    return render(request, 'analyzer_app/index.html')
