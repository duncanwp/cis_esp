from .models import Dataset, MeasurementFile, MeasurementDataset
from datetime import datetime

from django.contrib.gis.geos import GEOSGeometry


def run(verbose=True):
    pass
    # TODO
    # for f in files:
    #     shp = read_caliop_met_file(f)
    #     mf = MeasurementFile(spatial_extent=shp.wkt)
    # d = Dataset()
    # d.save()


def load_caliop_data(dirpath, test_set=False):
    import glob
    from os.path import join
    files = glob.iglob(join(dirpath, "*.hdf.met"))

    if test_set:
        files = files[::100]

    d = Dataset(time_start=datetime(2008,1,1,0,0,0), time_end=datetime(2008,12,31,0,0,0),
                platform_type='SA', source='NASA', public=True, name='CALIOP L2 Aerosol Profile V4',
                project_URL='https://www-calipso.larc.nasa.gov/resources/calips', region='Global')

    d.save()

    pbc = MeasurementDataset(measurement_type='PBC', dataset=d)
    tbc = MeasurementDataset(measurement_type='TBC', dataset=d)
    pbc.save()
    tbc.save()

    pbc.measurementvariable_set.create(variable_name='Perpendicular_Backscatter_Coefficient_532')
    tbc.measurementvariable_set.create(variable_name='Total_Backscatter_Coefficient_532')

    for f in files:
        mf = read_caliop_met_file(f)
        pbc.measurementfile_set.add(mf)
        tbc.measurementfile_set.add(mf)

        mf.save()


def read_caliop_met_file(filepath):
    import numpy as np
    from shapely.geometry import LineString, Polygon, MultiPoint
    vals = {}
    _in = ''

    with open(filepath) as f:

        for line in f:
            print(line)
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
                    elif val == 'END_DATE':
                        _in = 'end_date'
                elif key == 'END_OBJECT':
                    _in = ''

                if _in.endswith('date') and key == 'VALUE':
                    vals[_in] = datetime.strptime(val.strip('"'))
                elif _in and key == 'VALUE':
                    vals[_in] = val.strip('(').strip(')').split(',')

    ndarr = np.array([vals['longitude'], vals['latitude']], dtype=np.float).T

    # TODO: There is an issue here when reading points which cross the dateline. A quick google suggests that I should
    #  define an offset projection to define the data in (so it's all on one 360 degree domain), then transform it.
    # This is useful for plotting
    # points = MultiPoint(ndarr).buffer(4)
    points = MultiPoint(ndarr)
    line = LineString(ndarr)

    mf = MeasurementFile(time_start=vals['start_date'], time_end=vals['end_date'],
                         spatial_extent=line.wkt, filename=filepath)

    return mf


def plot_test():
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs

    # This is what I want out at the end. I could in principle create it directly, but I feel a bit happier creating the
    #  intermediate obkject for now.

    line = read_caliop_met_file("F:\Local Data\CAL_LID_L2_05kmAPro-Standard-V4-10.2007-12-31T23-51-28ZN.hdf.met")
    print(line.wkt)

    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=90))
    ax.coastlines()
    ax.set_global()
    ax.add_geometries([line], ccrs.PlateCarree(), facecolor='orange', edgecolor='black')

    plt.show()
