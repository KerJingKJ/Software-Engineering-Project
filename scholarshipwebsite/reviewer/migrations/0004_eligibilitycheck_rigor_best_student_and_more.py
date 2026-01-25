

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviewer', '0003_eligibilitycheck_academic_borderline_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='eligibilitycheck',
            name='rigor_best_student',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eligibilitycheck',
            name='rigor_competitions',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eligibilitycheck',
            name='rigor_none',
            field=models.BooleanField(default=False),
        ),
    ]
