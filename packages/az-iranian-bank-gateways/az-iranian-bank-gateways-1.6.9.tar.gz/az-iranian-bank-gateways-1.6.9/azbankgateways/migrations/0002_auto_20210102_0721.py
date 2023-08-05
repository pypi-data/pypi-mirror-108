# Generated by Django 3.1.4 on 2021-01-02 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('azbankgateways', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='bank_type',
            field=models.CharField(choices=[('BMI', 'BMI'), ('SEP', 'SEP'), ('ZARINPAL', 'Zarinpal'), ('IDPAY', 'IDPay'), ('ZIBAL', 'Zibal'), ('BAHAMTA', 'Bahamta')], max_length=50, verbose_name='Bank'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='status',
            field=models.CharField(choices=[('Waiting', 'Waiting'), ('Redirect to bank', 'Redirect To Bank'), ('Return from bank', 'Return From Bank'), ('Cancel by user', 'Cancel By User'), ('Expire gateway token', 'Expire Gateway Token'), ('Expire verify payment', 'Expire Verify Payment'), ('Complete', 'Complete')], max_length=50, verbose_name='Status'),
        ),
    ]
