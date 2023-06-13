from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


def avatar_preview_directory_path(instance: "Profile", filename: str) -> str:
    return "users/{pk}/user-details/{filename}".format(
        pk=instance.pk,
        filename=filename
    )


class Profile(models.Model):
    class Meta:
        verbose_name_plural = _("profiles")
        verbose_name = _("profile")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, blank=True, upload_to=avatar_preview_directory_path, )

    def __str__(self):
        return str(self.user)
