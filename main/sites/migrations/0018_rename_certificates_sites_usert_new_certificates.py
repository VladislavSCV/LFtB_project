# Generated by Django 4.2.2 on 2023-07-22 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0017_certificate_remove_sites_usert_certificates_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sites_usert',
            old_name='certificates',
            new_name='new_certificates',
        ),
    ]
