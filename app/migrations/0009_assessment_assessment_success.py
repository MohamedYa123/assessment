# Generated by Django 4.0.2 on 2022-06-25 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_rename_assumtion_index_assessment_assessment_index_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='assessment_success',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
