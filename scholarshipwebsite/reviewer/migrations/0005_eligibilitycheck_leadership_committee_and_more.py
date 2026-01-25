

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviewer', '0004_eligibilitycheck_rigor_best_student_and_more'),
        ('student', '0002_scholarshipapplication_guardian'),
    ]

    operations = [
        migrations.AddField(
            model_name='eligibilitycheck',
            name='leadership_committee',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eligibilitycheck',
            name='leadership_leader',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eligibilitycheck',
            name='leadership_member',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eligibilitycheck',
            name='leadership_secretary',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eligibilitycheck',
            name='leadership_subleader',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='eligibilitycheck',
            name='application',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='eligibility_check', to='student.scholarshipapplication'),
        ),
    ]
