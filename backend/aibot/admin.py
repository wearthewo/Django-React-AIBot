from django.contrib import admin
from .models import Message  # ✅ Import the Message model

# ✅ Register the Message model
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'response', 'created_at')  # ✅ Fields to display
    search_fields = ('user__username', 'message')  # ✅ Search by username or message
    list_filter = ('created_at',)  # ✅ Filter by created_at

# ✅ If you prefer a simple registration, use this instead:
# admin.site.register(Message)


# Register your models here.
