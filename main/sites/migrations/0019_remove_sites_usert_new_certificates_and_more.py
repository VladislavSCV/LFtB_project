# Generated by Django 4.2.2 on 2023-07-23 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0018_rename_certificates_sites_usert_new_certificates'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sites_usert',
            name='new_certificates',
        ),
        migrations.DeleteModel(
            name='Certificate',
        ),
        migrations.DeleteModel(
            name='sites_usert',
        ),
    ]
