# -*- coding: utf-8 -*-
import json

from django.conf import settings
from django.db import models
from netseasy.models.setup import Client


class Payment(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    ordernumber = models.CharField(max_length=32)
    amount = models.IntegerField(
        default=0,
        help_text='Pris i øre'
    )
    currency = models.CharField(
        max_length=3
    )
    created_date = models.DateTimeField(auto_now=True)

    def create_payment_json(self, items):
        """Create a json that will be sent as datastring to Nets Easy.
           ref: https://tech.dibspayment.com/easy/integration-guide#createpayment
        :param items: This is a list of dicts with these fields:
                      id, name, quantity, unit, unit_price, tax_rate,
                      tax_amount, gross_total_amount, net_total_amount
        :return: json to be sent to Easy
        """
        payment = {
            "order": {
                "amount": self.amount,
                "currency": self.currency,
                "reference": self.ordernumber,
                "items": []
            },
            "checkout": {
                "url": settings.EASY_CHECKOUT_URL,
                "termsUrl": self.client.terms_url,
                "shipping": {
                    "countries": [{
                        "countryCode": "NOR"
                    }],
                    "merchantHandlesShippingCost": False
                },
                "consumerType": {
                    "supportedTypes": ["B2C", "B2B"],
                    "default": "B2C"
                }
            },
            "notifications": {
                "webhooks": [{
                    "eventName": "payment.created",
                    "url": "https://www.testsite.xyz/easy/webhooks/",  # TODO: Define webhook urls in a model
                    "authorization": settings.EASY_AUTH_KEY
                    }
                ]
            },
        }
        items_list = []
        for item in items:
            items_list.append({
                "reference": item['id'],
                "name": item['name'],
                "quantity": item['quantity'],
                "unit": item['unit'],
                "unitPrice": item['unit_price'],
                "taxRate": item['tax_rate'],
                "taxAmount": item['tax_amount'],
                "grossTotalAmount": item['gross_total_amount'],
                "netTotalAmount": item['net_total_amount']
            })
        payment['order']['items'] = items_list
        return json.dumps(payment)


class Checkout(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now=True)
    ordernumber = models.CharField(max_length=32)
