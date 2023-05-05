from django.contrib.auth.models import User, Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = User.objects.get(pk="2")
        group, created = Group.objects.get_or_create(
            name="profile_manager"
        )
        permission_profile = Permission.objects.get(
            codename="view_profile",
        )
        permission_logentry = Permission.objects.get(
            codename="view_logentry",
        )
        permission_product_create = Permission.objects.get(
            codename="add_product"
        )
        permission_product_change = Permission.objects.get(
            codename="change_product"
        )

        #  добавление разрешения в группу
        group.permissions.add(permission_profile)

        #  присоединение пользователя к группе
        user.groups.add(group)

        #  связать пользователя напрямую с разрешением
        user.user_permissions.add(permission_logentry)
        user.user_permissions.add(permission_product_create)
        user.user_permissions.add(permission_product_change)

        group.save()
        user.save()

