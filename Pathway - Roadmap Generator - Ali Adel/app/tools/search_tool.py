import requests

def google_search(API_KEY, CX, query, max_results=5):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CX,
        "q": query,
        "num": max_results
    }

    response = requests.get(url, params=params)
    data = response.json()
    
    results = []
    for item in data.get("items", []):
        results.append({
            "title": item["title"],
            "link": item["link"],
            "snippet": item["snippet"]
        })

    return results