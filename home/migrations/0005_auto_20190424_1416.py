# Generated by Django 2.1.8 on 2019-04-24 14:16

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20190424_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='find_text',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='find_title',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='help_text',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='help_title',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
    ]
