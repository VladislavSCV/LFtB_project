# Generated by Django 4.2.2 on 2023-07-22 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0003_rename_lftbcourses_certificatest_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usert',
            name='confirm',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='usert',
            name='author',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='usert',
            name='certificates',
            field=models.ManyToManyField(default='', to='sites.certificatest'),
        ),
        migrations.AlterField(
            model_name='usert',
            name='courses',
            field=models.ManyToManyField(default=None, to='sites.coursest'),
        ),
        migrations.AlterField(
            model_name='usert',
            name='level',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='usert',
            name='pro',
            field=models.BooleanField(default=False),
        ),
    ]
