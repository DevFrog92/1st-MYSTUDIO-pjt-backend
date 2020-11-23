# Generated by Django 3.1.3 on 2020-11-21 09:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StudioGhibli',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spiritedaway', models.BooleanField(default=False)),
                ('princessmononoke', models.BooleanField(default=False)),
                ('Kikisdeliveryservice', models.BooleanField(default=False)),
                ('myneighbortotoro', models.BooleanField(default=False)),
                ('howlsmovingcastle', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roadmap', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]