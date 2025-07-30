from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "review_id",
        "book",
        "user",
        "rating",
        "created_at",
        "content",
    ]

    fields = [
        "book",
        "user",
        "rating",
        "content",
        "created_at",
    ]

    readonly_fields = ["created_at"]

    search_fields = [
        "content",
        "book__title",
        "user__username",
    ]

    list_filter = [
        "rating",
        "created_at",
        "book",
        "user",
    ]

    ordering = ["-created_at"]

    date_hierarchy = "created_at"