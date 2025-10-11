from django.core.management.base import BaseCommand
from users.models import Profile
import uuid


class Command(BaseCommand):
    help = 'Generate referral codes for existing users'

    def handle(self, *args, **kwargs):
        profiles_without_codes = Profile.objects.filter(referral_code='')
        count = 0
        
        for profile in profiles_without_codes:
            profile.referral_code = str(uuid.uuid4())[:8].upper()
            profile.save()
            count += 1
            
        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated {count} referral codes')
        )
