# Generated by Django 3.2.4 on 2021-06-15 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github_dashboards', '0025_auto_20210615_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panel',
            name='panel_size',
            field=models.CharField(choices=[('S', 'small'), ('M', 'medium'), ('L', 'large')], default='S', max_length=20),
        ),
        migrations.AlterField(
            model_name='panel',
            name='panel_style',
            field=models.CharField(choices=[('DefaultStyle', 'Defaultstyle'), ('DarkSolarizedStyle', 'Darksolarizedstyle'), ('LightSolarizedStyle', 'Lightsolarizedstyle'), ('LightStyle', 'Lightstyle'), ('CleanStyle', 'Cleanstyle'), ('RedBlueStyle', 'Redbluestyle'), ('DarkColorizedStyle', 'Darkcolorizedstyle'), ('LightColorizedStyle', 'Lightcolorizedstyle'), ('TurquoiseStyle', 'Turquoisestyle'), ('LightGreenStyle', 'Lightgreenstyle'), ('DarkGreenStyle', 'Darkgreenstyle'), ('DarkGreenBlueStyle', 'Darkgreenbluestyle'), ('BlueStyle', 'Bluestyle')], default='DefaultStyle', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='panel',
            name='repo_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
