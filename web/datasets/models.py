from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User


class Measurement(models.Model):
    """
    A MeasurementDataset is a specific type of measurement (CCN, AOD, N10, etc...), which may have more than variable,
    and be stored in more than one file.
    """
    # TODO: I might want to link these a bit more explicitly to MeasurementVariable types
    NO2 = 'NO2'
    AOD = 'AOD'

    MEASUREMENT_TYPE_CHOICES = (
        (NO2, 'NO2'),
        (AOD, 'AOD')
    )

    measurement_type = models.CharField(max_length=3, choices=MEASUREMENT_TYPE_CHOICES)
    instrument = models.CharField(max_length=50, blank=True)

    # A file wildcard
    files = models.CharField(max_length=250, blank=True)

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

    name = models.CharField(max_length=250)

    # This is a generic Geometry field as it may be a line string (for aircraft), a point (for stations) or a Polygon
    # Set Geography to 'true' to force PostGIS to treat this data on WGS84
    spatial_extent = models.GeometryField(geography=True)

    time_start = models.DateTimeField()
    time_end = models.DateTimeField()

    def __str__(self):
        return "{}".format(self.name)


class CIS_Job(models.Model):
    """
    A CIS job is a single CIS transaction which takes an input dataset (and optionally a sampling dataset) and
     produces an output dataset.
    """
    # Protect Measurements with associated jobs
    input = models.ForeignKey(Measurement, on_delete=models.PROTECT, related_name="input_measurement")
    output = models.ForeignKey(Measurement, on_delete=models.PROTECT, related_name="output_measurement")

    # Optional dataset used for collocation jobs only
    sample = models.ForeignKey(Measurement, on_delete=models.PROTECT, null=True, related_name="sample_measurement")

    # Job types. These could be subclasses but a type is fine for now.
    COLLOCATE = 'C'
    SUBSET = 'S'
    AGGREGATE = 'A'

    JOB_TYPE_CHOICES = (
        (COLLOCATE, 'Collocate'),
        (SUBSET, 'Subset'),
        (AGGREGATE, 'Aggregate')
    )
    type = models.CharField(max_length=1, choices=JOB_TYPE_CHOICES)

    # Command arguments
    # arguments = JSONField()

    # Job status - this should reflect the ARC-CE statuses
    PENDING = 'P'
    RUNNING = 'R'
    FINISHED = 'F'
    ERROR = 'E'

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (RUNNING, 'Running'),
        (FINISHED, 'Finished'),
        (ERROR, 'Error')
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    # Deleting a user does NOT delete their jobs
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Region(models.Model):
    """
    A spatial region of interest
    """
    # Optional name of the region
    name = models.CharField(max_length=250)
    # Is this a built-in region? (Otherwise the user must have defined it)
    built_in = models.BooleanField()
    # Spatial extent polygon (could be a point)
    spatial_extent = models.GeometryField()
    # String describing the CIS lat/lon extent (if applicable)
    cis_extent = models.CharField(max_length=250)

    def __str__(self):
        return "{}".format(self.name)


class AggregationResult(models.Model):
    # Protect datasets with associated jobs
    from django.contrib.postgres.fields import ArrayField

    job = models.ForeignKey(CIS_Job, on_delete=models.PROTECT, related_name="cis_job")
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="region")

    # TODO - In the real app this should probably be an OpenDAP/THREDDS end point
    data_x = ArrayField(models.CharField(max_length=19))
    data_y = ArrayField(models.FloatField())
