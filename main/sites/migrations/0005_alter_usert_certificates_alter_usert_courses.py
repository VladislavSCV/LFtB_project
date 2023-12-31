# Generated by Django 4.2.2 on 2023-07-22 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0004_usert_confirm_alter_usert_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usert',
            name='certificates',
            field=models.ManyToManyField(through='sites.Enrollment', to='sites.certificatest'),
        ),
        migrations.AlterField(
            model_name='usert',
            name='courses',
            field=models.ManyToManyField(default=None, through='sites.Enrollment', to='sites.coursest'),
        ),
    ]
