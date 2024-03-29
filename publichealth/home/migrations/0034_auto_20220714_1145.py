# Generated by Django 3.2.13 on 2022-07-14 09:45

from django.db import migrations, models
import django.db.models.deletion
import wagtail.contrib.table_block.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('home', '0033_auto_20220207_0731'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleindexpage',
            name='header_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='articleindexpage',
            name='table_de',
            field=wagtail.core.fields.StreamField([('table_de', wagtail.contrib.table_block.blocks.TableBlock(template='home/program_table.html'))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='articleindexpage',
            name='table_en',
            field=wagtail.core.fields.StreamField([('table_en', wagtail.contrib.table_block.blocks.TableBlock(template='home/program_table.html'))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='articleindexpage',
            name='table_fr',
            field=wagtail.core.fields.StreamField([('table_fr', wagtail.contrib.table_block.blocks.TableBlock(template='home/program_table.html'))], blank=True, null=True),
        ),
    ]
