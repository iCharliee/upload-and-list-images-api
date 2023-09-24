import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uploadImageApi.settings")

import django

django.setup()

from api.models import User


def create_superuser():
    if User.objects.filter(username="admin").exists():
        print("Admin user already exists.")
        return

    User.objects.create_superuser(
        username="admin", password="admin", email="admin@admin.admin"
    )
    print("Admin user created.")


if __name__ == "__main__":
    create_superuser()
