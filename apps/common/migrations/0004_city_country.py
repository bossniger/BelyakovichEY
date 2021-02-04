# Generated by Django 2.2.6 on 2020-12-03 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0003_delete_revenue'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('population', models.PositiveIntegerField()),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Country')),
            ],
        ),
    ]
