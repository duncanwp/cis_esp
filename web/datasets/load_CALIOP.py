from datasets.models import Dataset, MeasurementFile, Measurement, Campaign
from datetime import datetime


def load_caliop_data(dirpath, test_set=False):
    import glob
    from .utils import GLOBAL_EXTENT
    from os.path import join
    from django.contrib.auth.models import User
    from django.contrib.gis.geos import GeometryCollection
    files = glob.glob(join(dirpath, "*.hdf.met"))

    if test_set:
        files = files[::100]

    c, _ = Campaign.objects.get_or_create(name='CALIOP')

    d = Dataset.objects.create(time_start=datetime(2008,1,1,0,0,0), time_end=datetime(2008,12,31,0,0,0),
                               platform_type='SA', source='NASA', public=True, name='CALIOP L2 Aerosol Profile V4',
                               project_URL='https://www-calipso.larc.nasa.gov/resources/calips', region='Global',
                               spatial_extent=GeometryCollection(GLOBAL_EXTENT).wkt,
                               owner=User.objects.filter(username='duncan').first(), campaign=c,
                               is_gridded=False)

    pbc = Measurement(measurement_type='PBC', dataset=d)
    tbc = Measurement(measurement_type='TBC', dataset=d)
    pbc.save()
    tbc.save()

    pbc.measurementvariable_set.create(variable_name='Perpendicular_Backscatter_Coefficient_532')
    tbc.measurementvariable_set.create(variable_name='Total_Backscatter_Coefficient_532')

    for f in files:
        mf = read_caliop_met_file(f)
        mf.save()
        pbc.measurementfile_set.add(mf)
        tbc.measurementfile_set.add(mf)


def read_caliop_met_file(filepath):
    from .utils import lat_lon_points_to_linestring
    import numpy as np
    import dateutil.parser
    vals = {}
    _in = ''

    with open(filepath) as f:

        for line in f:
            if len(line.split('=')) > 1:
                key, val = line.split('=')
                key = key.strip()
                val = val.strip()
                if key == 'OBJECT':
                    if val == 'GRINGLATITUDE':
                        _in = 'latitude'
                    elif val == 'GRINGLONGITUDE':
                        _in = 'longitude'
                    elif val == 'START_DATE':
                        _in = 'start_date'
                    elif val == 'STOP_DATE':
                        _in = 'end_date'
                elif key == 'END_OBJECT':
                    _in = ''

                if _in.endswith('date') and key == 'VALUE':
                    vals[_in] = dateutil.parser.parse(val.strip('"'))
                elif _in and key == 'VALUE':
                    vals[_in] = val.strip('(').strip(')').split(',')

    # Use this helper method to convert to linestring taking into account dateline crossing
    line = lat_lon_points_to_linestring(np.array(vals['longitude'], dtype=np.float), np.array(vals['latitude'], dtype=np.float))

    mf = MeasurementFile(time_start=vals['start_date'], time_end=vals['end_date'],
                         spatial_extent=line.wkt, filename=filepath)

    return mf


def plot_test():
    from .utils import plot_shape
    from shapely.wkt import loads
    mf = read_caliop_met_file("/Users/watson-parris/Local data/2008_metfiles/CAL_LID_L2_05kmAPro-Standard-V4-10.2007-12-31T23-51-28ZN.hdf.met")
    line = mf.spatial_extent
    print(line.wkt)
    plot_shape(loads(line.wkt))


if __name__ == '__main__':
    load_caliop_data('/Users/watson-parris/Local data/2008_metfiles', test_set=True)
