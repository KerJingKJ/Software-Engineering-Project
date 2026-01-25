

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('committee', '0002_scholarshipapplication_guardian'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='guardian',
            table='student_guardian',
        ),
        migrations.AlterModelTable(
            name='scholarshipapplication',
            table='student_scholarship_application',
        ),
    ]
