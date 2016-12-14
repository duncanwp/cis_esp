from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Dataset(models.Model):
    """
    A Dataset is a collection of files and variables from a specific platform (but possibly different sensors).
    """
    name = models.CharField(max_length=50)

    SATELLITE = 'SA'
    AIRCRAFT = 'AI'
    SHIP = 'SH'
    GROUND_STATION = 'GS'
    GLOBAL_MODEL = 'GM'
    REGIONAL_MODEL = 'RM'

    PLATFORM_TYPE_CHOICES = (
        (SATELLITE, 'Satellite'),
        (AIRCRAFT, 'Aircraft'),
        (SHIP, 'Ship'),
        (GROUND_STATION, 'Ground station'),
        (GLOBAL_MODEL, 'Global Model'),
        (REGIONAL_MODEL, 'Regional Model')
    )
    platform_type = models.CharField(max_length=2, choices=PLATFORM_TYPE_CHOICES)
    platform_name = models.CharField(max_length=50, blank=True)

    # Human readable region description
    region = models.CharField(max_length=50, blank=True)
    # The actual polygon
    spatial_extent = models.MultiPolygonField()

    # Temporal extent
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()

    # Misc attributes
    project_URL = models.CharField(max_length=50, blank=True)
    principal_investigator = models.CharField(max_length=50, blank=True)
    source = models.CharField(max_length=5050, blank=True)

    # Deleting a user also deletes their datasets
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    public = models.BooleanField(default=False)


class MeasurementDataset(models.Model):
    """
    A MeasurementDataset is a specific type of measurement (CCN, AOD, N10, etc...), which may have more than variable,
    and be stored in more than one file.
    """
    # TODO: I might want to link these a bit more explicitly to MeasurementVariable types
    NUMBER_CONCENTRATION = 'N'
    AOD = 'AOD'
    AOT = 'AOT'
    CCN = 'CCN'
    CN = 'CN'
    N = 'N'

    MEASUREMENT_TYPE_CHOICES = (
        (AOD, 'AOD'),
        (CCN, 'CCN'),
        (CN, 'CN'),
        (AOT, 'AOT'),
        (N, 'Number concentration')
    )
    measurement_type = models.CharField(max_length=3, choices=MEASUREMENT_TYPE_CHOICES)
    instrument = models.CharField(max_length=50, blank=True)

    dataset = models.ForeignKey('Dataset', on_delete=models.CASCADE)


class MeasurementVariable(models.Model):
    """
    A MeasurementVariable is a specific variable name used to reference the MeasurementDataset in the MeasurementFile
    """
    variable_name = models.CharField(max_length=50)

    measurement_dataset = models.ForeignKey('MeasurementDataset', on_delete=models.CASCADE)


class CCNMeasurementVariable(MeasurementVariable):
    """
    A specific MeasurementVariable for dealing with CCN measurements which will have an associated supersaturation
    """
    ss_variable = models.CharField(max_length=50, blank=True)
    fixed_ss = models.FloatField(blank=True)


class CNMeasurementVariable(MeasurementVariable):
    """
    A specific MeasurementVariable for dealing with CCN measurements which will have associated cutoffs
    """
    cutoff_low_diameter = models.IntegerField(blank=True)  # in nm
    cutoff_high_diameter = models.IntegerField(blank=True)  # in nm
    volatile = models.BooleanField(blank=True)  # I assume None to be both combined


class AODMeasurementVariable(MeasurementVariable):
    """
    A specific MeasurementVariable for dealing with AOD measurements which will have an associated wavelength
    """
    wavelength = models.FloatField(blank=True)  # in nm


class MeasurementFile(models.Model):
    """
    A MeasurementFile is a reference to an actual file containing the MeasurementDataset that CIS can read.
    """
    measurement_dataset = models.ForeignKey('MeasurementDataset', on_delete=models.CASCADE)
    filename = models.CharField(max_length=250)

    spatial_extent = models.MultiPolygonField()
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
