# Generated by Django 3.2.25 on 2025-07-14 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0009_auto_20250713_1802'),
    ]

    operations = [
        migrations.CreateModel(
            name='Duty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=100)),
                ('sub_department', models.CharField(blank=True, max_length=100, null=True)),
                ('allocated_post', models.CharField(max_length=100)),
                ('duty_description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracker.departmenthead')),
            ],
            options={
                'verbose_name_plural': 'Duties',
                'ordering': ['allocated_post', 'duty_description'],
            },
        ),
    ]
