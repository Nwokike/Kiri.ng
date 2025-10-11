# Generated migration for referral_code field

from django.db import migrations, models
import uuid


def generate_referral_codes(apps, schema_editor):
    """Generate referral codes for existing users"""
    Profile = apps.get_model('users', 'Profile')
    for profile in Profile.objects.filter(referral_code=''):
        profile.referral_code = str(uuid.uuid4())[:8].upper()
        profile.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_socialmedialink_platform'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='referral_code',
            field=models.CharField(blank=True, help_text='Unique referral code for this user', max_length=20, unique=True),
        ),
        migrations.RunPython(generate_referral_codes, reverse_code=migrations.RunPython.noop),
    ]
