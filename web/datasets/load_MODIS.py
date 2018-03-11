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

    # We only want the day-time files
    df = df[df.DayNightFlag == "D"]

    # Create a Multi-point object for each set of GRings
    df["poly"] = df.filter(regex="GRing").apply(gring_to_obj, axis=1)
    # The granules are 5 minutes each
    df['EndDateTime'] = df['StartDateTime'] + timedelta(minutes=5)
    return df


def load_modis_geoData(dirpath, test_set=False):
    from datasets.models import MeasurementFile, Measurement

    df = _read_modis_geoData(dirpath, test_set)

    aod = Measurement(measurement_type='AOD')
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
