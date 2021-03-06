# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 08:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
        ('wagtailimages', '0018_remove_rendition_filter'),
        ('home', '0002_create_homepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('title_fr', models.CharField(default='', max_length=255)),
            ],
            options={
                'verbose_name': 'Rubrik',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ArticlePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('title_fr', models.CharField(default='', max_length=255)),
                ('date', models.DateField(verbose_name='Date')),
                ('intro_de', wagtail.core.fields.RichTextField(default='')),
                ('intro_fr', wagtail.core.fields.RichTextField(default='')),
                ('body_de', wagtail.core.fields.StreamField([('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('section', wagtail.core.blocks.CharBlock(classname='full title'))], blank=True, null=True)),
                ('body_fr', wagtail.core.fields.StreamField([('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('section', wagtail.core.blocks.CharBlock(classname='full title'))], blank=True, null=True)),
                ('feed_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'verbose_name': 'Artikel',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ArticleRelatedLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_links', to='home.ArticlePage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='homepage',
            name='body_de',
            field=wagtail.core.fields.RichTextField(default=''),
        ),
        migrations.AddField(
            model_name='homepage',
            name='body_fr',
            field=wagtail.core.fields.RichTextField(default=''),
        ),
        migrations.AddField(
            model_name='homepage',
            name='infos_de',
            field=wagtail.core.fields.StreamField([('info', wagtail.core.blocks.StructBlock([(b'title', wagtail.core.blocks.CharBlock(required=True)), (b'photo', wagtail.images.blocks.ImageChooserBlock()), (b'summary', wagtail.core.blocks.RichTextBlock(required=True)), (b'action', wagtail.core.blocks.CharBlock()), (b'url', wagtail.core.blocks.URLBlock())]))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='infos_fr',
            field=wagtail.core.fields.StreamField([('info', wagtail.core.blocks.StructBlock([(b'title', wagtail.core.blocks.CharBlock(required=True)), (b'photo', wagtail.images.blocks.ImageChooserBlock()), (b'summary', wagtail.core.blocks.RichTextBlock(required=True)), (b'action', wagtail.core.blocks.CharBlock()), (b'url', wagtail.core.blocks.URLBlock())]))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='intro_de',
            field=wagtail.core.fields.RichTextField(default=''),
        ),
        migrations.AddField(
            model_name='homepage',
            name='intro_fr',
            field=wagtail.core.fields.RichTextField(default=''),
        ),
    ]
