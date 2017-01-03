from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Campaign(models.Model):
    """
    A Campaign (or mission) is a coordinated collection of datasets, perhaps from different platforms or different
     retrievals.
    """
    name = models.CharField(max_length=20)


class Dataset(models.Model):
    """
    A Dataset is a collection of files and variables from a specific platform (but possibly different sensors).
    """
    name = models.CharField(max_length=50, null=True)

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

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
    platform_name = models.CharField(max_length=50, blank=True, null=True)

    # Human readable region description
    region = models.CharField(max_length=50, blank=True, null=True)
    # The actual polygon
    spatial_extent = models.PolygonField(null=True)

    # Temporal extent
    time_start = models.DateTimeField(null=True)
    time_end = models.DateTimeField(null=True)

    # Misc attributes
    project_URL = models.CharField(max_length=50, blank=True, null=True)
    principal_investigator = models.CharField(max_length=50, blank=True, null=True)
    source = models.CharField(max_length=50, blank=True, null=True)

    # Deleting a user also deletes their datasets
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    public = models.BooleanField(default=False)

    def __str__(self):
        if self.name is None:
            return "{} ({})".format(self.campaign.name, self.get_platform_type_display())
        else:
            return "{}".format(self.name)


class Measurement(models.Model):
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
    EC = 'EC'
    TBC = 'TBC'
    PBC = 'PBC'
    UNK = 'UNK'
    SO4 = 'SO4'
    BC = 'BC'
    NSD = 'NSD'

    MEASUREMENT_TYPE_CHOICES = (
        (AOD, 'AOD'),
        (CCN, 'CCN'),
        (CN, 'CN'),
        (AOT, 'AOT'),
        (NSD, 'NSD'),
        (SO4, 'Sulphate Mass Concentration'),
        (BC, 'Black Carbon Concentration'),
        (N, 'Number concentration'),
        (EC, 'Extinction Coefficient'),
        (TBC, 'Total Backscatter Coefficient'),
        (PBC, 'Perpendicular Backscatter Coefficient'),
        (UNK, 'Unknown')
    )

    measurement_type = models.CharField(max_length=3, choices=MEASUREMENT_TYPE_CHOICES, default=UNK)
    instrument = models.CharField(max_length=50, blank=True)

    # A file wildcard
    files = models.CharField(max_length=250, blank=True)

    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{}".format(self.get_measurement_type_display())


class MeasurementVariable(models.Model):
    """
    A MeasurementVariable is a specific variable name used to reference the MeasurementDataset in the MeasurementFile
    """
    variable_name = models.CharField(max_length=50)

    measurement_type = models.ForeignKey(Measurement, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.variable_name)


class CCNMeasurementVariable(MeasurementVariable):
    """
    A specific MeasurementVariable for dealing with CCN measurements which will have an associated supersaturation
    """
    ss_variable = models.CharField(max_length=50, blank=True)
    fixed_ss = models.FloatField(blank=True, null=True)


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
    measurements = models.ManyToManyField(Measurement)

    #TODO: Note that there are specific fields for filenames - I might want to use one of those
    filename = models.CharField(max_length=250)

    # This is a generic Geometry field as it may be a line string (for aircraft), a point (for stations) or a Polygon
    spatial_extent = models.GeometryField()
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()

    def __str__(self):
        return "{}".format(self.filename)
