

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('committee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScholarshipApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('home_address', models.TextField()),
                ('correspondence_address', models.TextField()),
                ('ic_no', models.CharField(max_length=20)),
                ('age', models.IntegerField()),
                ('date_of_birth', models.DateField()),
                ('intake', models.DateField()),
                ('programme', models.CharField(max_length=200)),
                ('nationality', models.CharField(max_length=100)),
                ('race', models.CharField(choices=[('Malay', 'Malay'), ('Chinese', 'Chinese'), ('India', 'India')], max_length=20)),
                ('gender', models.CharField(choices=[('Female', 'Female'), ('Male', 'Male')], max_length=10)),
                ('contact_number', models.CharField(max_length=20)),
                ('email_address', models.EmailField(max_length=254)),
                ('highest_qualification', models.CharField(max_length=200)),
                ('passport_photo', models.ImageField(upload_to='passport_photos/')),
                ('academic_result', models.FileField(upload_to='academic_results/')),
                ('supporting_document', models.FileField(upload_to='supporting_docs/')),
                ('personal_achievement', models.TextField()),
                ('reason_deserve', models.TextField()),
                ('ea_form', models.FileField(upload_to='ea_forms/')),
                ('payslip', models.FileField(upload_to='payslips/')),
                ('scholarship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='committee.scholarship')),
            ],
        ),
        migrations.CreateModel(
            name='Guardian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relationship', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=200)),
                ('ic_no', models.CharField(max_length=20)),
                ('date_of_birth', models.DateField()),
                ('age', models.IntegerField()),
                ('nationality', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('Female', 'Female'), ('Male', 'Male')], max_length=10)),
                ('address', models.TextField()),
                ('contact_number', models.CharField(max_length=20)),
                ('email_address', models.EmailField(max_length=254)),
                ('monthly_income', models.DecimalField(decimal_places=2, max_digits=12)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guardians', to='committee.scholarshipapplication')),
            ],
        ),
    ]
