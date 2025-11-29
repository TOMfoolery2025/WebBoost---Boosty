from django.shortcuts import render, redirect
from django.http import HttpResponse
from .logic import fetch_page, analyze_page

def index(request):
    return render(request, 'analyzer_app/index.html')

def analyze(request):
    url = None
    if request.method == 'POST':
        url = request.POST.get('url')
        if url:
            request.session['analyzed_url'] = url
    else:
        # Try to get from session if not POST (e.g. redirect after login)
        url = request.session.get('analyzed_url')

    if not url:
        return render(request, 'analyzer_app/index.html', {'error': 'Please provide a URL.'})
    
    try:
        # Check if we have cached analysis results for this URL
        cached_data_key = f'analysis_data_{url}'
        
        if cached_data_key in request.session:
            # Use cached analysis results to prevent score changes
            analysis_data = request.session[cached_data_key]
        else:
            # Perform new analysis and cache it
            html_content = fetch_page(url)
            analysis_data = analyze_page(html_content, url=url)
            request.session[cached_data_key] = analysis_data
        
        is_premium = request.session.get('is_premium', False)
        return render(request, 'analyzer_app/result.html', {
            'data': analysis_data, 
            'url': url,
            'is_premium': is_premium
        })
    except ValueError as e:
        return render(request, 'analyzer_app/index.html', {'error': str(e)})

def pricing(request):
    return render(request, 'analyzer_app/pricing.html')

def register(request):
    if request.method == 'POST':
        # Simulate registration
        request.session['is_premium'] = True
        return redirect('analyze')
    return render(request, 'analyzer_app/register.html')

def premium_dashboard(request):
    return render(request, 'analyzer_app/premium_dashboard.html')

def logout(request):
    # Clear all session data
    request.session.flush()
    return redirect('index')
