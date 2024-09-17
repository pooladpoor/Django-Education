from django.contrib import admin
from .models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', "author", "created", "status"]
    ordering = ["-created"]
    search_fields = ['title', "author", 'created']
    raw_id_fields = ["author"]
    date_hierarchy = "created"
    prepopulated_fields = {'slug': ['title', 'author']}
    list_display_links = ['title']
    list_filter = ["status", 'created']
    list_editable = ['status']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['subject', "name", "phone"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'name', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'body']
    list_editable = ['active']