# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('ordernumber', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('test_mode', models.BooleanField(default=True, verbose_name='Testmodus')),
                ('merchant_id', models.CharField(help_text='Kontakt Nets for å få merchant-id', max_length=20, verbose_name='Forhandler ID')),
                ('checkout', models.CharField(verbose_name='Utsjekk', max_length=2, choices=[('DS', 'Digital goods / services checkout'), ('FC', 'Full checkout'), ('OF', 'Payment methods on file'), ('MO', 'Mobile SDK')])),
                ('integration_type', models.CharField(verbose_name='Integrasjonstype', max_length=1, choices=[('E', 'Embedded'), ('H', 'Hosted')])),
                ('terms_url', models.URLField(verbose_name='Url til vilkår')),
                ('return_url', models.URLField(verbose_name='Url som Easy skal redirecte til')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sites.Site')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('ordernumber', models.CharField(max_length=32)),
                ('amount', models.IntegerField(default=0, help_text='Pris i øre')),
                ('currency', models.CharField(max_length=3)),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, to='netseasy.Client')),
            ],
        ),
        migrations.AddField(
            model_name='checkout',
            name='payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='netseasy.Payment'),
        ),
    ]
