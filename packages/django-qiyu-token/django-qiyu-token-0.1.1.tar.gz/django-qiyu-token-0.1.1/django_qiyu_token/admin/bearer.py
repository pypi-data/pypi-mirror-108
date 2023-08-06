from django.contrib import admin

from django_qiyu_token.models import BearerTokenModel


@admin.register(BearerTokenModel)
class BearerTokenAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "token_name",
        "token_type",
        "revoked",
        "expire_time",
        "create_time",
    )
    list_display_links = ("user", "token_name", "token_type")
    list_filter = ("user",)
