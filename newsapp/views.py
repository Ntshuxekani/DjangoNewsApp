from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils import timezone

from .models import NewsArticle, Category, BreakingAlert
from .utils import fetch_api_news, fetch_category_news, fetch_trending_news


# -------------------------------------------------------
# HOME PAGE
# -------------------------------------------------------
def home(request):
    # External API news (safe try)
    try:
        api_news = fetch_api_news()
    except:
        api_news = []

    search_query = request.GET.get("q", "")
    sort = request.GET.get("sort", "newest")
    category_id = request.GET.get("category", "")
    page = request.GET.get("page", 1)

    # Database articles
    articles_qs = NewsArticle.objects.filter(is_published=True)

    # Search filter
    if search_query:
        articles_qs = articles_qs.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )

    # Category filter
    if category_id:
        articles_qs = articles_qs.filter(category_id=category_id)

    # Sorting
    if sort == "oldest":
        articles_qs = articles_qs.order_by("created_at")
    elif sort == "most_viewed":
        articles_qs = articles_qs.order_by("-views")
    elif sort == "most_liked":
        articles_qs = articles_qs.order_by("-likes_count")
    else:
        articles_qs = articles_qs.order_by("-created_at")

    # Pagination
    paginator = Paginator(articles_qs, 6)
    articles = paginator.get_page(page)

    # Sidebar content
    categories = Category.objects.all()
    trending = NewsArticle.objects.filter(is_published=True).order_by("-views")[:5]
    latest = NewsArticle.objects.filter(is_published=True).order_by("-created_at")[:5]

    # Favourites stored in session
    favourite_ids = request.session.get("favorites", [])
    favourite_articles = NewsArticle.objects.filter(id__in=favourite_ids)

    breaking_alert = BreakingAlert.objects.filter(is_active=True).first()

    context = {
        "articles": articles,
        "api_news": api_news,
        "categories": categories,
        "trending": trending,
        "latest": latest,
        "favorite_articles": favourite_articles,
        "breaking_alert": breaking_alert,
        "search_query": search_query,
        "selected_category": category_id,
        "sort": sort,
        "paginator": paginator,
    }

    return render(request, "newsapp/home.html", context)


# -------------------------------------------------------
# ARTICLE DETAILS
# -------------------------------------------------------
def article_detail(request, pk):
    article = get_object_or_404(NewsArticle, pk=pk, is_published=True)

    # Count views
    article.views += 1
    article.save(update_fields=["views"])

    comments = article.comments.all().order_by("-created_at")

    context = {
        "article": article,
        "comments": comments,
    }
    return render(request, "newsapp/article_detail.html", context)


# -------------------------------------------------------
# COMMENTS
# -------------------------------------------------------
@require_POST
def add_comment(request, article_id):
    article = get_object_or_404(NewsArticle, id=article_id, is_published=True)
    name = request.POST.get("name", "Anonymous")
    content = request.POST.get("content", "").strip()

    if not content:
        return HttpResponseBadRequest("Comment cannot be empty.")

    article.comments.create(author_name=name, content=content, created_at=timezone.now())
    return redirect("article_detail", pk=article_id)


# -------------------------------------------------------
# FAVOURITES (SESSION-BASED)
# -------------------------------------------------------
def add_favorite(request, article_id):
    favs = request.session.get("favorites", [])
    if article_id not in favs:
        favs.append(article_id)

    request.session["favorites"] = favs
    return redirect("favourites")


def remove_favorite(request, article_id):
    favs = request.session.get("favorites", [])
    if article_id in favs:
        favs.remove(article_id)

    request.session["favorites"] = favs
    return redirect("favourites")


def favourites(request):
    fav_ids = request.session.get("favorites", [])
    fav_articles = NewsArticle.objects.filter(id__in=fav_ids)
    return render(request, "newsapp/favourites.html", {"favourites": fav_articles})


# -------------------------------------------------------
# SUBSCRIBE PAGE
# -------------------------------------------------------
subscribers = []  # temporary storage

def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()

        if email:
            subscribers.append(email)
            messages.success(request, "Thank you for subscribing! 🎉")
        else:
            messages.error(request, "Please enter a valid email address.")

    return render(request, "newsapp/subscribe.html")


# -------------------------------------------------------
# CATEGORY PAGE
# -------------------------------------------------------
def categories(request):
    category_data = {
        "technology": fetch_category_news("technology"),
        "business": fetch_category_news("business"),
        "sports": fetch_category_news("sports"),
        "entertainment": fetch_category_news("entertainment"),
        "health": fetch_category_news("health"),
        "science": fetch_category_news("science"),
    }
    return render(request, "newsapp/categories.html", {"categories": category_data})


# -------------------------------------------------------
# TRENDING PAGE
# -------------------------------------------------------
def trending(request):
    trending_news = fetch_trending_news()
    return render(request, "newsapp/trending.html", {"trending": trending_news})


# -------------------------------------------------------
# ALL NEWS PAGE
# -------------------------------------------------------
def all_news(request):
    all_articles = fetch_api_news()
    return render(request, "newsapp/all_news.html", {"all_news": all_articles})


# -------------------------------------------------------
# PROFILE PAGE
# -------------------------------------------------------
def profile(request):
    return render(request, "newsapp/profile.html")


# -------------------------------------------------------
# SEARCH PAGE
# -------------------------------------------------------
def search(request):
    query = request.GET.get("query", "")
    results = []

    if query:
        results = fetch_api_news(q=query)

    return render(request, "newsapp/search.html", {
        "query": query,
        "results": results
    })
    
    