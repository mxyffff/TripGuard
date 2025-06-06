# Generated by Django 5.2.2 on 2025-06-04 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('countries', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SafetyNotice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notice_id', models.CharField(max_length=30, unique=True)),
                ('country_name', models.CharField(max_length=50)),
                ('country_en_name', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('category', models.CharField(max_length=20)),
                ('written_dt', models.DateField()),
                ('file_url', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
