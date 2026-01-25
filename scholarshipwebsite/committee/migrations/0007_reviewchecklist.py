

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('committee', '0006_approvedapplication'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewChecklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citizenship_check', models.BooleanField(default=False, verbose_name='Citizenship: Malaysian')),
                ('programme_level_check', models.BooleanField(default=False, verbose_name='Programme Level')),
                ('qualifying_exam_check', models.BooleanField(default=False, verbose_name='Qualifying Exam')),
                ('minimum_grades_check', models.BooleanField(default=False, verbose_name='Minimum Grades/CGPA')),
                ('documents_verified_check', models.BooleanField(default=False, verbose_name='Documents Verified')),
                ('academic_borderline', models.BooleanField(default=False, verbose_name='Academic: Borderline')),
                ('academic_competent', models.BooleanField(default=False, verbose_name='Academic: Competent')),
                ('academic_superior', models.BooleanField(default=False, verbose_name='Academic: Superior')),
                ('academic_elite', models.BooleanField(default=False, verbose_name='Academic: Elite')),
                ('rigor_award', models.BooleanField(default=False, verbose_name="Received 'Best Student' / Dean's List / Book Prize award")),
                ('rigor_competition', models.BooleanField(default=False, verbose_name='Participated in National/State Academic Competitions')),
                ('rigor_none', models.BooleanField(default=False, verbose_name='None of the above')),
                ('leadership_leader', models.BooleanField(default=False, verbose_name='Leader (President, Captain, Founder)')),
                ('leadership_subleader', models.BooleanField(default=False, verbose_name='Sub-leader (Vice-President, Vice-Captain, Co-Founder)')),
                ('leadership_secretary', models.BooleanField(default=False, verbose_name='Secretary/Treasurer')),
                ('leadership_committee', models.BooleanField(default=False, verbose_name='Committee Chairs')),
                ('leadership_member', models.BooleanField(default=False, verbose_name='Member')),
                ('achievement_national', models.BooleanField(default=False, verbose_name='National Level')),
                ('achievement_state', models.BooleanField(default=False, verbose_name='State Level')),
                ('achievement_university', models.BooleanField(default=False, verbose_name='University/District Level')),
                ('achievement_participant', models.BooleanField(default=False, verbose_name='Participant')),
                ('essay_compelling', models.BooleanField(default=False, verbose_name='Compelling')),
                ('essay_generic', models.BooleanField(default=False, verbose_name='Generic')),
                ('essay_poor', models.BooleanField(default=False, verbose_name='Poor')),
                ('application', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='review_checklist', to='committee.scholarshipapplication')),
            ],
            options={
                'db_table': 'review_checklist',
            },
        ),
    ]
