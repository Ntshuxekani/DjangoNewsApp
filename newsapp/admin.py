from django.contrib import admin
from .models import NewsArticle, BreakingAlert, Subscriber, Category

@admin.action(description="Mark selected articles as Published")
def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)


@admin.action(description="Mark selected articles as Unpublished")
def make_unpublished(modeladmin, request, queryset):
    queryset.update(is_published=False)


class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "created_at", "is_published"]
    list_filter = ["category", "is_published", "created_at"]
    search_fields = ["title", "content"]
    actions = [make_published, make_unpublished]

admin.site.register(NewsArticle, NewsArticleAdmin)
admin.site.register(BreakingAlert)
admin.site.register(Subscriber)
admin.site.register(Category)