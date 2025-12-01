import requests

API_KEY = "644b16b6bbd0a064b9057e1beca7f2bc"
BASE_URL = "https://newsapi.org/v2"


# -------------------------------------------------------
# Safe Request Function (Prevents App From Crashing)
# -------------------------------------------------------
def safe_request(url, params):
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        # NewsAPI returns status != 'ok' when there's an error
        if data.get("status") != "ok":
            return []

        return data.get("articles", [])

    except Exception as error:
        print(f"API Error: {error}")
        return []  # return empty list so app does not break


# -------------------------------------------------------
# Fetch General News
# -------------------------------------------------------
def fetch_api_news(q="latest"):
    if not API_KEY or API_KEY == "644b16b6bbd0a064b9057e1beca7f2bc":
        return demo_articles("General News (Demo Mode)")

    url = f"{BASE_URL}/everything"
    params = { 
        "q": q,
        "language": "en",
        "apiKey": API_KEY,
        "pageSize": 20,
        "sortBy": "publishedAt",
    }

    return safe_request(url, params)


# -------------------------------------------------------
# Fetch News by Category
# -------------------------------------------------------
def fetch_category_news(category):
    if not API_KEY or API_KEY == "644b16b6bbd0a064b9057e1beca7f2bc":
        return demo_articles(f"{category} News (Demo Mode)")

    url = f"{BASE_URL}/top-headlines"
    params = {
        "category": category,
        "country": "us",
        "apiKey": API_KEY,
        "pageSize": 20,
    }

    return safe_request(url, params)


# -------------------------------------------------------
# Fetch Trending News
# -------------------------------------------------------
def fetch_trending_news():
    if not API_KEY or API_KEY == "644b16b6bbd0a064b9057e1beca7f2bc":
        return demo_articles("Trending News (Demo Mode)")

    url = f"{BASE_URL}/everything"
    params = {
        "q": "breaking",
        "sortBy": "popularity",
        "language": "en",
        "apiKey": API_KEY,
        "pageSize": 20,
    }

    return safe_request(url, params)


# -------------------------------------------------------
# DEMO ARTICLES (Used when API fails or key missing)
# -------------------------------------------------------
def demo_articles(title="General News"):
    return [
        {
            "title": f"{title} Example Article 1",
            "description": "This is a demo article because the API key is missing or API failed.",
            "urlToImage": "https://via.placeholder.com/800x450.png?text=Demo+News+Image+1",
            "url": "#",
            "author": "Demo Author",
        },
        {
            "title": f"{title} Example Article 2",
            "description": "You are seeing demo data. Add your NewsAPI key to fetch real news.",
            "urlToImage": "https://via.placeholder.com/800x450.png?text=Demo+News+Image+2",
            "url": "#",
            "author": "Demo Author",
        }
    ]
