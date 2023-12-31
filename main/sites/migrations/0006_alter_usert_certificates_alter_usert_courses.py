# Generated by Django 4.2.2 on 2023-07-22 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0005_alter_usert_certificates_alter_usert_courses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usert',
            name='certificates',
            field=models.ManyToManyField(to='sites.certificatest'),
        ),
        migrations.AlterField(
            model_name='usert',
            name='courses',
            field=models.ManyToManyField(default=None, to='sites.coursest'),
        ),
    ]
