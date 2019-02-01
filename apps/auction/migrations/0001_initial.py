# Generated by Django 2.1.5 on 2019-02-01 04:34

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Amount')),
                ('status', models.CharField(choices=[('open', 'Open Status'), ('closed', 'Close Status')], default='open', help_text="If it's switched to closed, we must to choose the winners bids", max_length=10, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Auction',
                'verbose_name_plural': 'Auctions',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Bid amount')),
                ('discount_rate', models.FloatField(help_text="Criteria for selecting winners bids. If it's lower, it increases the chances", verbose_name='Discount Rate')),
                ('winner', models.BooleanField(default=False, help_text='Is this a winner bid?', verbose_name='Winner Bid?')),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auction.Auction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Bid',
                'verbose_name_plural': 'Bids',
                'ordering': ['id'],
            },
        ),
    ]
