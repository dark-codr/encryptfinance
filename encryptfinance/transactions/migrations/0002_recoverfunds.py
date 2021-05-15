# Generated by Django 3.1.10 on 2021-05-14 03:28

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecoverFunds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('approval', models.CharField(blank=True, choices=[('VERIFIED', 'VERIFIED'), ('PENDING', 'PENDING'), ('FAILED', 'FAILED')], default='PENDING', max_length=15, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, help_text='min-amount: $100, max-amount: $100000', max_digits=20, null=True, validators=[django.core.validators.MinValueValidator(Decimal('100.00')), django.core.validators.MaxValueValidator(Decimal('1000000.00'))], verbose_name='Lost Amount')),
                ('wallet_id', models.CharField(blank=True, max_length=255, null=True)),
                ('previous_broker', models.CharField(blank=True, max_length=255, null=True)),
                ('issue_date', models.DateField(default=django.utils.timezone.now)),
                ('resolved_date', models.DateField(default=django.utils.timezone.now)),
                ('requester', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Fund Recovery',
                'verbose_name_plural': 'Fund Recoveries',
                'ordering': ['-modified'],
            },
        ),
    ]
