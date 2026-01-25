

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviewer', '0002_rename_minimum_grades_check_eligibilitycheck_exam_degree_matriculation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='eligibilitycheck',
            name='academic_borderline',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eligibilitycheck',
            name='academic_competent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eligibilitycheck',
            name='academic_elite',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eligibilitycheck',
            name='academic_superior',
            field=models.BooleanField(default=False),
        ),
    ]
