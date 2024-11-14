from django.contrib.auth.models import AbstractUser
from django.db import models


class DMSUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ("maker", "Maker"),
        ("checker", "Checker"),
        ("mis_view", "MIS View"),
        ("admin", "Admin"),
    ]

    # Fields that aren't part of AbstractUser
    emp_code = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role_tag = models.CharField(max_length=50)
    branch_id = models.IntegerField()
    branch_name = models.CharField(max_length=50)
    deleted_by_admin_id = models.IntegerField(null=True, blank=True)
    user_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default="maker"
    )
    created_by = models.IntegerField(null=True)
    updated_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Override the email field to ensure it's unique, as AbstractUser already defines it
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True)
    # Ensure email is used for authentication instead of the default username field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    # REQUIRED_FIELDS = [
    #     "email"
    # ]  # List the fields you want required when creating a superuser

    # Custom related names for 'groups' and 'user_permissions'
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="dmsuser_set",  # Custom related name to avoid clash
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="dmsuser_set",  # Custom related name to avoid clash
        blank=True,
    )

    def save(self, *args, **kwargs):
        # Ensure that `created_by` and `updated_by` are set to the ID of the currently authenticated user
        if not self.id:  # When creating a new user
            # You can access the current user from `request` (assuming you are passing `request.user` when calling `save()`)
            self.created_by = self.updated_by = kwargs.get("user", None)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
