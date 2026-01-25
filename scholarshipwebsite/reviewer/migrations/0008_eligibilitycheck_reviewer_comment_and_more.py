

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviewer', '0007_eligibilitycheck_financial_priority_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='eligibilitycheck',
            name='reviewer_comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='eligibilitycheck',
            name='total_marks',
            field=models.IntegerField(default=0),
        ),
    ]
