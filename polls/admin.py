from django.contrib import admin
from .models import Poll, Option, Vote


class OptionInline(admin.TabularInline):
    model = Option
    extra = 1


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'expires_at', 'is_active')
    inlines = [OptionInline]
    search_fields = ('title',)
    list_filter = ('is_active',)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'poll', 'order')
    search_fields = ('text',)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter_id', 'poll', 'option', 'created_at')
    search_fields = ('voter_id',)
    list_filter = ('poll',)
