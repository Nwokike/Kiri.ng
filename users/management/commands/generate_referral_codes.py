from django.core.management.base import BaseCommand
from users.models import Profile


class Command(BaseCommand):
    help = 'Generate referral codes for existing users (now uses usernames)'

    def handle(self, *args, **kwargs):
        profiles_without_codes = Profile.objects.filter(referral_code='')
        count = 0
        
        for profile in profiles_without_codes:
            profile.referral_code = profile.user.username
            profile.save()
            count += 1
            
        self.stdout.write(
            self.style.SUCCESS(f'Successfully set {count} referral codes to usernames')
        )
