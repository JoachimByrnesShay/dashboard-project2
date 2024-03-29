# Generated by Django 3.2.4 on 2021-06-12 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github_dashboards', '0020_alter_dashboardpanel_svg'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dashboardpanel',
            old_name='repo_description',
            new_name='description',
        ),
        migrations.AlterField(
            model_name='dashboardpanel',
            name='panel_type',
            field=models.CharField(choices=[('TableOfRepos', 'table- ALL repos for user'), ('Pie', 'pie chart- 1 repo'), ('Bar', 'bar chart- 1 repo'), ('HorizontalBar', 'horizontal bar chart- 1 repo'), ('Gauge', 'gauge chart- 1 repo'), ('Dot', 'dot chart- 1 repo'), ('Treemap', 'treemap chart- 1 repo')], default='Bar', max_length=100),
        ),
    ]
