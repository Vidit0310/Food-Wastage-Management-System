from django.contrib import admin
from .models import CustomUser, UserProfile, FoodCollectorProfile

class UserProfileAdmin(admin.StackedInline):
    model = UserProfile

class FoodCollectorProfileAdmin(admin.StackedInline):
    model = FoodCollectorProfile

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'is_superuser']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(FoodCollectorProfile)
admin.site.register(UserProfile)