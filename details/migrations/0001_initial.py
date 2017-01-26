# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-10 12:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_date', models.DateField(auto_now_add=True)),
                ('bill_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('cashier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Employee')),
            ],
            options={
                'ordering': ('bill_date',),
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(default='Customer Name', max_length=100)),
                ('phone_number', models.CharField(default='Not Available', max_length=15)),
                ('address', models.TextField(default='Address')),
                ('points', models.DecimalField(decimal_places=3, default=0.0, max_digits=7)),
            ],
            options={
                'ordering': ('customer_name',),
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(default='Item Name', max_length=100)),
                ('unit_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('qty_avail', models.IntegerField(default=0)),
                ('discount', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('item_name',),
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty_purchased', models.IntegerField(default=0)),
                ('bill', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='details.Bill')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='details.Item')),
            ],
            options={
                'ordering': ('bill', 'item'),
            },
        ),
        migrations.AddField(
            model_name='bill',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='details.Customer'),
        ),
    ]