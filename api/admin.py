from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Item, Bid, Question, Answer


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Admin configuration for custom User model."""
    list_display = ('username', 'email', 'date_of_birth', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    
    # Add custom fields to the admin form
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': ('profile_image', 'date_of_birth'),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Profile Information', {
            'fields': ('email', 'profile_image', 'date_of_birth'),
        }),
    )


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Admin configuration for Item model."""
    list_display = ('title', 'owner', 'starting_price', 'end_datetime', 'is_active', 'winner_notified')
    list_filter = ('winner_notified', 'end_datetime', 'created_at')
    search_fields = ('title', 'description', 'owner__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    def is_active(self, obj: Item) -> bool:
        return obj.is_active
    is_active.boolean = True


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    """Admin configuration for Bid model."""
    list_display = ('item', 'bidder', 'amount', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('item__title', 'bidder__username')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin configuration for Question model."""
    list_display = ('item', 'asker', 'text_preview', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('item__title', 'asker__username', 'text')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)
    
    def text_preview(self, obj: Question) -> str:
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Question'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Admin configuration for Answer model."""
    list_display = ('question', 'responder', 'text_preview', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('question__text', 'responder__username', 'text')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)
    
    def text_preview(self, obj: Answer) -> str:
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Answer'
