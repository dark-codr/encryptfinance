# Generated by Django 3.1.10 on 2021-05-13 19:48

import datetime
from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Withdrawal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('approval', models.CharField(blank=True, choices=[('VERIFIED', 'VERIFIED'), ('PENDING', 'PENDING'), ('FAILED', 'FAILED')], default='PENDING', max_length=15, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, help_text='min-amount: $100, max-amount: $100000', max_digits=20, null=True, validators=[django.core.validators.MinValueValidator(Decimal('100.00')), django.core.validators.MaxValueValidator(Decimal('1000000.00'))], verbose_name='Withdrawal Amount')),
                ('wallet_id', models.CharField(blank=True, max_length=255, null=True)),
                ('withdrawn', models.DateField(default=datetime.datetime.now)),
                ('withdrawer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='withdrawals', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Withdrawal',
                'verbose_name_plural': 'Withdrawals',
                'ordering': ['-modified'],
            },
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('approval', models.CharField(blank=True, choices=[('VERIFIED', 'VERIFIED'), ('PENDING', 'PENDING'), ('FAILED', 'FAILED')], default='PENDING', max_length=15, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, help_text='min-amount: $50, max-amount: $100000', max_digits=20, null=True, validators=[django.core.validators.MinValueValidator(Decimal('50.00')), django.core.validators.MaxValueValidator(Decimal('1000000.00'))], verbose_name='Deposited Amount')),
                ('deposited', models.DateField(default=datetime.datetime.now)),
                ('depositor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deposits', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Deposit',
                'verbose_name_plural': 'Deposits',
                'ordering': ['-modified'],
            },
        ),
    ]
