

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('committee', '0008_delete_reviewchecklist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guardian',
            name='application',
        ),
        migrations.RemoveField(
            model_name='scholarshipapplication',
            name='scholarship',
        ),
    ]
