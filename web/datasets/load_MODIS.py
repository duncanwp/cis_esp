from datetime import datetime
import django
django.setup()


def gring_to_obj(gring):
    from datasets.utils import lat_lon_points_to_polygon

    line = lat_lon_points_to_polygon(gring[:4], gring[4:])
    return line


def _read_modis_geoData(dirpath, test_set):
    import pandas as pd
    import glob
    from os.path import join
    from datetime import timedelta

    files = glob.glob(join(dirpath, "*.txt"))
    if test_set:
        files = files[::100]

    df = pd.concat(pd.read_csv(f, header=2, parse_dates=[1]) for f in files)

    # Create a Multi-point object for each set of GRings
    df["poly"] = df.filter(regex="GRing").apply(gring_to_obj, axis=1)
    # The granules are 5 minutes each
    df['EndDateTime'] = df['StartDateTime'] + timedelta(minutes=5)
    return df


def load_modis_geoData(dirpath, test_set=False):
    from datasets.models import Dataset, MeasurementFile, Measurement, Campaign
    from django.contrib.auth.models import User
    from datasets.utils import GLOBAL_EXTENT

    df = _read_modis_geoData(dirpath, test_set)

    c, _ = Campaign.objects.get_or_create(name='MODIS C6')

    d = Dataset.objects.create(time_start=datetime(2008,1,1,0,0,0), time_end=datetime(2008,12,31,0,0,0),
                               platform_type='SA', source='NASA', public=True, name='MODIS L2 AOD C6',
                               project_URL='https://modis-atmos.gsfc.nasa.gov', region='Global',
                               spatial_extent=GLOBAL_EXTENT.wkt,
                               owner=User.objects.filter(username='duncan').first(), campaign=c,
                               is_gridded=False)

    aod = Measurement(measurement_type='AOD', dataset=d)
    aod.save()

    aod.measurementvariable_set.create(variable_name='AOD_550_Dark_Target_Deep_Blue_Combined')

    for _index, row in df.iterrows():
        mf = MeasurementFile(time_start=row['StartDateTime'], time_end=row['EndDateTime'],
                             spatial_extent=row['poly'].wkt, name=row['# GranuleID'])
        mf.save()
        aod.measurementfile_set.add(mf)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('path', help="MODIS input path")
    parser.add_argument('--test_set', help="Only do a subset", action='store_true')

    # Gets command line args by default
    args = parser.parse_args()

    load_modis_geoData(args.path, args.test_set)
