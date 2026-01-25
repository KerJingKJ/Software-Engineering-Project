

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviewer', '0005_eligibilitycheck_leadership_committee_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='eligibilitycheck',
            name='competition_national',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eligibilitycheck',
            name='competition_participant',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eligibilitycheck',
            name='competition_state',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eligibilitycheck',
            name='competition_university',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eligibilitycheck',
            name='essay_compelling',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eligibilitycheck',
            name='essay_generic',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eligibilitycheck',
            name='essay_poor',
            field=models.BooleanField(default=False),
        ),
    ]
