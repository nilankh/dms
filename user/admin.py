from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import DMSUser


class CustomUserAdmin(UserAdmin):
    model = DMSUser
    list_display = (
        "email",  # username removed
        "first_name",
        "last_name",
        "emp_code",
        "phone_number",
        "role_tag",
        "user_type",
        "branch_name",
        "branch_id",
        "is_active",
        "is_staff",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_active", "is_staff", "user_type", "branch_name")
    search_fields = ("email", "emp_code")  # username removed
    ordering = ("email",)

    # Define the fieldsets for the user creation and change forms
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "emp_code",
                    "role_tag",
                    "branch_id",
                    "branch_name",
                )
            },
        ),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", "user_type")},
        ),
        # ("Important dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "emp_code",
                    "role_tag",
                    "user_type",
                    "branch_id",
                    "branch_name",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )
    exclude = ("created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        """Override save_model to set created_by and updated_by fields."""
        if not change:  # If this is a new user, set created_by
            obj.created_by = request.user.id
        obj.updated_by = request.user.id  # Always set updated_by on save
        obj.save()


# Register the custom user model and its admin class
admin.site.register(DMSUser, CustomUserAdmin)
