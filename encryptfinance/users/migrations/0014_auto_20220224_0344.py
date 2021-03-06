# Generated by Django 3.2.3 on 2022-02-24 08:44

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('countries_plus', '0005_auto_20160224_1804'),
        ('users', '0013_auto_20210731_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testimonial',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='nationality',
            field=models.ForeignKey(default='AF', null=True, on_delete=django.db.models.deletion.CASCADE, to='countries_plus.country'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, default='12345678', help_text='Example: 1234567890 (10 digits only)', max_length=10, null=True, validators=[django.core.validators.RegexValidator(code='Invalid_input, Only Integers', message='Must Contain Numbers Only', regex='^[0-9]*$')], verbose_name='Contact 10 digit Phone Number'),
        ),
        migrations.AlterField(
            model_name='userverify',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
