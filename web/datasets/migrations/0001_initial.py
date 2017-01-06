# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-06 14:37
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='CIS_Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('C', 'Collocate'), ('S', 'Subset'), ('A', 'Aggregate')], max_length=1)),
                ('arguments', django.contrib.postgres.fields.jsonb.JSONField()),
                ('status', models.CharField(choices=[('P', 'Pending'), ('R', 'Running'), ('F', 'Finished'), ('E', 'Error')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('platform_type', models.CharField(choices=[('SA', 'Satellite'), ('AI', 'Aircraft'), ('SH', 'Ship'), ('GS', 'Ground station'), ('GM', 'Global Model'), ('RM', 'Regional Model')], max_length=2)),
                ('platform_name', models.CharField(blank=True, max_length=50, null=True)),
                ('region', models.CharField(blank=True, max_length=50, null=True)),
                ('spatial_extent', django.contrib.gis.db.models.fields.GeometryCollectionField(null=True, srid=4326)),
                ('time_start', models.DateTimeField(null=True)),
                ('time_end', models.DateTimeField(null=True)),
                ('project_URL', models.CharField(blank=True, max_length=50, null=True)),
                ('principal_investigator', models.CharField(blank=True, max_length=50, null=True)),
                ('source', models.CharField(blank=True, max_length=50, null=True)),
                ('public', models.BooleanField(default=False)),
                ('is_gridded', models.BooleanField()),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.Campaign')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measurement_type', models.CharField(choices=[('AOD', 'AOD'), ('CCN', 'CCN'), ('CN', 'CN'), ('AOT', 'AOT'), ('NSD', 'NSD'), ('SO4', 'Sulphate Mass Concentration'), ('BC', 'Black Carbon Concentration'), ('N', 'Number concentration'), ('EC', 'Extinction Coefficient'), ('TBC', 'Total Backscatter Coefficient'), ('PBC', 'Perpendicular Backscatter Coefficient'), ('UNK', 'Unknown')], default='UNK', max_length=3)),
                ('instrument', models.CharField(blank=True, max_length=50)),
                ('files', models.CharField(blank=True, max_length=250)),
                ('dataset', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='datasets.Dataset')),
            ],
        ),
        migrations.CreateModel(
            name='MeasurementFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=250)),
                ('spatial_extent', django.contrib.gis.db.models.fields.GeometryField(srid=4326)),
                ('time_start', models.DateTimeField()),
                ('time_end', models.DateTimeField()),
                ('measurements', models.ManyToManyField(to='datasets.Measurement')),
            ],
        ),
        migrations.CreateModel(
            name='MeasurementVariable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variable_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='AODMeasurementVariable',
            fields=[
                ('measurementvariable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='datasets.MeasurementVariable')),
                ('wavelength', models.FloatField(blank=True)),
            ],
            bases=('datasets.measurementvariable',),
        ),
        migrations.CreateModel(
            name='CCNMeasurementVariable',
            fields=[
                ('measurementvariable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='datasets.MeasurementVariable')),
                ('ss_variable', models.CharField(blank=True, max_length=50)),
                ('fixed_ss', models.FloatField(blank=True, null=True)),
            ],
            bases=('datasets.measurementvariable',),
        ),
        migrations.CreateModel(
            name='CNMeasurementVariable',
            fields=[
                ('measurementvariable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='datasets.MeasurementVariable')),
                ('cutoff_low_diameter', models.IntegerField(blank=True)),
                ('cutoff_high_diameter', models.IntegerField(blank=True)),
                ('volatile', models.BooleanField()),
            ],
            bases=('datasets.measurementvariable',),
        ),
        migrations.AddField(
            model_name='measurementvariable',
            name='measurement_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.Measurement'),
        ),
        migrations.AddField(
            model_name='cis_job',
            name='input',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='input_dataset', to='datasets.Dataset'),
        ),
        migrations.AddField(
            model_name='cis_job',
            name='output',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='output_dataset', to='datasets.Dataset'),
        ),
        migrations.AddField(
            model_name='cis_job',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cis_job',
            name='sample',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sample_dataset', to='datasets.Dataset'),
        ),
    ]
