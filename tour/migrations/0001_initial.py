# Generated by Django 2.2.5 on 2021-02-04 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Gu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gu_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.CharField(max_length=100)),
                ('user_pw', models.CharField(max_length=100)),
                ('user_nickname', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Toursite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('toursite_name', models.CharField(max_length=100)),
                ('toursite_address', models.CharField(max_length=100)),
                ('toursite_img', models.CharField(max_length=1000)),
                ('toursite_detail', models.CharField(max_length=5000)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tour.Category')),
                ('gu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tour.Gu')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_rate', models.IntegerField(default=0)),
                ('review_date', models.DateTimeField(verbose_name='published date')),
                ('review_content', models.CharField(max_length=100)),
                ('toursite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tour.Toursite')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tour.User')),
            ],
        ),
    ]