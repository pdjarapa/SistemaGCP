# Generated by Django 4.1.2 on 2022-11-13 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seguridad', '0007_rename_navegador_logactivity_browser_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='logactivity',
            name='type',
            field=models.CharField(choices=[('M', 'Mobile'), ('T', 'Tablet'), ('P', 'Pc')], default='O', max_length=1),
        ),
    ]
