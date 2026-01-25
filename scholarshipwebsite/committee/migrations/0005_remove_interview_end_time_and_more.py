

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('committee', '0004_scholarshipapplication_status_interview'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interview',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='interview',
            name='start_time',
        ),
        migrations.AddField(
            model_name='interview',
            name='interview_time',
            field=models.CharField(default='12:00 PM', max_length=20),
        ),
    ]
