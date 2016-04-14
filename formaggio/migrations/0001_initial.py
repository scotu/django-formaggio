# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-08 16:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.FORMAGGIO_FORM_MODEL),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FormaggioField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('index', models.BigIntegerField()),
                ('label', models.TextField()),
                ('kind', models.CharField(choices=[('TEXT_FIELD', 'text'), ('TEXT_FIELD_NUM', 'number'), ('TEXT_FIELD_PHONE', 'phone'), ('TEXT_FIELD_MAIL', 'email'), ('TEXT_FIELD_NAME', 'name'), ('CHECKBOX', 'checkbox'), ('TEXT_AREA', 'text area'), ('FILEUPLOAD', 'file upload')], max_length=100)),
                ('hint', models.TextField(blank=True)),
                ('extra', models.TextField(blank=True)),
                ('mandatory', models.BooleanField(default=False)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.FORMAGGIO_FORM_MODEL)),
            ],
            options={
                'ordering': ['form', 'index'],
                'verbose_name': 'form field',
            },
        ),
        migrations.CreateModel(
            name='FormaggioFieldValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_index', models.BigIntegerField()),
                ('original_label', models.TextField()),
                ('original_kind', models.CharField(max_length=100)),
                ('original_hint', models.TextField(blank=True)),
                ('original_extra', models.TextField(blank=True)),
                ('original_mandatory', models.BooleanField(default=False)),
                ('value', models.TextField(blank=True)),
                ('file_value', models.FileField(blank=True, null=True, upload_to=b'')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formaggio.FormaggioField')),
            ],
            options={
                'verbose_name': 'form value',
            },
        ),
        migrations.CreateModel(
            name='FormaggioFormResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_info', models.CharField(blank=True, max_length=255)),
                ('answered_date', models.DateTimeField(blank=True, null=True)),
                ('valid', models.BooleanField(default=False)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.FORMAGGIO_FORM_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-answered_date'],
                'verbose_name': 'form result',
            },
        ),
        migrations.AddField(
            model_name='formaggiofieldvalue',
            name='form_result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formaggio.FormaggioFormResult'),
        ),
    ]