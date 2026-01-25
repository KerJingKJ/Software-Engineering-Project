

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('committee', '0008_delete_reviewchecklist'),
    ]

    operations = [
        migrations.CreateModel(
            name='EligibilityCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citizenship_check', models.BooleanField(default=False)),
                ('programme_level_check', models.BooleanField(default=False)),
                ('qualifying_exam_check', models.BooleanField(default=False)),
                ('minimum_grades_check', models.BooleanField(default=False)),
                ('documents_verified', models.BooleanField(default=False)),
                ('application', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='eligibility_check', to='committee.scholarshipapplication')),
            ],
        ),
    ]
