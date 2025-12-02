import requests

API_KEY = "6d8dc587c10b44fd91632de4297ddeea"
BASE_URL = "https://newsapi.org/v2"


def safe_request(url, params):
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if data.get("status") != "ok":
            print("API returned error:", data)
            return []

        return data.get("articles", [])

    except Exception as e:
        print("API ERROR:", e)
        return []


# Fetch general news
def fetch_api_news(query="South Africa"):
    url = f"{BASE_URL}/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": API_KEY,
        "pageSize": 20,
    }
    return safe_request(url, params)


# Fetch category news
def fetch_category_news(category):
    # Map categories to search terms
    mapping = {
        "technology": "technology south africa",
        "business": "business south africa",
        "sports": "sports south africa",
        "entertainment": "entertainment south africa",
        "health": "health south africa",
        "science": "science south africa",
    }

    query = mapping.get(category, "south africa news")

    url = f"{BASE_URL}/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": API_KEY,
        "pageSize": 20,
    }
    return safe_request(url, params)


# Trending = most recent
def fetch_trending_news():
    url = f"{BASE_URL}/everything"
    params = {
        "q": "breaking news south africa",
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": API_KEY,
        "pageSize": 20,
    }
    return safe_request(url, params)
