from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from business.models import Client


class Command(BaseCommand):

    def handle(self, *args, **options):
        public_schema = Client.objects.filter(
            schema_name=settings.PUBLIC_SCHEMA_NAME
        )
        User = get_user_model()
        if not public_schema.exists():
            tenant = Client(
                domain_url=settings.DEFAULT_PUBLIC_TENANT_DOMAIN,
                schema_name=settings.PUBLIC_SCHEMA_NAME,
                name=settings.PUBLIC_SCHEMA_NAME,
                on_trial=True,
            )
            tenant.save()
            self.stdout.write(self.style.SUCCESS('PUBLIC TENANT CREATED!'))
            self.stdout.write(
                "Use your DEFAULT_PUBLIC_TENANT_DOMAIN to get to it"
            )
        else:
            self.stdout.write(self.style.NOTICE(
                "Your public tenant was already up man!"))
            self.stdout.write(self.style.NOTICE(
                "I ain't creating no already existing things!"))
        # default_admin = User.objects.filter(
        #     is_superuser=True, email=settings.DEFAULT_ADMIN_EMAIL
        # )
