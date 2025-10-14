# Generated manually for ModuleQuiz model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0011_alter_pathwaymodule_video_url_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuleQuiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(verbose_name='Quiz Question')),
                ('option_a', models.CharField(max_length=500, verbose_name='Option A')),
                ('option_b', models.CharField(max_length=500, verbose_name='Option B')),
                ('option_c', models.CharField(max_length=500, verbose_name='Option C')),
                ('option_d', models.CharField(max_length=500, verbose_name='Option D')),
                ('correct_answer', models.CharField(choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')], max_length=1, verbose_name='Correct Answer')),
                ('module', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='academy.pathwaymodule')),
            ],
        ),
    ]
