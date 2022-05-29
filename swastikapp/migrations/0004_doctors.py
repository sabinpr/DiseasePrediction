# Generated by Django 4.0.4 on 2022-04-29 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swastikapp', '0003_delete_shippingaddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='Doctor')),
            ],
        ),
    ]