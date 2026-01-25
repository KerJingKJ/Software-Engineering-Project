

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviewer', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eligibilitycheck',
            old_name='minimum_grades_check',
            new_name='exam_degree_matriculation',
        ),
        migrations.RenameField(
            model_name='eligibilitycheck',
            old_name='qualifying_exam_check',
            new_name='exam_degree_stpm_uec',
        ),
        migrations.AddField(
            model_name='eligibilitycheck',
            name='exam_foundation_spm',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eligibilitycheck',
            name='grade_foundation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eligibilitycheck',
            name='grade_spm',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eligibilitycheck',
            name='grade_stpm',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eligibilitycheck',
            name='grade_uec',
            field=models.BooleanField(default=False),
        ),
    ]
