import requests
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import JsonResponse
from .models import NewsArticle, BreakingAlert, Category
from .forms import SubscriberForm
from django.http import JsonResponse
from .models import Article
from django.core.mail import send_mail


# JSON ENDPOINT (LOCAL NEWS ONLY)


def api_news(request):
    articles = Article.objects.all().values("title", "content", "author", "created_at")
    return JsonResponse(list(articles), safe=False)


# EXTERNAL API FETCH

def fetch_api_news():
    API_KEY = "644b16b6bbd0a064b9057e1beca7f2bc"
    API_URL = f"https://gnews.io/api/v4/top-headlines?category=general&lang=en&country=za&apikey={API_KEY}"

    try:
        response = requests.get(API_URL, timeout=5)
        data = response.json()

        articles = data.get("articles", [])

        formatted_articles = []
        for item in articles:
            formatted_articles.append({
                "title": item.get("title"),
                "content": item.get("description"),
                "image": item.get("image"),
                "published": item.get("publishedAt"),
                "url": item.get("url"),  # ⭐ ADD THIS
            })

        return formatted_articles

    except Exception as e:
        print("API ERROR:", e)
        return []



# HOME VIEW (LOCAL + API NEWS)

def home(request):

    search_query = request.GET.get("q", "")

    category_id = request.GET.get("category", "")
 
    # ALL published articles

    articles = NewsArticle.objects.filter(is_published=True).order_by("-created_at")

    categories = Category.objects.all()
 
    # Trending = most viewed

    trending = NewsArticle.objects.filter(is_published=True).order_by("-views")[:5]
 
    # Latest = newest

    latest = NewsArticle.objects.filter(is_published=True).order_by("-created_at")[:5]
 
    # SEARCH

    if search_query:

        articles = articles.filter(

            Q(title__icontains=search_query) |

            Q(content__icontains=search_query)

        )
 
    # CATEGORY FILTER

    if category_id:

        articles = articles.filter(category_id=category_id)
 
    breaking_alert = BreakingAlert.objects.filter(is_active=True).first()
 
    # EXTERNAL API NEWS — from utils.py

    api_news = fetch_api_news()
 
    return render(request, "newsapp/home.html", {

        "articles": articles,

        "api_news": api_news,

        "categories": categories,

        "trending": trending,

        "latest": latest,

        "breaking_alert": breaking_alert,

        "search_query": search_query,

        "selected_category": category_id,

    })
 

# ARTICLE DETAIL VIEW
def article_detail(request, pk):
    article = get_object_or_404(NewsArticle, pk=pk)
    article.views += 1
    article.save()
    return render(request, "newsapp/article_detail.html", {"article": article})

# SUBSCRIBE VIEW
def subscribe(request):
    message = None
    if request.method == "POST":
        email = request.POST.get("email")

        # Dummy email sending
        send_mail(
            subject="Subscription Successful",
            message="Thank you for subscribing to Yinhla Yeru News!",
            from_email="no-reply@yinhlayeru.com",
            recipient_list=[email],
            fail_silently=True
        )

        message = f"Subscribed successfully! A confirmation email was sent to {email}."

    return render(request, "newsapp/subscribe.html", {"message": message})
