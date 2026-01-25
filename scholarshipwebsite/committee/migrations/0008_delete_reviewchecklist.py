

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('committee', '0007_reviewchecklist'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ReviewChecklist',
        ),
    ]
