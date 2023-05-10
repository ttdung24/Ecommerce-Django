from django.db import models
from rest_framework import serializers
import requests

# Create your models here.
class Order(models.Model):
    account = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        response = requests.get('http://127.0.0.1:8000/accounts/' + self.account)
        response.raise_for_status()
        account_data = response.json()
        username = account_data.get('username', 'Unknown')
        return f'{username} - Order {self.pk}'
    
    def clear_cart(self):
        self.items.all().delete()
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product_id = models.CharField(max_length=200, null=True)
    itemType = models.CharField(max_length=200, null=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        if(self.itemType == 'apparel'):
            url = 'http://127.0.0.1:8001/apparels/' + self.product_id
        response = requests.get(url)
        response.raise_for_status()
        product_data = response.json()
        name = product_data.get('name', 'Unknown')
        return f'{name}'
    
    def itemURL(self):
        if(self.itemType == 'apparel'):
            url = 'http://127.0.0.1:8001/apparels/' + self.product_id
        
        return url