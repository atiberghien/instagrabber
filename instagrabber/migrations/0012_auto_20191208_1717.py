# Generated by Django 2.2.8 on 2019-12-08 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instagrabber', '0011_remove_instaconfig_search_terms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instapicture',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='instagrabber.InstaUser'),
        ),
    ]