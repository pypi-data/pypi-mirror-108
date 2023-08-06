# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.db import models


class Client(models.Model):
    CHECKOUT_TYPES = (
        ('DS', 'Digital goods / services checkout'),
        ('FC', 'Full checkout'),
        ('OF', 'Payment methods on file'),
        ('MO', 'Mobile SDK')
    )
    INTEGRATION_TYPES = (
        ('E', 'Embedded'),
        ('H', 'Hosted')
    )
    site = models.ForeignKey(Site, on_delete=models.PROTECT)
    test_mode = models.BooleanField(
        default=True,
        verbose_name="Testmodus"
    )
    merchant_id = models.CharField(
        max_length=20,
        verbose_name="Forhandler ID",
        help_text="Kontakt Nets for å få merchant-id"
    )
    checkout = models.CharField(
        max_length=2,
        choices=CHECKOUT_TYPES,
        verbose_name="Utsjekk"
    )
    integration_type = models.CharField(
        max_length=1,
        choices=INTEGRATION_TYPES,
        verbose_name="Integrasjonstype"
    )
    terms_url = models.URLField(verbose_name="Url til vilkår")
    return_url = models.URLField(
        verbose_name="Url som Easy skal redirecte til"
    )
