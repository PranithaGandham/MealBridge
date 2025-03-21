# Generated by Django 5.1.6 on 2025-03-09 06:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mealbridge', '0002_alter_user_managers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(max_length=255)),
                ('contact_person_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15)),
                ('location', models.TextField()),
                ('registration_certificate', models.FileField(blank=True, null=True, upload_to='registration_certificates/')),
                ('is_approved', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='donee_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FoodDonation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_details', models.TextField()),
                ('quantity', models.PositiveIntegerField()),
                ('expiry_time', models.DateTimeField()),
                ('is_claimed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='food_images/')),
                ('preferred_organizations', models.ManyToManyField(blank=True, related_name='preferred_food', to='mealbridge.donee')),
            ],
        ),
        migrations.AddField(
            model_name='donee',
            name='previous_donations_received',
            field=models.ManyToManyField(blank=True, related_name='received_by', to='mealbridge.fooddonation'),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant_name', models.CharField(max_length=255)),
                ('owner_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15)),
                ('location', models.TextField()),
                ('cuisine_type', models.CharField(choices=[('Indian', 'Indian'), ('Chinese', 'Chinese'), ('Italian', 'Italian'), ('Mexican', 'Mexican'), ('Continental', 'Continental'), ('Others', 'Others')], default='Indian', max_length=20)),
                ('restaurant_logo', models.ImageField(blank=True, null=True, upload_to='restaurant_logos/')),
                ('food_donations', models.ManyToManyField(blank=True, related_name='donated_by', to='mealbridge.fooddonation')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='fooddonation',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donations', to='mealbridge.restaurant'),
        ),
    ]
