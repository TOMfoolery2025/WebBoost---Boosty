import requests
import sys

def test_django_app():
    base_url = "http://127.0.0.1:8001"
    
    # 1. Test Landing Page
    print("Testing Landing Page...")
    try:
        resp = requests.get(base_url)
        if resp.status_code == 200 and "Website Analyzer" in resp.text:
            print("SUCCESS: Landing page loaded.")
        else:
            print(f"FAILURE: Landing page status {resp.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"FAILURE: Could not connect to {base_url}: {e}")
        sys.exit(1)

    # 2. Test Analysis (POST)
    print("\nTesting Analysis Flow...")
    try:
        # Need to get CSRF token first if we were a real browser, but for this simple test 
        # we might hit 403 Forbidden because of CSRF protection. 
        # For this quick test script, we'll just check if the endpoint exists.
        # To properly test POST, we'd need a client that handles cookies/CSRF like requests.Session()
        
        client = requests.Session()
        resp = client.get(base_url)
        if 'csrfmiddlewaretoken' in resp.text:
             # Extract token (simple split, not robust parsing)
            csrf_token = resp.text.split('name="csrfmiddlewaretoken" value="')[1].split('"')[0]
            
            data = {'url': 'https://example.com', 'csrfmiddlewaretoken': csrf_token}
            headers = {'Referer': base_url}
            
            post_resp = client.post(f"{base_url}/analyze/", data=data, headers=headers)
            
            if post_resp.status_code == 200 and "Analysis Result" in post_resp.text:
                print("SUCCESS: Analysis flow worked.")
                if "70/100" in post_resp.text:
                     print("SUCCESS: Score calculation verified (70/100).")
            else:
                print(f"FAILURE: Analysis failed. Status: {post_resp.status_code}")
                # print(post_resp.text)
        else:
            print("WARNING: Could not find CSRF token to test POST.")

    except Exception as e:
        print(f"FAILURE: Error during analysis test: {e}")

if __name__ == "__main__":
    test_django_app()
